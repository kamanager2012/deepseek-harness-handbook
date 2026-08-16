# Community 当前发行状态

> 事实快照：2026-08-16。本文区分代码线、Release 层级和 CI 证据，不替代 GitHub 最新 Release、Actions 结果或安装包实测。

## 三层版本模型

| 层级 | 当前值 | 应如何理解 |
|---|---|---|
| Codebase trunk | `0.1.4` | `dsh-community` 当前代码/package 线；不是 Stable Release 标签 |
| Stable Release | `v0.1.4` | 当前 Stable；GitHub Release 已发布 Linux AppImage、Windows NSIS 安装包和 macOS dmg，并提供对应 SHA256 文件 |
| Preview Release | `v0.1.3` | 当前最新 Preview；不是当前 Stable 下载目标 |

README 和网页应使用“Stable / Preview / code line”三层表述，不要把旧 Preview、代码线
和 Stable 混成一个版本号。

## 用户选择

### Stable 用户

正式入口仍是 [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest)。
当前 Stable 用户应直接下载 [`v0.1.4`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.4)。
`v0.1.1` 的 Web 启动问题属于历史版本说明，不应继续作为当前下载建议。

### Preview / 测试用户

需要测试最新预发布行为时使用 [`v0.1.3`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.3)。
`v0.1.2-preview` 只作为旧 Preview 回归记录，普通用户不应把它当成比 Stable 更新的下载目标。

`v0.1.4` 当前发布资产为：

- `dsh-community-0.1.4.AppImage` + `.sha256`（可选/次要 Linux artifact）
- `DSH.Community.Setup.0.1.4.exe` + `.sha256`（Windows Desktop）
- `dsh-community-0.1.4.dmg` + `.sha256`（macOS Desktop）

Linux 的主力 Community endpoint 是 WSL/Linux Terminal；官方 Web 是上游兼容入口，不是 Community 发行端。

## 三平台 Release Gate

以下是本快照对应的最新观察结果：

| Gate | 状态 | 事实 |
|---|---|---|
| 普通 `dsh-community` CI | `[REAL]` / GREEN | 代码、类型和常规测试通过 |
| Linux packaging | `[REAL]` / GREEN | AppImage 和 SHA256 资产生成 |
| Windows packaging | `[REAL]` / GREEN | NSIS 安装包和 SHA256 已随 `v0.1.4` 发布 |
| macOS packaging | `[REAL]` / GREEN | dmg 和 SHA256 已随 `v0.1.4` 发布 |
| Release publish | `[REAL]` / GREEN | [`v0.1.4` GitHub Release](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.4) 已公开下载 |
| 3-OS release gate | `[REAL]` / GREEN | `v0.1.4` 已完成 Linux、Windows、macOS 资产和校验文件闭环 |

目标链路是：

```text
tag
  → Linux / Windows / macOS build
  → artifact + SHA256
  → publish GitHub Release
```

`v0.1.4` 已完成这条三平台 Stable 链路。下一目标是维护 Release 资产、安装验证和
版本漂移检测，而不是在事实未闭合前继续堆叠版本号。

## Stable 发布基线与当前 main

`v0.1.4` 是当前三系统 Stable 的发布基线。当前 `main` 代码/package 线为 `0.1.4`，不能用 main 源码或 CI 结果替代已发布安装包的验证。`v0.1.2` 仅是历史上的第一个三系统 Stable 基线；当前验证必须从 [v0.1.4 Release](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.4) 下载并记录实际文件名和 SHA256。

## Distribution Reality Gate

当前进入用户现实门禁，而不是继续扩大 Build Gate。下表是待完成的 exact-release-artifact 证据；在没有干净环境实测前统一标为 `[UNVERIFIED]`：

