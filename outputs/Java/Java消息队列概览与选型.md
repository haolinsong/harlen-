---
title: Java 消息队列概览与选型
type: output
tags: [Java/消息队列, 系统设计]
aliases: [2026-09-23-Java消息队列概览与选型]
created: 2026-09-23
updated: 2026-09-24
related: []
---

# Java 消息队列概览与选型

## 一句话结论

Java 项目中最常见的是 RabbitMQ、Apache Kafka、Apache RocketMQ、Apache Pulsar 和 ActiveMQ Artemis：普通业务异步与复杂路由优先看 RabbitMQ，事件流与海量日志优先看 Kafka，订单类顺序、延时和事务消息可重点看 RocketMQ，多租户和跨地域的大规模消息平台可评估 Pulsar，已有 JMS/Jakarta EE 体系则常见 ActiveMQ Artemis。

## 消息队列解决什么问题

消息队列把生产者和消费者之间的同步调用，改成通过 Broker 传递消息，主要价值是：

- **异步**：下单完成后，把短信、积分、推荐等非核心操作放到后台处理。
- **解耦**：生产者只发送业务事件，不需要知道有多少下游系统。
- **削峰填谷**：流量高峰时先积压消息，由消费者按自身能力处理。
- **广播事件**：同一条订单事件可被库存、风控、数据分析分别消费。
- **失败恢复**：借助持久化、确认、重试和死信机制，降低短暂故障造成的数据丢失。

代价也很明确：系统会引入最终一致性、重复消费、消息积压、顺序性和运维复杂度。用了消息队列，并不等于自动获得“绝对不丢、不重、严格有序”。

## Java 常见产品

| 产品 | 更准确的定位 | 擅长场景 | Java 常用接入 | 主要注意点 |
| --- | --- | --- | --- | --- |
| **RabbitMQ** | 传统消息 Broker，核心协议包括 AMQP | 业务异步、工作队列、灵活路由、低延迟消息 | Spring AMQP、`RabbitTemplate`、`@RabbitListener`，或官方 Java Client | Exchange/Queue/Binding 模型易用；大量历史消息长期保留和反复回放不是它最典型的用法 |
| **Apache Kafka** | 分布式事件流平台、持久化分区日志 | 日志采集、埋点、CDC、事件驱动、流处理、超高吞吐 | Spring for Apache Kafka、`KafkaTemplate`、`@KafkaListener`，或官方 Java Client | 只保证分区内顺序；分区数影响并行度；业务型延时、优先级和复杂路由不是其传统强项 |
| **Apache RocketMQ** | 面向业务消息的分布式消息中间件 | 电商订单、顺序消息、延时消息、事务消息、消息过滤 | RocketMQ Java SDK；5.x 新客户端使用 gRPC 协议并要求 5.0+ 服务端及 Proxy | 4.x Remoting SDK 与 5.x gRPC SDK 存在代际差异，选型时要先确认服务端和客户端版本 |
| **Apache Pulsar** | 云原生分布式消息与流平台 | 多租户、海量 Topic、长期积压、跨地域复制、消息与流统一 | `pulsar-client`、Spring for Apache Pulsar | Broker、BookKeeper 和元数据组件分层，扩展灵活，但部署与运维认知成本较高 |
| **ActiveMQ Artemis** | Java/Jakarta Messaging 友好的通用 Broker | 传统企业 Java、JMS/Jakarta EE、应用服务器集成、嵌入式 Broker | Spring JMS、`JmsTemplate`、`@JmsListener` | 适合既有 JMS 体系；全新大规模事件平台通常会同时对比 Kafka、RocketMQ 或 Pulsar |

此外，云上还常见 AWS SQS/SNS、Azure Service Bus、Google Cloud Pub/Sub，以及阿里云、腾讯云等托管消息服务。它们可以省掉 Broker 运维，但会带来厂商 API、费用模型和可迁移性的权衡。

## 两类系统不要混为一谈

### 1. 传统消息队列 / Broker

代表：RabbitMQ、ActiveMQ Artemis，RocketMQ 也具有很强的业务队列属性。

消息通常以“交给消费者完成一次业务处理”为中心，常见能力包括确认、重试、死信、路由、延时和优先级。消费成功后，消息通常不再作为长期事件历史供任意回放。

### 2. 事件流 / 持久化日志

代表：Kafka、Pulsar。

