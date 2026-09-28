package io.harlan.kafka.hello;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.errors.WakeupException;

import java.time.Duration;
import java.util.List;
import java.util.concurrent.atomic.AtomicBoolean;

/**
 * 实验 1 的消息消费者：加入固定 Consumer Group，批量拉取消息，处理成功后手动提交 Offset。
 *
 * <p>这里展示基础 At Least Once 顺序：{@code poll -> process -> commit}。如果业务处理完成后、
 * Offset 提交成功前进程崩溃，该批消息会再次投递，所以真实业务还需要幂等处理。</p>
 */
public final class ConsumerApp {
    private ConsumerApp() {
    }

    public static void main(String[] args) throws Exception {
        // 这是本次示例希望至少处理的消息数，不是 Kafka Consumer 的批次大小。
        int maxMessages = args.length == 0 ? 10 : Integer.parseInt(args[0]);

        // Shutdown Hook 和主循环可能由不同线程访问该值，因此使用 AtomicBoolean 保证可见性。
        AtomicBoolean running = new AtomicBoolean(true);
        TopicAdmin.ensureTopicExists();

        // KafkaConsumer 不是线程安全的：poll、处理和 commit 都在当前主线程执行。
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(KafkaSettings.consumerProperties())) {
            // subscribe() 让 Consumer Group 协调器分配 Topic 的 Partition；分配可能在首次 poll 时完成。
            consumer.subscribe(List.of(KafkaSettings.TOPIC));

            // Ctrl+C 或正常终止时，wakeup() 会让正在阻塞的 poll() 尽快抛出 WakeupException。
            // wakeup() 是 KafkaConsumer 唯一明确允许从其他线程调用的方法。
            Runtime.getRuntime().addShutdownHook(new Thread(() -> {
                running.set(false);
                consumer.wakeup();
            }));

            int processed = 0;
            try {
                while (running.get() && processed < maxMessages) {
                    // poll() 从当前已分配的 Partition 拉取一批消息，并维持组协调/心跳流程。
                    // 1 秒是本次调用最多等待数据的时间，不代表每秒只能消费一次。
                    ConsumerRecords<String, String> records = consumer.poll(Duration.ofSeconds(1));

                    for (ConsumerRecord<String, String> record : records) {
                        // 这里用打印模拟业务处理。真实项目应在成功完成数据库写入等操作后才计为成功。
                        System.out.printf("received: key=%s value=%s partition=%d offset=%d%n",
                                record.key(), record.value(), record.partition(), record.offset());
                        processed++;
                    }

                    if (!records.isEmpty()) {
                        // 当前批次全部处理成功后，提交各 Partition 的“下一条待消费位置”。
                        // commitSync() 会等待 Broker 响应，逻辑直观，适合第一个实验。
                        consumer.commitSync();
                    }
                }
            } catch (WakeupException exception) {
                // 由 Shutdown Hook 主动 wakeup 属于正常退出；运行中意外出现则继续抛出。
                if (running.get()) {
                    throw exception;
                }
            }
            // 离开 try 块后自动 close()，Consumer 会释放连接并离开 Group，触发必要的 Rebalance。
        }
    }
}
