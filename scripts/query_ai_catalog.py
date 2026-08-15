#!/usr/bin/env python3
"""Search the static AI catalog without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "ai/catalog.jsonl"
TERM_RE = re.compile(r"[A-Za-z][A-Za-z0-9+._/-]{1,}|[\u4e00-\u9fff]+")


def terms(value: str) -> list[str]:
    result: list[str] = []
    for part in TERM_RE.findall(value.lower()):
        if re.fullmatch(r"[\u4e00-\u9fff]+", part):
            result.append(part)
            for size in (2, 3, 4):
                result.extend(part[index : index + size] for index in range(len(part) - size + 1))
        else:
            result.append(part)
    return list(dict.fromkeys(term for term in result if term))


def score(record: dict, query_terms: list[str]) -> int:
    title = str(record.get("title", "")).lower()
    section = str(record.get("section_title", "")).lower()
    summary = str(record.get("summary", "")).lower()
    keywords = " ".join(str(value).lower() for value in record.get("keywords", []))
    content = str(record.get("content", "")).lower()
    total = 0
    for term in query_terms:
        if term in title:
            total += 12
        if term in section:
            total += 9
        if term in keywords:
            total += 5
        if term in summary:
            total += 3
        if term in content:
            total += 1
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="natural-language search query")
    parser.add_argument("--catalog", type=Path, default=CATALOG)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--full", action="store_true", help="include full Markdown content")
    args = parser.parse_args()
    query_terms = terms(args.query)
    if not query_terms:
        raise SystemExit("query must contain searchable text")

    results = []
    with args.catalog.open(encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            value = score(record, query_terms)
            if value:
                item = {
                    "score": value,
                    "id": record["id"],
                    "title": record["title"],
                    "section_title": record["section_title"],
                    "summary": record["summary"],
                    "source": record["source"],
                }
                if args.full:
                    item["content"] = record["content"]
                results.append(item)

    results.sort(key=lambda item: (-item["score"], item["id"]))
    print(json.dumps(results[: max(args.limit, 0)], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
