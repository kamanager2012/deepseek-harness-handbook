# DeepSeek Harness Community 生态与产品入口

> 本页是 DeepSeek Harness Community 生态的项目 handoff。基线日期：2026-08-16。

本项目不是 DeepSeek Harness 的 fork，也不是另一套 Agent Runtime。唯一的执行核心仍然是官方 [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness)；社区仓库围绕官方 Runtime 提供发行、兼容、插件、知识、诊断和实验能力。

## 先记住三个结论

1. **官方 Runtime 是发动机**：Agent loop、模型调用、工具执行、官方 session 持久化和核心生命周期由官方 Runtime 负责。
2. **`dsh-community` 是唯一正式产品**：普通用户只需要下载、安装和使用它。
3. **Suite 是实验室**：`deepseek-harness-suite` 的能力只有通过 Reality Gate、真实 E2E、安全验证和跨平台烟测后，才可以进入 `dsh-community` 的 Canary、Preview 或 Stable。

## 普通用户从哪里开始

```text
官方 DeepSeek Harness Runtime
            │
            ▼
       dsh-community
        ├── Desktop
        └── Terminal / TUI
```

正式软件入口统一指向 [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest)。本 handoff 记录的当前 Stable 是 `v0.1.1`；发布前仍应以仓库最新 Release、安装包和兼容说明为准。

用户不应该在 `Suite`、`Edition`、`Marketplace` 和 `Plugins` 之间做产品选择：它们分别是研发、归档、分发体验和数据注册表，不是第二、第三或第四个客户端。

## 六个仓库的职责

| 仓库 | 定位 | 面向谁 | 是否是正式下载入口 |
| --- | --- | --- | --- |
| [`dsh-community`](https://github.com/kamanager2012/dsh-community) | Canonical Product：官方 Runtime 上的 Desktop、TUI、诊断、兼容和发行层 | 所有用户、维护者 | **是，唯一入口** |
| [`deepseek-harness-suite`](https://github.com/kamanager2012/deepseek-harness-suite) | Community Labs：SDK transport、安全、Checkpoint、Bridge 和实验 UX | 维护者、实验开发者 | 否 |
| [`deepseek-harness-handbook`](https://github.com/kamanager2012/deepseek-harness-handbook) | Knowledge / Evidence：工程实施、验收、运维和版本事实 | 用户、维护者、Agent | 否 |
| [`dsh-community-plugins`](https://github.com/kamanager2012/dsh-community-plugins) | Compatibility Registry：插件元数据、版本和验证线 | 插件作者、维护者 | 否 |
| [`dsh-marketplace`](https://github.com/kamanager2012/dsh-marketplace) | Discovery / Distribution UX：浏览、搜索和安装入口 | 用户、插件作者 | 否；不是 Runtime |
| [`dsh-community-edition`](https://github.com/kamanager2012/dsh-community-edition) | Merge & Archive：历史发行线，价值合流后归档 | 维护者 | 否；停止双线发展 |

关系可以简化为：

```text
                         Official DeepSeek Harness
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │       dsh-community        │
                    │      Canonical Product     │
                    └────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
             Handbook / Evidence        Plugins / Registry
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                         dsh-marketplace
                      Discovery / Install UX

             deepseek-harness-suite → Community Labs
             dsh-community-edition  → Merge & Archive
```

## 官方层和社区层的边界

| 官方 Runtime 负责 | 社区层负责 |
| --- | --- |
| Agent loop 和模型执行 | Desktop / TUI 发行体验 |
| 工具执行和 Runtime 生命周期 | 生命周期包装、诊断和兼容层 |
| 官方 Session persistence | 官方 session 的读取、恢复和展示 |
| 官方事件与插件 surface | Bridge normalization、插件目录和验证说明 |
| 官方 profile、CLI 和协议 | 安全集成、发行打包和用户入口 |

社区层不得重新实现 Agent loop、维护第二套等价 Session 真源、fork 官方 event vocabulary，或 vendor 官方 core packages。官方能力已经存在时，优先调用官方能力；只有确认存在缺口时才增加社区扩展。

## Marketplace 和 Plugins 不是一回事

```text
dsh-community-plugins
        │  catalog / testedDsh / verification
        ▼
dsh-marketplace
        │  browse / search / install UX
        ▼
官方 dsh plugin add / 官方安装链
```

`dsh-community-plugins` 是兼容性注册表，不是另一个 Plugin Manager；`dsh-marketplace` 是发现和安装体验，不是 Package Manager replacement，也不拥有 Runtime。安装应尽量回到官方 `dsh plugin add` 链路。

## 面向维护者的阅读入口

- 想了解当前边界：阅读本页和 [官方架构概览](architecture.md)。
- 想接手实验舱：阅读 [Community Labs handoff](../11-operations/community-labs-handoff.md)。
- 想发布正式版本：阅读 [发布检查清单](../11-operations/release-checklist.md)。
- 想维护插件生态：阅读 [插件与 Cordis](../10-plugins/README.md)。

## 文档中的状态标签

文档必须区分“代码存在”和“能力已被真实证明”：

| 标签 | 含义 |
| --- | --- |
| `[REAL]` | 有对应代码、测试和可复现运行证据 |
| `[PARTIAL]` | 已实现一部分，但仍有已知缺口 |
| `[LABS]` | 只属于 Community Labs，尚未进入正式产品 |
| `[PROBE]` | 探针可以观察到行为，但不等于稳定契约 |
| `[FAIL-CLOSED]` | 未知或高风险能力默认拒绝或要求审批 |
| `[WORKSPACE-JAIL]` | 已纳入 workspace 边界和越界测试 |
| `[BLOCKED_BY_UPSTREAM]` | 上游 Runtime 或 SDK 尚未提供完整闭环 |
| `[UNVERIFIED]` | 尚未完成真实 E2E、跨平台或失败路径验证 |
| `[NOT_IMPLEMENTED]` | 当前没有实现，不应以未来计划描述成现状 |

除非有相应证据，不要使用“production-ready”“完全安全”“100% 兼容”等表述。
