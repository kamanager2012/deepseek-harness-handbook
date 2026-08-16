# Community Labs handoff：给接手 Agent 的执行基线

> 内部维护说明。基线日期：2026-08-16。本文约束研发方向，不替代官方 Runtime 文档。

## 目标和禁止事项

`deepseek-harness-suite` 是 Community Labs，不是第二个用户发行版。它用于验证官方 SDK transport、Bridge、先进 TUI、安全能力、Checkpoint、Undo、审计和实验性 Desktop UX。

接手 Agent 必须遵守：

- 不重新设计六仓战略；
- 不把 Suite 变成正式下载入口；
- 不继续发展 `dsh-community-edition`；
- 不重新实现官方 Agent loop 或官方 Session persistence；
- 不 vendor 官方 core packages；
- 不用 README、单元测试或 fallback 成功冒充真实 Runtime E2E；
- 不在 Reality Gate 未通过前增加新的 UI、命令、Dashboard、Marketplace 功能或大型架构；
- 未知 capability 默认 fail-closed；
- 所有进入 `dsh-community` 的 Labs 能力都必须经过门禁、失败路径和跨平台验证。

## 当前状态矩阵

以下是 handoff 状态，不是对未来版本的承诺。代码、测试和运行结果变化后，必须同步更新状态和证据。

| 能力 | 当前状态 | 不能宣称 |
| --- | --- | --- |
| Official Session 污染隔离 | `[REAL]` `[READ-SAFE]`：官方 `~/.dsh/sessions` 只读；Suite 自有数据使用 `~/.dsh/suite_sessions` | 不能宣称两边已经完全兼容所有迁移场景 |
| Checkpoint workspace jail | `[WORKSPACE-JAIL]`：包含 realpath、最近存在祖先、symlink escape、`..`、NUL 和控制字符检查；undo 前再次校验边界 | 不能宣称已有 durable rollback 或 crash recovery |
| Checkpoint 持久化 | `[NOT_IMPLEMENTED]`：主要仍是进程生命周期内的 `CheckpointRecord[]` | 不能宣称重启后可恢复 Undo |
| Risk Engine capability model | `[FAIL-CLOSED]`：按 `fs:read`、`fs:write`、`fs:delete`、`process:exec` 等 capability 判断；未知工具默认拒绝 | 不能把工具名前缀当成完整安全模型 |
| Shell policy | `[PARTIAL]`：仍需移除 `startsWith("git status")` 等字符串白名单绕过 | 不能宣称已防住 `&&`、管道、重定向、替换和复合命令 |
| Official SDK 依赖与 Bridge 架构 | `[LABS]`：已接入 `@deepseek-ai/dsh-sdk-client` 方向 | 不能把依赖存在等同于 SDK 真 E2E |
| SDK JSON-RPC 真 E2E | `[UNVERIFIED]`：`jsonrpc-agent` 不是普通 shipped profile，fallback 不能证明 SDK 成功 | 不能宣称 `executionMode = sdk_jsonrpc` 已被真实验收 |
| SessionEvent adapter | `[PARTIAL]`：事件名称已开始对齐，但仍有直接猜 `content`、`delta`、`args` 等字段的 mapping | 不能依赖 `as any` 或猜测字段 |
| Fallback | `[PARTIAL]`：SDK 失败会显式通知；仍需防止 prompt 已入队后重复执行 | 不能自动重放可能已经产生副作用的 prompt |
| Runtime HITL | `[BLOCKED_BY_UPSTREAM]`：SDK 尚未开放完整 server→client approval request/response 闭环 | 不能假装客户端 `requiresApproval` 已等于 Runtime 审批闭环 |
| Dynamic Contract Probe | `[PROBE]`：可探测 CLI、profile 和配置不变量；CI 稳定性仍需单独证明 | 不能把一次探针成功写成完整 Contract Diff |

## 当前 P0 顺序

不要并行扩展功能，按 seam 收口：

1. **Shell Policy**：解析 executable、argv、redirection、pipeline 和 side effects；拒绝 `|`、`&&`、`||`、`;`、`>`、`>>`、`$()`、反引号等未经验证的复合语法。
2. **True SDK Runtime E2E**：找到官方正确 JSON-RPC runtime entrypoint；测试必须硬断言 `executionMode === sdk_jsonrpc`，禁止 fallback 掩盖失败。
3. **Typed SessionEvent Adapter**：严格走 `notification.params.event.type` 和 `event.data`，再进入 typed decoder 和社区事件模型。
4. **Fallback Replay Safety**：区分 `NOT_STARTED`、`INITIALIZED`、`PROMPT_ENQUEUED`、`ACTIVE`；一旦 prompt 已被官方 Runtime 接受，禁止自动 fallback，必须 fail loud。

## Reality Gate：Labs 如何进入产品

代码写好、单测通过或 README 写完都不足以晋升。至少要经过：

```text
Reality Gate
  → Upstream Contract Gate
  → Security Boundary Gate
  → Real E2E
  → Cross-platform Smoke
  → Failure-path Test
  → Documentation
  → Canary
  → Preview
  → Stable
```

晋升路径只有一条：

```text
Community Labs
  → 验证通过
  → dsh-community Canary
  → dsh-community Preview
  → dsh-community Stable
```

Suite 不成为发行渠道。Edition 的价值应合流到 `dsh-community` 后归档，而不是继续形成 Stable / Advanced / Experimental 三条产品线。

## Agent 完成任务时必须报告什么

每个 Labs 任务结束时，用以下结构报告，避免把推断写成事实：

```text
状态：[REAL] / [PARTIAL] / [LABS] / [PROBE] / [UNVERIFIED]
范围：实际修改了哪些文件和模块
真实证据：执行过的命令、测试、退出码、E2E 或探针结果
未验证：没有运行、被 fallback、受上游限制或只做了 mock 的部分
风险：失败路径、重复执行、权限、workspace 或跨平台缺口
下一步：只列当前门禁允许的最小下一步
```

禁止用“全部完成”“完全安全”“生产就绪”“100% 兼容”代替证据。

## 文档维护规则

- 官方 Runtime 的事实以官方仓库、当前 `--help`、导出的配置和运行结果为准；
- 社区产品的事实必须指向真实代码、测试、Release 或 Evidence Record；
- 计划、假设和未验证能力必须显式加状态标签；
- 用户下载入口只能写 [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest)；
- 更新架构边界时，同时检查 [社区生态与产品入口](../00-overview/community-ecosystem.md)、项目 README 和发布清单是否仍一致。
