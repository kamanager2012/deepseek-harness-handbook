# 发布检查清单

## Community 产品边界

发布 DeepSeek Harness Community 生态的文档或软件时，先检查产品入口没有漂移：

- [ ] 普通用户的下载、安装和 Release 链接只指向 [`dsh-community/releases/latest`](https://github.com/kamanager2012/dsh-community/releases/latest)；
- [ ] `deepseek-harness-suite` 明确标为 Community Labs，不作为第二发行渠道；
- [ ] `dsh-community-edition` 明确标为 Merge & Archive，不再作为并行产品；
- [ ] `dsh-community-plugins` 被描述为 Compatibility Registry，而不是 Plugin Manager；
- [ ] `dsh-marketplace` 被描述为 Discovery / Distribution UX，而不是 Runtime 或 Package Manager replacement；
- [ ] 官方 Runtime 的 Agent loop、工具执行和 Session persistence 没有被社区仓库的 README 重新认领；
- [ ] 任何 Labs 能力都标注 `[LABS]`、`[PARTIAL]` 或 `[UNVERIFIED]`，直到 Reality Gate 完成。

统一边界见[社区生态与产品入口](../00-overview/community-ecosystem.md)，实验能力的当前状态见 [Community Labs handoff](community-labs-handoff.md)。

## 手册发布前

### 内容

- [ ] 首页能让读者选路径；
- [ ] 安装命令与当前官方资料一致；
- [ ] Web、CLI、Provider、SDK 和插件章节分开；
- [ ] 所有事实有官方来源或版本说明；
- [ ] 所有建议没有冒充 dsh 原生字段；
- [ ] 没有虚构的运行记录、截图、数字或成功承诺；
- [ ] 任务模板包含范围、停止和验收；
- [ ] 故障章节能按层定位；
- [ ] 术语和命令一致。

### 安全

- [ ] 没有真实 key、token、Cookie 或 Authorization；
- [ ] 没有个人绝对路径；
- [ ] 示例 endpoint、模型和变量都是 placeholder；
- [ ] session、日志、图片和私有代码的处理写清；
- [ ] 高权限示例带隔离说明；
- [ ] 远程 Web 使用带网络和认证警告。

### 链接和构建

- [ ] Markdown 相对链接通过；
- [ ] 官方外链可访问；
- [ ] 代码块语言标记正确；
- [ ] 表格渲染正常；
- [ ] 目录和文件名大小写一致；
- [ ] PDF/网页生成没有截断代码块；
- [ ] 发布包不含维护者私有附录。

## 版本发布前

记录：

~~~text
手册版本：
发布日期：
对应 dsh 版本：
Node/Python：
官方 README：
用户指南：
CLI 参考：
工具目录：
已知不兼容：
下一次复核：
~~~

## 发现错误后

不要悄悄改一处就结束。更新：

- 受影响章节；
- 版本说明；
- 命令速查；
- 任务模板；
- 来源链接；
- 变更记录；
- 必要时的迁移说明。
