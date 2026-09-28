package io.harlan.kafka.hello;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.Properties;

/**
 * 集中保存实验 1 使用的 Kafka 配置。
 *
 * <p>把 Producer 和 Consumer 的配置放在一个类里有两个好处：</p>
 * <ol>
 *     <li>应用入口只关注“发送”或“消费”的业务流程，不被大量配置淹没；</li>
 *     <li>单元测试可以直接检查可靠性相关参数，而不必真的启动 Kafka。</li>
 * </ol>
 *
 * <p>这是教学用配置，不包含生产环境常见的 TLS、SASL、ACL 和监控设置。</p>
 */
final class KafkaSettings {
    /** Producer 和 Consumer 共同使用的 Topic 名称。 */
    static final String TOPIC = "learning.hello";

    // 这是一个纯工具类，不需要、也不允许创建实例。
    private KafkaSettings() {
    }

    /**
     * 返回客户端最初用来发现 Kafka 集群的地址。
     *
     * <p>本机运行时默认连接 {@code localhost:9092}。如果 Java 程序运行在
     * Docker 或另一台机器上，可以通过环境变量覆盖，而不必修改源码。</p>
     */
    static String bootstrapServers() {
        return System.getenv().getOrDefault("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092");
    }

    /** 创建 Producer 配置；键和值在本实验中都使用 String。 */
    static Properties producerProperties() {
        Properties properties = new Properties();

        // bootstrap.servers 只是“入口地址”。连接后，Producer 会获取完整的集群元数据。
        properties.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers());

        // Kafka 最终传输的是 byte[]；Serializer 负责把 Java String 转成字节。
        properties.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // acks=all：Leader 要等满足 ISR/min.insync.replicas 条件后才确认成功。
        properties.put(ProducerConfig.ACKS_CONFIG, "all");

        // 幂等 Producer 会使用 Producer ID 和序列号，避免客户端重试造成 Kafka 内重复写入。
        // 它不等于“业务幂等”，也不能自动去重数据库写入或 HTTP 调用。
        properties.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, true);

        // 压缩以 Batch 为单位进行。LZ4 通常在吞吐、压缩率和 CPU 成本之间较均衡。
        properties.put(ProducerConfig.COMPRESSION_TYPE_CONFIG, "lz4");

        // 最多等待 10 ms 聚合更多消息形成 Batch；吞吐通常更高，但会增加少量排队延迟。
        properties.put(ProducerConfig.LINGER_MS_CONFIG, 10);
        return properties;
    }

    /** 创建 Consumer 配置，采用“处理成功后手动提交”的基础 At Least Once 模式。 */
    static Properties consumerProperties() {
        Properties properties = new Properties();
        properties.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers());

        // group.id 同时决定组内负载均衡的身份，以及 Broker 上保存消费进度的命名空间。
        properties.put(ConsumerConfig.GROUP_ID_CONFIG, "hello-java-group");

        // Deserializer 与 Producer 的 Serializer 对应，把 Kafka 字节还原为 Java String。
        properties.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        properties.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());

        // 仅在这个 Group 没有有效 Committed Offset 时生效；不是每次启动都从头读取。
        properties.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");

        // 关闭定时自动提交，交给 ConsumerApp 在业务处理成功后调用 commitSync()。
        properties.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, false);
        return properties;
    }
}
