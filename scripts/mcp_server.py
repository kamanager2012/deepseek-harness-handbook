#!/usr/bin/env python3
"""Expose the static bilingual handbook catalogs through a read-only MCP server.

The server intentionally uses only the Python standard library.  It supports
the current stateless discovery flow and the legacy initialize flow so that it
can be launched by MCP clients with different protocol generations.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from query_ai_catalog import score, terms


ROOT = Path(__file__).resolve().parents[1]
SERVER_NAME = "deepseek-harness-knowledge"
SERVER_VERSION = "0.1.0"
MODERN_PROTOCOL_VERSION = "2026-07-28"
LEGACY_PROTOCOL_VERSIONS = ("2025-11-25", "2025-06-18", "2024-11-05")
SUPPORTED_PROTOCOL_VERSIONS = (MODERN_PROTOCOL_VERSION, *LEGACY_PROTOCOL_VERSIONS)
MAX_LIMIT = 20
INSTRUCTIONS = (
    "This is a read-only server over the public DeepSeek Harness handbook. "
    "Use query_docs to find relevant source sections, then use get_source when "
    "you need the complete section and provenance. Preserve source.url in answers."
)


def _source_copy(record: dict[str, Any]) -> dict[str, Any]:
    return dict(record.get("source", {}))


def _record_view(record: dict[str, Any], include_content: bool = True, value: int | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": record["id"],
        "language": record["language"],
        "title": record["title"],
        "section_title": record["section_title"],
        "summary": record["summary"],
        "source": _source_copy(record),
    }
    if value is not None:
        result["score"] = value
    if include_content:
        result["content"] = record["content"]
    return result


class CatalogStore:
    """Load the two generated catalogs from fixed repository-relative paths."""

    CATALOGS = {
        "zh-CN": Path("ai/catalog.jsonl"),
        "en": Path("ai/catalog.en.jsonl"),
    }

    def __init__(self, root: Path) -> None:
        self.root = root
        self.records_by_language: dict[str, list[dict[str, Any]]] = {}
        self.records_by_id: dict[str, dict[str, Any]] = {}
        for language, relative_path in self.CATALOGS.items():
            records = self._load(relative_path)
            self.records_by_language[language] = records
            for record in records:
                self.records_by_id[record["id"]] = record

    def _load(self, relative_path: Path) -> list[dict[str, Any]]:
        path = self.root / relative_path
        records: list[dict[str, Any]] = []
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    records.append(json.loads(line))
        return records

    @staticmethod
    def language_for(query: str, requested: str) -> str:
        if not isinstance(requested, str):
            raise ValueError("language must be one of: auto, zh-CN, en")
        if requested in {"zh-CN", "en"}:
            return requested
        if requested != "auto":
            raise ValueError("language must be one of: auto, zh-CN, en")
        return "zh-CN" if any("\u4e00" <= char <= "\u9fff" for char in query) else "en"

    def query(
        self,
        query: str,
        language: str = "auto",
        limit: int = 5,
        include_content: bool = True,
    ) -> dict[str, Any]:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string")
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise ValueError("limit must be an integer")
        if limit < 1 or limit > MAX_LIMIT:
            raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")
        if not isinstance(include_content, bool):
            raise ValueError("include_content must be a boolean")
        selected_language = self.language_for(query, language)
        query_terms = terms(query)
        ranked: list[tuple[int, dict[str, Any]]] = []
        for record in self.records_by_language[selected_language]:
            value = score(record, query_terms)
            if value:
                ranked.append((value, record))
        ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
        return {
            "query": query,
            "language": selected_language,
            "results": [
                _record_view(record, include_content=include_content, value=value)
                for value, record in ranked[:limit]
            ],
        }

    def source(self, record_id: str) -> dict[str, Any]:
        if not isinstance(record_id, str) or not record_id.strip():
            raise ValueError("id must be a non-empty string")
        record = self.records_by_id.get(record_id)
        if record is None:
            raise ValueError(f"unknown record id: {record_id}")
        return _record_view(record, include_content=True)


TOOLS = [
    {
        "name": "query_docs",
        "title": "Query handbook documents",
        "description": (
            "Search the static Chinese or English DeepSeek Harness handbook. "
            "Returns ranked original sections with summaries, content, and provenance."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural-language question to search for."},
                "language": {
                    "type": "string",
                    "enum": ["auto", "zh-CN", "en"],
                    "default": "auto",
                    "description": "Catalog to search; auto selects Chinese when the query contains Han characters.",
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": MAX_LIMIT,
                    "default": 5,
                    "description": "Maximum number of records to return.",
                },
                "include_content": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether each result includes the original Markdown section.",
                },
            },
            "required": ["query"],
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    },
    {
        "name": "get_source",
        "title": "Get an original handbook section",
        "description": "Fetch one exact catalog record, including its original Markdown and source URL.",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string", "description": "Stable record ID returned by query_docs."}},
            "required": ["id"],
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    },
]


def _server_info() -> dict[str, str]:
    return {"name": SERVER_NAME, "title": "DeepSeek Harness Knowledge", "version": SERVER_VERSION}


def _error(request_id: Any, code: int, message: str, data: Any = None) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if data is not None:
        error["data"] = data
    return {"jsonrpc": "2.0", "id": request_id, "error": error}


class UnknownToolError(ValueError):
    """A protocol-level error: the requested tool is not advertised."""


class MCPServer:
    def __init__(self, store: CatalogStore) -> None:
        self.store = store

    def dispatch(self, message: dict[str, Any]) -> tuple[dict[str, Any] | None, bool]:
        """Dispatch one JSON-RPC message and return (response, should_exit)."""

        if not isinstance(message, dict):
            return _error(None, -32600, "JSON-RPC message must be an object"), False
        method = message.get("method")
        has_id = "id" in message
        request_id = message.get("id")
        if not isinstance(method, str):
            # A server does not answer JSON-RPC responses sent by a client.
            return (None, False) if not has_id else (_error(request_id, -32600, "method is required"), False)

        if method in {
            "notifications/initialized",
            "notifications/cancelled",
            "notifications/progress",
            "notifications/tools/list_changed",
        }:
            return None, False
        if method == "notifications/exit":
            return None, True
        if not has_id:
            return None, False

        params = message.get("params") or {}
        if not isinstance(params, dict):
            return _error(request_id, -32602, "params must be an object"), False

        try:
            if method == "server/discover":
                result = {
                    "resultType": "complete",
                    "supportedVersions": list(SUPPORTED_PROTOCOL_VERSIONS),
                    "capabilities": {"tools": {"listChanged": False}},
                    "_meta": {"io.modelcontextprotocol/serverInfo": _server_info()},
                    "instructions": INSTRUCTIONS,
                    "ttlMs": 3600000,
                    "cacheScope": "public",
                }
            elif method == "initialize":
                requested = params.get("protocolVersion")
                selected = requested if requested in SUPPORTED_PROTOCOL_VERSIONS else LEGACY_PROTOCOL_VERSIONS[0]
                result = {
                    "protocolVersion": selected,
                    "capabilities": {"tools": {"listChanged": False}},
                    "serverInfo": _server_info(),
                    "instructions": INSTRUCTIONS,
                }
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                result = {"resultType": "complete", "tools": TOOLS, "ttlMs": 3600000, "cacheScope": "public"}
            elif method == "tools/call":
                result = self._call_tool(params)
            elif method == "shutdown":
                result = None
            else:
                return _error(request_id, -32601, f"method not found: {method}"), False
        except UnknownToolError as exc:
            return _error(request_id, -32602, str(exc)), False
        except ValueError as exc:
            if method == "tools/call":
                result = {
                    "resultType": "complete",
                    "content": [{"type": "text", "text": str(exc)}],
                    "isError": True,
                }
            else:
                return _error(request_id, -32602, str(exc)), False

        return {"jsonrpc": "2.0", "id": request_id, "result": result}, False

    def _call_tool(self, params: dict[str, Any]) -> dict[str, Any]:
        name = params.get("name")
        arguments = params.get("arguments") or {}
        if not isinstance(name, str):
            raise ValueError("tools/call requires a tool name")
        if not isinstance(arguments, dict):
            raise ValueError("tools/call arguments must be an object")
        if name == "query_docs":
            payload = self.store.query(
                query=arguments.get("query", ""),
                language=arguments.get("language", "auto"),
                limit=arguments.get("limit", 5),
                include_content=arguments.get("include_content", True),
            )
        elif name == "get_source":
            payload = {"record": self.store.source(arguments.get("id", ""))}
        else:
            raise UnknownToolError(f"unknown tool: {name}")
        return {
            "resultType": "complete",
            "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False)}],
            "structuredContent": payload,
        }


def run_stdio(server: MCPServer, verbose: bool = False) -> int:
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError as exc:
            response = _error(None, -32700, f"parse error: {exc.msg}")
            should_exit = False
        else:
            response, should_exit = server.dispatch(message)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False, separators=(",", ":")) + "\n")
            sys.stdout.flush()
        if verbose:
            print("handled MCP message", file=sys.stderr)
        if should_exit:
            return 0
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="handbook repository root")
    parser.add_argument("--verbose", action="store_true", help="write minimal diagnostics to stderr")
    args = parser.parse_args()
    try:
        store = CatalogStore(args.root.resolve())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"unable to load AI catalogs: {exc}", file=sys.stderr)
        return 1
    return run_stdio(MCPServer(store), verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
