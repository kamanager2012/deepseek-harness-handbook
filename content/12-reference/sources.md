# 官方来源与阅读方法

## 优先级

使用 dsh 时，按以下优先级判断：

1. 当前版本的 --help；
2. 当前发布包或源码版本的官方 README；
3. 对应版本的官方用户指南；
4. 官方配置目录和源码说明；
5. 本手册的操作建议；
6. 社区文章、截图和二手教程。

二手资料可以帮助发现问题，但不能替代当前版本的命令和配置。

## 方法论对照

- [Harness Engineering 橙皮书](https://www.huasheng.ai/orange-books/harness/)：用于对照 Harness 的概念组织和案例化阅读方式，不作为 dsh 命令、字段、版本或运行结果的事实来源。

## 官方资料

- [官方仓库 README](https://github.com/deepseek-ai/deepseek-harness)
- [官方中文 README](https://github.com/deepseek-ai/deepseek-harness/blob/master/README.zh.md)
- [Web UI 中文指南](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/index.zh.md)
- [Provider 中文指南](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/providers.zh.md)
- [Python SDK 中文指南](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/user/guide/python-sdk.zh.md)
- [架构中文文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.zh.md)
- [Cordis 入门](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cordis-primer.zh.md)
- [CLI 中文参考](https://github.com/deepseek-ai/deepseek-harness/blob/master/apps/cli/reference/README.zh.md)
- [开发指南](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/development.zh.md)
- [工具 Schema 目录](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/tool-catalog.zh.md)
- [官方隐私说明](https://deepseek.com/harness/privacy/)
- [官方数据处理说明](https://deepseek.com/harness/data-processing/)

## 更新方法

每次上游版本变化，先检查：

- 根 README 的运行命令；
- user guide 的字段和界面名称；
- CLI profile 和 flag；
- Python SDK 包名、示例和结果字段；
- tool catalog 的工具名称与参数；
- architecture/Cordis 的扩展 seam；
- Node/Python 和平台要求。

然后在本手册中只更新受影响章节，并把版本注意写在命令附近。不要为了显得“验证充分”而添加没有实际来源的运行数字、截图或日志。
