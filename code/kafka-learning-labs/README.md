# Kafka Learning Labs

这是与 `outputs/系统框架/Apache Kafka学习指南.md` 配套的入门项目。它不追求业务功能复杂度，而是把 Kafka 的一条消息从“Java 对象”到“Broker 日志”，再到“Consumer 处理并提交 Offset”的过程拆开给你看。

项目统一使用 Apache Kafka 4.3.1、KRaft 和 Java 21。目前只包含两个循序渐进的实验：先跑通字符串消息，再把消息升级为结构化 JSON 日志。

## 1. 学完后应该能回答什么

完成两个实验后，你应该能够解释：

1. Producer 为什么需要 Serializer，Consumer 为什么需要 Deserializer。
2. 消息 key 如何影响 Partition，相同 key 的顺序保证有什么边界。
3. `send()` 为什么是异步的，Callback、`flush()` 和 `close()` 分别做什么。
4. Consumer Group 如何分配 Partition，为什么 Consumer 多于 Partition 时会空闲。
5. `poll()`、业务处理、`commitSync()` 为什么必须按这个顺序出现。
6. At Least Once 为什么仍可能重复，以及业务幂等为什么不能省略。
7. Batch、`linger.ms` 和压缩如何共同提高吞吐。
8. Poison Record 为什么会阻塞进度，生产系统为什么需要 Retry/DLT。

## 2. 总体结构

```text
kafka-learning-labs/
├── pom.xml                         # Maven 聚合项目：统一 Java、依赖和插件版本
├── mvnw / mvnw.cmd                 # Maven Wrapper：无需预装 Maven
├── compose.yaml                    # Kafka 4.3.1 单节点 KRaft 学习环境
├── scripts/
│   └── create-topics.sh            # 幂等创建两个实验 Topic
├── 01-hello-world-java/
│   ├── README.md                   # 实验 1 学习说明
│   ├── pom.xml                     # Kafka Client、日志和测试依赖
│   └── src/                        # 配置、Admin、Producer、Consumer、测试
└── 02-log-pipeline-java/
    ├── README.md                   # 实验 2 学习说明
    ├── pom.xml                     # 增加 Jackson JSON 依赖
    └── src/                        # 事件、编解码、Producer、Consumer、测试
```

运行时的数据链路是：

```text
Java 对象
  -> Serializer / JSON 编码
  -> ProducerRecord(key, value)
  -> Producer Batch
  -> Topic Partition Leader
  -> Consumer poll()
  -> Deserializer / JSON 解码
  -> 业务处理
  -> commitSync() 提交下一条待消费 Offset
```

## 3. 项目是怎样一步步开发出来的

这也是你以后从零开发 Kafka 小项目时可以复用的顺序。

### 第一步：确定版本和项目骨架

根 `pom.xml` 使用 `packaging=pom`，负责聚合两个子模块，并统一规定 Java 21、Kafka Client 4.3.1、Jackson 和 JUnit 的版本。子模块只声明自己需要哪些依赖，不重复写版本。

这样做的目的不是“文件越多越好”，而是避免两个实验使用不同 Kafka Client 或 Java 版本。

### 第二步：准备可重复的 Kafka 环境

`compose.yaml` 固定官方 `apache/kafka:4.3.1` 镜像，启动一个同时承担 Broker 和 Controller 的 KRaft 节点：

```text
宿主机 Java 客户端 --localhost:9092--> Kafka Broker + KRaft Controller
```

单节点环境把内部 Topic 的副本因子设为 1，目的是让实验能在一台电脑运行；它没有 Broker 容灾能力。

### 第三步：先定义 Topic

`scripts/create-topics.sh` 创建：

| Topic | Partition | 用途 |
| --- | ---: | --- |
| `learning.hello` | 3 | 实验 1 的字符串消息 |
| `learning.logs` | 3 | 实验 2 的 JSON 日志 |

脚本使用 `--if-not-exists`，因此可以重复执行。把两个实验拆成不同 Topic，是为了让消息契约和 Consumer Group 互不干扰。

### 第四步：先完成最小闭环

实验 1 的开发顺序是：

```text
KafkaSettings
  -> TopicAdmin
  -> ProducerApp
  -> ConsumerApp
  -> KafkaSettingsTest
```

