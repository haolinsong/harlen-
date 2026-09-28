package io.harlan.kafka.logs;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * 在 Java {@link LogEvent} 与 Kafka 中传输的 JSON 字符串之间转换。
 *
 * <p>把序列化集中在单独的类中，Producer 和 Consumer 不必各写一套 JSON 逻辑，
 * 也方便用单元测试验证消息能否往返转换。生产系统通常还会引入 Schema Registry，
 * 明确定义字段兼容性，而不只依赖普通 JSON。</p>
 */
final class LogEventCodec {
    // ObjectMapper 创建成本较高且配置完成后可复用，因此使用单个静态实例。
    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    private LogEventCodec() {
    }

    /** 把 Java 事件编码为要写入 Kafka Record value 的 JSON。 */
    static String encode(LogEvent event) throws JsonProcessingException {
        return OBJECT_MAPPER.writeValueAsString(event);
    }

    /** 把从 Kafka Record value 读到的 JSON 还原为 Java 事件。 */
    static LogEvent decode(String json) throws JsonProcessingException {
        return OBJECT_MAPPER.readValue(json, LogEvent.class);
    }
}
