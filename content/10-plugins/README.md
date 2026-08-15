# 插件、Profile 与 Cordis

官方项目采用“一切皆插件”的架构。普通使用者不需要一开始就写插件，但理解插件模型能解释为什么 profile、bundle、patch、工具和权限会影响行为。

## 本章路径

- [插件模型](plugin-model.md)
- [Cordis 入门](cordis-primer.md)
- [Profile、Bundle 与 Patch](profiles-bundles-patches.md)
- [添加工具和 Provider](adding-capabilities.md)
- [插件调试与发布](debugging-and-release.md)

## 什么时候需要插件

适合做插件的需求：

- 新的模型 Provider 或协议适配；
- 新的工具和执行后端；
- 文件、Shell、沙箱或审批策略；
- session 存储或事件策略；
- Web UI 节点；
- 组织级默认组合。

不适合做插件的需求：

- 一次任务的目标；
- 一段只在一个项目使用的说明；
- 一条本可由脚本完成的固定命令；
- 为了绕过审批而隐藏动作。

## 插件开发的风险

插件可以增加工具、读取 context、监听事件、启动进程或改变配置。开发时优先使用隔离 profile 和临时 workspace，不要在日常生产 DSH_HOME 里测试未审查插件。
