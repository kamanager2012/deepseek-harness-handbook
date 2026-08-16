# Community 当前发行状态

> 事实快照：2026-08-16。本文区分代码线、Release 层级和 CI 证据，不替代 GitHub 最新 Release、Actions 结果或安装包实测。

## 三层版本模型

| 层级 | 当前值 | 应如何理解 |
|---|---|---|
| Codebase trunk | `0.1.2` | `dsh-community` 当前代码/package 线；不是 Stable Release 标签 |
| Stable Release | `v0.1.2` | 当前 Stable；GitHub Release 已发布 Linux AppImage、Windows NSIS 安装包和 macOS dmg，并提供对应 SHA256 文件 |
| Preview Release | `v0.1.2-preview` | 历史 Preview；保留用于回归对比，不是当前正式下载目标 |

README 和网页应使用“Stable / Preview / code line”三层表述，不要把旧 Preview、代码线
和 Stable 混成一个版本号。

## 用户选择

### Stable 用户

正式入口仍是 [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest)。
当前 Stable 用户应直接下载 [`v0.1.2`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.2)。
`v0.1.1` 的 Web 启动问题属于历史版本说明，不应继续作为当前下载建议。

### 测试用户

如需复现旧 Preview 行为，再使用 [`v0.1.2-preview`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.2-preview)。
普通用户不应把它当成比 Stable 更新的下载目标。

`v0.1.2` 当前发布资产为：

- `dsh-community-0.1.2.AppImage` + `.sha256`
- `DSH.Community.Setup.0.1.2.exe` + `.sha256`
- `dsh-community-0.1.2.dmg` + `.sha256`

## 三平台 Release Gate

以下是本快照对应的最新观察结果：

| Gate | 状态 | 事实 |
|---|---|---|
| 普通 `dsh-community` CI | `[REAL]` / GREEN | 代码、类型和常规测试通过 |
| Linux packaging | `[REAL]` / GREEN | AppImage 和 SHA256 资产生成 |
| Windows packaging | `[REAL]` / GREEN | NSIS 安装包和 SHA256 已随 `v0.1.2` 发布 |
| macOS packaging | `[REAL]` / GREEN | dmg 和 SHA256 已随 `v0.1.2` 发布 |
| Release publish | `[REAL]` / GREEN | [`v0.1.2` GitHub Release](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.2) 已公开下载 |
| 3-OS release gate | `[REAL]` / GREEN | `v0.1.2` 已完成 Linux、Windows、macOS 资产和校验文件闭环 |

目标链路是：

```text
tag
  → Linux / Windows / macOS build
  → artifact + SHA256
  → publish GitHub Release
```

`v0.1.2` 已完成这条三平台 Stable 链路。下一目标是维护 Release 资产、安装验证和
版本漂移检测，而不是在事实未闭合前继续堆叠版本号。

## 当前项目阶段

| 阶段 | 估计状态 | 当前事实 |
|---|---:|---|
| Phase 1 · Suite Reality Gate | 约 80–90% | Shell compound/metacharacter fail-closed、typed `SessionEvent.data` adapter、pre-enqueue fallback guard 和测试方向已有明显进展；True SDK runtime E2E 仍未证明，upstream probe CI 仍红 |
| Phase 2 · Edition → Community | 100% | Session selector、`new` / `resume last` / `sessions` / `doctor` 等功能已合流；Edition 代码已冻结，GitHub 仓库已归档，description 已指向 Community |
| Phase 3 · Cross-platform Release | 100% | `v0.1.2` 已发布 Linux、Windows、macOS 安装包和 SHA256 文件 |
| Phase 4 · Plugin supply chain | 主体完成 | Registry 当前有 9 个第三方插件在 rc.6 上完成官方安装链与组合验证；shape、npm existence、`dist.integrity`、仓库可达性和 provenance 已进入 CI，runtime smoke 仍需逐条人工证据 |
| Phase 5 · Handbook drift CI | 尚未展开 | 本页先作为人工版本事实入口 |
| Phase 6 · Marketplace UX | 100% | `info` 展示 digest/provenance，`install` 输出 registry digest 与 `npm view ... dist.integrity` 核对命令；当前测试 11/11 通过 |

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
