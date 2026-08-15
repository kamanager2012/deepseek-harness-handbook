# 只读 MCP 服务 / Read-only MCP server

本服务把静态双语 AI 知识包接到 MCP 客户端。它只检索已经生成的
`ai/catalog.jsonl` 和 `ai/catalog.en.jsonl`，不会执行 dsh、访问任意路径、写文件、
修改 Session 或联网抓取内容。

This server exposes the generated bilingual catalogs through MCP. It is deliberately
read-only: it does not run dsh, access arbitrary paths, write files, mutate sessions, or
fetch network content.

## 两个工具 / Two tools

| Tool | 用途 / Purpose |
| --- | --- |
| `query_docs` | 按自然语言检索中文或英文原始章节，并返回排名、正文和来源。 / Search original Chinese or English sections with ranking, content, and provenance. |
| `get_source` | 根据稳定 `id` 取回完整章节和 GitHub 来源。 / Fetch one complete record and its GitHub source by stable `id`. |

每条结果都保留 `source.path`、行号和 `source.url`。英文记录还保留
`translation_of`，方便 Agent 同时追溯英文和中文事实来源。

Every result preserves `source.path`, line numbers, and `source.url`. English records also
carry `translation_of` when a Chinese source exists.

## 启动 / Launch

先克隆仓库，然后用绝对路径启动 stdio server：

```bash
python3 /absolute/path/to/deepseek-harness-handbook/scripts/mcp_server.py
```

MCP 客户端配置示例：

```json
{
  "mcpServers": {
    "deepseek-harness": {
      "command": "python3",
      "args": [
        "/absolute/path/to/deepseek-harness-handbook/scripts/mcp_server.py"
      ]
    }
  }
}
```

Windows 可以把 `command` 换成 `py`，并使用 Windows 绝对路径。不要把仓库相对路径
或依赖当前工作目录的命令直接放进团队配置。

On Windows, use `py` as the command and provide an absolute Windows path. Do not rely on
a repository-relative path or the client's current working directory in shared config.

## 最小调用流程 / Minimal protocol flow

服务使用 MCP stdio 传输：stdin/stdout 上每行一个 JSON-RPC 消息；诊断信息只写入
stderr。它支持当前的 `server/discover` 发现流程，也兼容使用 `initialize`/
`notifications/initialized` 的旧客户端。

The server uses MCP stdio: one JSON-RPC message per line on stdin/stdout, with diagnostics
on stderr only. It supports `server/discover` for the current stateless flow and also
accepts the legacy `initialize`/`notifications/initialized` handshake.

手工检查：

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"server/discover"}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' \
  | python3 scripts/mcp_server.py
```

典型 Agent 调用顺序是先用 `query_docs` 找到 3～5 条候选，再用 `get_source` 补齐
需要引用的原文。回答时保留 `source.url`，不要把模型自己的概括当成新的事实来源。

An Agent should normally call `query_docs` for three to five candidates and then call
`get_source` for the sections it will cite. Preserve `source.url` in the final answer;
do not turn a model-generated summary into a new source of truth.

## 边界与校验 / Boundaries and validation

- 服务只读取仓库内两个生成的 JSONL 文件；`get_source` 只接受已有稳定 ID。
- 工具声明 `readOnlyHint: true` 和 `destructiveHint: false`，但客户端仍应展示并复核工具权限。
- 修改正文或 catalog 生成逻辑后，先重新生成并校验知识包，再运行 MCP 测试。

```bash
python3 scripts/build_ai_catalog.py --check
python3 scripts/validate_ai_catalog.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

The implementation follows the JSON-RPC and stdio framing rules in the
[Model Context Protocol specification](https://modelcontextprotocol.io/specification/2026-07-28)
and keeps the generated Markdown catalogs as the only factual source.
