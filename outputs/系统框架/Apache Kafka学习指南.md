---
title: Apache Kafka 学习指南
type: output
tags: [系统框架/Kafka, 分布式系统]
aliases: [Kafka Learning Guide, Kafka学习路线]
created: 2026-09-28
updated: 2026-09-28
related: ["[[Apache Kafka]]", "[[Kafka核心架构]]", "[[Kafka可靠性与交付语义]]", "[[Kafka KRaft开发环境]]"]
---

# Apache Kafka 学习指南

这是 Kafka 系统学习手册的第一阶段，当前聚焦零基础、Java 开发接入和可靠性原理。阅读时不要只背参数：先理解 Partition 这条主线，再用配套实验观察写入、消费、复制和 Lag。生产运维主题已记入第 12 章，本阶段不提前展开。

> [!info] 版本基线（核验于 2026-09-28）
> - Broker 与命令以 [Apache Kafka 4.3.1](https://kafka.apache.org/blog/2026/06/25/apache-kafka-4.3.1-release-announcement/) 为准；官方当前维护版本见 [Downloads](https://kafka.apache.org/community/downloads/)。
> - Kafka 4.x 只支持 KRaft，ZooKeeper 仅作为旧集群迁移背景，不再用于新部署。
> - Broker/Connect 使用 Java 17、21 或 25；本文示例选择 Java 21。准确支持矩阵见 [Java Version](https://kafka.apache.org/43/operations/java-version/)。
> - Java Client 使用 `kafka-clients 4.3.1`；Python 使用 `confluent-kafka 2.15.1`。
> - Kafka 4.3 的新 Consumer Rebalance Protocol 已可用，但仍需客户端显式设置 `group.protocol=consumer`；`classic` 仍是默认值。

## 学习地图

```text
基础概念
   |
   v
Topic -> Partition -> Log Segment -> Offset
   |          |                         |
   |          +-> Leader/Replica/ISR -> HW/LEO
   |
   +-> Producer: key/partition/batch/acks/idempotence
   |
   +-> Consumer Group: assignment/rebalance/commit/lag
                         |
                         v
          Connect / Streams / Schema / Security
                         |
                         v
        Monitoring / Troubleshooting / Tuning / K8s
                         |
                         v
              Production Architecture & DR
```

推荐顺序：第 1～6 章与实验 1，接着第 7～10 章与实验 2。第 11 章汇总当前实战，第 12 章只记录后续学习范围，等本阶段学完后再展开。

---

## 1 Kafka 简介

### 1.1 Kafka 是什么

Apache Kafka 是分布式事件流平台。它把事件按 Topic 分类、按 Partition 追加写入持久日志，并允许多个独立 Consumer Group 以自己的进度重复读取。

Kafka 主要解决四类问题：

- **解耦**：生产者不必知道消费者地址和处理速度。
- **削峰**：短时间流量先写入 Kafka，消费者按能力处理。
- **回放**：在保留期内重置 Offset，重新计算历史数据。
- **事件流**：持续处理日志、指标、订单、CDC 变更和业务事件。

### 1.2 消息队列与事件日志

| 维度 | 传统消息队列常见模型 | Kafka |
| --- | --- | --- |
| 消费后数据 | 常在 ACK 后从可消费集合删除 | 按保留策略删除，与某个消费者是否读过无关 |
| 消费进度 | Broker 维护消息状态 | Consumer Group 提交每个 Partition 的 Offset |
| 顺序 | Queue 级或分片级 | 只保证单个 Partition 内有序 |
| 扩展单位 | Queue/Consumer | Partition/Consumer |
| 回放 | 通常不是核心能力 | 原生支持调整 Offset 后回放 |
| 典型定位 | 任务分发、复杂路由 | 事件流、日志、数据管道、高吞吐消息 |

Kafka 不会自动取代 RabbitMQ。需要复杂路由、逐消息 TTL、优先级或命令任务时，RabbitMQ 往往更自然；需要大吞吐、长期保留、回放和流处理时，Kafka 更合适。

### 1.3 常见场景

- 微服务领域事件与异步集成。
- 应用日志、审计日志和指标汇聚。
- 数据库 CDC，经 Debezium/Connect 进入数据湖或搜索系统。
- 实时风控、监控告警、推荐特征计算。
- Event Sourcing 的事件存储之一，但业务仍需设计快照、版本与一致性。

> [!warning] 常见误区
> Kafka 的高吞吐不等于所有消息都低延迟，也不等于自动拥有端到端 Exactly Once。吞吐、延迟、可靠性和成本始终需要按业务目标权衡。

---

## 2 Kafka 架构

### 2.1 整体架构

```text
                          KRaft Metadata Quorum
                    +------------+------------+
                    | Controller | Controller |   3 或 5 个投票节点
                    +------+-----+-----+------+
                           | metadata
            +--------------+------------------+
            |                                 |
      +-----v------+                    +-----v------+
      | Broker 1   |                    | Broker 2   |
      | T-P0 L     |<---- replication-->| T-P0 F     |
      | T-P1 F     |<---- replication-->| T-P1 L     |
      +-----+------+                    +-----+------+
            ^                                 ^
            | produce / fetch                 |
        +---+--------+                   +----+-------+
        | Producers  |                   | Consumers  |
        +------------+                   +------------+
```

Kafka 整体可分为控制面、数据面和客户端：

- **KRaft Controller Quorum（控制面）**：保存集群元数据，负责 Broker 注册、Partition Leader 选举和故障切换，不承担普通消息读写。
- **Broker（数据面）**：存放 Partition 的日志副本，处理 Producer 写入、Consumer 读取和 Broker 间复制。
- **Topic 与 Partition（数据组织）**：Topic 是逻辑分类，Partition 是实际存储和并行读写的有序日志。
- **Leader 与 Follower（高可用）**：一个 Partition 的 Leader 接收读写，Follower 从 Leader 复制数据，Leader 故障时同步副本可参与接管。
- **Producer 与 Consumer（客户端）**：Producer 把消息发到目标 Partition 的 Leader；Consumer 从分配给它的 Partition 拉取数据并维护消费进度。

一条消息的主要流转关系是：

```text
Producer
   | 1. 获取 Metadata，选择 Topic 和 Partition
   v
Partition Leader（所在 Broker）
   |-- 2. 复制 --> Follower Replicas（其他 Broker）
   |
   `-- 3. 拉取 --> Consumer（由 Consumer Group 分配 Partition）
                         `-> 处理消息 -> 提交 Offset
```

开发环境可以让一个进程同时承担 `broker,controller`；关键生产环境通常将 Controller 和 Broker 角色拆分。

### 2.2 十个核心名词

十个名词不是孤立的，可以先用下面的层级理解：

```text
Kafka Cluster
├── Broker 1
│   ├── Topic A / Partition 0 / Leader Replica
│   └── Topic A / Partition 1 / Follower Replica
└── Broker 2
    ├── Topic A / Partition 0 / Follower Replica
    └── Topic A / Partition 1 / Leader Replica

Producer -> Topic A -> 选择 Partition -> 写入该 Partition 的 Leader

Consumer Group
├── Consumer 1 -> 读取 Partition 0 -> 提交 Offset
└── Consumer 2 -> 读取 Partition 1 -> 提交 Offset
```

#### Partition Leader 与 Leader Replica

**Partition Leader 和 Leader Replica 是同一个实际副本的两种表述角度。**

- **Partition Leader**：从 Partition 角度说，指这个 Partition 当前由哪个副本负责读写。
- **Leader Replica**：从 Replica 角度说，指这个副本当前承担 Leader 角色。
- **Replica Leader** 不是推荐的常用说法；建议使用 Partition Leader 或 Leader Replica。

```text
orders-P0（一个 Partition）
├── Broker 1: P0 Replica（Leader）   <- Partition Leader
├── Broker 2: P0 Replica（Follower）
└── Broker 3: P0 Replica（Follower）
```

Producer 和 Consumer 默认与 Leader Replica 读写。如果 Broker 1 故障，符合条件的同步 Follower 可被选为新 Leader。`orders-P0` 仍是原来的 Partition，只是承担 Leader 角色的 Replica 变了。

> [!info] 层级关系
> 不是“一个 Replica 里包含 Leader 和 Follower”，而是“一个 Partition 有多个 Replica，其中一个是 Leader Replica，其余是 Follower Replica”。

它们之间的关系可概括为：

1. **Cluster 与 Broker**：一个 Kafka 集群通常有多个 Broker。一个 Broker 会保存多个 Topic 的若干 Partition 副本，但不一定保存任何一个 Topic 的全部数据。
2. **Topic 与 Partition**：一个 Topic 由一个或多个 Partition 组成；每条消息只属于其中一个 Partition。
3. **Partition 与 Replica**：一个 Partition 可有多个 Replica，这些副本应分布在不同 Broker 上。
4. **Replica、Leader 与 Follower**：每个 Partition 的多个 Replica 中，同一时刻只有一个 Leader，其余是 Follower。Leader 处理读写，Follower 负责复制和容灾。
5. **Producer 与存储结构**：Producer 指定 Topic，再由分区策略决定 Partition，最终将消息发给该 Partition Leader 所在的 Broker。
6. **Consumer 与 Consumer Group**：一个 Group 可包含多个 Consumer。同一 Group 内，一个 Partition 同时最多分配给一个 Consumer；不同 Group 作为独立的整体，可按各自的进度消费同一 Topic。
7. **Offset 与消费进度**：每条消息的 Offset 只在所在 Partition 内有意义；消费进度归属于 `Consumer Group + Topic + Partition`，因此不同 Group 互不影响。

#### 用一个例子理解 Consumer、Group 和 Partition

假设 `orders` Topic 有 4 个 Partition：`P0、P1、P2、P3`。

**1. Consumer 数量大于 Partition 数量时，为什么有 Consumer 空闲？**

```text
inventory-group
C1 <- P0    C2 <- P1    C3 <- P2    C4 <- P3
C5 <- 无     C6 <- 无
```

同一 Group 内，一个 Partition 不能在同一时刻再拆给多个 Consumer。这里只有 4 个 Partition，因此最多只有 4 个 Consumer 并行工作；`C5` 和 `C6` 没有分到 Partition，`poll()` 不会拉到业务消息，这就是“空闲”。它们仍是 Group 成员；如果工作中的 Consumer 退出，重新分配后空闲成员可能接管 Partition。

> 结论：对单个 Topic 而言，**同一 Consumer Group 的最大有效并行度通常不超过 Partition 数量**。一个 Consumer 可负责多个 Partition。

**2. “消费进度归属于 `Consumer Group + Topic + Partition`”是什么意思？**

Kafka 不是只为整个 Topic 保存一个进度数字，而是为每个 Group 的每个 Partition 分别保存 Committed Offset：

```text
(inventory-group, orders, P0) -> 101
(inventory-group, orders, P1) -> 56

(notification-group, orders, P0) -> 89
(notification-group, orders, P1) -> 40
```

这表示库存组和通知组即使消费同一 Topic，也可处在完全不同的位置。库存组重启后，会从自己在 `P0` 提交的 101 继续，不会受通知组的 89 影响。Committed Offset 通常表示“下一条要读的位置”。

**3. “同一 Group 内分工，不同 Group 独立消费”是什么意思？**

```text
orders:  P0  P1  P2  P3

inventory-group:     C1 <- P0,P1    C2 <- P2,P3
notification-group:  C3 <- P0,P1    C4 <- P2,P3
```

- **Group 内是负载均衡**：`C1` 和 `C2` 共同完成库存组的工作，每个 Consumer 只读自己被分配的 Partition，不是每人都读全部消息。
- **Group 之间是独立订阅**：库存组和通知组都可以各自处理 `orders` 的整条数据流，互不抢消息，也互不共享进度。

> [!warning] “读取全部消息”的边界
> 这是指 Group 作为整体，从自己的起始 Offset 开始读取各个 Partition；不代表 Group 中的每个 Consumer 都收到一份，也不代表已被 Retention 删除的历史消息仍可读取。

> [!warning] 准确说法
> 可以用“Broker 中有多个 Topic 的数据”帮助入门理解，但物理存储单位其实是 **Partition Replica**。一个 Topic 往往横跨多个 Broker，一个 Broker 也往往同时保存多个 Topic 的部分 Partition 副本。

| 名词 | 定义 | 作用与机制 | 示例 | 常见误区 |
| --- | --- | --- | --- | --- |
| **Broker** | 一个 Kafka 服务节点 | 保存 Partition 副本、响应 Produce/Fetch 请求 | `broker.id/node.id=1` 的服务器 | Broker 不是一条 Queue；一个 Broker 通常承载许多 Topic 的部分 Partition |
| **Topic** | 事件的逻辑分类名 | Producer 写 Topic，Consumer 订阅 Topic；物理上由多个 Partition 组成 | `orders.created` | Topic 本身不提供全局顺序 |
| **Partition** | Topic 的有序、只追加日志分片 | 扩展吞吐、并行度和存储；每条记录只属于一个 Partition | `orders.created-2` | Partition 越多不一定越好，会增加元数据、文件和恢复成本 |
| **Replica** | Partition 的副本 | 分布到不同 Broker，提高故障容忍；副本数 3 可容忍最多 2 个副本丢失，但能否继续写还受 `min.insync.replicas` 影响 | P0 在 Broker 1/2/3 各有副本 | Replica 不是三份独立可并发写的数据；写入走 Leader |
| **Leader** | 某 Partition 当前处理客户端读写的副本 | 接收写入，Follower 从它复制；故障时从合格副本中选新 Leader | Broker 1 是 P0 Leader | Topic 没有一个总 Leader，每个 Partition 各有 Leader |
| **Follower** | 跟随 Leader 复制日志的副本 | 定期 Fetch，保持与 Leader 同步，满足条件时属于 ISR | Broker 2 的 P0 副本 | Follower 默认不分担读请求，它主要用于容灾 |
| **Producer** | 发布事件的客户端 | 获取 Metadata，序列化、分区、批量、压缩，再发给目标 Leader | 订单服务发送 `OrderCreated` | `send()` 成功入本地缓冲不等于 Broker 已确认，必须观察回调/Future |
| **Consumer** | 从 Broker 拉取事件的客户端 | 对被分配的 Partition 调用 Fetch，并管理处理与提交进度 | 库存服务消费订单事件 | Consumer 数大于 Partition 数时，多出的成员会空闲 |
| **Consumer Group** | 共享 `group.id` 的消费者集合 | 同组内每个 Partition 同时只分给一个成员；不同组可按各自 Offset 独立消费 | 库存组与通知组各自处理订单流 | Group 不是 Topic；它是消费视角和进度命名空间 |
| **Offset** | Partition 中记录的递增位置 | Broker Offset 标识记录；Committed Offset 表示该 Group 下次从哪里读 | 提交 18 意味着下次通常从 18 开始 | Offset 只在某个 Partition 内有意义，不是全局消息 ID |

### 2.3 KRaft 中的角色

#### KRaft 是什么

**KRaft（Kafka Raft Metadata mode）** 是 Kafka 内置的集群元数据管理和共识机制。它使 Controller 组成 Raft Quorum，用一条可复制的 Metadata Log 记录集群状态，从而取代 Kafka 早期依赖的 ZooKeeper。Kafka 4.x 只使用 KRaft。

KRaft 管理的是“Kafka 集群如何组织”，例如：

- 集群中有哪些 Broker，它们是否存活。
- 有哪些 Topic，每个 Topic 有多少 Partition。
- 每个 Partition 的 Replica 分布在哪些 Broker。
- 哪个 Replica 是 Partition Leader，ISR 有哪些成员。
- Topic 配置、ACL、配额和集群功能版本等元数据。

KRaft **不存放普通业务消息**，也不是 Producer 和 Consumer 之间的消息中转站。业务消息仍保存在 Broker 的 Topic Partition 日志中。

#### KRaft 如何工作

```text
                    Controller Quorum
              +---------------------------+
Admin Request | Active Controller          |
------------->| Metadata Log Leader        |
              +-------------+-------------+
                            | Raft 复制，多数派确认后提交
                 +----------+----------+
                 v                     v
          Standby Controller    Standby Controller
                 |
                 | 同步已提交的元数据
                 v
          Broker 1 / Broker 2 / Broker 3
                 ^
                 | 业务消息读写
          Producer / Consumer
```

1. Controller Quorum 中有一个 **Active Controller**，其他 Controller 是备用成员。
2. Topic 创建、Partition 变更或 Broker 故障等操作，最终由 Active Controller 生成元数据记录并追加到 Metadata Log。
3. 记录复制到 Controller 多数派后才提交；这保证故障后新 Controller 仍能看到已提交的集群状态。
4. Broker 从 Controller 获取元数据变更，再按新状态创建 Replica、切换 Partition Leader 或更新配置。
5. Active Controller 故障时，剩余 Controller 通过 Raft 选出新 Leader，继续处理元数据。

#### 如何理解 KRaft 的角色

可以把 KRaft 理解为 Kafka 集群的“**可容错控制系统 + 元数据账本**”：

- **Controller 管规则和调度**：记录 Topic/Partition 结构，决定 Partition Leader，处理 Broker 上下线。
- **Broker 管数据和读写**：保存真实消息，处理 Producer/Consumer 请求并复制 Partition。
- **Raft 管 Controller 之间的一致性**：保证大家按同一顺序应用元数据变更，一台 Controller 故障不会丢失已提交状态。

#### 节点可以承担哪些角色

- `process.roles=broker`：Broker-only，保存业务数据并服务客户端。
- `process.roles=controller`：Controller-only，参加 Metadata Quorum，不承担普通消息读写。
- `process.roles=broker,controller`：Combined Mode，同一进程兼任两种角色，适合本地学习，不建议关键生产环境。
- `node.id`：节点在整个集群中的唯一编号。
- `controller.listener.names`：Controller 用于仲裁和 Broker 通信的 Listener 名称。

生产通常部署 3 或 5 个 Controller，并保持多数派存活：3 个可容忍 1 个失效，5 个可容忍 2 个失效。新版本支持 Dynamic Quorum；生产新集群应根据 [KRaft 官方文档](https://kafka.apache.org/43/operations/kraft/) 配置 `controller.quorum.bootstrap.servers`。本地单节点实验仍可按官方示例使用静态单节点 Quorum。

---

## 3 Kafka 核心概念

### 3.1 消息 Key 如何决定 Partition

#### Key 是什么

一条 Kafka Record 不只有消息内容（Value），还可以携带 Key：

```text
ProducerRecord
├── Topic:     orders
├── Partition: null（可选，交给分区器决定）
├── Key:       order-42
├── Value:     {"status":"CREATED"}
├── Headers:   ...
└── Timestamp: ...
```

**Key 是 Producer 发送消息时主动指定的可选字段**。它通常选用能代表同一业务实体的值，例如 `orderId`、`userId` 或 `deviceId`。Kafka 不会自动生成 Key，也不理解 `order-42` 的业务含义；它只把序列化后的 Key 字节用于分区等操作。

在 Java Client 中，类型签名是 `ProducerRecord<K, V>`：

- `K` 是 **Key 的 Java 类型**。
- `V` 是 **Value 的 Java 类型**。

```java
ProducerRecord<String, String> record = new ProducerRecord<>(
        "orders",                    // Topic
        "order-42",                  // Key：K 的实际类型是 String
        "{\"status\":\"CREATED\"}"    // Value：V 的实际类型是 String
);
```

`key.serializer` 会把 `K` 转成字节；例如 `StringSerializer` 把 `"order-42"` 转为字节数组，再交给 Partitioner。

#### Key 有什么作用

1. **选择 Partition**：默认情况下，Partitioner 对 Key 计算哈希，再映射到某个 Partition。
2. **保持实体内顺序**：当 Partition 数量不变时，相同 Key 通常进入同一 Partition，因此同一订单的事件可以按写入顺序读取。
3. **支持 Log Compaction**：启用 Compaction 后，Kafka 可按 Key 保留最新值。

Key 不是 Kafka 的全局主键，也不要求唯一；多条消息正可以使用同一 Key。

#### Producer 如何选择 Partition

Producer 决定 Partition 的常见顺序：

1. `ProducerRecord` 显式指定 Partition，就直接使用。
2. 存在 key 时，默认分区器对 key 哈希，使相同 key 通常落入同一 Partition。
3. 没有 key 时，默认采用粘性批处理策略，在一段时间内把记录聚到同一 Partition 以形成更大的 Batch。

```text
key=order-42 ----hash----> Partition 2 ----append----> offset 105
key=order-42 ----hash----> Partition 2 ----append----> offset 106
```

因此“按订单有序”的实现通常是用 `orderId` 做 Key，而不是追求整个 Topic 全局有序。增加 Partition 数可能改变 Key 到 Partition 的映射，不能假设历史消息与新消息继续落在同一 Partition。不同 Key 也可能因哈希映射而进入同一 Partition。

### 3.2 Partition 数如何决定并行度

一个 Consumer Group 中，一个 Partition 同时最多由一个 Consumer 读取：

```text
Topic: P0 P1 P2 P3

Group A: C1 <- P0,P1    C2 <- P2,P3
Group B: C3 <- P0,P1,P2,P3
```

- Group A 内有两个消费者，所以并行处理两组 Partition。
- Group B 是另一个业务视角；它作为整体按自己的 Offset 消费四个 Partition，进度与 Group A 无关。
- 若 Group A 扩到 6 个消费者，仍只有 4 个工作，另外 2 个空闲。

Partition 数至少要覆盖目标消费并行度，但还应考虑单 Partition 吞吐、Leader 分布、文件句柄、Controller 元数据和未来扩容。

### 3.3 Offset 的三个值

- **Record Offset**：记录在 Partition 中的位置。
- **Current Position**：Consumer 下一次 `poll()` 将读取的位置，只存在客户端内存中。
- **Committed Offset**：Group 持久化的恢复位置，保存在内部 Topic `__consumer_offsets`。

处理消息后提交的是“下一条要读的位置”。处理完 Offset 17，应提交 18。

### 3.4 Retention 与 Compaction

- `cleanup.policy=delete`：达到时间或大小阈值后按 Segment 删除，适合事件历史。
- `cleanup.policy=compact`：为每个 key 最终保留最新值，旧值会异步清理，适合状态变更日志。
- `compact,delete`：同时做压缩和时间/大小删除。
- key 为 `null` 的记录无法按 key 压缩；`key -> null` 是 Tombstone，用于声明删除该 key。

> [!warning] 常见误区
> Compaction 不保证磁盘上立即只剩最新值，也不保证消费者只看到最新值。它是后台清理策略，消费者仍可能在清理前读到多个版本。

---

## 4 Kafka 安装部署

### 4.1 本地二进制安装

先安装 Java 21，再从 [Apache 下载页](https://kafka.apache.org/community/downloads/) 下载 Kafka 4.3.1 并校验 SHA-512/PGP。解压后：

```bash
cd kafka_2.13-4.3.1

# 生成 Cluster ID，并以单节点开发模式格式化日志目录。
KAFKA_CLUSTER_ID="$(bin/kafka-storage.sh random-uuid)"
bin/kafka-storage.sh format --standalone \
  -t "$KAFKA_CLUSTER_ID" \
  -c config/server.properties

bin/kafka-server-start.sh config/server.properties
```

`format` 只对新的空数据目录执行一次。不要为了“修复启动失败”反复格式化生产数据目录。

核心配置：

| 配置 | 作用 | 开发值 | 生产关注点 |
| --- | --- | --- | --- |
| `process.roles` | 节点角色 | `broker,controller` | 分离 Broker 和 Controller |
| `node.id` | 节点唯一 ID | `1` | 全集群不重复 |
| `listeners` | 本机监听地址 | `PLAINTEXT://:9092` | 数据面、控制面与内外网分 Listener |
| `advertised.listeners` | 返回给客户端的可达地址 | `localhost:9092` | 必须是客户端网络真正可达的 DNS/IP |
| `log.dirs` | Partition 日志目录 | 临时目录 | 多盘容量、性能、故障域与监控 |
| `controller.quorum.*` | Controller 仲裁发现 | 单节点开发值 | 3/5 Controller，使用 Dynamic Quorum |

### 4.2 Docker Compose

配套项目已固定官方镜像与 KRaft 参数：

```bash
cd code/kafka-learning-labs
docker compose up -d
docker compose ps
./scripts/create-topics.sh
```

不要把单节点 Compose 原样用于生产：它的副本因子和 `min.insync.replicas` 都是 1，没有 TLS、SASL、ACL、配额、监控或跨节点容灾。

### 4.3 基础命令

```bash
# 创建 Topic
bin/kafka-topics.sh --bootstrap-server localhost:9092 \
  --create --topic demo.orders --partitions 3 --replication-factor 1

# 查看 Topic 与副本状态
bin/kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --topic demo.orders

# 控制台生产
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic demo.orders --property parse.key=true --property key.separator=:

# 输入：order-1:{"status":"CREATED"}

# 控制台消费，指定 Group 并从无提交记录时的最早位置开始
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic demo.orders --group demo-group --from-beginning \
  --property print.key=true --property print.offset=true

# 查看 Group、Offset 与 Lag
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --describe --group demo-group

# 查看 KRaft 仲裁
bin/kafka-metadata-quorum.sh --bootstrap-server localhost:9092 \
  describe --status
```

### 4.4 常见启动错误

| 现象 | 优先检查 | 解决方向 |
| --- | --- | --- |
| 客户端能连 Bootstrap，却随后超时 | `advertised.listeners` | 改成客户端所在网络可解析、可访问的地址 |
| `InconsistentClusterIdException` | 数据目录中的 Cluster ID 与配置 | 找出误用的数据卷；不要直接删除生产元数据 |
| 单节点内部 Topic 无法创建 | 默认副本因子大于 Broker 数 | 仅开发环境把 offsets/transaction 副本参数设为 1 |
| `NotEnoughReplicas` | ISR 数量和 `min.insync.replicas` | 修复慢/离线副本，而不是先降低安全阈值 |
| Controller 无法形成 Quorum | `node.id`、Listener、Quorum 配置 | 检查唯一 ID、DNS、端口和多数节点存活 |

完整命令来源：[Quickstart](https://kafka.apache.org/43/getting-started/quickstart/)、[Basic Operations](https://kafka.apache.org/43/operations/basic-kafka-operations/)、[Docker](https://kafka.apache.org/43/getting-started/docker/)。

---

## 5 Kafka Producer

### 5.1 工作流程

```text
ProducerRecord
  -> Serializer
  -> Partitioner + Metadata Cache
  -> RecordAccumulator（按 Topic-Partition 聚合 Batch）
  -> Sender Thread（压缩并发送）
  -> Partition Leader
  -> ACK / retry / callback
```

`send()` 通常先进入本地 Buffer，返回 Future，并非每条记录都同步发网络。Batch 满足 `batch.size` 或等待到 `linger.ms` 后发送；压缩也以 Batch 为单位，因此适度等待可能同时提高吞吐和压缩率。

### 5.2 关键参数

| 参数 | 机制 | 调整影响 | 生产建议 |
| --- | --- | --- | --- |
| `key.serializer` / `value.serializer` | 对象转字节 | 决定协议与兼容性 | 不要用语言私有序列化跨服务；采用 Schema 管理 |
| `batch.size` | 单 Partition Batch 上限 | 大可提高吞吐但占内存 | 从 32～128 KiB 压测，不盲猜 |
| `linger.ms` | 等待形成 Batch 的最长时间 | 大可提高吞吐、增加排队延迟 | Kafka 4.x 默认 5 ms；按延迟 SLO 调整 |
| `buffer.memory` | Producer 总缓冲估算值 | 太小会阻塞 `send()` | 结合峰值吞吐与 Broker 抖动配置 |
| `compression.type` | `none/gzip/snappy/lz4/zstd` | 节省网络/磁盘，消耗 CPU | 通常优先 LZ4 或 Zstd，必须压测 |
| `delivery.timeout.ms` | 一条记录从发送到最终成功/失败的总上限 | 限制重试总时长 | 应不小于 `request.timeout.ms + linger.ms` |
| `retries` | 可重试错误的次数 | 增强恢复能力 | Kafka 4.3 默认很大，通常用 `delivery.timeout.ms` 控总时长 |
| `max.in.flight.requests.per.connection` | 单连接未确认请求数 | 大提高吞吐；与顺序相关 | 幂等开启时不超过 5 |
| `enable.idempotence` | Producer ID + Sequence 去重 | 防止单 Producer 会话重试重复 | 通常开启；不是业务端到端幂等 |

以 [Kafka 4.3 Producer Configs](https://kafka.apache.org/43/configuration/producer-configs/) 为准，不要照搬旧文章：Kafka 4.0 起 `linger.ms` 默认值已由 0 改为 5。

### 5.3 `acks` 的取舍

| 配置 | 何时认为成功 | 性能/延迟 | 可靠性 |
| --- | --- | --- | --- |
| `acks=0` | 不等待 Broker | 吞吐最高、延迟最低 | 客户端不知道是否写入，可能静默丢失 |
| `acks=1` | Leader 写入本地日志 | 中等 | ACK 后 Leader 立刻故障且 Follower 未复制时可能丢失 |
| `acks=all` | Leader 等待当前 ISR 满足写入条件 | 延迟较高、吞吐可能下降 | 配合 RF=3、`min.insync.replicas=2` 提供常用高可靠基线 |

`acks=all` 不是“所有配置副本永远都确认”，而是等待符合 ISR 与 Topic/Broker 配置要求的副本。若 ISR 小于 `min.insync.replicas`，写入会失败，这是用可用性换数据安全的设计。

### 5.4 可靠 Producer 基线

```properties
acks=all
enable.idempotence=true
compression.type=lz4
linger.ms=10
batch.size=65536
delivery.timeout.ms=120000
```

代码必须处理异步回调中的失败。不要无限阻塞业务线程，也不要对认证失败、序列化错误这类永久错误无脑重试。

---

## 6 Kafka Consumer

### 6.1 工作流程

```text
subscribe Topic
   -> Join Consumer Group
   -> Partition Assignment
   -> poll() Fetch Records
   -> Business Processing
   -> Commit next Offset
   -> heartbeat / rebalance when membership changes
```

Consumer 是 Pull 模型。`poll()` 不只是取数据，还参与组协调、心跳和 Rebalance 流程；业务处理过久导致超过 `max.poll.interval.ms`，Coordinator 会认为成员无法继续工作并重新分配 Partition。

### 6.2 Partition 分配与 Rebalance

触发 Rebalance 的典型事件：成员加入/离开、订阅 Topic Partition 数改变、会话超时、静态成员变化。Rebalance 期间可能暂停处理，因此要避免频繁扩缩容、长时间阻塞 Poll 线程和不稳定网络。

Kafka 4.3 有两套协议：

- `group.protocol=classic`：默认；心跳和会话参数主要由客户端配置。
- `group.protocol=consumer`：KIP-848 新协议；Broker 侧控制心跳、会话和可用 Assignor，降低大组 Rebalance 成本。

新协议不是把所有应用直接切换即可。先核对客户端支持、Assignor、监控和回滚流程，再灰度迁移。参考 [Consumer Rebalance Protocol](https://kafka.apache.org/43/operations/consumer-rebalance-protocol/)。

### 6.3 自动与手动提交

| 模式 | 行为 | 风险 | 适合场景 |
| --- | --- | --- | --- |
| 自动提交 | 周期性提交最近 `poll()` 返回位置 | 业务尚未完成时提交，崩溃可能丢处理 | 可容忍少量丢失或快速原型 |
| 同步手动提交 | 处理成功后 `commitSync()` | 提交阻塞；提交成功前崩溃会重复 | 最易理解的 At Least Once |
| 异步手动提交 | `commitAsync()` | 回调与提交顺序处理更复杂 | 高吞吐且能正确处理失败顺序 |
| 事务提交 | 输出记录和输入 Offset 同一 Kafka 事务 | 配置与运维更复杂 | Kafka 读-处理-写 EOS |

### 6.4 三种交付语义

```text
At Most Once:   commit -> process    崩溃可能丢，不重复
At Least Once:  process -> commit    崩溃可能重复，尽量不丢
Exactly Once:   process + output + offset 在受控事务边界原子提交
```

- **At Most Once**：先提交后处理；适合可丢弃指标等少数场景。
- **At Least Once**：先处理后提交；最常见，要求业务消费者幂等。
- **Exactly Once Semantics (EOS)**：Kafka 内通过幂等 Producer、事务与 `read_committed` 实现读-处理-写的一次可见性。

> [!warning] 边界
> Kafka 事务不能自动把数据库、HTTP、邮件等外部副作用纳入同一事务。涉及外部系统时仍需 Inbox/Outbox、唯一约束、幂等键或专用分布式事务方案。

### 6.5 Consumer 关键参数

| 参数 | 作用 | 排查提示 |
| --- | --- | --- |
| `group.id` | 消费进度和负载分配命名空间 | 不同业务必须用不同 Group |
| `auto.offset.reset` | 没有有效提交位置时从 `earliest/latest` 开始 | 它不是每次启动都重置 Offset |
| `enable.auto.commit` | 是否自动提交 | 生产常关闭并显式定义提交点 |
| `max.poll.records` | 一次 Poll 返回的最大记录数 | 处理超时先减小它或做并行处理 |
| `max.poll.interval.ms` | 两次 Poll 的最大业务处理间隔 | 超过会被踢出 Group |
| `session.timeout.ms` | Coordinator 判断成员失联的时间 | 新协议下由 Broker 端对应参数控制 |
| `fetch.min.bytes` / `fetch.max.wait.ms` | Broker 聚合 Fetch 响应 | 提吞吐会增加等待延迟 |
| `isolation.level` | 是否只读已提交事务 | EOS 下使用 `read_committed` |

准确默认值见 [Consumer Configs](https://kafka.apache.org/43/configuration/consumer-configs/)。

---

## 7 Kafka 存储机制

### 7.1 Partition 日志与 Segment

每个 Partition 是目录，内部按大小或时间滚动生成多个 Log Segment：

```text
orders-0/
  00000000000000000000.log      # 消息批次数据
  00000000000000000000.index    # 稀疏 Offset -> 物理位置索引
  00000000000000000000.timeindex# 时间戳 -> Offset 索引
  00000000000000102400.log
  00000000000000102400.index
  00000000000000102400.timeindex
```

文件名是该 Segment 的 Base Offset。Kafka 先定位可能包含目标 Offset 的 Segment，再用稀疏索引靠近目标位置，最后顺序扫描 Batch。

### 7.2 为什么吞吐高

- 追加写把随机写转换成顺序写。
- Page Cache 让操作系统统一管理缓存，避免 JVM 堆复制和长 GC。
- Producer/Consumer 以 Batch 传输和压缩。
- Partition 让多个 Broker、磁盘和客户端并行工作。
- 网络传输尽量减少不必要的数据复制。

“顺序写很快”不是完整答案。吞吐来自批处理、压缩、操作系统缓存、协议和分区并行的组合。

### 7.3 删除时机

Retention 通常按 Segment 删除，而不是逐条记录删除。某条记录超过 `retention.ms` 后仍可能保留到所属 Segment 可整体删除为止。`retention.bytes` 是每个 Partition 的近似上限，不是整个 Topic 总上限。

### 7.4 磁盘与操作系统

官方 [Hardware and OS](https://kafka.apache.org/43/operations/hardware-and-os/) 建议重点利用 Page Cache、使用高吞吐磁盘、合理挂载 `noatime`，并把 Kafka 数据日志与应用日志分开。不要把 JVM Heap 配到占满机器内存，应给 Page Cache 留出足够空间。

---

## 8 Kafka 副本机制

### 8.1 ISR、LEO 与 HW

- **ISR (In-Sync Replicas)**：与 Leader 保持在允许滞后范围内的副本集合，包含 Leader。
- **LEO (Log End Offset)**：某副本日志末端的下一 Offset；不同副本可能不同。
- **HW (High Watermark)**：所有合格同步副本都已复制到的边界；普通消费者只看到 HW 之前的数据。

```text
offset:  0 1 2 3 4 5 6 7 8
Leader:  x x x x x x x x x   LEO=9
F1:      x x x x x x x x     LEO=8
F2:      x x x x x x x       LEO=7
                          ^
                          HW=7（可见范围通常为 offset < 7）
```

数字表示“下一位置”时容易混淆：LEO=9 意味着已有的最后记录 Offset 是 8。

### 8.2 写入与复制

```text
Producer -> Leader append
                |
       +--------+--------+
       v                 v
  Follower 1 Fetch  Follower 2 Fetch
       |                 |
       +------ ISR ------+
                |
       acks=all + minISR 条件满足
                |
             ACK Producer
```

Follower 主动向 Leader Fetch，而不是 Leader 推送。副本持续落后会移出 ISR；恢复追上后重新加入。

### 8.3 Leader 故障

Controller 检测失败后，为受影响 Partition 选新 Leader，并发布新元数据。客户端收到错误或刷新 Metadata 后重试到新 Leader。若允许从非 ISR 副本选 Leader，可提升可用性但可能丢已确认数据，因此 `unclean.leader.election.enable` 通常保持 `false`。

### 8.4 ELR

Kafka 4.x 的 Eligible Leader Replicas (ELR) 在 ISR 不足时记录一组仍可作为 Leader 候选的副本，改善特定多数故障场景下的安全恢复。它不是 RF/ISR 的替代品；启用前要理解集群 Feature Level、`min.insync.replicas` 和恢复流程。参考 [ELR 官方文档](https://kafka.apache.org/43/operations/eligible-leader-replicas/)。

---

## 9 Kafka 高可用与数据可靠性

### 9.1 常用生产基线

```properties
# Topic
replication.factor=3
min.insync.replicas=2
unclean.leader.election.enable=false

# Producer
acks=all
enable.idempotence=true

# Consumer
enable.auto.commit=false
```

这组配置的含义是：3 个副本中至少 2 个同步副本参与可靠写入。失去一个副本时仍可写；只剩一个 ISR 时拒绝写入，避免在脆弱状态继续接受可能丢失的数据。

### 9.2 可靠性不是一个参数

端到端链路至少包含：

```text
业务数据库
  -> Producer 是否真的发送
  -> Broker 是否达到 ISR 条件
  -> 副本与磁盘是否健康
  -> Consumer 是否处理成功后提交
  -> 下游副作用是否幂等
```

任一环节配置错误都可能导致丢失或重复。数据库与 Kafka 双写应使用 Transactional Outbox；消费与数据库更新应使用 Inbox/唯一键或业务幂等状态机。

### 9.3 跨机房容灾

不要把一个 Kafka 集群横跨高延迟 WAN。更稳妥的架构是每个 Region/DC 一个本地集群，通过 MirrorMaker 2 或受管复制做异步镜像：

```text
Region A Kafka -- MirrorMaker 2 --> Region B Kafka
      ^ Active                         ^ Standby / Read
```

必须明确：RPO（允许丢多少数据）、RTO（多久恢复）、Topic 方向、ACL/配置同步、Consumer Offset 同步与故障切换/回切步骤。异步复制不能承诺零 RPO。参考 [Datacenters](https://kafka.apache.org/43/operations/datacenters/) 与 [Geo Replication](https://kafka.apache.org/43/operations/geo-replication-cross-cluster-data-mirroring/)。

### 9.4 容量与故障域

- Broker 分散到不同宿主机、机架或可用区，配置 Rack Awareness。
- 副本不能都落在同一故障域。
- 磁盘使用率预留重复制和 Reassignment 空间，通常不要长期逼近 80%～85%。
- 扩容前估算 Leader/Partition 数、网络、磁盘和恢复时间，而不是只看总存储容量。
- 定期做故障演练：停 Broker、断网络、磁盘只读、Controller 失效、跨 Region 切换。

---

## 10 Kafka Java 开发

### 10.1 Maven 依赖

```xml
<dependency>
    <groupId>org.apache.kafka</groupId>
    <artifactId>kafka-clients</artifactId>
    <version>4.3.1</version>
</dependency>
```

客户端与 Broker 不要求完全同版本，但上线前必须查 [Compatibility Matrix](https://kafka.apache.org/43/getting-started/compatibility/)，并验证计划使用的协议特性。新客户端连接旧 Broker 时会协商能力；这不代表所有新特性都可用。

### 10.2 Producer 最小示例

```java
Properties props = new Properties();
props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
props.put(ProducerConfig.ACKS_CONFIG, "all");
props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);

try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
    ProducerRecord<String, String> record =
            new ProducerRecord<>("orders.created", "order-42", "{\"status\":\"CREATED\"}");
    producer.send(record, (metadata, error) -> {
        if (error != null) {
            error.printStackTrace();
            return;
        }
        System.out.printf("partition=%d offset=%d%n", metadata.partition(), metadata.offset());
    });
}
```

`KafkaProducer` 是线程安全的，通常按进程复用。不要为每条消息新建 Producer；那会反复建立连接、获取 Metadata 并破坏批处理。

### 10.3 Consumer Group 与手动提交

```java
Properties props = new Properties();
props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
props.put(ConsumerConfig.GROUP_ID_CONFIG, "inventory-service");
props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
    consumer.subscribe(List.of("orders.created"));
    while (true) {
        ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));
        for (ConsumerRecord<String, String> record : records) {
            processIdempotently(record.key(), record.value());
        }
        if (!records.isEmpty()) {
            consumer.commitSync();
        }
    }
}
```

`KafkaConsumer` 不是线程安全的。常见并行模式是每个消费线程一个 Consumer；若 Poll 与业务处理解耦，必须处理 Partition 级顺序、背压、`pause/resume`、Offset 聚合与 Rebalance 回调。

### 10.4 批量、异步、异常与重试

- Producer 的 `send()` 天然异步；用 Callback/Future 观察最终结果。
- Consumer 的一次 `poll()` 返回批量记录；业务可按 Partition 分组处理。
- 可重试异常如 Leader 切换、短暂网络失败，客户端会在 `delivery.timeout.ms` 内重试。
- 永久异常如序列化、认证、ACL、消息过大，应快速失败并告警。
- Consumer 业务失败要明确选择：暂停重试、重试 Topic、DLT，或人工补偿；不能吞异常后继续提交。

完整可运行代码：

- [Hello World Java](../../code/kafka-learning-labs/01-hello-world-java/README.md)
- [日志管道 Java](../../code/kafka-learning-labs/02-log-pipeline-java/README.md)

---

## 11 当前两个入门实战

代码统一位于 [kafka-learning-labs](../../code/kafka-learning-labs/README.md)。两个项目共享根目录的 Kafka 4.3.1 KRaft 单节点环境，但各自使用独立 Topic 和 Consumer Group。

### 11.0 新手如何阅读和开发这套代码

项目源码已经为类、方法、Kafka 参数、消息生命周期和失败边界补充中文注释。不要按文件名字母顺序读，应该沿一条消息的生命周期学习：

```text
项目与环境
  -> Topic
  -> 消息契约与序列化
  -> Producer 分区、批量和异步发送
  -> Broker Partition 日志
  -> Consumer Group 分配与 poll
  -> 业务处理
  -> Offset 提交与失败恢复
```

推荐阅读顺序：

1. 根 `README.md`：先理解总体结构、完整开发流程、运行方式和观察指标。
2. 根 `pom.xml`、`compose.yaml`、`scripts/create-topics.sh`：理解构建、KRaft 环境和 Topic 准备。
3. 实验 1：`KafkaSettings` → 配置测试 → `TopicAdmin` → `ProducerApp` → `ConsumerApp`。
4. 实验 2：`LogEvent` → `LogEventCodec` → 编解码测试 → `LogProducer` → `LogConsumer`。
5. 最后运行 Group CLI，核对 Partition 分配、Committed Offset 和 Lag；不要只看 Java 控制台打印。

这套项目的开发顺序也遵循同一思路：先固定版本和环境，再定义 Topic 与消息契约；先测试不依赖 Broker 的配置/编解码，后实现 Producer 和 Consumer，最后做 Compose 端到端验证。详细的逐文件问题、预期输出、新手练习和常见错误见项目根 README 与两个实验 README。

### 11.1 项目 1：Kafka Hello World

**项目目标**：用原生 Java Client 跑通 Producer、Topic、Consumer 的最小闭环，并观察 key、Partition、Offset 和 Consumer Group 的关系。

```text
ProducerApp
   | key=user-n
   v
learning.hello（3 Partitions）
   |
   v
ConsumerApp（hello-java-group，手动提交 Offset）
```

**技术栈**：Java 21、Kafka Client 4.3.1、Maven、官方 `apache/kafka:4.3.1` 镜像。

**关键代码**：

- `KafkaSettings`：可靠 Producer 与手动提交 Consumer 的配置基线。
- `TopicAdmin`：通过 Admin Client 幂等创建 3 Partition Topic。
- `ProducerApp`：使用相同 key 保证同一用户事件进入同一 Partition，异步 Callback 打印 Partition/Offset。
- `ConsumerApp`：一批业务处理成功后 `commitSync()`，形成基础 At Least Once。
- `KafkaSettingsTest`：不连接 Broker，快速锁定 Producer 可靠性和 Consumer 手动提交参数。

**运行步骤**：

```bash
cd code/kafka-learning-labs
docker compose up -d
./scripts/create-topics.sh

# 终端 1
./mvnw -pl 01-hello-world-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.hello.ConsumerApp \
  -Dexec.args=10

# 终端 2
./mvnw -pl 01-hello-world-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.hello.ProducerApp \
  -Dexec.args=10
```

**验证方法**：Producer 与 Consumer 都显示 10 条消息；相同 key 的 Partition 一致。启动两个 Consumer 后发送更多消息，可以看到同 Group 内 Partition 被分摊，而不是每个 Consumer 都收到全量消息。

### 11.2 项目 2：Kafka 日志管道

**项目目标**：发送结构化 JSON 日志，练习异步发送、Batch、压缩、批量 Poll、手动提交和坏消息处理边界。

```text
LogProducer
   | JSON + service key + Zstd
   v
learning.logs
   |
   v
LogConsumer（log-analytics-group）
   |
   +-> 按 service 累计 ERROR 数
```

**技术栈**：Java 21、Kafka Client 4.3.1、Jackson、JUnit 5。

**关键代码**：

- `LogEvent`：结构化日志事件契约。
- `LogEventCodec`：JSON 编解码集中管理，便于测试与后续替换 Schema。
- `LogProducer`：`linger.ms`、`batch.size`、Zstd 和异步 Callback。
- `LogConsumer`：处理完整批次后提交；解析失败不提交当前批次，明确展示 Poison Record 会阻塞进度的问题。
- `LogEventCodecTest`：先验证 Java 对象与 JSON 的 Round Trip，再进行 Kafka 端到端联调。

**运行步骤**：

```bash
# 终端 1
./mvnw -pl 02-log-pipeline-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.logs.LogConsumer

# 终端 2
./mvnw -pl 02-log-pipeline-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.logs.LogProducer \
  -Dexec.args=20
```

**验证方法**：Consumer 输出 20 条事件并累计 ERROR 数；使用下面命令确认 Lag 最终归零：

```bash
docker compose exec kafka /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group log-analytics-group
```

两个项目的全部单元测试：

```bash
./mvnw test
```

> [!warning] 实验边界
> 单节点、RF=1、PLAINTEXT 和内存聚合只适合本地学习，不能直接作为生产模板。项目 2 的本地解析重试用于观察失败；生产需要区分瞬时错误与永久坏数据，并设计 Retry Topic、DLT、告警和人工补偿。

---

## 12 后续学习清单（暂不生成）

完成前两个项目后，再按下面顺序扩展。此处只登记范围和交付物，不提前生成代码或长章节。

### 12.1 后续章节

| 顺序 | 主题 | 后续要覆盖的内容 |
| ---: | --- | --- |
| 1 | Python Client | `confluent-kafka` Producer/Consumer、批量、异步、手动 Offset |
| 2 | Kafka Connect 与 CDC | Connector/Task/Worker、Distributed Mode、Debezium、Outbox |
| 3 | Kafka Streams | KStream/KTable、Window、State Store、`exactly_once_v2` |
| 4 | Schema Registry | Avro/Protobuf/JSON Schema、兼容模式、契约演进 |
| 5 | 安全 | TLS、SASL/PLAIN、SCRAM、GSSAPI、OAuth、ACL |
| 6 | 监控 | JMX Exporter、Kafka Exporter、Prometheus、Grafana、告警 |
| 7 | 故障排查 | Lag、发送失败、Broker、Offline Partition、ISR、磁盘、重复/丢失 |
| 8 | 性能调优 | Producer、Consumer、Broker、OS、磁盘和网络的压测方法 |
| 9 | Kubernetes | Strimzi、Helm、KafkaNodePool、StatefulSet、PVC、Operator |
| 10 | 生产架构 | 3～5 Broker、独立 Controller、监控、安全、Connect、Schema、DR |
| 11 | 资源筛选 | 至少 15 个活跃 GitHub 项目、版本状态、推荐阶段与过时标记 |
| 12 | 30 天计划 | 每日主题、资料、实验、验收标准 |

### 12.2 后续项目

| 项目 | 目标 | 触发条件 |
| --- | --- | --- |
| 项目 3：Python 实时处理 | 两个 Topic 间转换数据，手动提交并处理重复 | 完成项目 1、2，能解释 Offset 提交点 |
| 项目 4：Prometheus + Grafana | 同时监控 Broker/JVM、Topic/Partition 与 Consumer Lag | 学完副本、ISR、Lag 与基础排障 |
| 项目 5：事件驱动微服务 | Spring Boot 订单、库存、通知服务，加入幂等和事件契约 | 学完 Schema、重试/DLT、Outbox |

### 12.3 已核定但暂不展开的版本基线

- Kafka Broker 与 Java Client：4.3.1。
- Python 主线客户端：`confluent-kafka 2.15.1`。
- KRaft Only；ZooKeeper 只讲旧集群迁移。
- Kubernetes 主线：Strimzi Operator，直接 Helm Chart 作为对照。
- 监控主线：JMX Exporter + Kafka Exporter + Prometheus + Grafana。

## 相关

- [[Apache Kafka]] — 工具与版本入口
- [[Kafka核心架构]] — 核心概念关系
- [[Kafka可靠性与交付语义]] — 副本、ACK、Offset 与幂等
- [[Kafka KRaft开发环境]] — 本地部署步骤
- [Kafka 4.3 官方文档](https://kafka.apache.org/43/) — 当前章节的首要事实来源
- [配套实验代码](../../code/kafka-learning-labs/README.md) — 当前只包含项目 1、2
