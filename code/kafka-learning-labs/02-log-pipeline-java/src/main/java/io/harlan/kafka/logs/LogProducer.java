package io.harlan.kafka.logs;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;

import java.time.Instant;
import java.util.Properties;
import java.util.UUID;

/**
 * 实验 2 的日志生产者：构造 {@link LogEvent}，编码成 JSON，再异步发送到 Kafka。
 *
 * <p>这个类在实验 1 的基础上增加 Batch、linger 和 Zstd 压缩配置，用于说明 Kafka
 * 的吞吐来自“批量 + 压缩 + 异步发送”的组合，而不是逐条同步网络请求。</p>
 */
public final class LogProducer {
    /** 结构化日志实验使用的 Topic。 */
    static final String TOPIC = "learning.logs";

    private LogProducer() {
    }

    public static void main(String[] args) throws Exception {
        // 默认生成 20 条日志；可通过 -Dexec.args=100 等方式改变数量。
        int count = args.length == 0 ? 20 : Integer.parseInt(args[0]);

        // 环境变量便于把同一程序连接到不同环境；本机实验使用默认地址。
        String bootstrapServers = System.getenv().getOrDefault("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092");

        Properties properties = new Properties();
        properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);

        // key 与 value 最终都以 String 形式交给 Serializer 转换为 byte[]。
        properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // 可靠性基线：等待 ISR 条件满足，并避免客户端重试造成 Kafka 内重复记录。
        properties.put(ProducerConfig.ACKS_CONFIG, "all");
        properties.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);

        // 最多等待 20 ms 收集同一 Partition 的更多记录，形成更大的 Batch。
        properties.put(ProducerConfig.LINGER_MS_CONFIG, 20);

        // 32 KiB 是每个 Partition Batch 的目标上限，不是单条消息大小限制。
        properties.put(ProducerConfig.BATCH_SIZE_CONFIG, 32 * 1024);

        // Kafka 对整个 Batch 压缩。Zstd 压缩率通常较好，但具体选择必须结合 CPU 与延迟压测。
        properties.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "zstd");

        // Producer 应复用；try-with-resources 确保退出时等待发送并释放网络资源。
        try (KafkaProducer<String, String> producer = new KafkaProducer<>(properties)) {
            for (int sequence = 1; sequence <= count; sequence++) {
                // 每第 7 条生成 ERROR，其余为 INFO，便于 Consumer 展示状态聚合。
                String level = sequence % 7 == 0 ? "ERROR" : "INFO";

                // UUID 是稳定的事件标识；时间戳记录事件发生时间，而不是 Kafka 写入时间。
                LogEvent event = new LogEvent(
                        UUID.randomUUID().toString(),
                        "checkout-service",
                        level,
                        "request completed, sequence=" + sequence,
                        Instant.now().toEpochMilli()
                );

                // service 作为 key，使同一服务的日志在 Partition 数不变时进入同一 Partition，
                // 从而保留该服务内的写入顺序；Kafka 不保证跨 Partition 的全局顺序。
                ProducerRecord<String, String> record =
                        new ProducerRecord<>(TOPIC, event.service(), LogEventCodec.encode(event));

                // send() 异步返回；回调才代表 Broker 最终确认成功或发送失败。
                // event 是本轮循环创建后不再修改的变量，可以安全地在 Lambda 中读取。
                producer.send(record, (metadata, exception) -> {
                    if (exception != null) {
                        System.err.printf("event %s failed: %s%n", event.eventId(), exception.getMessage());
                    } else {
                        System.out.printf("event %s -> partition=%d offset=%d%n",
                                event.eventId(), metadata.partition(), metadata.offset());
                    }
                });
            }

            // 等待所有异步发送完成，确保命令行程序不会在回调执行前结束。
            producer.flush();
        }
    }
}
