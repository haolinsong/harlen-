# 实验 1：Kafka Hello World

这是第一个实验。目标不是背 API，而是亲眼看到一条消息如何经过 Producer、Partition、Consumer，最后变成 Consumer Group 的 Committed Offset。

## 1. 学习目标

完成后，你应该能解释：

- `bootstrap.servers` 为什么只是集群入口，而不是消息固定发送的节点。
- Serializer、`ProducerRecord`、key、Partition 和 Offset 的关系。
- `send()` 的异步 Callback 为什么必须检查异常。
- `subscribe()`、`poll()` 和 Consumer Group 的关系。
- 为什么先处理再 `commitSync()` 属于 At Least Once，为什么仍要业务幂等。

## 2. 架构与消息生命周期

本实验运行一个 Java Producer 和一个手动提交 Offset 的 Java Consumer：

```text
ProducerApp
  | 1. StringSerializer 把 key/value 转成 byte[]
  | 2. 默认分区器根据 key 选择 Partition
  v
learning.hello（P0、P1、P2）
  | 3. Broker 为消息分配 Partition 内 Offset
  | 4. hello-java-group 分配 Partition 给 Consumer
  v
ConsumerApp
  | 5. poll() 拉取一批消息
  | 6. 打印模拟业务处理
  ` 7. commitSync() 提交下一条待消费 Offset
```

相同 key 在 Partition 数不变时进入同一 Partition。Consumer 在一批消息处理完后调用 `commitSync()`；如果处理完成后、提交成功前崩溃，恢复时可能重复处理，但不会因为提前提交而直接漏掉尚未处理的消息。

## 3. 文件与推荐阅读顺序

| 顺序 | 文件 | 作用 | 阅读重点 |
| ---: | --- | --- | --- |
| 1 | `pom.xml` | 声明 Kafka Client、SLF4J、JUnit 和运行插件 | 子模块为什么不写 Kafka 版本？ |
| 2 | `KafkaSettings.java` | 集中创建 Producer/Consumer 配置 | 可靠发送和手动提交分别由哪些参数控制？ |
| 3 | `KafkaSettingsTest.java` | 不启动 Broker 就检查关键配置 | 单元测试能覆盖什么，不能覆盖什么？ |
| 4 | `TopicAdmin.java` | 用 Admin Client 幂等创建 Topic | 为什么并发创建时要重新检查 Topic？ |
| 5 | `ProducerApp.java` | 构造并异步发送字符串消息 | key、Callback、`flush()` 的作用是什么？ |
| 6 | `ConsumerApp.java` | 拉取、处理并提交消息 | `poll -> process -> commit` 为什么不能颠倒？ |

建议先完整读一遍 `KafkaSettings`，再把 Producer 和 Consumer 并排打开，对照消息的写入端与读取端。

## 4. 代码开发顺序

如果你自己从空目录实现这个实验，可以按以下顺序：

1. 在 `pom.xml` 引入 `kafka-clients`，先让项目能够编译。
2. 在 `KafkaSettings` 定义 Topic、Broker 地址和序列化配置。
3. 加入可靠 Producer 参数：`acks=all` 和 `enable.idempotence=true`。
4. 加入 Consumer 的 `group.id`、反序列化器，并关闭自动提交。
5. 用 `TopicAdmin` 创建 3 Partition Topic，避免依赖 Broker 自动创建。
6. 写 `ProducerApp`：生成 key/value、构造 `ProducerRecord`、异步发送并检查 Callback。
7. 写 `ConsumerApp`：订阅 Topic、循环 `poll()`、处理整批消息后 `commitSync()`。
8. 写 `KafkaSettingsTest`，锁定最重要的可靠性配置。
9. 启动 Kafka 做端到端验证，观察 Partition、Offset 和 Lag。

## 5. 运行前准备

以下命令从项目根目录 `code/kafka-learning-labs` 执行：

```bash
docker compose up -d
./scripts/create-topics.sh
./mvnw -pl 01-hello-world-java test
```

先运行测试可以快速确认 Java、Maven 和源码都正常；测试本身不需要 Kafka。

## 6. 运行实验

打开两个终端。先启动 Consumer，它会等待消息。

终端 1：

```bash
./mvnw -pl 01-hello-world-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.hello.ConsumerApp \
  -Dexec.args=10
```

再启动 Producer，发送 10 条消息。

终端 2：

```bash
./mvnw -pl 01-hello-world-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.hello.ProducerApp \
  -Dexec.args=10
```

参数 `10` 分别表示 Producer 要发送的条数，以及 Consumer 本次希望处理的消息数。

## 7. 怎样读懂输出

Producer 输出类似：

```text
sent: key=user-1 partition=0 offset=12
```

- `key=user-1`：应用指定的消息 key。
- `partition=0`：默认分区器选择的 Partition。
- `offset=12`：Broker 分配的位置，只在 P0 内有意义。

Consumer 输出类似：

```text
received: key=user-1 value=hello-kafka-1 partition=0 offset=12
```

它应与 Producer 输出的 key、Partition 和 Offset 对应。不要要求控制台行的整体顺序完全一致：Producer 异步发送到多个 Partition，不同 Partition 之间没有全局顺序。

## 8. 验证 Consumer Group 与 Offset

查看 Group 状态：

```bash
docker compose exec kafka /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group hello-java-group
```

正常完成后 `LAG` 应趋近 0。`CURRENT-OFFSET` 表示该 Group 在每个 Partition 下一条要读的位置。

再同时启动两个 Consumer 并发送更多消息，可以观察同一 Group 内的分工：

```text
Consumer A <- P0、P2
Consumer B <- P1
```

具体分配可能不同，但一个 Partition 同时不会分给同一 Group 的两个 Consumer。

## 9. 新手练习

1. 把消息数改为 30，记录三个 key 分别进入哪个 Partition。
2. 把 `sequence % 3` 改为 `% 5`，观察 key 种类增加后 Partition 如何分布。
3. 启动 4 个 Consumer。Topic 只有 3 个 Partition，观察是否有一个 Consumer 空闲。
4. 把其中一个 Consumer 的 `group.id` 改成 `hello-second-group`，观察它是否也能独立读取消息。
5. 在 `commitSync()` 前加入一个受控异常，思考重启后为什么可能再次读取。

每次只改一处，先写下预测，再运行验证。

## 10. 这个实验故意省略了什么

- 单 Broker 和副本因子 1 没有 Broker 容灾能力。
- 字符串 value 没有 Schema 演进能力。
- 打印不是需要幂等的真实业务写入。
- 没有 Retry Topic、DLT、安全认证、监控与告警。

这些不是“以后把参数补齐”就自然完成的功能，而是后续章节需要单独设计的生产能力。
