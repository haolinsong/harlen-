package io.harlan.kafka.hello;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

/**
 * 实验 1 的消息生产者：生成若干字符串消息，并异步发送到 {@code learning.hello}。
 *
 * <p>运行时重点观察控制台中的 key、partition 和 offset：</p>
 * <ul>
 *     <li>相同 key 在 Partition 数不变时会稳定映射到同一 Partition；</li>
 *     <li>offset 是消息在该 Partition 内的位置，不是整个 Topic 的全局编号。</li>
 * </ul>
 */
public final class ProducerApp {
    // 应用只有 main 入口，不需要实例化。
    private ProducerApp() {
    }

    public static void main(String[] args) throws Exception {
        // 命令行第一个参数决定发送数量；没有参数时默认发送 10 条。
        int messageCount = args.length == 0 ? 10 : Integer.parseInt(args[0]);

        // 先准备 Topic，避免发送时才遇到 Topic 不存在或等待自动创建。
        TopicAdmin.ensureTopicExists();

        // KafkaProducer 是线程安全且创建成本较高的对象，通常在进程内复用。
        // try-with-resources 会在程序退出前 close；close 也会等待未完成的发送。
        try (KafkaProducer<String, String> producer = new KafkaProducer<>(KafkaSettings.producerProperties())) {
            for (int sequence = 1; sequence <= messageCount; sequence++) {
                // 只生成 user-0、user-1、user-2 三种 key，便于观察“相同 key -> 相同 Partition”。
                // 这种顺序保证只限同一 Partition，且增加 Partition 数可能改变映射结果。
                String key = "user-" + (sequence % 3);
                String value = "hello-kafka-" + sequence;

                // 不显式传 Partition，让默认分区器根据 key 和 Topic 元数据选择 Partition。
                ProducerRecord<String, String> record = new ProducerRecord<>(KafkaSettings.TOPIC, key, value);

                // send() 通常先把记录放进客户端缓冲区并立即返回；真正网络发送由后台线程完成。
                // Callback 在 Broker 最终确认成功或发送失败后执行，因此必须检查 exception。
                producer.send(record, (metadata, exception) -> {
                    if (exception != null) {
                        System.err.printf("send failed: key=%s, reason=%s%n", key, exception.getMessage());
                        return;
                    }
                    System.out.printf("sent: key=%s partition=%d offset=%d%n",
                            key, metadata.partition(), metadata.offset());
                });
            }

            // flush() 等待当前缓冲区中的异步发送结束，确保示例在打印完结果前不退出。
            // close() 也会 flush；这里显式调用是为了让初学者看到这个等待边界。
            producer.flush();
        }
    }
}
