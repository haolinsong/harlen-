package com.harlan.rabbitmqdemo.model;

import java.time.Instant;
import java.util.UUID;

/**
 * “订单已创建”事件，也就是生产者和消费者之间约定的消息数据结构。
 *
 * <p>Java {@code record} 适合表示不可变的数据载体。编译器会自动生成构造方法、
 * 访问方法（例如 {@code eventId()}）、{@code equals/hashCode} 和 {@code toString}。</p>
 *
 * @param eventId   事件的唯一 ID；消费者用它识别重复消息，而不是用订单 ID 去重
 * @param orderId   发生业务事件的订单 ID
 * @param occurredAt 事件发生时间；使用 UTC 时间线上的 {@link Instant}，避免时区歧义
 */
public record OrderCreatedEvent(
        UUID eventId,
        String orderId,
        Instant occurredAt
) {
}
