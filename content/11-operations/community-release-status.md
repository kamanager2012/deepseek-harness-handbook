# Community 当前发行状态

> 初稿事实快照：2026-08-16。所有“当前状态”均标为 `[待复核]`；本文不替代 GitHub Release、Actions 结果、staging 复核或安装包实测。

## 三层版本模型

| 层级 | 当前值 | 应如何理解 |
|---|---|---|
| Codebase trunk | `[待复核]` | 当前代码/package 线；不能从 Stable tag 反推 |
| Stable Release | `v0.1.2` `[待复核]` | Latest Stable；资产为 Linux AppImage、macOS dmg、Windows `DSH.Community.Setup.exe`，各有 `.sha256` |
| Preview Release | `[待复核]` | 本任务事实未指定当前 Preview，不在初稿中臆造 |

README 和网页应使用“Stable / Preview / code line”三层表述，不要把旧 Preview、代码线
和 Stable 混成一个版本号。

## 用户选择

### Stable 用户

正式入口仍是 [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest)。
当前 Stable 用户应直接下载 [`v0.1.2`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.2) `[待复核]`。
不要把未复核的 Preview、main 代码线或 staging 产物当成 Stable 下载建议。

### Preview / 测试用户

当前 Preview 值未纳入本任务事实 `[待复核]`。普通用户不要因为某个 Preview 或开发号
更新就绕过 `v0.1.2` Stable。

`v0.1.2` 当前发布资产为 `[待复核]`：

- `dsh-community-0.1.2.AppImage` + `.sha256`
- `DSH.Community.Setup.0.1.2.exe` + `.sha256`
- `dsh-community-0.1.2.dmg` + `.sha256`

三个 Community endpoint 是 WSL/Linux Terminal、Windows Desktop、macOS Desktop `[待复核]`。
官方 Web 是共享 `~/.dsh` 的官方兼容入口，不是 Community endpoint。

## 三平台 Release Gate

以下是本快照对应的最新观察结果 `[待复核]`：

| Gate | 状态 | 事实 |
|---|---|---|
| 普通 `dsh-community` CI | `[待复核]` | 不在本任务事实中单独宣称通过 |
| Release assets | `[待复核]` | `v0.1.2` 包含 AppImage、dmg、Windows Setup，均有 sha256 |
| artifact-smoke | `[待复核]` | 已完成一轮 Windows、macOS、WSL/Linux 干净机首启检查 |
| Official Runtime staging | `NOT_READY` `[待复核]` | 暂存方案正在重做；不得写成安装包已验证 |
| 3-OS release gate | `[待复核]` | 资产发布和 smoke 子集有记录，但 staging / 完整用户闭环尚未定稿 |

目标链路是：

```text
tag
  → Linux / Windows / macOS build
  → artifact + SHA256
  → publish GitHub Release
```

`v0.1.2` 是本初稿采用的 Latest Stable 事实 `[待复核]`。下一步不是继续堆叠版本号，
而是完成 staging 重做、复核 exact artifact 和保留完整用户闭环证据。

## Stable 发布基线与当前 main

`v0.1.2` 是当前 Stable 发布基线 `[待复核]`。代码/package 线不能从本页臆造，
main 源码或 CI 结果也不能替代 Release asset 与 staging 复核。当前官方 Runtime
staging 为 `NOT_READY`，因此本页禁止写“安装包已验证”。

## Distribution Reality Gate

当前进入用户现实门禁，而不是继续扩大 Build Gate。下表记录 exact-release-artifact 证据；在 staging 未就绪、事实尚未定稿前统一标为 `[待复核]`：

| 场景 | 状态 | 必须证明 |
|---|---|---|
| Windows clean VM + `DSH.Community.Setup.0.1.2.exe` | `[待复核]` | artifact-smoke 已有一轮首启记录；不等于 installer/staging 已验证 |
| macOS clean host + `dsh-community-0.1.2.dmg` | `[待复核]` | artifact-smoke 已有一轮首启记录；不等于 installer/staging 已验证 |
| WSL/Linux clean host + `dsh-community` / `pnpm tui` | `[待复核]` | artifact-smoke 已有一轮首启记录；不等于完整用户闭环已验证 |
| Session 闭环 | `[待复核]` | 新建、恢复、官方 Web ↔ Windows/macOS Desktop ↔ WSL/Linux TUI 共享同一 `~/.dsh` Session |
| Plugin / restart | `[待复核]` | 官方 `dsh plugin add`、重启后仍可用、失败时有明确错误 |
| Lifecycle recovery | `[待复核]` | 卸载重装、升级、断网、缺少密钥、Runtime 解压中断后的行为 |
| Official Runtime staging | `NOT_READY` `[待复核]` | 暂存方案正在重做；不能宣称安装包已验证 |

这条门禁的结论必须来自 Release 页面真实下载的包，并且要结合 staging 重做结果；
main 源码 smoke、普通 CI 或 README 声明都不能代替它。`v0.1.2` artifact-smoke
已完成一轮 Windows、macOS、WSL/Linux 干净机首启检查 `[待复核]`，但当前
`NOT_READY` staging 使“安装包已验证”仍然是禁止表述。

## 当前项目阶段

| 阶段 | 估计状态 | 当前事实 |
|---|---:|---|
| Phase 1 · Suite Reality Gate | 约 80–90% `[待复核]` | Shell compound/metacharacter fail-closed、typed `SessionEvent.data` adapter、pre-enqueue fallback guard 和测试方向已有明显进展；True SDK runtime E2E 仍未证明，upstream probe CI 仍红 |
| Phase 2 · Edition → Community | 100% `[待复核]` | Session selector、`new` / `resume last` / `sessions` / `doctor` 等功能已合流；Edition 代码已冻结，GitHub 仓库已归档，description 已指向 Community |
| Phase 3 · Cross-platform Release | `[待复核]` | `v0.1.2` 资产和 sha256 已发布；不能据此宣称安装包已验证 |
| Phase 4 · Distribution Reality Gate | `[待复核]` | artifact-smoke 已完成一轮 Win/mac/Linux 首启检查，但 staging 为 NOT_READY，完整用户闭环未定稿 |
| Phase 4 工作流 · Plugin supply chain | `[待复核]` | 9 个验证插件；shape、npm 存在性/版本、`dist.integrity`、provenance、仓库可达与 compose 已纳入验证 |
| Phase 4 工作流 · Marketplace UX | `[待复核]` | CLI 为 `list/search/info/install`；`info` 展示 digest/provenance |
| Phase 5 · Handbook drift CI | 尚未展开 `[待复核]` | 本页先作为人工版本事实入口 |

## Runtime 版本来源差异

当前需要同时记录两个事实来源 `[待复核]`：

```text
Official GitHub / package source: [待复核]
Community published-package target: [待复核]
```

涉及 CLI、Session、Event、SDK 或 Plugin surface 时，优先核对已安装/发布包、当前
`--help`、导出配置、contract snapshot 和真实运行结果；不要从旧快照推断当前版本。

参考：

- [`dsh-community` release workflow](https://github.com/kamanager2012/dsh-community/blob/main/.github/workflows/release.yml)
- [`dsh-community` changelog](https://github.com/kamanager2012/dsh-community/blob/main/CHANGELOG.md)
- [`dsh-community` contract snapshots](https://github.com/kamanager2012/dsh-community/tree/main/contracts)
- [`deepseek-harness-suite` Actions](https://github.com/kamanager2012/deepseek-harness-suite/actions)
- [`dsh-community-edition` freeze commit `09eb1c0`](https://github.com/kamanager2012/dsh-community-edition/commit/09eb1c0)
