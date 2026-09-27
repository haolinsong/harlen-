package com.harlan.rabbitmqdemo.config;

import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.BindingBuilder;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.core.QueueBuilder;
import org.springframework.amqp.support.converter.JacksonJsonMessageConverter;
import org.springframework.amqp.support.converter.MessageConverter;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 使用 Spring Bean 描述本示例需要的 RabbitMQ 拓扑。
 *
 * <pre>
 *                          +-- orders.notify.q --失败--+--> orders.notify.dead.q
 * Producer -> orders.direct                           |          ^
 *                          +-- orders.audit.q          +--> orders.dlx
 * </pre>
 *
 * <p>Spring Boot 自动配置的 RabbitAdmin 会在应用连接 RabbitMQ 时发现这些 Bean，
 * 并向 Broker 声明对应的 Exchange、Queue 和 Binding。因此，这里的 Java 对象既是
 * 应用配置，也会决定 RabbitMQ 中实际创建的资源。</p>
 */
@Configuration
public class RabbitTopology {

    // 正常业务消息首先发送到这个 Direct Exchange。
    public static final String ORDER_EXCHANGE = "orders.direct";

    // 两个业务 Queue 都绑定该 routing key，所以每个 Queue 都会得到一份消息副本。
    public static final String ORDER_CREATED_ROUTING_KEY = "order.created";

    // 没有 Binding 使用这个 routing key，专门用来演示 publisher return。
    public static final String UNROUTABLE_ROUTING_KEY = "order.unknown";

    // 通知 Queue 使用手动 ACK，并配置了死信去向。
    public static final String ORDER_NOTIFICATION_QUEUE = "orders.notify.q";

    // 审计 Queue 与通知 Queue 相互独立，演示“多个 Queue 才是发布/订阅”。
    public static final String ORDER_AUDIT_QUEUE = "orders.audit.q";

    // 通知失败的消息由 RabbitMQ 转发到这个 Dead Letter Exchange。
    public static final String ORDER_DLX = "orders.dlx";
    public static final String ORDER_DEAD_ROUTING_KEY = "order.created.dead";
    public static final String ORDER_DEAD_QUEUE = "orders.notify.dead.q";

    /**
     * 声明业务 Direct Exchange。
     *
     * <p>第二个参数 durable=true：Broker 重启后保留 Exchange；
     * 第三个参数 autoDelete=false：没有消费者时也不自动删除。</p>
     */
    @Bean
    DirectExchange orderExchange() {
        return new DirectExchange(ORDER_EXCHANGE, true, false);
    }

    /** 声明专门接收死信的 Direct Exchange。 */
    @Bean
    DirectExchange orderDeadLetterExchange() {
        return new DirectExchange(ORDER_DLX, true, false);
    }

    /**
     * 声明通知 Queue，并设置死信参数。
     *
     * <p>当消费者执行 {@code basicNack(requeue=false)} 时，RabbitMQ 会把消息交给
     * {@code orders.dlx}，并把 routing key 改为 {@code order.created.dead}。</p>
     */
    @Bean
    Queue orderNotificationQueue() {
        return QueueBuilder.durable(ORDER_NOTIFICATION_QUEUE)
                .deadLetterExchange(ORDER_DLX)
                .deadLetterRoutingKey(ORDER_DEAD_ROUTING_KEY)
                .build();
    }

    /** 声明审计 Queue。它不配置 DLX，保持示例重点清晰。 */
    @Bean
    Queue orderAuditQueue() {
        return QueueBuilder.durable(ORDER_AUDIT_QUEUE).build();
    }

    /** 声明最终保存失败通知消息的死信 Queue。 */
    @Bean
    Queue orderDeadQueue() {
        return QueueBuilder.durable(ORDER_DEAD_QUEUE).build();
    }

    /**
     * 把通知 Queue 绑定到业务 Exchange。
     *
     * <p>项目中存在多个 Queue 和 DirectExchange Bean，所以使用 {@link Qualifier}
     * 明确告诉 Spring 此处需要注入哪一个，避免按类型注入时产生歧义。</p>
     */
    @Bean
    Binding orderNotificationBinding(
            @Qualifier("orderNotificationQueue") Queue queue,
            @Qualifier("orderExchange") DirectExchange exchange
    ) {
        return BindingBuilder.bind(queue)
                .to(exchange)
                .with(ORDER_CREATED_ROUTING_KEY);
    }

    /** 把审计 Queue 绑定到同一个业务事件，因此它会收到独立的消息副本。 */
    @Bean
    Binding orderAuditBinding(
            @Qualifier("orderAuditQueue") Queue queue,
            @Qualifier("orderExchange") DirectExchange exchange
    ) {
        return BindingBuilder.bind(queue)
                .to(exchange)
                .with(ORDER_CREATED_ROUTING_KEY);
    }

    /** 把死信 Queue 绑定到 DLX，形成失败消息的最终去向。 */
    @Bean
    Binding orderDeadBinding(
            @Qualifier("orderDeadQueue") Queue queue,
            @Qualifier("orderDeadLetterExchange") DirectExchange exchange
    ) {
        return BindingBuilder.bind(queue)
                .to(exchange)
                .with(ORDER_DEAD_ROUTING_KEY);
    }

    /**
     * 使用 Jackson 在 Java 对象与 JSON 消息之间转换。
     *
     * <p>构造参数限制了允许反序列化的 Java 包，避免对任意类型进行反序列化。
     * Spring Boot 会把这个 MessageConverter 自动应用到 RabbitTemplate 和默认监听容器。</p>
     */
    @Bean
    MessageConverter jsonMessageConverter() {
        return new JacksonJsonMessageConverter("com.harlan.rabbitmqdemo.model");
    }
}
