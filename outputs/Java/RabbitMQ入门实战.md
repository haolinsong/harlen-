---
title: RabbitMQ 入门实战
type: output
tags: [Java/消息队列, RabbitMQ, Spring Boot]
aliases: [2026-09-23-RabbitMQ入门实战, 2026-09-24-Spring-AMQP与Maven-Wrapper, Spring AMQP 与 Maven Wrapper]
created: 2026-09-23
updated: 2026-09-25
related: ["[[Java消息队列概览与选型]]", "[[Maven-Wrapper]]"]
---

# RabbitMQ 入门实战

## 学习目标

完成这份练习后，你应该能够：

- 解释 Producer、Exchange、Binding、Queue、Consumer 的关系。
- 说明 RabbitMQ 客户端、Broker 节点、Virtual Host、元数据和消息存储之间的关系。
- 使用 Docker 启动 RabbitMQ 4.x，并通过管理界面观察消息。
- 使用 Spring Boot、`RabbitTemplate` 和 `@RabbitListener` 收发消息。
- 理解 Direct、Topic、Fanout 三种常用 Exchange。
- 正确区分 publisher confirm、publisher return 和 consumer ack。
- 为消费者设计幂等、有限重试和死信队列。

这份文档优先帮助你建立一条完整链路，不追求第一遍就掌握 RabbitMQ 的所有参数。

配套的可运行 Spring Boot 项目位于 [`code/rabbitmq-demo`](../../code/rabbitmq-demo/README.md)，包含本文的消息路由、确认、死信和幂等示例。

