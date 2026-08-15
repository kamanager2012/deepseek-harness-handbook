# DeepSeek Harness 中文使用手册

> 工程实施、验收与运维手册

这不是 dsh API 的镜像，也不是把模型回复堆成长文的教程。它面向需要把 DeepSeek Harness 放进真实工程流程的人：从安装、Provider 和 workspace，到任务边界、权限控制、Session 恢复、外部验收和团队运维。

## 从这里开始

- [连续阅读书稿目录](BOOK.md)
- [五层模型：先理解 Harness 如何工作](content/00-overview/harness-five-layers.md)
- [主线实战：从空白 workspace 到可验收交付](content/05-workflows/from-blank-to-delivery.md)
- [按任务查找章节](content/tasks/index.md)

## 选择阅读路线

| 你的目标 | 推荐路线 |
| --- | --- |
| 第一次使用 dsh | [安装](content/01-installation/README.md) → [Web UI 首次任务](content/02-web-ui/first-run.md) → [主线实战](content/05-workflows/from-blank-to-delivery.md) |
| 让 Agent 修改代码 | [任务契约](content/core/task-contract.md) → [代码修改](content/05-workflows/code-change.md) → [结果验收](content/02-web-ui/result-review.md) |
| 接入 DeepSeek 或公司网关 | [Provider 与模型](content/04-providers/README.md) → [自定义端点](content/04-providers/custom-endpoints.md) → [Provider 排错](content/04-providers/troubleshooting.md) |
| 接入 CLI、CI 或 Python | [CLI](content/03-cli/README.md) → [自动化](content/08-automation/README.md) → [SDK 工程实践](content/08-automation/sdk-engineering.md) |
| 做安全评审或团队落地 | [安全](content/06-security/README.md) → [Session](content/07-sessions/README.md) → [团队规范](content/11-operations/team.md) |
| 开发插件和扩展 | [插件模型](content/10-plugins/plugin-model.md) → [Cordis 入门](content/10-plugins/cordis-primer.md) → [调试与发布](content/10-plugins/debugging-and-release.md) |

## 阅读原则

- 先读再写，先建立基线再扩大权限；
- Agent 的最终回答不是验收结果，检查真实 diff、测试、退出码和数据流；
- 命令、字段和模型能力以当前版本的 `--help`、上游资料和实际结果为准；
- 示例是任务契约和验收模板，不是虚构的运行记录；
- `evidence/` 和 `labs/` 是维护者附录，普通读者不需要从那里开始。

本网站由仓库中的 Markdown 源稿自动构建；需要查看版本、修改历史或编辑正文时，回到 [GitHub 仓库](https://github.com/kamanager2012/deepseek-harness-handbook)。