先集中配置，再保证 Topic 存在，然后发送和消费字符串消息。Consumer 关闭自动提交，在打印模拟的业务处理完成后调用 `commitSync()`，形成最容易理解的 At Least Once 基线。

### 第五步：把字符串升级为业务事件

实验 2 的开发顺序是：

```text
LogEvent
  -> LogEventCodec
  -> LogEventCodecTest
  -> LogProducer
  -> LogConsumer
```

先定义事件契约，再实现和测试 JSON 编解码。消息格式稳定后，Producer 才负责发送，Consumer 才负责解析、聚合和提交 Offset。这个顺序能更早发现契约问题。

### 第六步：增加吞吐和失败场景

实验 2 再增加 `linger.ms`、`batch.size` 和 Zstd 压缩，并演示非法 JSON 如何导致整批不提交。它故意不自动跳过坏消息，让你看到“可靠消费”不仅是提交一个 Offset，还要设计错误分类、Retry、DLT 和告警。

### 第七步：分别验证纯逻辑与真实链路

- 单元测试不启动 Broker，快速检查关键配置和 JSON 契约。
- Compose 联调验证真实的 Topic、Partition、Offset、Consumer Group 和 Lag。
- 两类测试不能互相替代：单元测试快，端到端联调更接近真实运行。

## 4. 新手推荐阅读顺序

不要一上来同时打开所有文件。按下面顺序读，每一步只回答一个问题。

| 顺序 | 文件 | 阅读时关注的问题 |
| ---: | --- | --- |
| 1 | 根 `README.md` | 两个实验解决什么问题，整体消息链路是什么？ |
| 2 | 根 `pom.xml` | 父 POM、modules、dependencyManagement 各自做什么？ |
| 3 | `compose.yaml` | Broker、Controller、Listener 和数据卷如何组成本地环境？ |
| 4 | `scripts/create-topics.sh` | Topic 如何幂等创建，为什么有 3 个 Partition？ |
| 5 | `01-hello-world-java/README.md` | 第一个闭环如何运行和验证？ |
| 6 | `KafkaSettings.java` | Producer/Consumer 最少需要哪些配置？ |
| 7 | `KafkaSettingsTest.java` | 哪些配置可以不启动 Kafka 就测试？ |
| 8 | `TopicAdmin.java` | Java 如何通过 Admin Client 创建 Topic？ |
| 9 | `ProducerApp.java` | Record 如何构造，key 如何映射 Partition，异步结果在哪里？ |
| 10 | `ConsumerApp.java` | `subscribe -> poll -> process -> commit` 如何连起来？ |
| 11 | `02-log-pipeline-java/README.md` | 结构化消息比 Hello World 多了什么？ |
| 12 | `LogEvent.java` | 消息契约包含哪些字段？ |
| 13 | `LogEventCodec.java` 与测试 | Java 对象如何可靠地变成 JSON 再还原？ |
| 14 | `LogProducer.java` | Batch、linger 和压缩配置放在哪里？ |
| 15 | `LogConsumer.java` | 聚合、整批提交和 Poison Record 如何处理？ |

推荐学习动作：先读注释并预测运行结果，再启动程序核对；不要只复制命令。

## 5. 环境要求与检查

- Docker Desktop 或兼容的 Docker Engine，支持 `docker compose`
- Java 21
- Maven Wrapper 会自动下载 Maven 3.9.11，无需全局安装 Maven

先检查版本：

```bash
docker --version
docker compose version
java -version
./mvnw -version
```

`./mvnw -version` 显示的 Java 应为 21。若不是，先修正当前终端的 `JAVA_HOME`。

## 6. 从零运行

以下命令都从本目录 `code/kafka-learning-labs` 执行。

### 6.1 启动 Kafka

```bash
docker compose up -d
docker compose ps
```

`docker compose ps` 中 Kafka 应最终显示为 `healthy`。

### 6.2 创建并查看 Topic

```bash
./scripts/create-topics.sh

docker compose exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --list

docker compose exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe --topic learning.hello
```

你应该看到 `learning.hello` 和 `learning.logs`，并看到 `learning.hello` 有 3 个 Partition。

### 6.3 运行实验 1

