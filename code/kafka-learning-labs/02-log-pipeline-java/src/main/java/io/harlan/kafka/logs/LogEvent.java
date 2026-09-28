package io.harlan.kafka.logs;

/**
 * 一条结构化日志事件的数据契约。
 *
 * <p>Java {@code record} 会自动生成构造器、只读访问方法（如 {@code service()}）、
 * {@code equals/hashCode} 和 {@code toString}，很适合表达只承载数据的不可变消息。</p>
 *
 * @param eventId 唯一事件标识；真实系统可用它做消费幂等键
 * @param service 产生日志的服务名；本实验也把它作为 Kafka 消息 key
 * @param level 日志级别，例如 INFO 或 ERROR
 * @param message 便于人阅读的日志正文
 * @param occurredAtEpochMillis 事件发生时间，Unix Epoch 毫秒
 */
public record LogEvent(
        String eventId,
        String service,
        String level,
        String message,
        long occurredAtEpochMillis
) {
}
