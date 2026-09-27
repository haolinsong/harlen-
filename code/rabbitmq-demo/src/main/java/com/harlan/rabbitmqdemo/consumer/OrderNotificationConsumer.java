package com.harlan.rabbitmqdemo.consumer;

import com.harlan.rabbitmqdemo.config.RabbitTopology;
import com.harlan.rabbitmqdemo.model.OrderCreatedEvent;
import com.harlan.rabbitmqdemo.service.InMemoryIdempotencyStore;
import com.rabbitmq.client.Channel;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.core.Message;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

/**
 * 通知消费者：从 orders.notify.q 取出订单创建事件并模拟发送通知。
 *
 * <p>本消费者使用手动 ACK，目的是清楚展示“业务成功后确认、业务失败后拒绝”的边界。
 * RabbitMQ 在收到 ACK 前会把消息保留在 Unacked 状态；连接中断时，未确认消息可以
 * 重新投递，因此消费者仍然必须具备幂等能力。</p>
 */
@Component
public class OrderNotificationConsumer {

    private static final Logger log = LoggerFactory.getLogger(OrderNotificationConsumer.class);

    private final InMemoryIdempotencyStore idempotencyStore;

    public OrderNotificationConsumer(InMemoryIdempotencyStore idempotencyStore) {
        this.idempotencyStore = idempotencyStore;
    }

    /**
     * Spring AMQP 会为该方法创建消息监听端点。
     *
     * <ul>
     *     <li>{@code queues}：只消费通知 Queue；</li>
     *     <li>{@code ackMode=MANUAL}：代码必须显式调用 basicAck/basicNack；</li>
     *     <li>{@code concurrency=2}：启动两个消费者线程，竞争处理同一个 Queue。</li>
     * </ul>
     *
     * @param event   JSON 负载经 MessageConverter 反序列化得到的业务事件
     * @param message Spring AMQP 原始消息，可读取 deliveryTag 等 AMQP 元数据
     * @param channel RabbitMQ Channel，用来发送 ACK 或 NACK
     */
    @RabbitListener(
            queues = RabbitTopology.ORDER_NOTIFICATION_QUEUE,
            ackMode = "MANUAL",
            concurrency = "2"
    )
    public void handle(OrderCreatedEvent event, Message message, Channel channel)
            throws IOException {
        // deliveryTag 标识当前 Channel 上的这次投递，ACK/NACK 时必须原样带回。
        long deliveryTag = message.getMessageProperties().getDeliveryTag();

        // 先做幂等占用。返回 false 表示相同 eventId 已经处理或正在处理。
        if (!idempotencyStore.tryBegin(event.eventId())) {
            log.info("Skip duplicate notification eventId={}, orderId={}",
                    event.eventId(), event.orderId());

            // 重复消息不再执行业务，但仍要 ACK，否则它会持续重新投递。
            // 第二个参数 multiple=false 表示只确认当前 deliveryTag。
            channel.basicAck(deliveryTag, false);
            return;
        }

        try {
            // 关键顺序：先完成业务，再 ACK。若反过来，业务失败时消息已经被删除。
            processNotification(event);
            channel.basicAck(deliveryTag, false);
            log.info("Notification completed eventId={}, orderId={}",
                    event.eventId(), event.orderId());
        } catch (Exception exception) {
            // 业务没有完成，撤销内存幂等标记，便于以后人工补偿或重新投递。
            idempotencyStore.rollBack(event.eventId());

            // multiple=false：只拒绝当前消息；requeue=false：不放回原 Queue。
            // 因通知 Queue 配置了 DLX，RabbitMQ 会把消息路由到死信 Queue。
            channel.basicNack(deliveryTag, false, false);
            log.error("Notification rejected eventId={}, orderId={}",
                    event.eventId(), event.orderId(), exception);
        }
    }

    private void processNotification(OrderCreatedEvent event) {
        // orderId=fail 是教学开关，用来稳定复现“消费失败 -> NACK -> 死信”。
        if ("fail".equalsIgnoreCase(event.orderId())) {
            throw new IllegalStateException("Simulated permanent notification failure");
        }

        // 真实项目会在这里调用短信、邮件或推送服务；示例只打印日志。
        log.info("Sending notification for orderId={}", event.orderId());
    }
}
