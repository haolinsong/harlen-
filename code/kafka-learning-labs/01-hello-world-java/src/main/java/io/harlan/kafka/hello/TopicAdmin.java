package io.harlan.kafka.hello;

import org.apache.kafka.clients.admin.Admin;
import org.apache.kafka.clients.admin.NewTopic;

import java.util.List;
import java.util.Properties;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;

/**
 * 用 Kafka Admin Client 保证实验所需的 Topic 已存在。
 *
 * <p>也可以先运行根目录的 {@code scripts/create-topics.sh} 创建 Topic；这里仍保留
 * 自动创建逻辑，使单独启动 Java 示例时也更容易成功。重复执行不会故意创建第二个 Topic。</p>
 */
final class TopicAdmin {
    // 工具类只提供静态方法，不创建对象。
    private TopicAdmin() {
    }

    /**
     * 若 {@link KafkaSettings#TOPIC} 不存在，则创建一个 3 Partition、1 Replica 的 Topic。
     *
     * <p>副本因子 1 只适用于这个单 Broker 本地实验，不能提供 Broker 故障容忍。</p>
     */
    static void ensureTopicExists() throws Exception {
        Properties properties = new Properties();

        // Admin Client 和 Producer/Consumer 一样，先通过 bootstrap.servers 发现集群。
        properties.put("bootstrap.servers", KafkaSettings.bootstrapServers());

        // try-with-resources 会在方法结束时关闭 Admin Client 及其网络资源。
        try (Admin admin = Admin.create(properties)) {
            // Topic 已存在时直接返回；这样多次运行实验不会报“Topic 已存在”。
            if (admin.listTopics().names().get().contains(KafkaSettings.TOPIC)) {
                return;
            }
            try {
                // 第三个参数是 replication factor。当前 Compose 只有一个 Broker，所以必须是 1。
                admin.createTopics(List.of(new NewTopic(KafkaSettings.TOPIC, 3, (short) 1)))
                        .all()
                        // Admin API 是异步的；get() 在这里等待 Broker 完成创建。
                        .get();
            } catch (ExecutionException exception) {
                // Producer 与 Consumer 可能同时发现 Topic 不存在并发起创建。
                // 若另一个进程已经创建成功，这次异常可以忽略；否则保留原异常，避免掩盖真实故障。
                if (!admin.listTopics().names().get().contains(KafkaSettings.TOPIC)) {
                    throw exception;
                }
            }

            // 再发一个轻量查询，限定最多等待 10 秒，用于确认 Admin Client 能正常访问集群。
            admin.describeCluster().clusterId().get(10, TimeUnit.SECONDS);
        }
    }
}
