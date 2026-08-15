#!/usr/bin/env python3
"""Validate the generated AI retrieval package and its source ranges."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="handbook root")
    args = parser.parse_args()
    root = args.root.resolve()
    ai_root = root / "ai"
    errors: list[str] = []

    try:
        manifest = json.loads((ai_root / "manifest.json").read_text(encoding="utf-8"))
        records = []
        with (ai_root / "catalog.jsonl").open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                try:
                    records.append((line_number, json.loads(line)))
                except json.JSONDecodeError as exc:
                    errors.append(f"catalog.jsonl:{line_number}: invalid JSON: {exc}")
    except (OSError, json.JSONDecodeError, KeyError) as exc:
        print(f"AI catalog validation failed: {exc}")
        return 1

    expected_documents = manifest.get("stats", {}).get("documents")
    expected_records = manifest.get("stats", {}).get("records")
    documents = manifest.get("documents", [])
    if expected_documents != len(documents):
        errors.append("manifest stats.documents does not match documents")
    if expected_records != len(records):
        errors.append("manifest stats.records does not match catalog")

    source_documents = {path.relative_to(root).as_posix() for path in (root / "content").rglob("*.md")}
    manifest_sources = {item.get("source") for item in documents}
    if source_documents != manifest_sources:
        missing = sorted(source_documents - manifest_sources)
        extra = sorted(manifest_sources - source_documents)
        errors.append(f"manifest source mismatch; missing={missing}, extra={extra}")

    ids: set[str] = set()
    document_ids: set[str] = set()
    for item in documents:
        document_ids.add(item.get("id", ""))

    for line_number, record in records:
        required = ("schema_version", "id", "document_id", "title", "section_title", "kind", "language", "content", "source")
        for field in required:
            if field not in record:
                errors.append(f"catalog.jsonl:{line_number}: missing {field}")
        record_id = record.get("id")
        if record_id in ids:
            errors.append(f"catalog.jsonl:{line_number}: duplicate id {record_id}")
        ids.add(record_id)
        if record.get("document_id") not in document_ids:
            errors.append(f"catalog.jsonl:{line_number}: unknown document_id {record.get('document_id')}")

        source = record.get("source", {})
        relative_path = source.get("path")
        if not isinstance(relative_path, str) or not relative_path.startswith("content/"):
            errors.append(f"catalog.jsonl:{line_number}: source must be under content/")
            continue
        source_path = root / relative_path
        if not source_path.exists():
            errors.append(f"catalog.jsonl:{line_number}: missing source {relative_path}")
            continue
        lines = source_path.read_text(encoding="utf-8").splitlines(keepends=True)
        line_start = source.get("line_start")
        line_end = source.get("line_end")
        if not isinstance(line_start, int) or not isinstance(line_end, int) or not (1 <= line_start <= line_end <= len(lines)):
            errors.append(f"catalog.jsonl:{line_number}: invalid source range {line_start}-{line_end}")
            continue
        expected_content = "".join(lines[line_start - 1 : line_end])
        if record.get("content") != expected_content:
            errors.append(f"catalog.jsonl:{line_number}: content does not match {relative_path}:{line_start}-{line_end}")

    if errors:
        print(f"AI catalog validation failed: {len(errors)} error(s)")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"AI catalog validation passed: {len(documents)} documents, {len(records)} records")
    return 0


if __name__ == "__main__":
    sys.exit(main())
