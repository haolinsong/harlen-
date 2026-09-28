---
title: Kafka KRaft 开发环境
type: howto
tags: [系统框架/Kafka, Docker]
aliases: [Kafka本地环境, Kafka Docker环境]
sources: []
created: 2026-09-28
updated: 2026-09-28
verified: ""
env: "macOS/Linux · Docker Compose · Apache Kafka 4.3.1 · KRaft"
domain_volatility: high
confidence: medium
---

# Kafka KRaft 开发环境

这份操作使用官方 Kafka 4.3.1 容器，在本机启动一个 KRaft Combined Mode 节点，并验证 Topic、Producer、Consumer 和 Consumer Group。

## 适用环境

- Docker Desktop 或支持 Compose V2 的 Docker Engine。
- 项目目录：`code/kafka-learning-labs/`。
- 仅用于本地学习，不用于生产。

## 目标

启动 Broker，创建 `learning.hello` 与 `learning.logs`，运行两个 Java 入门项目，并能查看 Partition、Offset 与 Lag。

## 步骤

```bash
cd code/kafka-learning-labs
docker compose up -d
docker compose ps
./scripts/create-topics.sh
```

列出并描述 Topic：

```bash
docker compose exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --list

docker compose exec kafka /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe --topic learning.hello
```

运行 Java 测试：

```bash
./mvnw test
```

具体 Producer/Consumer 命令见两个实验各自的 `README.md`。

## 验证

- `docker compose ps` 中 Kafka 为 Healthy。
- Topic 列表包含 `learning.hello` 与 `learning.logs`，每个有 3 个 Partition。
- 项目 1 能发送并消费指定数量消息。
- 项目 2 的 `log-analytics-group` 最终 Lag 为 0。

```bash
docker compose exec kafka /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group log-analytics-group
```

## 已知坑

- 客户端连上 Bootstrap 后仍超时，优先检查 `advertised.listeners` 是否从客户端网络可达。
- 本地已经有服务占用 9092 时，修改端口映射后也要同步调整对外 Advertised Listener。
- `docker compose down` 保留数据卷；完全重置实验需 `docker compose down -v`。
- 该环境 RF=1、Min ISR=1 且无安全配置，不能验证 Broker 故障或复制可靠性。
- `kafka-storage.sh format` 只用于新数据目录，不能把重复格式化当作生产修复手段。
- 当前环境没有 `docker` 命令，Compose 启动与 Broker 联调尚未实际验证；Java 代码已完成从零编译和单元测试。

## 相关

- [[Apache Kafka]] — 平台概览
- [[Kafka核心架构]] — 命令背后的对象关系
- [[Kafka可靠性与交付语义]] — 单节点实验不能验证的生产边界
- [[Apache Kafka学习指南]] — 当前学习顺序与两个项目
