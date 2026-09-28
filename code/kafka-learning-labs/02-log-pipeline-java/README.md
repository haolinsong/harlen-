# 实验 2：Kafka 日志管道

这个实验在 Hello World 的基础上，把字符串消息升级为结构化 JSON 事件，并加入 Batch、压缩、状态聚合和坏消息路径。

## 1. 学习目标

完成后，你应该能解释：

- 为什么应先定义消息契约，再编写 Producer 和 Consumer。
- Java `record`、Jackson 和 Kafka String Serializer 分别负责哪一层。
- `linger.ms`、`batch.size` 与 `compression.type` 如何配合。
- 为什么 `poll()` 返回的是批次，手动提交需要考虑整批是否成功。
- 为什么固定的非法 JSON 不是“多重试几次”就能解决。

## 2. 架构与消息生命周期

```text
LogEvent（Java record）
  | LogEventCodec.encode()
  v
JSON String
  | StringSerializer + service key
  | Producer Batch + Zstd
  v
learning.logs（3 Partitions）
  | log-analytics-group poll()
  v
JSON String
  | LogEventCodec.decode()
  v
LogEvent -> 按 service 累计 ERROR -> 整批成功后 commitSync()
```

本实验演示结构化 JSON、异步发送回调、压缩与批处理、手动 Offset，以及坏消息如何阻塞当前批次。示例中的本地重试只用于观察行为；生产中应区分瞬时故障与永久数据错误，后者通常进入 Dead Letter Topic 并触发告警。

## 3. 文件与推荐阅读顺序

| 顺序 | 文件 | 作用 | 阅读重点 |
| ---: | --- | --- | --- |
| 1 | `pom.xml` | 在 Kafka Client 之外增加 Jackson | 为什么 JSON 库属于消息契约层？ |
| 2 | `LogEvent.java` | 定义不可变结构化事件 | 每个字段由谁生成、由谁消费？ |
| 3 | `LogEventCodec.java` | Java 对象与 JSON 的唯一转换入口 | 为什么不在 Producer/Consumer 中各写一次？ |
| 4 | `LogEventCodecTest.java` | 验证往返转换与非法 JSON | 为什么契约测试不需要 Kafka？ |
| 5 | `LogProducer.java` | 生成事件，批量压缩并异步发送 | service key、Batch 和 Callback 如何配合？ |
| 6 | `LogConsumer.java` | 解码、统计、失败分类、提交 | 一条坏消息为何使整批不提交？ |

这里特意把测试放在 Producer 之前阅读：先确认“消息可以正确编码和还原”，再关心它如何通过 Kafka 运输。

## 4. 代码开发顺序

从零实现时，建议按以下顺序：

1. 定义 `LogEvent` 字段，先明确消息的业务含义。
2. 编写 `LogEventCodec`，把 JSON 处理集中到一个位置。
3. 先写 `LogEventCodecTest`，验证对象到 JSON 再回来的 Round Trip。
4. 编写 Producer 基础配置，确认可靠性参数后再加入 Batch 和压缩。
5. 使用 service 作为 key，构造 `ProducerRecord<String, String>`。
6. 在 Callback 中处理最终成功与失败，退出前 `flush()`。
7. 编写 Consumer 配置，关闭自动提交并限制一次 Poll 的最大记录数。
8. 实现 `poll -> decode -> aggregate -> commit` 主循环。
9. 明确 Poison Record 分支：本实验不提交，生产设计应进入 DLT 并告警。
10. 运行端到端实验，通过 Group CLI 检查 Lag 是否归零。

## 5. 运行前准备

以下命令从项目根目录 `code/kafka-learning-labs` 执行：

```bash
docker compose up -d
./scripts/create-topics.sh
./mvnw -pl 02-log-pipeline-java test
```

## 6. 运行实验

先启动 Consumer：

```bash
# 终端 1
./mvnw -pl 02-log-pipeline-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.logs.LogConsumer
```

再启动 Producer：

```bash
# 终端 2
./mvnw -pl 02-log-pipeline-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.logs.LogProducer \
  -Dexec.args=20
```

Producer 发送完 20 条后退出；Consumer 会持续等待后续日志，需要按 `Ctrl+C` 停止。

## 7. 怎样读懂输出

Producer 输出：

```text
event <uuid> -> partition=1 offset=8
```

所有事件的 service 都是 `checkout-service`，因此在 Partition 数不变时，它们应进入同一 Partition。即便只有一个 Partition 活跃，Producer 仍可以在该 Partition 内把多条记录组成 Batch。

Consumer 输出：

```text
processed event=<uuid> level=ERROR errors=2
```

`errors=2` 表示当前进程已为该 service 处理两条 ERROR。它只是内存状态，重启后清零；Kafka 中的原始日志和 Consumer Group Offset 不因此消失。

## 8. 验证 Offset 与 Lag

Consumer 会打印事件与累计 ERROR 数。查看 Consumer Group 的已提交 Offset 和 Lag：

```bash
docker compose exec kafka /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group log-analytics-group
```

正常处理后，活跃 Partition 的 `CURRENT-OFFSET` 应追上 `LOG-END-OFFSET`，`LAG` 变为 0。

## 9. Poison Record 实验

先保持 `LogConsumer` 运行，再使用 Kafka 控制台 Producer 写入一条不是 JSON 的消息：

```bash
docker compose exec -T kafka /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic learning.logs \
  --property parse.key=true \
  --property key.separator=:
```

然后输入并结束：

```text
checkout-service:not-json
```

你会看到 Consumer 打印 `poison record`，本批不执行 `commitSync()`。再次查看 Group Lag，并思考：

- 为什么相同非法 JSON 重试仍会失败？
- 如果直接提交，会不会静默丢掉坏消息？
- 如果永不提交，会不会阻塞后续正常消息？
- DLT 应保存哪些原始字段，怎样让人工能够追查？

实验结束后若希望从全新状态开始，可在确认无需保留数据后执行 `docker compose down -v`。

## 10. 新手练习

1. 让 Producer 在 `checkout-service` 与 `payment-service` 之间轮换，观察两个 key 的 Partition。
2. 把每第 7 条 ERROR 改成每第 3 条，预测最终 `errors`。
3. 分别发送 1、20、1000 条消息，对比异步输出和运行耗时；不要仅凭一次结果下性能结论。
4. 暂时把压缩从 `zstd` 改成 `none`，解释为什么少量本地消息可能看不出明显差异。
5. 为 `LogEventCodecTest` 增加缺少字段或字段类型错误的 JSON 用例。
6. 设计一个 `learning.logs.dlt` 事件结构，至少包含原 Topic、Partition、Offset、原始 value、错误原因和失败时间。

## 11. 这个实验故意省略了什么

- 普通 JSON 没有 Schema Registry 和兼容性规则。
- 内存 Map 不是持久状态，也不是 Kafka Streams State Store。
- 立即重试没有退避，对永久数据错误没有帮助。
- 示例没有真的发送 DLT，只展示了需要处理的边界。
- At Least Once 下，聚合更新仍需要可恢复、可幂等的状态设计。

不要把“打印后提交”直接替换成“写数据库后提交”就当作生产完成；数据库更新、幂等记录与 Offset 之间还需要明确的一致性方案。
