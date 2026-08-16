# Community 当前发行状态

> 事实快照：2026-08-16。本文区分代码线、Release 层级和 CI 证据，不替代 GitHub 最新 Release、Actions 结果或安装包实测。

## 三层版本模型

| 层级 | 当前值 | 应如何理解 |
|---|---|---|
| Codebase trunk | `0.1.2` | `dsh-community` 当前代码/package 线；不是 Stable Release 标签 |
| Preview Release | `v0.1.2-preview` | 当前更值得测试的预览版；修复 Web 启动、system Node 优先、`DSH_COMMUNITY_BIN`、readiness polling、502 warm-up、插件子进程 teardown、`doctor` 和官方插件安装/卸载链路 |
| Stable Release | `v0.1.1` | 当前 Stable；已知 Linux AppImage 中官方 `dsh web` 可能无法正确绑定端口，不能把它写成当前最佳体验 |

README 和网页应使用“Stable / Preview / code line”三层表述，不要再写成
`DSH Community = 0.1.1`。

## 用户选择

### Stable 用户

正式入口仍是 [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest)。
但在推广 Linux Desktop 前，应明确说明 `v0.1.1` 的已知 Web 启动问题，并优先等待修复后的跨平台 Stable。

### 测试用户

当前应测试 [`v0.1.2-preview`](https://github.com/kamanager2012/dsh-community/releases/tag/v0.1.2-preview)。
它比 `v0.1.1` 更接近可用版本，但当前可见资产仍主要是 Linux AppImage；Windows/macOS
不能因为 workflow 已写出就宣称已经可下载、可验证。

## 三平台 Release Gate

以下是本快照对应的最新观察结果：

| Gate | 状态 | 事实 |
|---|---|---|
| 普通 `dsh-community` CI | `[REAL]` / GREEN | 代码、类型和常规测试通过 |
| Linux packaging | `[REAL]` / GREEN | AppImage 和 SHA256 资产生成 |
| Windows packaging | `[UNVERIFIED]` / RED | NSIS 与 portable zip workflow 仍失败 |
| macOS packaging | `[UNVERIFIED]` / RED | dmg workflow 仍失败 |
| Release publish | `SKIPPED` | publish 依赖三平台 jobs，Windows/macOS 失败时不会闭环 |
| 3-OS Release Gate | `RED` | Phase 3 已建立工程骨架，但尚未完成 |

目标链路是：

```text
tag
  → Linux / Windows / macOS build
  → artifact + SHA256
  → publish GitHub Release
```

目标链路已经存在，不等于当前链路已成功。下一目标是把 `0.1.2` 做成真正的三平台
Stable，而不是继续堆叠 `0.1.3` 功能。

## 当前项目阶段

| 阶段 | 估计状态 | 当前事实 |
|---|---:|---|
| Phase 1 · Suite Reality Gate | 约 80–90% | Shell compound/metacharacter fail-closed、typed `SessionEvent.data` adapter、pre-enqueue fallback guard 和测试方向已有明显进展；True SDK runtime E2E 仍未证明，upstream probe CI 仍红 |
| Phase 2 · Edition → Community | 约 90% | Session selector、`new` / `resume last` / `sessions` / `doctor` 等功能已合流；Edition 代码已冻结，但 GitHub archive 和 repository metadata 仍未完成 |
| Phase 3 · Cross-platform Release | 约 60% | Linux 绿，Windows/macOS 红，publish 未闭环 |
| Phase 4 · Plugin supply chain | 尚未正式展开 | 当前先保持 7 个 rc.6 已验证插件，提升 existence/install/compose/runtime smoke/digest/provenance 深度 |
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
