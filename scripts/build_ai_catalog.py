#!/usr/bin/env python3
"""Build the deterministic AI retrieval package from the handbook source.

The Markdown under ``content/`` remains the source of truth.  This script only
extracts document metadata and exact Markdown sections; it does not ask a
model to summarize, rewrite, or invent claims.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = ROOT / "content"
AI_ROOT = ROOT / "ai"
CATALOG_PATH = AI_ROOT / "catalog.jsonl"
MANIFEST_PATH = AI_ROOT / "manifest.json"
MAX_CHUNK_CHARS = 7200
REPOSITORY_URL = "https://github.com/kamanager2012/deepseek-harness-handbook"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
INLINE_LINK_RE = re.compile(r"\[([^]]+)\]\([^)]*\)")
INLINE_MARKUP_RE = re.compile(r"[`*_~]")
TERM_RE = re.compile(r"[A-Za-z][A-Za-z0-9+._/-]{1,}|[\u4e00-\u9fff]{2,}")

KIND_BY_DIRECTORY = {
    "00-overview": "overview",
    "01-installation": "installation",
    "02-web-ui": "web-ui",
    "03-cli": "cli",
    "04-providers": "provider",
    "05-workflows": "workflow",
    "06-security": "security",
    "07-sessions": "session",
    "08-automation": "automation",
    "09-tools": "tools",
    "10-plugins": "plugin",
    "11-operations": "operations",
    "12-reference": "reference",
    "core": "core",
    "quickstart": "quickstart",
    "tasks": "task",
    "automation": "automation",
    "safety": "security",
}


def heading(line: str) -> tuple[int, str] | None:
    match = HEADING_RE.match(line.rstrip("\r\n"))
    if not match:
        return None
    return len(match.group(1)), match.group(2).strip()


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def plain_text(text: str) -> str:
    text = INLINE_LINK_RE.sub(r"\1", text)
    text = INLINE_MARKUP_RE.sub("", text)
    return compact(text)


def first_summary(text: str, fallback: str) -> str:
    """Return an exact, lightly cleaned first prose paragraph."""

    paragraphs = re.split(r"\n\s*\n", text)
    for paragraph in paragraphs:
        lines = []
        in_fence = False
        for raw_line in paragraph.splitlines():
            line = raw_line.strip()
            if line.startswith(("```", "~~~")):
                in_fence = not in_fence
                continue
            if in_fence or not line or line.startswith("#"):
                continue
            if line.startswith((">", "|")):
                continue
            lines.append(line)
        candidate = plain_text(" ".join(lines))
        if candidate:
            return candidate[:480].rstrip() + ("…" if len(candidate) > 480 else "")
    return fallback


def slug(value: str) -> str:
    value = value.lower().replace("`", "")
    value = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "-", value)
    return value.strip("-") or "section"


def unique(values: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        value = compact(value)
        if not value:
            continue
        key = value.lower()
        if key not in seen:
            seen.add(key)
            result.append(value)
    return result


def document_kind(relative_path: Path) -> str:
    directory = relative_path.parent.name
    if relative_path.name in {"faq.md", "troubleshooting.md"}:
        return "troubleshooting"
    return KIND_BY_DIRECTORY.get(directory, "guide")


def keywords(relative_path: Path, title: str, headings: list[str]) -> list[str]:
    path_terms = []
    for part in relative_path.parts[:-1]:
        path_terms.append(re.sub(r"^\d+-", "", part).replace("-", " "))
    heading_terms: list[str] = []
    for value in [title, *headings]:
        heading_terms.extend(TERM_RE.findall(value))
    return unique(
        [
            "dsh",
            "DeepSeek Harness",
            *path_terms,
            title,
            *headings,
            *heading_terms,
        ]
    )[:80]


def split_large_ranges(lines: list[str], start: int, end: int) -> list[tuple[int, int]]:
    """Split a source range at paragraph boundaries when it is very large."""

    if start >= end:
        return []
    if sum(len(line) for line in lines[start:end]) <= MAX_CHUNK_CHARS:
        return [(start, end)]

    ranges: list[tuple[int, int]] = []
    current_start = start
    current_size = 0
    in_fence = False
    for index in range(start, end):
        line = lines[index]
        current_size += len(line)
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
        at_boundary = not in_fence and not stripped
        hard_boundary = not in_fence and current_size >= int(MAX_CHUNK_CHARS * 1.35)
        if (at_boundary and current_size >= MAX_CHUNK_CHARS) or hard_boundary:
            ranges.append((current_start, index + 1))
            current_start = index + 1
            current_size = 0
    if current_start < end:
        ranges.append((current_start, end))
    return ranges


def source_ranges(lines: list[str]) -> list[tuple[str, int, int]]:
    headings: list[tuple[int, int, str]] = []
    for index, line in enumerate(lines):
        value = heading(line)
        if value:
            headings.append((index, value[0], value[1]))

    h2_positions = [item for item in headings if item[1] == 2]
    if not h2_positions:
        return [("正文", 0, len(lines))]

    ranges: list[tuple[str, int, int]] = []
    first_h2 = h2_positions[0][0]
    if first_h2 > 0 and plain_text("".join(lines[:first_h2])):
        ranges.append(("导语", 0, first_h2))

    for offset, (start, _level, title) in enumerate(h2_positions):
        end = h2_positions[offset + 1][0] if offset + 1 < len(h2_positions) else len(lines)
        ranges.append((title, start, end))
    return ranges


def build_records() -> tuple[list[dict], list[dict]]:
    records: list[dict] = []
    documents: list[dict] = []
    for source_path in sorted(SOURCE_ROOT.rglob("*.md")):
        relative_path = source_path.relative_to(ROOT)
        lines = source_path.read_text(encoding="utf-8").splitlines(keepends=True)
        title = next((value[1] for value in (heading(line) for line in lines) if value and value[0] == 1), source_path.stem)
        all_headings = [value[1] for value in (heading(line) for line in lines) if value]
        kind = document_kind(relative_path)
        document_id = "dsh." + ".".join(relative_path.with_suffix("").parts)
        doc_summary = first_summary("".join(lines), title)
        doc_keywords = keywords(relative_path, title, all_headings)
        section_count = 0
        seen_slugs: dict[str, int] = {}

        for section_index, (section_title, start, end) in enumerate(source_ranges(lines), start=1):
            for part_index, (part_start, part_end) in enumerate(split_large_ranges(lines, start, end), start=1):
                section_count += 1
                section_slug = slug(section_title)
                seen_slugs[section_slug] = seen_slugs.get(section_slug, 0) + 1
                if seen_slugs[section_slug] > 1:
                    section_slug += f"-{seen_slugs[section_slug]}"
                part_suffix = f".part-{part_index}" if len(split_large_ranges(lines, start, end)) > 1 else ""
                record_id = f"{document_id}.{section_slug}{part_suffix}"
                content = "".join(lines[part_start:part_end])
                source_url = (
                    f"{REPOSITORY_URL}/blob/main/{relative_path.as_posix()}"
                    f"#L{part_start + 1}-L{part_end}"
                )
                records.append(
                    {
                        "schema_version": "1.0",
                        "id": record_id,
                        "document_id": document_id,
                        "title": title,
                        "section_title": section_title,
                        "section_index": section_index,
                        "part_index": part_index,
                        "kind": kind,
                        "language": "zh-CN",
                        "summary": first_summary(content, section_title),
                        "keywords": doc_keywords,
                        "content": content,
                        "source": {
                            "path": relative_path.as_posix(),
                            "line_start": part_start + 1,
                            "line_end": part_end,
                            "url": source_url,
                        },
                    }
                )

        documents.append(
            {
                "id": document_id,
                "title": title,
                "kind": kind,
                "summary": doc_summary,
                "keywords": doc_keywords,
                "source": relative_path.as_posix(),
                "section_count": section_count,
            }
        )
    return records, documents


def build_terms(root: Path) -> list[dict]:
    path = root / "content/12-reference/glossary.md"
    lines = path.read_text(encoding="utf-8").splitlines()
    terms: list[dict] = []
    for line_number, line in enumerate(lines, start=1):
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in {"术语", "---"} or set(cells[0]) <= {"-", ":"}:
            continue
        term, definition = cells[0], cells[1]
        terms.append(
            {
                "term": term,
                "definition": definition,
                "source": {
                    "path": "content/12-reference/glossary.md",
                    "line_start": line_number,
                    "line_end": line_number,
                    "url": (
                        f"{REPOSITORY_URL}/blob/main/content/12-reference/glossary.md"
                        f"#L{line_number}"
                    ),
                },
            }
        )
    return terms


def render(records: list[dict], documents: list[dict], terms: list[dict]) -> tuple[str, str, str]:
    catalog = "".join(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n" for record in records)
    terms_json = json.dumps(
        {
            "schema_version": "1.0",
            "name": "DeepSeek Harness 术语索引",
            "description": "从正文术语表逐行提取的机器可读定义，不替代当前版本官方字段说明。",
            "language": "zh-CN",
            "source": {
                "path": "content/12-reference/glossary.md",
                "repository": REPOSITORY_URL,
                "branch": "main",
            },
            "terms": terms,
        },
        ensure_ascii=False,
        indent=2,
    ) + "\n"
    manifest = {
        "schema_version": "1.0",
        "package": {
            "id": "deepseek-harness-handbook",
            "name": "DeepSeek Harness 中文 AI 知识包",
            "description": "供 AI 按主题检索 DeepSeek Harness 使用、工程、安全和运维说明。",
            "language": "zh-CN",
            "source_of_truth": "Markdown under content/",
            "transformation": "deterministic section extraction; no model-generated claims",
        },
        "source": {
            "repository": REPOSITORY_URL,
            "branch": "main",
            "root": "content/",
            "included": "content/**/*.md",
            "excluded": ["evidence/**", "labs/**", "BOOK.md"],
        },
        "retrieval": {
            "format": "JSON Lines (UTF-8)",
            "entry_file": "catalog.jsonl",
            "record_unit": "one Markdown H2 section or a bounded part of one section",
            "recommended_fields": ["title", "section_title", "summary", "content", "source", "keywords"],
        },
        "files": {
            "catalog": "catalog.jsonl",
            "terms": "terms.json",
            "schema": "schema.json",
            "usage": "README.md",
        },
        "stats": {
            "documents": len(documents),
            "records": len(records),
            "terms": len(terms),
        },
        "documents": documents,
    }
    return catalog, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", terms_json


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="handbook root")
    parser.add_argument("--check", action="store_true", help="check generated files without writing")
    args = parser.parse_args()
    root = args.root.resolve()
    global SOURCE_ROOT, AI_ROOT, CATALOG_PATH, MANIFEST_PATH
    SOURCE_ROOT = root / "content"
    AI_ROOT = root / "ai"
    CATALOG_PATH = AI_ROOT / "catalog.jsonl"
    MANIFEST_PATH = AI_ROOT / "manifest.json"
    terms_path = AI_ROOT / "terms.json"

    records, documents = build_records()
    terms = build_terms(root)
    catalog, manifest, terms_json = render(records, documents, terms)
    expected = {CATALOG_PATH: catalog, MANIFEST_PATH: manifest, terms_path: terms_json}
    mismatches: list[str] = []
    for path, content in expected.items():
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            mismatches.append(str(path.relative_to(root)))

    if args.check:
        if mismatches:
            print("AI catalog is out of date: " + ", ".join(mismatches))
            print("Run: python3 scripts/build_ai_catalog.py")
            return 1
        print(f"AI catalog is current: {len(documents)} documents, {len(records)} records, {len(terms)} terms")
        return 0

    AI_ROOT.mkdir(parents=True, exist_ok=True)
    for path, content in expected.items():
        path.write_text(content, encoding="utf-8")
    print(f"AI catalog built: {len(documents)} documents, {len(records)} records, {len(terms)} terms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