项目源码已经加入面向新手的中文 JavaDoc 与关键行注释。第一次阅读建议按项目 README 中的[代码阅读顺序](../../code/rabbitmq-demo/README.md#建议的代码阅读顺序)，沿着“HTTP 请求 → 发布消息 → Exchange 路由 → 消费 → ACK/NACK → 死信”的生命周期逐步跟踪。

## 学习路线

| 阶段 | 内容 | 验收标准 |
| --- | --- | --- |
| 1 | 理解架构并启动 RabbitMQ | 能说明 Connection、Channel、Exchange、Queue 和 Broker 节点的关系 |
| 2 | Spring Boot 最小收发示例 | HTTP 请求发送消息，消费者打印订单通知 |
| 3 | 工作队列与消息路由 | 能解释多个消费者如何分工，以及 routing key 如何匹配 |
| 4 | 确认、失败处理与死信 | 能制造失败，并在死信队列中看到消息 |
| 5 | 幂等与生产化检查 | 能说明重复消费为什么存在，以及如何防重 |

建议分两次完成：第一次做到阶段 3，第二次完成阶段 4 和阶段 5。

## 一、先建立心智模型

RabbitMQ 中，生产者通常不直接把消息发给 Queue，而是先发给 Exchange：

```text
Producer
   |
   | exchange + routing key
   v
Exchange ---- Binding ----> Queue ----> Consumer
```

- **Producer**：生产消息的 Java 应用。
- **Exchange**：根据类型、routing key 和 Binding 决定消息去哪里。
- **Binding**：Exchange 与 Queue 之间的路由规则。
- **Queue**：保存等待消费的消息。
- **Consumer**：从 Queue 获取并处理消息。
- **Virtual Host**：RabbitMQ 内部的逻辑隔离空间，类似数据库实例中的独立数据库。

第一遍只使用 `DirectExchange`：消息的 routing key 与 Binding key 完全相等时，消息进入对应 Queue。

> [!info] 关键区别
> Exchange 负责路由，Queue 负责存储。消息发到了 Exchange，不代表一定有 Queue 接收它；没有匹配路由时，消息可能被退回，也可能被丢弃，取决于发送配置。

### 1.1 核心名词详解

先把所有核心名词放到一条消息链路上：

```text
Publisher / Producer
        │
        │ Connection（TCP 长连接）
        │   └─ Channel（轻量逻辑连接）
        v
RabbitMQ Broker / Node
        │
        │ Virtual Host（逻辑隔离空间）
        v
    Exchange
        │  发布时携带 Routing Key
        │
        ├─ Binding + Binding Key ──> Queue A
        │                              │ Ready
        │                              v
        │                           Consumer
        │                              │ Unacked
        │                              ├─ ACK：处理成功，从 Queue 删除
        │                              └─ NACK/Reject
        │                                  ├─ requeue=true：重新入队
        │                                  └─ requeue=false：进入 DLX 或丢弃
        │
        └─ Binding + Binding Key ──> Queue B ──> Consumer
```

#### Broker、Node 与 Cluster

**Broker** 是消息代理服务这个角色：接收生产者发布的消息，完成路由、存储和投递，并接收生产者与消费者的确认。

**Node** 是一个实际运行的 RabbitMQ 实例，通常对应一个 Erlang VM 进程。在单节点环境里，“Broker”和“Node”经常可以近似理解成同一台 RabbitMQ 服务；在集群环境里，一个 RabbitMQ Cluster 由多个 Node 组成，Broker 则更像整个消息服务。

**Cluster** 是多个 RabbitMQ Node 组成的逻辑集群。节点共享拓扑等分布式状态，但“组成集群”不代表每条消息自动拥有副本；消息是否复制由 Queue 类型决定，例如 Classic Queue 不复制，Quorum Queue 使用 Raft 复制。

#### Publisher / Producer

**Publisher** 与 **Producer** 通常都指生产消息的应用。它负责：

1. 选择目标 Exchange。
2. 设置 routing key。
3. 构造消息正文和属性。
4. 发布后根据需要等待或异步处理 publisher confirm。
5. 对无法路由的消息处理 publisher return。

在本项目中，`OrderEventController` 创建事件，`OrderEventPublisher` 才是真正调用 `RabbitTemplate` 发布消息的 Producer。

#### Message

**Message** 是在线路中传递的消息，通常可以拆成三部分：

| 部分 | 示例 | 谁使用 |
| --- | --- | --- |
| Body / Payload | `OrderCreatedEvent` 转成的 JSON | 主要由生产者和消费者理解；Broker 通常不解析业务内容 |
| Properties | `messageId`、`contentType`、`deliveryMode`、`correlationId` | 客户端和 Broker 的标准元数据 |
| Headers | 自定义键值、死信产生的 `x-death` 等 | 业务扩展或 RabbitMQ 功能 |

消息还会在投递时带上 delivery metadata，例如 Exchange、routing key、delivery tag 和 `redelivered` 标志。它们描述“这次投递”，不是消息正文的一部分。

#### Exchange

**Exchange 是路由器，不是仓库。** Producer 把消息发布到 Exchange，Exchange 根据自己的类型、消息的 routing key 和现有 Binding，决定把消息复制到哪些 Queue 或其他 Exchange。

一条消息可能：

- 匹配 0 个 Queue：未路由；根据 `mandatory`、alternate exchange 等配置被返回、转发或丢弃。
- 匹配 1 个 Queue：常见的点对点任务路由。
- 匹配多个 Queue：每个 Queue 得到独立副本，从而实现发布/订阅。

常用 Exchange 类型：

| 类型 | 匹配方式 | 例子 | 常见用途 |
| --- | --- | --- | --- |
| Direct | routing key 与 binding key 完全相等 | `order.created` = `order.created` | 精确路由、业务命令 |
| Topic | 按点分段，`*` 匹配一段，`#` 匹配零到多段 | `order.*`、`audit.#` | 多维度事件订阅 |
| Fanout | 忽略 routing key，发给所有绑定目标 | 所有绑定 Queue 各收一份 | 广播通知 |
| Headers | 根据消息 headers 和 Binding 参数匹配 | `format=pdf` | 不适合用字符串 routing key 的场景 |
| Default Exchange | RabbitMQ 预置、名称为空字符串的特殊 Direct Exchange | routing key 写 Queue 名 | 简单地“按 Queue 名发送” |

RabbitMQ 声明 Queue 时会自动把它绑定到 Default Exchange，binding key 就是 Queue 名。因此看起来可以“直接发给 Queue”，实际仍经过 Default Exchange。业务系统通常显式创建自己的 Exchange，让生产者不必知道 Queue 名。

b #### Routing Key、Binding 与 Binding Key

这三个名词最容易混淆：

- **Routing Key**：Producer 发布每条消息时附带的路由字符串，例如 `order.created`。
- **Binding**：Exchange 到 Queue（或另一个 Exchange）的一条单向路由关系。
- **Binding Key**：创建 Binding 时填写的匹配规则；不同 Exchange 类型对它有不同解释。

可以把它们理解成“消息携带的值”和“路由表中的规则”：

```text
发布消息时：routing key = order.created
                         │
                         v
Exchange 逐条检查当前 Binding
                         │
                         ├─ binding key = order.created -> 匹配
                         └─ binding key = order.cancelled -> 不匹配
```

Routing Key 随每条消息一起到达 Exchange；Binding Key 在创建 Binding 时写进 RabbitMQ 的拓扑中。两者虽然通常都是字符串，但出现的时间和职责不同。Exchange 先看自己的类型，再决定如何使用这些值：

| Exchange 类型 | Binding 中配置什么 | Exchange 如何判断匹配 |
| --- | --- | --- |
| Direct | 一个普通字符串，例如 `order.created` | 消息的 routing key 必须与 binding key 完全相等 |
| Topic | 一个模式，例如 `order.*`、`order.#` | 把 routing key 按 `.` 分段；`*` 匹配一段，`#` 匹配零到多段 |
| Fanout | 可以填写 key，但没有路由意义 | 忽略 routing key 和 binding key，所有绑定的 Queue 都匹配 |
| Headers | 主要配置 Binding arguments，例如 `format=pdf`、`x-match=all` | 忽略 routing key，改为比较消息 headers 与 Binding arguments |
| Default Exchange | RabbitMQ 自动使用 Queue 名作为 binding key | 按“routing key 等于 Queue 名”精确匹配 |

所以，“不同 Exchange 类型对 Binding Key 有不同解释”具体是指：同样写在 Binding 上的值，在 Direct 中是**完整值**，在 Topic 中是**通配模式**，在 Fanout 和 Headers 中则基本不参与匹配。

以 Direct Exchange 为例：

```text
消息 routing key = order.created

orders.direct
  ├─ binding key = order.created ──> orders.notify.q  （匹配）
  ├─ binding key = order.created ──> orders.audit.q   （匹配）
  └─ binding key = order.cancelled ─> orders.cancel.q （不匹配）
```

因此同一条消息可以进入前两个 Queue。Binding 本身不保存消息，它只是 Exchange 路由表里的一条规则。

##### Exchange 与 Queue 是多对多关系

在标准的 Exchange 到 Queue 路由中，**Binding 就是映射关系**。Exchange 和 Queue 先各自独立声明，再单独创建 Binding；Exchange 在声明时并不自带一组固定 Queue。

```text
                         binding key
orders.direct ───────── order.created ───────> orders.notify.q
       │
       └─────────────── order.created ───────> orders.audit.q

alerts.direct ───────── critical ────────────> orders.audit.q
```

上面的拓扑说明：

- 一个 Exchange 可以不绑定 Queue，也可以绑定一个或多个 Queue。
- 一个 Queue 也可以同时绑定一个或多个 Exchange；示例中的 `orders.audit.q` 同时接收两个 Exchange 的消息。
- 同一个 Exchange 与同一个 Queue 之间可以有多条 Binding，每条使用不同的 binding key 或 Binding arguments。
- Binding 可以通过应用、管理界面或 HTTP API 添加和删除，因此它是“当前拓扑配置”，不是 Exchange 创建后永远不变的固有关系。
- RabbitMQ 还支持 Exchange-to-Exchange Binding：上游 Exchange 可以先路由到另一个 Exchange，再由下游 Exchange 路由到 Queue。

每次有消息到达时，Exchange 都会根据**当前所有 Binding**计算目标 Queue 集合：

- 匹配 0 个 Queue：消息无法路由。
- 匹配 1 个 Queue：向该 Queue 写入一份。
- 匹配多个不同 Queue：每个 Queue 各写入一份。

如果同一个 Queue 有多条 Binding 同时匹配一条消息，该消息仍然只会向这个 Queue 写入一次。例如：

```text
消息 routing key = order.created

orders.topic
  ├─ order.*   ──> analytics.q  （匹配）
  └─ *.created ──> analytics.q  （也匹配）

结果：analytics.q 只得到一份消息
```

这和 Consumer 数量也要分开理解：两个不同 Queue 匹配时会各得一份；两个 Consumer 监听同一个 Queue 时，则竞争处理 Queue 中的同一份消息。

在 Spring Boot 项目里，Exchange、Queue 和 Binding 通常都写成固定的 Bean，并由 `RabbitAdmin` 在每次启动时声明，所以代码层面看起来像“固定对应”。真正保存到 RabbitMQ 中的仍是可独立增删的拓扑关系。

#### Queue

**Queue 是消息等待消费的位置。** Exchange 完成路由后，消息才进入 Queue；Consumer 从 Queue 接收消息，而不是直接从 Exchange 消费。

Queue 的重要属性：

| 属性 | 含义 |
| --- | --- |
| `name` | Queue 名称；可以由应用指定，也可以由 Broker 生成 |
| `durable` | Broker 重启后是否保留 Queue 定义 |
| `exclusive` | 是否只允许声明它的 Connection 使用；连接关闭时会删除 |
| `autoDelete` | 曾经有消费者后，最后一个消费者取消订阅时是否删除 |
| `arguments` | DLX、TTL、长度限制、Queue 类型、优先级等扩展参数 |

管理界面中最常看的消息状态：

- **Ready**：仍在 Queue 中，等待投递给 Consumer。
- **Unacked**：已经投递给 Consumer，但 RabbitMQ 还没有收到 ACK。
- **Total**：通常是 Ready 与 Unacked 的总和。

Queue 经常按 FIFO 入队和出队，但“业务完成顺序”不一定严格 FIFO。多个消费者并行处理、消息重新入队、消费者优先级等因素都可能改变最终完成顺序。

> [!info] Durable Queue 不等于消息绝不丢
> `durable=true` 主要保证 Queue 定义能跨 Broker 重启保留。还需要发布持久化消息、使用 publisher confirm，并根据故障容忍要求选择 Quorum Queue 等合适类型。

#### Consumer 与 Subscription

**Consumer** 是订阅 Queue 并处理消息的应用逻辑。AMQP 0-9-1 支持 Broker 主动推送和客户端轮询，通常应使用推送式订阅；Spring 的 `@RabbitListener` 就会注册这种 Consumer。

每个订阅有一个 **consumer tag**，用于标识和取消订阅。一个 Queue 可以有多个 Consumer：

- 多个 Consumer 监听**同一个 Queue**：消息由其中一个 Consumer 处理，称为竞争消费。
- 多个 Consumer 分别监听**不同 Queue**，而这些 Queue 绑定同一个 Exchange：每个 Queue 都有消息副本，形成发布/订阅。

#### ACK、NACK、Reject 与 Requeue

RabbitMQ 把消息交给 Consumer 后，需要知道应用是否处理成功。先区分两个概念：

- **Message** 是 Queue 中的那条消息。
- **Delivery** 是 RabbitMQ 把这条消息交给某个 Consumer 的一次尝试。同一条 Message 可能经历多次 Delivery。

```text
Queue 中 Ready
    │
    └─ 第一次投递：tag=37, redelivered=false
                         │
                         v
                      Unacked
                         │
             ┌───────────┴───────────┐
             │                       │
          ACK 成功              Reject / NACK
             │                       │
      从 Queue 中删除       ┌────────┴────────┐
                            │                 │
                     requeue=true      requeue=false
                            │                 │
                         放回 Queue      进入 DLX 或丢弃
                            │
                            └─ 再次投递：tag=41, redelivered=true
```

##### 什么时候会 Reject 或 NACK

“拒绝”表示 Consumer 主动告诉 RabbitMQ：**当前这次 Delivery 没有被成功处理**。常见原因包括：

- 消息格式错误，无法反序列化。
- 缺少必要字段，或字段值不符合业务约束。
- 对应业务对象不存在，而且以后重试也不会恢复。
- 调用数据库、HTTP 服务或其他依赖失败。
- 消费代码抛出异常，业务事务没有完成。

`basic.reject` 和 `basic.nack` 都是否定确认，主要区别是处理数量：

| 方法 | 能处理多少 Delivery | 关键参数 |
| --- | --- | --- |
| `basicReject(tag, requeue)` | 只能拒绝当前一个 Delivery | `requeue` 决定是否放回 Queue |
| `basicNack(tag, multiple, requeue)` | `multiple=false` 时拒绝一个；`true` 时可批量拒绝当前 Channel 上截至该 tag 的未确认 Delivery | 同时控制批量范围和是否重新入队 |

不是所有“无需再次执行业务”的消息都应该 Reject。例如幂等检查发现 `eventId` 已经成功处理过，说明目标业务状态已经完成，此时应该直接 ACK；如果 Reject 并重新入队，它只会反复出现。

##### Requeue 决定拒绝后的去向

- `requeue=true`：RabbitMQ 把该消息放回原 Queue。它通常回到原位置或更靠近队头的位置，随后可能立刻交给同一个 Consumer，也可能交给同一 Queue 的另一个 Consumer。
- `requeue=false`：不再回到原 Queue；Queue 配置了 DLX 时进入死信流程，没有 DLX 时被丢弃。

可以按失败性质做初步判断：

| 失败类型 | 例子 | 建议 |
| --- | --- | --- |
| 永久失败 | JSON 损坏、必填字段缺失、业务规则确定不允许 | `requeue=false`，进入 DLQ 后排查或补偿 |
| 临时失败 | 数据库短暂不可用、下游服务超时 | 有限次数重试并增加退避；不要无限立即 `requeue=true` |
| 重复消息 | 相同 `eventId` 已成功处理 | 直接 ACK，避免继续重复投递 |

如果所有 Consumer 都因同一个故障立即执行 `requeue=true`，消息会在“投递 -> 失败 -> 重新入队 -> 再投递”之间高速循环，持续占用 CPU、网络和 Consumer。因此生产系统通常采用有限重试、延迟重试，最终转入 DLQ。

##### 什么是再次投递

**再次投递（redelivery）**是同一条 Queue 消息在没有被成功 ACK 后，又被 RabbitMQ 交给 Consumer。它不一定由应用主动 Reject 触发。手动 ACK 模式下，下列情况都可能让未确认消息自动重新入队：

- Consumer 处理到一半进程崩溃。
- Consumer 与 RabbitMQ 的 TCP 连接断开。
- 接收该 Delivery 的 Channel 在 ACK 前关闭或发生协议异常。
- 业务已经执行成功，但 ACK 在网络故障中没有到达 RabbitMQ。
- Consumer 主动调用 `basicReject` 或 `basicNack`，并设置 `requeue=true`。

再次投递时，消息可能交给原 Consumer，也可能交给同一 Queue 的另一个 Consumer。例如 Consumer A 已经更新数据库，但 ACK 丢失；RabbitMQ 随后把消息交给 Consumer B，B 就可能再次更新数据库。这就是消费者必须幂等的原因。

##### Delivery Tag 标识的是一次投递

**Delivery Tag** 是 RabbitMQ 在 Channel 内分配的递增正整数，用来标识当前这一次 Delivery。它不是消息的全局 ID，也不能跨 Channel 使用：

- ACK、Reject 或 NACK 必须在收到消息的同一个 Channel 上发送。
- 在另一个 Channel 上确认、使用不存在的 tag，或重复确认同一个 tag，会产生 `unknown delivery tag` 并关闭 Channel。
- 同一 Message 再次投递时会产生新的 Delivery，也会拿到该 Channel 上新的 Delivery Tag。

需要业务去重时，应使用消息中的 `messageId`、`eventId` 或业务唯一键，而不是 Delivery Tag。

##### Redelivered 只是 Broker 视角的提示

**Redelivered** 是本次 Delivery 携带的布尔标记：

- `false`：RabbitMQ 认为这是该 Queue 消息的首次投递。
- `true`：这条 Queue 消息之前已经投递并重新入队，现在正在再次投递。

它不能代替幂等判断，因为它只描述 RabbitMQ 是否重新投递了这条 Queue 消息：

- `true` 不代表上一次业务一定成功，也不代表一定失败；RabbitMQ 只知道没有收到 ACK。
- Producer 把相同业务事件发布两次，会形成两条消息，两次首次投递都可能是 `redelivered=false`。
- Consumer 仍应根据稳定的业务 ID 和持久化状态判断事件是否已经处理。

本项目使用手动 ACK。`orderId=fail` 会触发模拟的永久失败，随后执行 `basicNack(deliveryTag, false, false)`：第一个 `false` 表示不批量拒绝，第二个 `false` 表示不放回原 Queue；由于通知 Queue 配置了 DLX，消息最终进入死信 Queue，而不是立即再次投递。

手动 ACK 的关键顺序是：

```text
收到消息 -> 完成业务事务 -> ACK
```

如果先 ACK 再执行业务，随后业务失败，消息已经从 Queue 删除。反过来，如果业务已提交但 ACK 因网络故障丢失，RabbitMQ 可能重新投递，所以消费者仍要做幂等。

#### Prefetch / QoS

**Prefetch** 限制 RabbitMQ 最多向 Consumer 推送多少条尚未 ACK 的消息，相当于消费端的在途窗口和背压控制。

- `prefetch=1`：当前消息确认后才继续推送，容易观察公平分发，但吞吐较低。
- 较大的值：提高流水线并行度，但会增加 Consumer 内存占用和消息被单个 Consumer 囤积的风险。
- `prefetch=0`：表示不限制，通常不适合没有容量保护的业务消费者。

本项目设置为 1 是为了学习效果，不是通用的生产最优值。

#### Publisher Confirm 与 Publisher Return

两者都发生在生产者侧，但回答不同的问题：

| 机制 | 回答的问题 | 不代表什么 |
| --- | --- | --- |
| Publisher Confirm | RabbitMQ 是否接管了这次发布 | 不代表消费者已完成业务 |
| Publisher Return | 消息到达 Exchange 后，是否没有任何匹配 Queue | 不代表消费者处理成功或失败 |

发送到不存在的 Exchange 通常会导致 Channel 错误；发送到存在的 Exchange、但没有匹配 Binding 时，在 `mandatory=true` 且注册 return handler 的情况下，消息会退回生产者。

#### DLX、Dead Letter 与 DLQ

- **Dead Letter**：因为拒绝且不重新入队、消息 TTL 到期、Queue 超过长度限制，或 Quorum Queue 超过 delivery limit 等原因离开原 Queue 的消息。
- **DLX（Dead Letter Exchange）**：接收并重新路由死信的 Exchange。它仍然是普通 Exchange，不负责保存消息。
- **DLQ（Dead Letter Queue）**：绑定到 DLX、真正保存死信的 Queue。“DLQ”是常用架构叫法，不是一种特殊 Queue 类型。

```text
orders.notify.q
      │ basicNack(requeue=false)
      v
  orders.dlx                 <- DLX，只负责重新路由
      │ order.created.dead
      v
orders.notify.dead.q         <- DLQ，保存等待排查或补偿的消息
```

#### TTL、Policy 与 Queue Arguments

- **TTL（Time-To-Live）**：可以限制消息在 Queue 中存活多久，也可以让闲置 Queue 到期删除。消息过期后不会再交给 Consumer；配置 DLX 时可以进入死信流程。
- **Queue Arguments**：声明 Queue 时写死的扩展参数，例如 `x-dead-letter-exchange`。应用若用不同参数重复声明同名 Queue，会收到 `PRECONDITION_FAILED`。
- **Policy**：由运维侧按名称模式动态应用的 Broker 配置。DLX、TTL、长度限制等生产配置通常更适合 Policy，因为修改时不必重新部署应用或删除 Queue。

#### Virtual Host、User 与 Permission

**Virtual Host（vhost）** 是 RabbitMQ 内部的逻辑命名空间。Exchange、Queue、Binding、Permission 和 Policy 都属于某个 vhost；不同 vhost 可以存在同名 Queue，但不能直接跨 vhost 建 Binding。

**User** 用来认证客户端身份，**Permission** 决定该用户在特定 vhost 中可以配置、写入和读取哪些资源。vhost 提供逻辑隔离，不等于独立 CPU、内存或磁盘的物理隔离。

#### 本项目中的名词对应关系

| 名词                         | 本项目中的实例                                             |
| -------------------------- | --------------------------------------------------- |
| Broker / Node              | `compose.yaml` 启动的 `rabbitmq:4-management` 容器       |
| Virtual Host               | `/`                                                 |
| User                       | `learner`                                           |
| Producer                   | `OrderEventPublisher`                               |
| Message                    | `OrderCreatedEvent` 的 JSON 表示                       |
| Exchange                   | `orders.direct`                                     |
| Routing Key                | `order.created`                                     |
| Binding                    | `orders.direct` 到两个业务 Queue 的绑定                     |
| Queue                      | `orders.notify.q`、`orders.audit.q`                  |
| Consumer                   | `OrderNotificationConsumer`、`OrderAuditConsumer`    |
| DLX                        | `orders.dlx`                                        |
| DLQ                        | `orders.notify.dead.q`                              |
| Publisher Confirm / Return | `RabbitPublisherCallbacks`                          |
| Consumer ACK / NACK        | `OrderNotificationConsumer` 中的 `basicAck/basicNack` |
| Prefetch                   | `application.yml` 中的 `prefetch: 1`                  |

#### 最容易混淆的六组概念

| 不要混淆 | 正确区别 |
| --- | --- |
| Broker vs Exchange | Broker 是整个消息服务；Exchange 是 Broker 内的一套路由器 |
| Exchange vs Queue | Exchange 路由但通常不存消息；Queue 存储并向 Consumer 投递 |
| Routing Key vs Binding Key | 前者随消息发布；后者写在 Binding 上，供 Exchange 匹配 |
| Consumer vs Queue | Consumer 是处理程序；Queue 是 Broker 中保存消息的资源 |
| Publisher Confirm vs Consumer ACK | 前者确认 Producer 到 RabbitMQ；后者确认 RabbitMQ 到 Consumer |
| DLX vs DLQ | DLX 重新路由死信；DLQ 真正保存死信 |

### 1.2 单节点整体架构

从 Java 应用到 RabbitMQ 内部，一条消息会经过下面这些层次：

```text
┌──────────────────────── Java 应用 ────────────────────────┐
│                                                          │
│  Producer                                                │
│  RabbitTemplate                                          │
│       │                                                  │
│  ConnectionFactory                                      │
│       │  TCP Connection                                  │
│       ├── Channel：发布消息                              │
│       └── Channel：消费消息                              │
└───────┼──────────────────────────────────────────────────┘
        │ AMQP 0-9-1，默认端口 5672
        v
┌──────────────────── RabbitMQ Broker Node ─────────────────┐
│                                                          │
│  Virtual Host: /                                         │
│                                                          │
│  Exchange ── Binding ──> Queue ── delivery ──> Consumer  │
│     │                       │                             │
│     │ 路由                  └─ 消息数据、消费位置          │
│     └─ Exchange/Queue/Binding 等拓扑元数据                │
│                                                          │
│  用户、权限、策略、Virtual Host、拓扑由元数据存储管理      │
└──────────────────────────────────────────────────────────┘
        │
        └── Management Plugin：HTTP API 与管理界面，默认端口 15672
```

这里的 **Broker** 是提供消息服务的 RabbitMQ 服务器进程；**Node** 是一个 RabbitMQ 实例。在本教程的 Docker 环境中，一个容器里运行一个 Node，因此也是一个单节点 Broker。

Spring Boot 屏蔽了不少底层细节：`RabbitTemplate` 负责发布，监听容器负责接收，`CachingConnectionFactory` 管理并复用 Connection 和 Channel。理解这些层次仍然很重要，因为网络断开、Channel 关闭、路由失败和消费失败属于不同故障位置。

### 1.3 Connection 与 Channel

RabbitMQ 的 AMQP 客户端使用长连接：

- **Connection** 是应用到 RabbitMQ Node 的物理 TCP 连接，建立和维护成本较高，应长期复用。
- **Channel** 是复用在一个 Connection 上的轻量逻辑连接；声明拓扑、发布、消费和 ack 等协议操作都发生在 Channel 上。
- 一个 Connection 可以承载多个 Channel；Connection 关闭时，其上的 Channel 也全部关闭。
- Channel 出现协议错误时可能单独关闭，例如用不同参数重复声明同名 Queue 会触发 `PRECONDITION_FAILED`，不一定要立即摧毁整个 TCP Connection。

因此，不要为每条消息新建 Connection 或 Channel。使用 Spring Boot 时，一般让框架管理它们；直接使用 RabbitMQ Java Client 时，则需要显式设计生命周期和线程使用方式。

```text
一个 TCP Connection
├── Channel 1：Producer A 发布
├── Channel 2：Producer B 发布
├── Channel 3：Consumer A 消费并 ack
└── Channel 4：声明 Exchange、Queue 和 Binding
```

### 1.4 Virtual Host、拓扑与消息数据

RabbitMQ 中需要区分“控制信息”和“消息数据”：

| 类型 | 包含内容 | 作用 |
| --- | --- | --- |
| Virtual Host | Exchange、Queue、Binding、权限、策略等逻辑命名空间 | 隔离不同系统或环境，但不是物理资源隔离 |
| 拓扑元数据 | Exchange、Queue、Binding、用户、权限、Policy 等定义 | 决定谁可以连接、消息如何路由 |
| 消息数据 | Queue 或 Stream 中的消息内容和消费状态 | 承载真正的业务消息 |

客户端连接时必须指定一个 Virtual Host，并且只能操作该 Virtual Host 内有权限访问的资源。开发环境使用默认 `/` 足够；多项目或多租户环境通常按系统和环境拆分，例如 `/order-dev`、`/order-prod`。

### 1.5 RabbitMQ 的三类消息数据结构

RabbitMQ 4.x 不只有一种 Queue 实现：

| 类型 | 数据特征 | 是否复制 | 适合场景 |
| --- | --- | --- | --- |
| **Classic Queue** | 传统 FIFO Queue，功能丰富 | 不复制，只有一个副本 | 本地开发、可容忍节点故障丢失或有其他补偿手段的任务 |
| **Quorum Queue** | 基于 Raft 的持久化复制 Queue | 多节点复制 | 生产环境中重视数据安全和高可用的业务消息 |
| **Stream** | 持久化 append-only log，可重复读取 | 多节点复制 | 大吞吐、长时间保留、事件回放 |

本教程中的 `QueueBuilder.durable(ORDER_QUEUE)` 在未修改 Virtual Host 默认 Queue 类型时会创建 Classic Queue。`durable` 只表示重启后保留 Queue 定义以及允许持久化消息，并不等于跨节点复制。

> [!warning] 持久化不等于高可用
> 单节点容器停止或磁盘损坏时，没有其他 RabbitMQ Node 可以接管。本教程使用单节点是为了降低学习成本；生产环境需要结合 Quorum Queue、至少三个集群节点、publisher confirm、持久化消息和备份策略整体设计。

### 1.6 集群架构与复制边界

生产环境常把多个 RabbitMQ Node 组成一个逻辑 Cluster：

```text
                      ┌──────── Load Balancer / DNS ────────┐
                      │                                    │
Java Producer ────────┼──> Node A                          │
Java Consumer ────────┼──> Node B       RabbitMQ Cluster   │
                      └──> Node C                          │
                                                           │
共享的集群元数据：用户、Virtual Host、Exchange、Binding、   │
                  Queue 定义、Policy 等                     │

消息数据：
  Classic Queue  -> Leader 所在节点上的单一副本
  Quorum Queue   -> Leader + Followers，多节点 Raft 复制
  Stream         -> Leader + Replicas，持久化并支持重复读取
```

需要记住三个边界：

1. 集群中的 Node 会共享 RabbitMQ 拓扑和其他分布式状态，客户端通常可以连接任一合适节点。
2. 客户端连接的 Node 不一定就是 Queue Leader 所在节点；RabbitMQ 可以在集群内部把操作路由到正确节点。
3. **集群不等于消息自动复制**。Classic Queue 在 RabbitMQ 4.x 中不复制；需要消息副本时，应使用 Quorum Queue 或 Stream。

### 1.7 一条消息的完整生命周期

以本教程的订单通知为例：

1. `RabbitTemplate` 通过 Channel 把消息发布到 `orders.direct`。
2. Direct Exchange 使用 routing key `order.created` 查找 Binding。
3. 匹配的消息被写入 `orders.notify.q`；没有匹配 Queue 时，消息是否退回取决于 `mandatory` 和 return 配置。
4. RabbitMQ 把消息推送给监听容器中的 Consumer。
5. `@RabbitListener` 执行业务逻辑。
6. Consumer ack 后，RabbitMQ 才把消息视为成功处理；nack、连接中断或超时可能触发重新投递或死信流程。

后面的 publisher confirm、publisher return、consumer ack 和死信队列，分别保护这条生命周期中的不同阶段，不能互相替代。

## 二、启动 RabbitMQ

### 2.1 环境要求

- Java 17 或更高版本
- Maven 3.9+，或项目自带的 Maven Wrapper
- Docker Desktop 或其他可用的 Docker 环境
- `curl`

### 2.2 启动 RabbitMQ 4.x

```bash
docker run -d \
  --name rabbitmq-learning \
  -p 5672:5672 \
  -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=learner \
  -e RABBITMQ_DEFAULT_PASS=learner123 \
  -v rabbitmq-learning-data:/var/lib/rabbitmq \
  rabbitmq:4-management
```

端口用途：

- `5672`：Java 客户端使用的 AMQP 端口。
- `15672`：RabbitMQ Management 管理界面。

确认容器正在运行：

```bash
docker ps --filter name=rabbitmq-learning
docker logs rabbitmq-learning
```

浏览器访问 [http://localhost:15672](http://localhost:15672)，用户名 `learner`，密码 `learner123`。

以后可以保留数据并重复启停：

```bash
docker stop rabbitmq-learning
docker start rabbitmq-learning
```

## 三、创建 Spring Boot 项目

### 3.1 Spring AMQP 在这一层做什么

AMQP（Advanced Message Queuing Protocol）是消息中间件使用的一套协议。Spring AMQP 将 Spring 的依赖注入、模板方法、注解监听和消息转换等编程模型应用到 AMQP 消息系统中。

它不是 RabbitMQ Broker，也不是一种新协议。在本项目中的调用链是：

```text
业务代码
  ↓
Spring Boot 自动配置
  ↓
Spring AMQP / Spring Rabbit
  ↓
RabbitMQ Java Client
  ↓ AMQP
RabbitMQ Broker
```

常见的三个依赖层次：

- `spring-amqp`：提供 `Message`、`Queue`、`Exchange`、`Binding`、`AmqpTemplate` 等通用抽象。
- `spring-rabbit`：提供 RabbitMQ 实现，例如 `RabbitTemplate`、`RabbitAdmin`、`@RabbitListener` 和监听容器。
- `spring-boot-starter-amqp`：Spring Boot Starter，引入上述依赖并启用常用自动配置。

常用入口如下：

| 需求 | Spring AMQP API |
| --- | --- |
| 发送消息 | `RabbitTemplate.convertAndSend(...)` |
| 接收消息 | `@RabbitListener` |
| 定义 Queue | `Queue`、`QueueBuilder` |
| 定义 Exchange | `DirectExchange`、`TopicExchange`、`FanoutExchange` |
| 建立路由 | `Binding`、`BindingBuilder` |
| 声明或查询资源 | `AmqpAdmin` / `RabbitAdmin` |
| 对象与消息互转 | `MessageConverter` |
| 发布确认 | `RabbitTemplate.ConfirmCallback` |
| 无法路由回退 | `RabbitTemplate.ReturnsCallback` |

Spring Boot 会根据 `spring.rabbitmq.*` 配置创建连接工厂、`RabbitTemplate`、`AmqpAdmin` 和默认监听容器工厂。应用建立连接后，`RabbitAdmin` 会把 Spring 容器中的 Exchange、Queue、Binding Bean 声明到 RabbitMQ；`MessageConverter` 则负责在 Java 对象与消息负载之间转换。

本库的可运行项目展示了完整用法：

- [`RabbitTopology.java`](../../code/rabbitmq-demo/src/main/java/com/harlan/rabbitmqdemo/config/RabbitTopology.java)：拓扑与 JSON 转换器。
- [`OrderEventPublisher.java`](../../code/rabbitmq-demo/src/main/java/com/harlan/rabbitmqdemo/service/OrderEventPublisher.java)：使用 `RabbitTemplate` 发送事件。
- [`OrderNotificationConsumer.java`](../../code/rabbitmq-demo/src/main/java/com/harlan/rabbitmqdemo/consumer/OrderNotificationConsumer.java)：使用 `@RabbitListener`、手动 ACK 和 NACK。
- [`RabbitPublisherCallbacks.java`](../../code/rabbitmq-demo/src/main/java/com/harlan/rabbitmqdemo/config/RabbitPublisherCallbacks.java)：处理 publisher confirm 和 return。

声明 Bean 只是在描述 Broker 拓扑，并不自动等于消息可靠。完整可靠性仍需要持久化消息、publisher confirm、正确 ACK、重试/死信、幂等以及业务数据一致性共同保证。

在 [Spring Initializr](https://start.spring.io/) 创建项目：

- Project：Maven
- Language：Java
- Java：17 或更高版本
- Dependencies：Spring Web、Spring for RabbitMQ
- Group：`com.example`
- Artifact：`rabbitmq-demo`

项目里最关键的两个依赖如下。版本由 Spring Boot 的 dependency management 管理，不需要单独指定：

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-amqp</artifactId>
</dependency>
```

以下示例假设 Java 包名为 `com.example.rabbitmqdemo`。

### 3.2 连接配置

创建 `src/main/resources/application.yml`：

```yaml
spring:
  application:
    name: rabbitmq-demo
  rabbitmq:
    host: localhost
    port: 5672
    username: learner
    password: learner123
    virtual-host: /
    listener:
      simple:
        prefetch: 1
```

`prefetch: 1` 表示一个消费者在确认当前消息前，Broker 不再预先推送更多消息给它。这便于观察工作队列的公平分发，但生产环境需要结合处理耗时和吞吐量调优。

### 3.3 声明 Exchange、Queue 和 Binding

创建 `RabbitConfig.java`：

```java
package com.example.rabbitmqdemo;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.QueueBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitConfig {

    public static final String ORDER_EXCHANGE = "orders.direct";
    public static final String ORDER_QUEUE = "orders.notify.q";
    public static final String ORDER_ROUTING_KEY = "order.created";

    @Bean
    DirectExchange orderExchange() {
        return new DirectExchange(ORDER_EXCHANGE, true, false);
    }

    @Bean
    Queue orderQueue() {
        return QueueBuilder.durable(ORDER_QUEUE).build();
    }

    @Bean
    Binding orderBinding() {
        return BindingBuilder.bind(orderQueue())
                .to(orderExchange())
                .with(ORDER_ROUTING_KEY);
    }
}
```

参数含义：

- Exchange 的 `durable=true`：Broker 重启后仍保留 Exchange。
- Exchange 的 `autoDelete=false`：没有消费者时不自动删除。
- Queue 使用 `durable`：Broker 重启后仍保留 Queue 的定义。

Queue 持久化并不代表每一条消息都一定不会丢。完整可靠性还依赖消息持久化、publisher confirm、RabbitMQ 节点存储方式和消费者确认。

### 3.4 编写生产者

创建 `OrderMessageProducer.java`：

```java
package com.example.rabbitmqdemo;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

@Service
public class OrderMessageProducer {

    private final RabbitTemplate rabbitTemplate;

    public OrderMessageProducer(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public void sendOrderCreated(String orderId) {
        String message = "orderId=" + orderId;
        rabbitTemplate.convertAndSend(
                RabbitConfig.ORDER_EXCHANGE,
                RabbitConfig.ORDER_ROUTING_KEY,
                message
        );
    }
}
```

创建一个测试用 HTTP 接口 `OrderController.java`：

```java
package com.example.rabbitmqdemo;

import java.util.Map;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/orders")
public class OrderController {

    private final OrderMessageProducer producer;

    public OrderController(OrderMessageProducer producer) {
        this.producer = producer;
    }

    @PostMapping("/{orderId}/notify")
    public ResponseEntity<Map<String, String>> notify(@PathVariable String orderId) {
        producer.sendOrderCreated(orderId);
        return ResponseEntity.accepted().body(Map.of(
                "orderId", orderId,
                "status", "queued"
        ));
    }
}
```

### 3.5 编写消费者

创建 `OrderMessageConsumer.java`：

```java
package com.example.rabbitmqdemo;

import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class OrderMessageConsumer {

    @RabbitListener(queues = RabbitConfig.ORDER_QUEUE)
    public void handle(String message) {
        System.out.printf(
                "[%s] received: %s%n",
                Thread.currentThread().getName(),
                message
        );
    }
}
```

Spring Boot 会自动配置 ConnectionFactory、`RabbitTemplate`、`RabbitAdmin` 和监听容器。应用启动时，前面声明的 Bean 会被映射成 RabbitMQ 中的 Exchange、Queue 和 Binding。

### 3.6 运行与验证

启动应用：

```bash
./mvnw spring-boot:run
```

发送消息：

```bash
curl -i -X POST http://localhost:8080/orders/1001/notify
```

预期 HTTP 状态为 `202 Accepted`，应用日志包含：

```text
received: orderId=1001
```

在 RabbitMQ 管理界面验证：

1. `Exchanges` 中存在 `orders.direct`。
2. `Queues and Streams` 中存在 `orders.notify.q`。
3. Queue 的 `Consumers` 至少为 1。
4. 消费完成后 `Ready` 和 `Unacked` 都回到 0。

> [!question] 没看到消息积压？
> 这是正常的。消费者在线时，消息会很快被取走。可以先启动一次应用以声明 Queue，然后停止应用，再通过管理界面的 Exchange 页面发布消息；重新启动应用后观察消息被消费。

## 四、理解工作队列

同一个 Queue 可以有多个消费者。RabbitMQ 会把 Queue 中的消息分给不同消费者，而不是让每个消费者都收到一份。

把监听器临时改为两个并发消费者：

```java
@RabbitListener(queues = RabbitConfig.ORDER_QUEUE, concurrency = "2")
public void handle(String message) throws InterruptedException {
    Thread.sleep(1_000);
    System.out.printf(
            "[%s] received: %s%n",
            Thread.currentThread().getName(),
            message
    );
}
```

连续发送 10 条消息：

```bash
for id in $(seq 1 10); do
  curl -s -X POST "http://localhost:8080/orders/$id/notify"
done
```

观察两个消费线程交替处理消息。这里建立三个认识：

- 同一 Queue 下的多个消费者是**竞争消费**，一条消息通常只交给其中一个消费者。
- 想让库存服务和通知服务各收到一份订单事件，应让它们使用**不同 Queue**，并分别绑定同一个 Exchange。
- `prefetch` 和消费者并发数共同影响吞吐、公平性和未确认消息数量。

## 五、理解 Exchange 类型

| 类型 | 路由规则 | 典型用途 |
| --- | --- | --- |
| `Direct` | routing key 完全匹配 | 明确的业务事件，如 `order.created` |
| `Topic` | 使用 `*` 和 `#` 做模式匹配 | 按业务域或事件类别订阅，如 `order.*` |
| `Fanout` | 忽略 routing key，发给所有绑定 Queue | 广播配置刷新、缓存失效通知 |
| `Headers` | 根据消息 header 匹配 | 特殊组合路由，常规业务较少使用 |

Topic Exchange 中：

- `*` 匹配一个单词，例如 `order.*` 可匹配 `order.created`。
- `#` 匹配零个或多个单词，例如 `order.#` 可匹配 `order.created.email`。

练习：新增 `orders.audit.q`，同样绑定到 `orders.direct` 的 `order.created`。你会看到通知 Queue 与审计 Queue 都收到消息，而每个 Queue 内部仍是竞争消费。

## 六、理解可靠性链路

消息至少要经过下面几个阶段：

```text
Producer
  -> RabbitMQ Connection/Channel
  -> Exchange
  -> Binding
  -> Queue
  -> Consumer
  -> 业务处理与数据库
```

每一段都有独立的失败窗口：

- **publisher confirm**：Broker 告诉生产者，RabbitMQ 已接管消息。
- **publisher return**：消息到达 Exchange，但没有匹配到 Queue 时，将消息退回生产者。
- **consumer ack**：消费者告诉 Broker，这条消息已经处理完成，可以删除。

Publisher confirm 成功不等于消费者已经处理成功；consumer ack 也不解决数据库操作与 ack 之间的原子性问题。

### 6.1 开启 publisher confirm 和 return

在 `application.yml` 的 `spring.rabbitmq` 下增加：

```yaml
    publisher-confirm-type: correlated
    publisher-returns: true
    template:
      mandatory: true
```

为 `RabbitTemplate` 注册回调：

```java
package com.example.rabbitmqdemo;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.context.annotation.Configuration;

@Configuration
public class PublisherCallbacks {

    private static final Logger log =
            LoggerFactory.getLogger(PublisherCallbacks.class);

    public PublisherCallbacks(RabbitTemplate rabbitTemplate) {
        rabbitTemplate.setConfirmCallback((correlation, ack, cause) -> {
            if (ack) {
                log.info("broker confirmed message: {}", correlation);
            } else {
                log.error("broker rejected message: {}, cause={}", correlation, cause);
            }
        });

        rabbitTemplate.setReturnsCallback(returned ->
                log.error(
                        "unroutable message: exchange={}, routingKey={}, reply={}",
                        returned.getExchange(),
                        returned.getRoutingKey(),
                        returned.getReplyText()
                )
        );
    }
}
```

发送时带上业务关联 ID：

```java
import org.springframework.amqp.rabbit.connection.CorrelationData;

CorrelationData correlationData = new CorrelationData(orderId);
rabbitTemplate.convertAndSend(
        RabbitConfig.ORDER_EXCHANGE,
        RabbitConfig.ORDER_ROUTING_KEY,
        message,
        correlationData
);
```

把 routing key 临时改成不存在的值，例如 `order.unknown`，验证 ReturnsCallback 能捕获 `NO_ROUTE`。

### 6.2 手动确认消费结果

入门阶段使用 Spring 的默认 `AUTO` 模式通常足够：监听方法正常返回时由容器 ack，抛出异常时按容器策略处理。

需要精确控制时，可以使用手动 ack：

```java
import com.rabbitmq.client.Channel;
import java.io.IOException;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;

@RabbitListener(queues = RabbitConfig.ORDER_QUEUE, ackMode = "MANUAL")
public void handleManually(String payload, Message message, Channel channel)
        throws IOException {
    long tag = message.getMessageProperties().getDeliveryTag();

    try {
        processBusiness(payload);
        channel.basicAck(tag, false);
    } catch (Exception ex) {
        channel.basicNack(tag, false, false);
    }
}
```

最后一个参数 `requeue=false` 表示不把失败消息立即放回原 Queue。若配置了 Dead Letter Exchange，它会进入死信流程；否则会被丢弃。

不要对必然失败的消息无限 `requeue=true`，否则会形成高频失败循环，占用消费者和 Broker 资源。

## 七、配置死信队列

消息被 `reject`/`nack` 且不重新入队、超过 TTL、Queue 超过长度限制等情况下，可以被投递到 Dead Letter Exchange。

在 `RabbitConfig` 中增加下面的常量和死信 Bean，并用这里的新版本替换原有 `orderQueue()` 方法：

```java
public static final String ORDER_DLX = "orders.dlx";
public static final String ORDER_DEAD_QUEUE = "orders.notify.dead.q";
public static final String ORDER_DEAD_ROUTING_KEY = "order.created.dead";

@Bean
DirectExchange orderDeadLetterExchange() {
    return new DirectExchange(ORDER_DLX, true, false);
}

@Bean
Queue orderQueue() {
    return QueueBuilder.durable(ORDER_QUEUE)
            .deadLetterExchange(ORDER_DLX)
            .deadLetterRoutingKey(ORDER_DEAD_ROUTING_KEY)
            .build();
}

@Bean
Queue orderDeadQueue() {
    return QueueBuilder.durable(ORDER_DEAD_QUEUE).build();
}

@Bean
Binding orderDeadBinding() {
    return BindingBuilder.bind(orderDeadQueue())
            .to(orderDeadLetterExchange())
            .with(ORDER_DEAD_ROUTING_KEY);
}
```

> [!warning] Queue 参数不能原地冲突
> 如果 `orders.notify.q` 已经按旧参数创建，再用相同名字声明带 DLX 参数的 Queue，RabbitMQ 会报 `PRECONDITION_FAILED`。学习环境中可从管理界面删除旧 Queue，再重启应用。生产环境应通过迁移计划或 RabbitMQ Policy 修改，不能随意删 Queue。

让消费者遇到测试消息时失败并 `basicNack(..., false, false)`：

```java
private void processBusiness(String payload) {
    if (payload.contains("orderId=fail")) {
        throw new IllegalStateException("simulated failure");
    }
    System.out.println("processed: " + payload);
}
```

发送失败消息：

```bash
curl -i -X POST http://localhost:8080/orders/fail/notify
```

验收结果：`orders.notify.q` 中没有这条消息，而 `orders.notify.dead.q` 的 `Ready` 增加 1。可以在管理界面的 `Get messages` 中读取它。

生产系统中，死信 Queue 需要监控和处理流程。仅仅把消息送入死信队列，不等于问题已经解决。

## 八、幂等消费

**幂等（Idempotency）是指：针对同一个业务请求，执行一次和执行多次，最终可观察到的业务结果相同。**

“执行多次”并不一定表示代码真的只运行了一次；代码可能进入了两次，但第二次能够识别“这个业务已经做过”，因此不会重复产生副作用。

最直观的对比：

```text
幂等：   把订单状态设置为 PAID
         执行 1 次 -> PAID
         执行 3 次 -> 仍然是 PAID

不幂等： 账户余额增加 100 元
         执行 1 次 -> 增加 100 元
         执行 3 次 -> 增加 300 元
```

常见操作可以这样判断：

| 操作 | 是否天然幂等 | 原因 |
| --- | --- | --- |
| `status = 'PAID'` | 通常是 | 重复设置后最终状态相同 |
| 删除指定 ID 的临时记录 | 通常是 | 删除一次和多次，最终都不存在 |
| `balance = balance + 100` | 否 | 每执行一次都会继续增加 |
| `stock = stock - 1` | 否 | 重复执行会重复扣库存 |
| 发送短信、邮件或推送 | 否 | 每执行一次都可能产生一条新通知 |
| 创建支付、退款或转账 | 否 | 重复执行可能产生重复资金操作 |

这里的“结果相同”主要指业务状态和对外副作用相同，不要求每次调用的日志、耗时或返回文字完全一致。

**幂等是目标，去重是实现幂等的一种手段。** 常见实现方式包括：

- 为每个业务事件生成稳定且唯一的 `eventId` 或幂等键。
- 用数据库唯一约束保证同一 `eventId` 只能成功登记一次。
- 在处理记录表中保存已经完成的事件。
- 使用业务状态机，只允许合法状态迁移，例如 `PAID -> SHIPPED`，已经是 `SHIPPED` 时不再重复发货。
- 调用支付等外部服务时，把相同幂等键传给对方，让对方识别重复请求。

RabbitMQ 常见的是至少一次投递语义。下面这种时序会造成重复消费：

1. 消费者成功更新数据库。
2. 消费者发送 ack 前连接断开。
3. Broker 没收到 ack，重新投递消息。
4. 消费者再次执行同一业务操作。

因此，消费逻辑应根据业务唯一标识去重，而不是假设每条消息只来一次。常见做法包括：

- 数据库唯一约束，例如 `event_id` 唯一。
- 处理记录表，成功后保存 `event_id`。
- 业务状态机，例如订单只有从 `PAID` 才能进入 `SHIPPED`。
- Redis 去重只适用于能够接受缓存丢失或过期边界的场景。

一个简化的数据库方案：

```sql
create table consumed_event (
    event_id varchar(64) primary key,
    consumed_at timestamp not null
);
```

消费者在同一个数据库事务中：

1. 插入 `event_id`。
2. 插入冲突则说明已经处理，直接返回成功。
3. 插入成功后执行业务更新。
4. 提交事务后再让监听方法正常结束或手动 ack。

必须把“登记 `eventId`”和“更新业务数据”放在同一个事务里。否则可能出现两种错误：

- 先登记成功、业务更新失败：下次看到 `eventId` 会误以为业务已经完成。
- 业务更新成功、登记失败：下次重新投递又会重复更新业务。

本项目的 `InMemoryIdempotencyStore` 使用线程安全 `Set` 演示这个思路：第一次添加 `eventId` 返回 `true`，允许继续处理；相同 `eventId` 再次出现时返回 `false`，跳过业务并 ACK。它只适合学习，因为应用重启后记录会丢失，多个应用实例也不能共享这份内存状态。

可以把 RabbitMQ 消费端的目标概括为：

```text
RabbitMQ 允许消息再次到达
            +
Consumer 用 eventId 识别重复事件
            =
消息可能处理多次，但业务只生效一次
```

## 九、推荐练习

### 练习 1：最小链路

- 启动 RabbitMQ 和 Spring Boot。
- 发送 10 个订单通知。
- 在日志和管理界面确认消息全部消费。

### 练习 2：生产者先于消费者

- 启动一次应用以声明 Queue，然后停止应用。
- 通过管理界面向 Exchange 发布消息。
- 确认消息在 Queue 中积压。
- 重启应用，观察积压归零。

### 练习 3：竞争消费

- 设置 `concurrency = "2"`。
- 每条消息模拟处理 1 秒。
- 观察两个消费线程分担消息。

### 练习 4：发布失败

- 开启 publisher confirm 和 return。
- 使用不存在的 routing key。
- 确认 ReturnsCallback 记录 `NO_ROUTE`。

### 练习 5：死信

- 配置 DLX 和死信 Queue。
- 让 `orderId=fail` 的消息处理失败。
- 确认消息进入死信 Queue。

### 练习 6：幂等

- 给消息增加固定 `event_id`。
- 手动重复发送同一事件。
- 通过数据库唯一约束保证业务只生效一次。

## 十、常见坑

- **把发送成功当成业务成功**：`convertAndSend` 返回，不代表消息已持久化，更不代表消费完成。
- **无限重试**：永久性错误不断重新入队，会形成忙循环。应有限重试，然后进入死信队列。
- **先 ack 再处理业务**：业务失败时消息已经从 Queue 删除。
- **没有幂等**：网络抖动和消费者重启都可能带来重复消息。
- **误解广播**：多个消费者监听同一个 Queue 是分工；多个 Queue 绑定同一个 Exchange 才能各收一份。
- **随意修改 Queue 参数**：同名 Queue 的 durable、exclusive、auto-delete、DLX 等参数必须兼容，否则声明失败。
- **把 Java 对象直接当长期契约**：建议使用 JSON、Avro 或 Protobuf，并明确 schema 版本；避免依赖 Java 原生序列化。
- **只看 Queue 长度**：还要监控消息年龄、消费速率、Unacked 数量、失败率、Connection 和 Channel 数量。

## 十一、学完后的自测

如果下面的问题都能回答，就可以进入一个小型真实项目：

1. Exchange 和 Queue 分别负责什么？
2. Direct、Topic、Fanout Exchange 有什么区别？
3. 同一个 Queue 有三个消费者时，一条消息会被处理几次？
4. publisher confirm 与 consumer ack 分别确认哪一段？
5. 为什么消费者必须幂等？
6. `requeue=true` 为什么可能带来无限循环？
7. 死信队列中的消息由谁处理？
8. 数据库更新成功但 ack 丢失，会发生什么？

下一步适合做一个“订单创建 -> 异步通知”的双应用示例：一个应用只负责生产消息，另一个应用只负责消费，并加入 PostgreSQL 去重表和集成测试。

## 相关

- [[Java消息队列概览与选型]] — 消息队列产品定位与选型背景
- [[Maven-Wrapper]] — 项目构建工具与常用命令
- [RabbitMQ Spring Boot 配套代码](../../code/rabbitmq-demo/README.md)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials)
- [RabbitMQ AMQP 0-9-1 Model Explained](https://www.rabbitmq.com/tutorials/amqp-concepts)
- [RabbitMQ Exchanges](https://www.rabbitmq.com/docs/exchanges)
- [RabbitMQ Connections](https://www.rabbitmq.com/docs/connections)
- [RabbitMQ Channels](https://www.rabbitmq.com/docs/channels)
- [RabbitMQ Virtual Hosts](https://www.rabbitmq.com/docs/vhosts)
- [RabbitMQ Clustering Guide](https://www.rabbitmq.com/docs/clustering)
- [RabbitMQ Queues](https://www.rabbitmq.com/docs/queues)
- [RabbitMQ Consumer Acknowledgements and Publisher Confirms](https://www.rabbitmq.com/docs/confirms)
- [RabbitMQ Dead Letter Exchanges](https://www.rabbitmq.com/docs/dlx)
- [RabbitMQ TTL](https://www.rabbitmq.com/docs/ttl)
- [Spring：Messaging with RabbitMQ](https://spring.io/guides/gs/messaging-rabbitmq/)
- [Spring AMQP Reference](https://docs.spring.io/spring-amqp/reference/)
- [Spring Boot AMQP](https://docs.spring.io/spring-boot/reference/messaging/amqp.html)
