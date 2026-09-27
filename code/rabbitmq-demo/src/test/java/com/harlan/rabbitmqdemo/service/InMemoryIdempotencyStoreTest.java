package com.harlan.rabbitmqdemo.service;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.UUID;
import org.junit.jupiter.api.Test;

/** InMemoryIdempotencyStore 的行为测试，不需要启动 Spring 或 RabbitMQ。 */
class InMemoryIdempotencyStoreTest {

    // 直接 new 被测对象，使测试保持快速，也说明该类的核心逻辑不依赖 Spring。
    private final InMemoryIdempotencyStore store = new InMemoryIdempotencyStore();

    @Test
    void acceptsAnEventOnlyOnce() {
        UUID eventId = UUID.randomUUID();

        // 第一次占用成功，第二次使用相同 eventId 会被识别为重复。
        assertThat(store.tryBegin(eventId)).isTrue();
        assertThat(store.tryBegin(eventId)).isFalse();
    }

    @Test
    void allowsRetryAfterRollback() {
        UUID eventId = UUID.randomUUID();

        assertThat(store.tryBegin(eventId)).isTrue();

        // 模拟业务失败：消费者会撤销幂等占用。
        store.rollBack(eventId);

        // 撤销后允许同一事件再次处理，以支持重新投递或人工补偿。
        assertThat(store.tryBegin(eventId)).isTrue();
    }
}
