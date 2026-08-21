# Community 当前发行状态

> 事实快照：2026-08-21。`v0.1.2` exact-artifact smoke 已在真实 Windows、macOS 和 Linux runner 上通过；安装包/Runtime 首启为 `[PARTIAL]`，完整用户闭环仍按 `[待复核]` 处理。本文不替代 GitHub Release、Actions 结果或安装包实测。

## 三层版本模型

| 层级 | 当前值 | 应如何理解 |
|---|---|---|
| Codebase trunk | `0.1.0-rc.8-community.1` | 当前 `main` 的社区版本；尚未作为用户 Release 发布 |
| Official core | `@deepseek-ai/dsh@0.1.0-rc.8` | 社区版本的官方核心基线；社区后缀表示社区自有修补 |
| Published Latest | `v0.1.2` | GitHub 当前已发布 Stable；精确资产 smoke 已部分通过，完整用户闭环仍需复核 |
| Draft / pre-release | `v0.1.6` | draft/pre-release；当前只有 checksum 资产，不是下载入口 |

README 和网页应使用“Stable / Preview / code line”三层表述，不要把旧 Preview、代码线
和 Stable 混成一个版本号。

Desktop 与 TUI 的版本身份必须同时显示：

```text
DeepSeek Harness Community v0.1.0-rc.8-community.1 [Official Core: @deepseek-ai/dsh@0.1.0-rc.8]
```

## 用户选择

### Stable 用户

