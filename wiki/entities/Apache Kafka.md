---
title: Apache Kafka
type: entity
tags: [系统框架/Kafka, 分布式系统]
aliases: [Kafka]
sources: []
created: 2026-09-28
updated: 2026-09-28
domain_volatility: high
confidence: medium
---

# Apache Kafka

Apache Kafka 是把事件按 Topic 分类、按 Partition 追加写入持久日志的分布式事件流平台，支持高吞吐发布订阅、历史回放和流处理。

## 核心要点

- Kafka 4.x 的集群元数据由 KRaft Controller Quorum 管理，不再支持 ZooKeeper 模式。
- Broker 存储 Partition 副本并处理客户端读写；Producer 写 Partition Leader，Follower 主动复制。
- Consumer Group 以 Committed Offset 维护独立进度，同一 Group 内一个 Partition 同时只分配给一个 Consumer。
- 顺序保证的边界是单个 Partition；Partition 同时也是吞吐、消费并行和副本放置的基本单位。
- Kafka 记录按 Retention/Compaction 清理，不会因某个 Consumer ACK 就立即删除，因此天然支持多组消费和回放。

当前知识库以 Kafka 4.3.1、Java 21 和 KRaft 为学习基线。版本事实以 [Apache Kafka 4.3 Documentation](https://kafka.apache.org/43/) 和 [Downloads](https://kafka.apache.org/community/downloads/) 为准。

## 与相邻概念的区别

- Kafka 偏向事件日志、回放和流处理；RabbitMQ 偏向灵活路由与任务分发，不能只按吞吐高低替换。
- Kafka Streams 是嵌入 Java 应用的处理库；Kafka Connect 是外部系统与 Kafka 之间的数据集成运行时。
- Schema Registry、Prometheus、Grafana、Strimzi 都是常见生态组件，但不属于 Kafka Broker 核心。

## 前提与适用范围

本页描述 Kafka 4.3.x。旧教程中的 `zookeeper.connect`、ZooKeeper 启动命令和旧版默认参数不能直接用于 Kafka 4.x 新集群。

## 相关

- [[Kafka核心架构]] — Broker、Topic、Partition 与 Consumer Group
- [[Kafka可靠性与交付语义]] — Replica、ACK、Offset 与幂等
- [[Kafka KRaft开发环境]] — 本地启动和命令验证
- [[Apache Kafka学习指南]] — 当前 12 章复习材料与两个实验
