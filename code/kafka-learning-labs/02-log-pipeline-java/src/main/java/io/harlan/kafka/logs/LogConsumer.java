package io.harlan.kafka.logs;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;

import java.time.Duration;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * 实验 2 的日志消费者：批量拉取 JSON，解码后按服务统计 ERROR 数，并在整批成功后提交 Offset。
 *
 * <p>这个示例故意把“坏消息阻塞进度”的问题保留下来：只要本批有一条无法解析，整批就不提交。
 * 下一次启动时会从旧 Committed Offset 再读，因此真实系统需要 Retry Topic、Dead Letter Topic、
 * 告警和人工补偿，不能只无限重试同一条坏消息。</p>
 */
public final class LogConsumer {
    private LogConsumer() {
    }

    public static void main(String[] args) {
        // 先生成配置，再创建 Consumer；KafkaConsumer 本身不是线程安全的。
        Properties properties = consumerProperties();

        // key=service，value=已处理 ERROR 总数。这里只保存在内存中，重启后会清零。
        // 使用 ConcurrentHashMap 是为了演示线程安全聚合容器；当前代码仍是单线程消费。
        Map<String, Long> errorCountByService = new ConcurrentHashMap<>();
        AtomicBoolean running = new AtomicBoolean(true);

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(properties)) {
            // 首次 poll 时会加入 log-analytics-group，并由协调器分配 Partition。
            consumer.subscribe(List.of(LogProducer.TOPIC));

            // 这里最多等待 poll 的 1 秒超时后退出，没有跨线程调用 consumer.close()。
            Runtime.getRuntime().addShutdownHook(new Thread(() -> running.set(false)));

            while (running.get()) {
                // 一次 poll 最多返回 max.poll.records 配置的记录数，本实验设置为 100。
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));

                // 只有整批都成功，才允许提交这批记录之后的 Offset。
                boolean batchSucceeded = true;

                for (ConsumerRecord<String, String> record : records) {
                    try {
                        // 将 Kafka value 的 JSON 转回 LogEvent；本地最多尝试 3 次。
                        LogEvent event = decodeWithLocalRetry(record.value(), 3);

                        // merge 在 key 不存在时写入 1，存在时执行 Long::sum 累加。
                        if ("ERROR".equals(event.level())) {
                            errorCountByService.merge(event.service(), 1L, Long::sum);
                        }
                        System.out.printf("processed event=%s level=%s errors=%d%n",
                                event.eventId(), event.level(), errorCountByService.getOrDefault(event.service(), 0L));
                    } catch (Exception exception) {
                        // 相同 JSON 连续解析失败通常是不可重试的坏消息，而不是瞬时网络故障。
                        // 本实验停止处理当前批次且不提交；生产中通常应转发 DLT 并告警。
                        batchSucceeded = false;
                        System.err.printf("poison record partition=%d offset=%d reason=%s%n",
                                record.partition(), record.offset(), exception.getMessage());
                        break;
                    }
                }

                if (!records.isEmpty() && batchSucceeded) {
                    // commitSync() 提交 Consumer 当前 position，也就是各 Partition 下一条待读位置。
                    // 若处理成功后、提交成功前崩溃，该批会再次读取，所以业务聚合仍应设计幂等。
                    consumer.commitSync();
                }
            }
        }
    }

    /**
     * 在当前进程内重复尝试 JSON 解码。
     *
     * <p>该方法只用于展示“有限重试”的代码边界。对于固定的非法 JSON，立即重试并不会变好；
     * 真实系统应根据错误类型决定重试、退避、转入 DLT 或停止消费。</p>
     *
     * @param json 要解码的 Kafka value
     * @param maxAttempts 最大尝试次数，调用方应传入大于 0 的值
     * @return 成功解码的事件
     * @throws Exception 所有尝试都失败时抛出最后一次异常
     */
    static LogEvent decodeWithLocalRetry(String json, int maxAttempts) throws Exception {
        Exception lastFailure = null;
        for (int attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return LogEventCodec.decode(json);
            } catch (Exception exception) {
                lastFailure = exception;
            }
        }
        throw lastFailure;
    }

    /** 创建日志 Consumer 使用的配置。 */
    private static Properties consumerProperties() {
        Properties properties = new Properties();

        // 本机默认地址可被环境变量覆盖，便于以后把 Consumer 放进容器或连接远程实验集群。
        properties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG,
                System.getenv().getOrDefault("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"));

        // Group ID 决定消费进度和组内 Partition 分配；换一个 ID 会得到一套独立进度。
        properties.put(ConsumerConfig.GROUP_ID_CONFIG, "log-analytics-group");
        properties.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        properties.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());

        // 仅当这个 Group 没有有效 Offset 时，从最早仍保留的记录开始。
        properties.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        // 由上面的“整批成功”判断决定何时 commitSync()。
        properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);

        // 限制一次 poll 返回的记录数，给单次业务处理耗时一个直观上界。
        properties.put(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, 100);
        return properties;
    }
}