先开 Consumer，再开 Producer，方便直接看到新消息到达：

```bash
# 终端 1
./mvnw -pl 01-hello-world-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.hello.ConsumerApp \
  -Dexec.args=10
```

```bash
# 终端 2
./mvnw -pl 01-hello-world-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.hello.ProducerApp \
  -Dexec.args=10
```

详细观察点见 `01-hello-world-java/README.md`。

### 6.4 运行实验 2

```bash
# 终端 1
./mvnw -pl 02-log-pipeline-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.logs.LogConsumer
```

```bash
# 终端 2
./mvnw -pl 02-log-pipeline-java exec:java \
  -Dexec.mainClass=io.harlan.kafka.logs.LogProducer \
  -Dexec.args=20
```

Consumer 会持续运行；观察完成后按 `Ctrl+C` 停止。详细说明见 `02-log-pipeline-java/README.md`。

### 6.5 运行全部单元测试

```bash
./mvnw test
```

也可以只测试一个模块：

```bash
./mvnw -pl 01-hello-world-java test
./mvnw -pl 02-log-pipeline-java test
```

## 7. 如何观察 Kafka，而不只看 Java 输出

查看 Consumer Group 的提交位置和 Lag：

```bash
docker compose exec kafka /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group hello-java-group

docker compose exec kafka /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group log-analytics-group
```

重点看：

- `CURRENT-OFFSET`：Group 已提交的下一条待消费位置。
- `LOG-END-OFFSET`：Partition 当前日志末端位置。
- `LAG`：两者差值，即尚未处理的消息数量。
- `CONSUMER-ID`：当前由哪个 Consumer 负责该 Partition。

## 8. 建议的动手练习

按难度从低到高进行，每次只改一个变量并记录观察结果：

1. 把 Producer 消息数从 10 改成 30，观察三个 key 的 Partition 和 Offset。
2. 同时启动两个实验 1 Consumer，观察三个 Partition 如何在同一 Group 内分配。
3. 把第二个 Consumer 的 `group.id` 改成新值，观察两个 Group 是否都能读取整条流。
4. 停止 Consumer，单独发送消息，再重启 Consumer，观察 Committed Offset 和 Lag。
5. 修改 `LogProducer` 生成两个 service，观察 key 如何影响 Partition。
6. 用控制台 Producer 向 `learning.logs` 写入非法 JSON，观察 Poison Record 和 Lag。
7. 思考如何把坏消息转发到 `learning.logs.dlt`，但先不要直接跳过而丢失证据。

## 9. 常见问题

### 连接 `localhost:9092` 失败

先运行 `docker compose ps` 和 `docker compose logs kafka`。如果 Broker 已启动但客户端仍超时，重点检查 9092 端口占用和 `advertised.listeners`。

### Consumer 没有读到旧消息

`auto.offset.reset=earliest` 只在当前 Group 没有有效 Committed Offset 时生效。已有进度时，Consumer 会从已提交位置继续。学习阶段可换一个新的 `group.id`，或明确使用 Consumer Group CLI 重置 Offset。

### Maven 使用了错误的 Java

`java -version` 与 `./mvnw -version` 都应指向 Java 21。IDE 的项目 SDK 和终端 `JAVA_HOME` 是两套配置，需要分别检查。

### 相同 key 没有落入预期编号的 Partition

应该观察“相同 key 是否稳定进入同一 Partition”，不要预先猜它一定是 P0、P1 或 P2。默认分区器根据序列化后的 key 计算映射；增加 Partition 后映射还可能改变。

## 10. 停止与重置

停止容器但保留 Topic、消息和 Offset：

```bash
docker compose down
```

删除容器和命名卷，从全新集群重新实验：

```bash
docker compose down -v
```

`down -v` 会删除本项目的 Kafka 实验数据。执行前确认没有需要保留的观察结果。

## 11. 教学边界

本项目有意保持小而完整，不包含生产所需的 TLS、SASL、ACL、外部数据库、Schema Registry、监控和跨机房容灾。单 Broker、RF=1、PLAINTEXT、内存聚合以及本地立即重试都只是教学简化，不能直接作为生产模板。

Python、监控和微服务等后续项目已记录到主学习指南，本阶段暂不生成。
