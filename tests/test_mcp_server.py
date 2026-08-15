import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from mcp_server import CatalogStore, MCPServer, MODERN_PROTOCOL_VERSION  # noqa: E402


class MCPServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = MCPServer(CatalogStore(ROOT))

    def request(self, message):
        response, should_exit = self.server.dispatch(message)
        self.assertFalse(should_exit)
        self.assertIsNotNone(response)
        return response

    def test_modern_discovery_advertises_read_only_tools(self):
        response = self.request({"jsonrpc": "2.0", "id": 1, "method": "server/discover"})
        result = response["result"]
        self.assertIn(MODERN_PROTOCOL_VERSION, result["supportedVersions"])
        self.assertEqual(result["capabilities"], {"tools": {"listChanged": False}})

    def test_legacy_initialize_and_tools_list(self):
        initialized = self.request(
            {
                "jsonrpc": "2.0",
                "id": "init",
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-11-25",
                    "capabilities": {},
                    "clientInfo": {"name": "test-client", "version": "0"},
                },
            }
        )
        self.assertEqual(initialized["result"]["protocolVersion"], "2025-11-25")
        self.assertIsNone(self.server.dispatch({"jsonrpc": "2.0", "method": "notifications/initialized"})[0])

        response = self.request({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        tools = {tool["name"]: tool for tool in response["result"]["tools"]}
        self.assertEqual(set(tools), {"query_docs", "get_source"})
        for tool in tools.values():
            self.assertTrue(tool["annotations"]["readOnlyHint"])
            self.assertFalse(tool["annotations"]["destructiveHint"])

    def test_query_docs_returns_english_provenance(self):
        response = self.request(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "query_docs",
                    "arguments": {"query": "What does Provider mean in this handbook?", "limit": 3},
                },
            }
        )
        payload = response["result"]["structuredContent"]
        self.assertEqual(payload["language"], "en")
        self.assertEqual(payload["results"][0]["id"], "dsh.en.12-reference.glossary.body")
        self.assertIn("source", payload["results"][0])
        self.assertIn("url", payload["results"][0]["source"])

    def test_get_source_returns_exact_content(self):
        response = self.request(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "get_source",
                    "arguments": {"id": "dsh.en.12-reference.glossary.body"},
                },
            }
        )
        record = response["result"]["structuredContent"]["record"]
        self.assertEqual(record["source"]["path"], "en/12-reference/glossary.md")
        self.assertIn("# Glossary", record["content"])

    def test_tool_errors_are_visible_to_the_model(self):
        response = self.request(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "tools/call",
                "params": {"name": "get_source", "arguments": {"id": "not-a-record"}},
            }
        )
        self.assertTrue(response["result"]["isError"])
        self.assertIn("unknown record id", response["result"]["content"][0]["text"])

    def test_protocol_errors_are_json_rpc_errors(self):
        response = self.request({"jsonrpc": "2.0", "id": 6, "method": "unknown/method"})
        self.assertEqual(response["error"]["code"], -32601)

    def test_unknown_tool_is_a_protocol_error(self):
        response = self.request(
            {
                "jsonrpc": "2.0",
                "id": 7,
                "method": "tools/call",
                "params": {"name": "write_file", "arguments": {}},
            }
        )
        self.assertEqual(response["error"]["code"], -32602)


if __name__ == "__main__":
    unittest.main()