| 场景 | 状态 | 必须证明 |
|---|---|---|
| Windows clean VM + `DSH.Community.Setup.0.1.4.exe` | `[UNVERIFIED]` | 安装、首次启动、密钥配置、Runtime 解压和正常退出 |
| macOS clean host + `dsh-community-0.1.4.dmg` | `[UNVERIFIED]` | 安装、首次启动、权限提示、Runtime 启动和正常退出 |
| WSL/Linux clean host + `dsh-community` / `pnpm tui` | `[UNVERIFIED]` | 终端启动、密钥配置、新建/恢复和正常退出 |
| Linux optional artifact + `dsh-community-0.1.4.AppImage` | `[UNVERIFIED]` | AppImage 启动和 Runtime 启动；不代表 Linux 主端 |
| Session 闭环 | `[UNVERIFIED]` | 新建、恢复、官方 Web ↔ Windows/macOS Desktop ↔ WSL/Linux TUI 共享同一 `~/.dsh` Session |
| Plugin / restart | `[UNVERIFIED]` | 官方 `dsh plugin add`、重启后仍可用、失败时有明确错误 |
| Lifecycle recovery | `[UNVERIFIED]` | 卸载重装、升级、断网、缺少密钥、Runtime 解压中断后的行为 |

这条门禁的结论必须来自 Release 页面真实下载的包；main 源码 smoke、普通 CI 或 README 声明都不能代替它。
最新 `artifact-smoke` run [31935679026](https://github.com/kamanager2012/dsh-community/actions/runs/31935679026) 的 macOS exact job 通过、Windows exact job 失败，因此整条用户现实门禁仍是 `[UNVERIFIED]`。

## 当前项目阶段

| 阶段 | 估计状态 | 当前事实 |
|---|---:|---|
| Phase 1 · Suite Reality Gate | 约 80–90% | Shell compound/metacharacter fail-closed、typed `SessionEvent.data` adapter、pre-enqueue fallback guard 和测试方向已有明显进展；True SDK runtime E2E 仍未证明，upstream probe CI 仍红 |
| Phase 2 · Edition → Community | 100% | Session selector、`new` / `resume last` / `sessions` / `doctor` 等功能已合流；Edition 代码已冻结，GitHub 仓库已归档，description 已指向 Community |
| Phase 3 · Cross-platform Release | 100% | `v0.1.4` 已发布 Linux、Windows、macOS 安装包和 SHA256 文件 |
| Phase 4 · Distribution Reality Gate | 进行中 | 从 exact `v0.1.4` 资产开始做 Windows、macOS Desktop、WSL/Linux Terminal、插件、重启、升级和失败路径验证 |
| Phase 4 工作流 · Plugin supply chain | 主体完成 | Registry 当前有 9 个第三方插件在 rc.6 上完成官方安装链与组合验证；shape、npm existence、`dist.integrity`、仓库可达性和 provenance 已进入 CI，runtime smoke 仍需逐条人工证据 |
| Phase 4 工作流 · Marketplace UX | 100% | `info` 展示 digest/provenance，`install` 输出 registry digest 与 `npm view ... dist.integrity` 核对命令；当前测试 11/11 通过 |
| Phase 5 · Handbook drift CI | 尚未展开 | 本页先作为人工版本事实入口 |

## Runtime 版本来源差异

当前需要同时记录两个事实来源：

```text
Official GitHub main release commit: 47f9438 / rc.5
Community published-package target:  @deepseek-ai/dsh@0.1.0-rc.6
```

这不是自动矛盾：发布包可能先于 GitHub main 的可见 release commit 更新。
涉及 CLI、Session、Event、SDK 或 Plugin surface 时，优先核对已安装/发布包、当前
`--help`、导出配置、contract snapshot 和真实运行结果。

参考：

- [Official upstream commit `47f9438`](https://github.com/deepseek-ai/deepseek-harness/commit/47f9438)
- [`dsh-community` release workflow](https://github.com/kamanager2012/dsh-community/blob/main/.github/workflows/release.yml)
- [`dsh-community` changelog](https://github.com/kamanager2012/dsh-community/blob/main/CHANGELOG.md)
- [`dsh-community` contract snapshots](https://github.com/kamanager2012/dsh-community/tree/main/contracts)
- [`deepseek-harness-suite` Actions](https://github.com/kamanager2012/deepseek-harness-suite/actions)
- [`dsh-community-edition` freeze commit `09eb1c0`](https://github.com/kamanager2012/dsh-community-edition/commit/09eb1c0)