正式入口仍是 [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest)。
当前 Stable 用户应从 [`releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest)
下载已发布的 [`v0.1.2`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.2)。
不要下载 `v0.1.6` draft，也不要把 `0.1.0-rc.8-community.1` 源码线或 staging 产物当成 Stable 下载。

### Preview / 测试用户

`v0.1.6` 当前是 draft/pre-release，不是可供普通用户下载的 Preview；普通用户不要因为
draft、源码版本或 staging 更新就绕过已发布的 `v0.1.2`。

`v0.1.2` 已发布资产为：

- `dsh-community-0.1.2.AppImage` + `.sha256`
- `DSH.Community.Setup.0.1.2.exe` + `.sha256`（历史已发布资产命名）
- `dsh-community-0.1.2.dmg` + `.sha256`

三个 Community endpoint 是 WSL/Linux Terminal、Windows Desktop、macOS Desktop `[PARTIAL]`；首启/缺 key smoke 已覆盖，完整用户闭环仍需复核。
官方 Web 是共享 `~/.dsh` 的官方兼容入口，不是 Community endpoint。

## 三平台 Release Gate

以下是本快照对应的最新观察结果；完整用户闭环仍为 `[待复核]`：

| Gate | 状态 | 事实 |
|---|---|---|
| 普通 `dsh-community` CI | `[待复核]` | 当前 main 的 CI 通过不等于安装包验证 |
| Release assets | `[REAL]` | `v0.1.2` 包含 AppImage、dmg、Windows Setup，均有 sha256 |
| artifact-smoke | `[PARTIAL]` | [Run 32470195309](https://github.com/kamanager2012/dsh-community/actions/runs/32470195309) 的 resolve、Windows、macOS、Linux 四个 job 全部通过 |
| Official Runtime staging / installer | `[PARTIAL]` | v0.1.2 真实资产的 Windows/macOS 安装与 Runtime 首启通过；未覆盖完整生命周期 |
| 3-OS release gate | `[PARTIAL]` | 真实资产 checksum、Windows/macOS 首启和 Linux TUI 缺 key/无 TTY 通过；完整用户闭环尚未定稿 |

目标链路是：

```text
tag
  → Linux / Windows / macOS build
  → artifact + SHA256
  → publish GitHub Release
```

`v0.1.2` 是当前已发布 Latest。下一步不是继续堆叠版本号，而是补齐 exact artifact smoke
之外的 Session、插件、升级/卸载重装、网络失败和人工首对话证据；`0.1.0-rc.8-community.1`
在此之前保持为源码线。

## Stable 发布基线与当前 main

`v0.1.2` 是当前 Stable 发布基线。代码/package 线是 `0.1.0-rc.8-community.1`，
官方核心是 `@deepseek-ai/dsh@0.1.0-rc.8`；main 源码或 CI 结果不能替代 Release asset
与安装闭环复核，因此本页仍禁止写“安装包已验证”。

## Distribution Reality Gate

当前进入用户现实门禁，而不是继续扩大 Build Gate。下表记录 exact-release-artifact 证据；已完成的首启 smoke 标为 `[PARTIAL]`，未覆盖的完整闭环标为 `[待复核]`：

| 场景 | 状态 | 必须证明 |
|---|---|---|
| Windows clean VM + `DSH.Community.Setup.0.1.2.exe` | `[PARTIAL]` | [Run 32470195309](https://github.com/kamanager2012/dsh-community/actions/runs/32470195309) 下载真实资产、校验、静默安装、首启和 Runtime HTTP readiness 通过 |
| macOS clean host + `dsh-community-0.1.2.dmg` | `[PARTIAL]` | 同一 run 下载真实资产、校验、挂载、首启和 Runtime HTTP readiness 通过 |
| WSL/Linux clean host + `dsh-community` / `pnpm tui` | `[PARTIAL]` | 同一 run 的 Linux TUI help、version、缺 key doctor、sessions、无 TTY 拒绝路径通过 |
| Session 闭环 | `[待复核]` | 新建、恢复、官方 Web ↔ Windows/macOS Desktop ↔ WSL/Linux TUI 共享同一 `~/.dsh` Session |
| Plugin / restart | `[待复核]` | 官方 `dsh plugin add`、重启后仍可用、失败时有明确错误 |
| Lifecycle recovery | `[待复核]` | 卸载重装、升级、断网、缺少密钥、Runtime 解压中断后的行为 |
| Official Runtime staging / installer | `[PARTIAL]` | 真实 Windows/macOS 资产首启 readiness 通过；不能据此宣称完整安装生命周期已验证 |

这条门禁的结论必须来自 Release 页面真实下载的包，并且要结合安装、Runtime staging
和用户闭环结果；main 源码 smoke、普通 CI 或 README 声明都不能代替它。`v0.1.2`
artifact-smoke 已完成一轮真实 Windows、macOS、WSL/Linux runner 检查 `[PARTIAL]`，
但这仍不足以证明完整用户闭环已验证。

## 当前项目阶段

| 阶段 | 估计状态 | 当前事实 |
|---|---:|---|
| Phase 1 · Suite Reality Gate | 约 80–90% `[待复核]` | Shell compound/metacharacter fail-closed、typed `SessionEvent.data` adapter、pre-enqueue fallback guard 和测试方向已有明显进展；True SDK runtime E2E 仍未证明，upstream probe CI 仍红 |
| Phase 2 · Edition → Community | 100% `[待复核]` | Session selector、`new` / `resume last` / `sessions` / `doctor` 等功能已合流；Edition 代码已冻结，GitHub 仓库已归档，description 已指向 Community |
| Phase 3 · Cross-platform Release | `[PARTIAL]` | `v0.1.2` 真实资产和 sha256 已发布，exact-artifact smoke 通过；完整生命周期仍未覆盖 |
| Phase 4 · Distribution Reality Gate | `[PARTIAL]` | artifact-smoke 四个 job 通过；Session、插件、升级/卸载重装和完整用户闭环未定稿 |
| Phase 4 工作流 · Plugin supply chain | `[待复核]` | 9 个验证插件；shape、npm 存在性/版本、`dist.integrity`、provenance、仓库可达与 compose 已纳入验证 |
| Phase 4 工作流 · Marketplace UX | `[待复核]` | CLI 为 `list/search/info/install`；`info` 展示 digest/provenance |
| Phase 5 · Handbook drift CI | 尚未展开 `[待复核]` | 本页先作为人工版本事实入口 |

## Runtime 版本来源差异

当前需要同时记录这些事实来源：

```text
Official GitHub / package source: @deepseek-ai/dsh@0.1.0-rc.8
Community source line: 0.1.0-rc.8-community.1
Published Latest: v0.1.2
Draft/pre-release: v0.1.6 (not a user download)
```

涉及 CLI、Session、Event、SDK 或 Plugin surface 时，优先核对已安装/发布包、当前
`--help`、导出配置、contract snapshot 和真实运行结果；不要从旧快照推断当前版本。

参考：

- [`dsh-community` release workflow](https://github.com/kamanager2012/dsh-community/blob/main/.github/workflows/release.yml)
- [`dsh-community` changelog](https://github.com/kamanager2012/dsh-community/blob/main/CHANGELOG.md)
- [`dsh-community` contract snapshots](https://github.com/kamanager2012/dsh-community/tree/main/contracts)
- [`deepseek-harness-suite` Actions](https://github.com/kamanager2012/deepseek-harness-suite/actions)
- [`dsh-community-edition` freeze commit `09eb1c0`](https://github.com/kamanager2012/dsh-community-edition/commit/09eb1c0)
