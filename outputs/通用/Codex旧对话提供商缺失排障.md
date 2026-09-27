---
title: Codex旧对话提供商缺失排障
type: output
tags: [Codex/排障]
aliases: [2026-09-24-Codex旧对话提供商缺失排障]
created: 2026-09-24
updated: 2026-09-24
related: []
---

## 结论

四个旧对话保存了 `model_provider = deepseek`、`model = deepseek-flash`，但当前用户配置没有对应的提供商定义，打开时出现 `Model provider deepseek not found`。

## 已核实证据

- 2026-09-24 只读检查 `/Users/sjj/.codex/config.toml`：默认模型为 `gpt-6-astra`，未定义 DeepSeek 提供商。
- 只读查询本地 `state_5.sqlite`：恰好四条任务记录的提供商为 `deepseek`；对应会话文件首行元数据也保留了该值。
- 当前 wiki 没有相关技术页，本次依据用户截图、本地检查与官方配置文档作答。

## 解决路径

1. 要继续原来的 DeepSeek 对话：先备份配置，再从原有备份恢复 `[model_providers.deepseek]`，保留原来真实可用的服务地址、协议和认证配置；不必把全局默认模型改回 DeepSeek。保存后重新打开报错对话。
2. 要继续使用 ChatGPT：新建使用当前默认模型的对话可以避开旧记录中的提供商引用。需要保留上下文时，应迁移必要内容。
3. 要让原来的四个对话直接改用 ChatGPT：需要进一步确认应用支持的提供商迁移方式。仅改默认模型不能保证迁移成功；本次没有直接修改内部数据库或会话文件。

不要凭提供商名称猜测 API 地址。恢复定义后仍需验证认证、模型与协议是否兼容；消除配置错误不等于请求已能成功。

## 验证

重新打开四个对话，确认提供商缺失错误消失，再发送一条短消息验证完整链路。本次仅完成诊断，未执行配置修复或发送验证消息。

## 后续处理

用户选择今后使用 ChatGPT，并要求删除四个旧对话。2026-09-24 使用应用提供的归档接口处理四个任务，接口均返回成功，只读复核数据库确认四条记录均为 archived=1。实际完成的是归档，历史数据仍保留，并非永久删除。当前工具没有永久删除接口，电脑控制工具也禁止操作 Codex 自身。默认模型配置未变更。

## 相关

- [OpenAI 官方配置参考](https://learn.chatgpt.com/docs/config-file/config-reference) — `model_provider` 引用提供商 ID，`model_providers.<id>` 定义自定义提供商。
- [[index]] — 知识库索引；目前没有对应的概念或操作页。
