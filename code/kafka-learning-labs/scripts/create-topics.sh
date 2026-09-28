#!/usr/bin/env bash

# -e：任一命令失败就退出；-u：未定义变量报错；pipefail：管道中任一环节失败都算失败。
set -euo pipefail

# 通过 Kafka CLI 幂等创建 Topic。参数 1 是 Topic 名，参数 2 是 Partition 数。
create_topic() {
  local topic="$1"
  local partitions="$2"

  # 命令在 Kafka 容器内执行，因此容器里的 localhost:9092 指向 Kafka 自己。
  # --if-not-exists 使脚本可以重复运行，不会因 Topic 已存在而失败。
  docker compose exec kafka /opt/kafka/bin/kafka-topics.sh \
    --bootstrap-server localhost:9092 \
    --create \
    --if-not-exists \
    --topic "${topic}" \
    --partitions "${partitions}" \
    --replication-factor 1
}

# 两个实验使用不同 Topic，避免消息契约和 Consumer Group 相互干扰。
create_topic "learning.hello" 3
create_topic "learning.logs" 3

echo "Kafka learning topics are ready."
