package io.harlan.kafka.logs;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

/**
 * 验证 JSON 消息契约和坏消息路径；这些测试不连接 Kafka Broker。
 */
class LogEventCodecTest {
    @Test
    void roundTripsJson() throws Exception {
        // round trip：Java 对象 -> JSON -> Java 对象，结果应保持完全相等。
        LogEvent original = new LogEvent("event-1", "orders", "INFO", "created", 123L);

        LogEvent decoded = LogEventCodec.decode(LogEventCodec.encode(original));

        assertEquals(original, decoded);
    }

    @Test
    void rejectsMalformedJsonAfterRetries() {
        // 固定的非法 JSON 重试 3 次仍会失败，提醒我们永久错误需要 DLT/告警而非无限重试。
        assertThrows(Exception.class, () -> LogConsumer.decodeWithLocalRetry("not-json", 3));
    }
}
