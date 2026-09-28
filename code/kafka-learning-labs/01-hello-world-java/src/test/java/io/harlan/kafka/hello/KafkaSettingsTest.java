package io.harlan.kafka.hello;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.junit.jupiter.api.Test;

import java.util.Properties;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * 对关键配置做快速单元测试。
 *
 * <p>这些测试只检查本地生成的 Properties，不需要 Kafka Broker；端到端收发仍需按 README
 * 启动 Compose 环境验证。</p>
 */
class KafkaSettingsTest {
    @Test
    void producerUsesReliableDefaults() {
        Properties properties = KafkaSettings.producerProperties();

        // 两个断言共同保护本实验希望展示的可靠 Producer 基线。
        assertEquals("all", properties.get(ProducerConfig.ACKS_CONFIG));
        assertEquals(true, properties.get(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG));
    }

    @Test
    void consumerCommitsOnlyAfterProcessing() {
        Properties properties = KafkaSettings.consumerProperties();

        // 关闭自动提交后，提交时机由 ConsumerApp 的业务处理结果决定。
        assertEquals(false, properties.get(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG));

        // earliest 只在 Group 没有有效 Offset 时生效，便于第一次运行读到已有实验消息。
        assertEquals("earliest", properties.get(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG));
    }
}
