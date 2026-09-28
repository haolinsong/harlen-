---
title: Kafka 核心架构
type: concept
tags: [系统框架/Kafka, 分布式系统]
aliases: [Kafka Architecture, Kafka架构]
sources: []
created: 2026-09-28
updated: 2026-09-28
domain_volatility: medium
confidence: medium
---

# Kafka 核心架构

Kafka 以 Partition 为核心，把一个 Topic 拆成多条独立的有序日志，再用副本、Consumer Group 和 KRaft 元数据仲裁实现扩展与故障恢复。

## 核心要点

```text
Producer -> Topic -> Partition Leader -> Follower Replicas
                           |
                           v
                 Consumer Group Members

KRaft Controllers -> metadata / leader election / cluster coordination
```

- Topic 是逻辑分类，Partition 是存储、顺序、消费并行和副本管理单位。
- 相同 key 经分区器通常进入同一 Partition，从而获得实体级顺序。
- Consumer Group 内一个 Partition 同时只给一个成员；消费者多于 Partition 时会有成员空闲。
- 不同 Group 拥有独立 Committed Offset，因此可以各自读取同一份事件。
- Broker 承载数据面，KRaft Controller 管理元数据与 Leader 选举；生产通常分离角色。

## 与相邻概念的区别

- **Topic 与 Partition**：Topic 是名称和配置边界，Partition 才是实际日志分片。
- **Record Offset 与 Committed Offset**：前者标识记录位置，后者表示某 Group 下次恢复位置。
- **Leader 与 Controller**：Leader 属于某个 Partition 并服务读写；Controller 管理整个集群元数据。
- **Replica 与 Consumer 副本**：Replica 是日志数据副本，Consumer Group 是业务读取视角，二者无从属关系。

## 前提与适用范围

Kafka 只保证单 Partition 内顺序。增加 Partition 会改变 key 的哈希映射，并增加元数据、文件和恢复成本，不能只把 Partition 数当作越大越好的并发开关。

参考：[Kafka Design](https://kafka.apache.org/43/design/design/) 与 [KRaft](https://kafka.apache.org/43/operations/kraft/)。

## 相关

- [[Apache Kafka]] — 平台与版本入口
- [[Kafka可靠性与交付语义]] — 复制与消费进度
- [[Kafka KRaft开发环境]] — 用命令观察这些概念
- [[Apache Kafka学习指南]] — 完整讲解与图示
