package com.harlan.rabbitmqdemo.service;

import com.harlan.rabbitmqdemo.config.RabbitTopology;
import com.harlan.rabbitmqdemo.model.OrderCreatedEvent;
import org.springframework.amqp.rabbit.connection.CorrelationData;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Service;

/**
 * 订单事件生产者：把 Java 对象交给 Spring AMQP，并发送到 RabbitMQ Exchange。
 *
 * <p>这个类只负责“发布消息”，不等待消费者完成业务。HTTP 接口返回 202 时，
 * 最多表示发布方法已经被调用，不表示通知或审计消费者已经处理完毕。</p>
 */
@Service
public class OrderEventPublisher {

    private final RabbitTemplate rabbitTemplate;

    /**
     * Spring Boot 根据 {@code spring.rabbitmq.*} 自动创建 RabbitTemplate，
     * 再通过构造器注入到这里。构造器注入便于测试，也能保证依赖不为 null。
     */
    public OrderEventPublisher(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    /** 使用正常的 routing key 发布订单创建事件。 */
    public void publish(OrderCreatedEvent event) {
        publish(event, RabbitTopology.ORDER_CREATED_ROUTING_KEY);
    }

    /**
     * 使用一个没有任何 Queue 绑定的 routing key 发布事件。
     * 这个方法专门用来观察 publisher return（NO_ROUTE）。
     */
    public void publishUnroutable(OrderCreatedEvent event) {
        publish(event, RabbitTopology.UNROUTABLE_ROUTING_KEY);
    }

    private void publish(OrderCreatedEvent event, String routingKey) {
        // CorrelationData 只服务于 publisher confirm：Broker 确认后，可据此找到原事件。
        CorrelationData correlationData = new CorrelationData(event.eventId().toString());

        // convertAndSend 会先调用 MessageConverter，把 OrderCreatedEvent 转为 JSON 消息。
        rabbitTemplate.convertAndSend(
                // 1. 消息先到哪个 Exchange。
                RabbitTopology.ORDER_EXCHANGE,
                // 2. Direct Exchange 使用这个 routing key 选择匹配的 Binding。
                routingKey,
                // 3. 要发送的业务对象。
                event,
                // 4. MessagePostProcessor 可在发送前补充 AMQP 消息属性。
                message -> {
                    // messageId 属于消息元数据；这里与 eventId 保持一致，方便日志排查。
                    message.getMessageProperties().setMessageId(event.eventId().toString());
                    return message;
                },
                // 5. Broker confirm 回调会携带这个关联数据，而不是完整业务消息。
                correlationData
        );
    }
}
