package com.harlan.rabbitmqdemo.consumer;

import com.harlan.rabbitmqdemo.config.RabbitTopology;
import com.harlan.rabbitmqdemo.model.OrderCreatedEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

/**
 * 审计消费者：独立监听 orders.audit.q，证明“一个 Exchange 绑定多个 Queue”时，
 * 每个 Queue 都会获得自己的消息副本。
 *
 * <p>它与通知消费者不是竞争关系：通知消费者处理通知 Queue，审计消费者处理审计 Queue。</p>
 */
@Component
public class OrderAuditConsumer {

    private static final Logger log = LoggerFactory.getLogger(OrderAuditConsumer.class);

    /**
     * 未显式设置 ackMode，因此使用 Spring AMQP 默认的 AUTO 模式。
     * AUTO 不是“收到消息立刻确认”：方法正常返回后容器才 ACK；方法抛出异常时，
     * 容器会根据监听器配置决定拒绝或重新入队。
     */
    @RabbitListener(queues = RabbitTopology.ORDER_AUDIT_QUEUE)
    public void handle(OrderCreatedEvent event) {
        // 真实项目通常把审计事件写入数据库或日志平台；示例只打印结构化日志。
        log.info("Audit recorded eventId={}, orderId={}, occurredAt={}",
                event.eventId(), event.orderId(), event.occurredAt());
    }
}
