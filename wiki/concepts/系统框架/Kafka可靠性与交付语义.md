---
title: Kafka 可靠性与交付语义
type: concept
tags: [系统框架/Kafka, 分布式系统]
aliases: [Kafka Delivery Semantics, Kafka可靠性]
sources: []
created: 2026-09-28
updated: 2026-09-28
domain_volatility: medium
confidence: medium
---

# Kafka 可靠性与交付语义

Kafka 的可靠性来自 Producer 确认、Partition 副本、ISR 阈值、Consumer 提交点和业务幂等的组合，不由任何单一参数保证。

## 核心要点

- 常见可靠基线是 RF=3、`min.insync.replicas=2`、Producer `acks=all` 与 `enable.idempotence=true`。
- ISR 是当前保持同步的副本集合；LEO 是某副本日志末端的下一 Offset；HW 是普通消费者可见的复制边界。
- At Most Once 通常先提交后处理，可能丢；At Least Once 先处理后提交，可能重复；Kafka EOS 用事务原子提交 Kafka 输出与输入 Offset。
- Producer 幂等防止单个 Producer 会话因重试在 Kafka 中重复追加，不等于数据库、HTTP、邮件等业务副作用幂等。
- 外部系统一致性通常使用 Transactional Outbox、Inbox、唯一事件 ID、数据库唯一约束或业务状态机。

## 与相邻概念的区别

- **`acks=all` 与全部副本**：它等待 ISR 满足配置条件，不是要求所有配置副本永久在线。
- **Producer retry 与业务 retry**：客户端只应自动重试可恢复协议错误；业务失败需要独立的 Retry/DLT 和补偿策略。
- **Offset 与 ACK**：Kafka Consumer 提交 Offset 表示恢复位置，不会删除 Topic 中的记录。
- **Exactly Once 与不重复执行**：Kafka 事务控制 Kafka 内可见性；外部副作用仍需幂等。

## 前提与适用范围

配置 RF/Min ISR 前必须结合 Broker 数、故障域和可用性目标。只有 1 个 Broker 的本地实验只能学习 API，不能验证副本故障与仲裁行为。

参考：[Kafka Design](https://kafka.apache.org/43/design/design/)、[Producer Configs](https://kafka.apache.org/43/configuration/producer-configs/) 与 [Consumer Configs](https://kafka.apache.org/43/configuration/consumer-configs/)。

## 相关

- [[Kafka核心架构]] — Partition、Replica 与 Consumer Group
- [[Kafka KRaft开发环境]] — 当前本地验证环境
- [[Apache Kafka学习指南]] — 可靠性章节与 Java 示例
