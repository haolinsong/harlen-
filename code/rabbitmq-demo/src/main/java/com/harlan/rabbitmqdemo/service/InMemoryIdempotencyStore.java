package com.harlan.rabbitmqdemo.service;

import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Component;

/**
 * 学习用的内存幂等记录：同一个 eventId 只允许开始处理一次。
 *
 * <p>它使用线程安全 Set，因此两个并发消费者同时收到相同 eventId 时，只有一个
 * {@link #tryBegin(UUID)} 调用会成功。</p>
 *
 * <p><strong>生产环境不要直接使用：</strong>应用重启后数据会丢失，多实例之间也不共享。
 * 正式系统通常使用数据库唯一约束、业务状态表或支持原子写入的持久化存储，并把
 * “记录已处理”和业务数据更新放进同一个事务边界。</p>
 */
@Component
public class InMemoryIdempotencyStore {

    // ConcurrentHashMap.newKeySet() 提供线程安全、支持原子 add 的 Set。
    private final Set<UUID> processingOrCompleted = ConcurrentHashMap.newKeySet();

    /**
     * 尝试占用一个 eventId。
     *
     * @return true 表示此前不存在，可以继续处理；false 表示它正在处理或已经完成
     */
    public boolean tryBegin(UUID eventId) {
        // Set.add 是原子操作：首次添加返回 true，重复添加返回 false。
        return processingOrCompleted.add(eventId);
    }

    /**
     * 业务失败时撤销占用，使同一事件在未来被补偿或重新投递时可以再次处理。
     */
    public void rollBack(UUID eventId) {
        processingOrCompleted.remove(eventId);
    }
}
