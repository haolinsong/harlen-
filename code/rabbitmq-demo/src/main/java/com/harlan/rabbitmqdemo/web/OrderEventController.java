package com.harlan.rabbitmqdemo.web;

import com.harlan.rabbitmqdemo.model.OrderCreatedEvent;
import com.harlan.rabbitmqdemo.service.OrderEventPublisher;
import java.time.Instant;
import java.util.UUID;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

/**
 * 提供学习用 HTTP 接口，把一次 HTTP 请求转换成 OrderCreatedEvent 并发布到 RabbitMQ。
 *
 * <p>Controller 不直接处理通知或审计业务，它只是消息生产端的入口。</p>
 */
@RestController
@RequestMapping("/api/orders")
public class OrderEventController {

    private final OrderEventPublisher publisher;

    public OrderEventController(OrderEventPublisher publisher) {
        this.publisher = publisher;
    }

    /**
     * 发布一条可以正常路由的订单创建事件。
     *
     * @param orderId URL 路径中的订单 ID；传 {@code fail} 可让通知消费者模拟失败
     * @param eventId 可选的事件 ID；重复传同一个值可以观察消费者幂等处理
     */
    @PostMapping("/{orderId}/created")
    public ResponseEntity<OrderCreatedEvent> publishCreated(
            @PathVariable String orderId,
            @RequestParam(required = false) UUID eventId
    ) {
        OrderCreatedEvent event = newEvent(orderId, eventId);
        publisher.publish(event);

        // 202 Accepted 表示请求已被异步链路接受，不承诺消费者已经完成处理。
        return ResponseEntity.accepted().body(event);
    }

    /**
     * 发布到未绑定的 routing key，用于触发 RabbitTemplate 的 ReturnsCallback。
     */
    @PostMapping("/{orderId}/unroutable")
    public ResponseEntity<OrderCreatedEvent> publishUnroutable(
            @PathVariable String orderId,
            @RequestParam(required = false) UUID eventId
    ) {
        OrderCreatedEvent event = newEvent(orderId, eventId);
        publisher.publishUnroutable(event);
        return ResponseEntity.accepted().body(event);
    }

    private OrderCreatedEvent newEvent(String orderId, UUID eventId) {
        // 未指定 eventId 时，每次请求都生成新事件；指定后则可以重复发送同一事件。
        UUID resolvedEventId = eventId == null ? UUID.randomUUID() : eventId;
        return new OrderCreatedEvent(resolvedEventId, orderId, Instant.now());
    }
}