消息作为一段可保留的事件历史存在，消费者维护自己的消费位置，因此同一批消息可以被不同消费组独立读取，也可以按 offset/cursor 重放。它更适合数据管道、事件溯源和流式计算。

RabbitMQ 也提供 Stream，Pulsar 也支持队列式订阅，因此产品边界正在交叉；选型时仍应先问清楚：业务真正需要的是“可靠地处理一个任务”，还是“持续保存并分发一条事件流”。

## JMS 到底是什么

`JMS`（现在对应 `Jakarta Messaging`）是 Java 消息 API 规范，不是消息队列产品，也不规定统一的网络协议和 Broker 存储实现。

ActiveMQ Artemis 原生适合 JMS/Jakarta Messaging 场景；RabbitMQ 可通过自己的 JMS Client 使用部分 JMS 能力。Kafka、RocketMQ、Pulsar 通常优先使用各自的原生客户端和 Spring 集成，不应为了“统一接口”强行套成 JMS。

## 怎么选

可以先按下面的业务信号筛选：

- 普通 Spring Boot 业务异步、任务队列、路由规则较多：**RabbitMQ**。
- 日志、埋点、CDC、事件总线、流处理、需要长期保留和回放：**Kafka**。
- Java 电商业务，明确需要顺序、延时、事务消息：**RocketMQ**。
- 多租户、跨地域、海量 Topic，且团队能承担更复杂的平台运维：**Pulsar**。
- 公司已有 JMS/Jakarta EE、ActiveMQ 资产或应用服务器集成：**ActiveMQ Artemis**。
- 团队不想维护集群，且可以接受云厂商绑定：优先评估**云托管服务**。

对于多数中小型 Java 业务，RabbitMQ 与 Kafka 往往是第一轮对比对象：前者更像“把任务可靠地交给别人做”，后者更像“记录发生过的事件，供多个系统持续读取”。不要单凭吞吐量排行榜选型，还要看现有基础设施、运维经验、消息积压规模、是否需要回放，以及团队能否正确处理重复消息。

## Java 开发必须掌握的可靠性问题

无论使用哪一种产品，都应重点设计以下内容：

1. **生产端确认**：发送成功是进入客户端缓冲区，还是已被 Broker 持久化？失败如何重试？
2. **消费端确认**：业务逻辑完成后再 ack/提交 offset，还是收到消息就确认？
3. **幂等消费**：至少一次投递很常见，消费者应通过业务唯一键、去重表或状态机抵抗重复消息。
4. **重试与死信**：区分瞬时故障和永久业务错误，限制重试次数并保留人工处理入口。
5. **顺序边界**：大多数系统只保证单个 Queue、MessageGroup 或 Partition 内有序；并发消费会改变全局顺序。
6. **消息积压**：监控队列深度、消费延迟、消费者存活、失败率和死信数量。
7. **数据库一致性**：数据库提交与发消息不是天然原子操作，常见方案是 Transactional Outbox、CDC，或产品支持的事务消息。
8. **消息契约**：为事件定义稳定 schema 和版本兼容策略，避免生产者升级后击穿旧消费者。

## 建议的学习顺序

1. 先理解 Producer、Consumer、Broker、Topic、Queue、消费组、ack、offset、死信和幂等。
2. 用 RabbitMQ 做一个“下单后异步发通知”的例子，练习确认、重试与死信。
3. 用 Kafka 做一个“订单事件流”的例子，练习分区键、消费组、offset 和消息回放。
4. 再根据工作环境学习 RocketMQ、Pulsar 或 ActiveMQ Artemis，不必一开始把所有产品都学一遍。

## 相关

- [Spring Boot Messaging 官方文档](https://docs.spring.io/spring-boot/reference/messaging/index.html)
- [RabbitMQ Java Client 与教程](https://www.rabbitmq.com/client-libraries/java-api-guide)
- [Apache Kafka Introduction](https://kafka.apache.org/intro/)
- [Apache RocketMQ Java Client SDK](https://rocketmq.apache.org/docs/sdk/02java/)
- [Apache Pulsar Java Client](https://pulsar.apache.org/docs/client-libraries/java/)
- [Apache ActiveMQ Artemis 文档](https://activemq.apache.org/components/artemis/documentation/latest/)
- [Jakarta Messaging 规范](https://jakarta.ee/specifications/messaging/)
