package com.harlan.rabbitmqdemo.config;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.stereotype.Component;

/**
 * 给 RabbitTemplate 注册生产者侧的两个结果回调。
 *
 * <ul>
 *     <li>Confirm：Broker 是否接管了发布动作；</li>
 *     <li>Return：消息到达 Exchange 后，是否因为没有匹配的 Binding 而无法路由。</li>
 * </ul>
 *
 * <p>这两种回调都不表示消费者已经完成业务。消费结果由 consumer ack 负责。</p>
 */
@Component
public class RabbitPublisherCallbacks {

    private static final Logger log = LoggerFactory.getLogger(RabbitPublisherCallbacks.class);

    public RabbitPublisherCallbacks(RabbitTemplate rabbitTemplate) {
        // ConfirmCallback 需要 application.yml 中 publisher-confirm-type=correlated。
        rabbitTemplate.setConfirmCallback((correlation, ack, cause) -> {
            // correlation 就是发送时传入的 CorrelationData，可将确认结果关联回 eventId。
            String eventId = correlation == null ? "unknown" : correlation.getId();
            if (ack) {
                // ack=true 只说明 Exchange 所在 Broker 接收了发布，不代表消息已被消费。
                log.info("Broker confirmed eventId={}", eventId);
            } else {
                log.error("Broker rejected eventId={}, cause={}", eventId, cause);
            }
        });

        // ReturnsCallback 需要 publisher-returns=true 且 template.mandatory=true。
        rabbitTemplate.setReturnsCallback(returned ->
                log.error(
                        "Unroutable message: exchange={}, routingKey={}, replyCode={}, replyText={}",
                        returned.getExchange(),
                        returned.getRoutingKey(),
                        returned.getReplyCode(),
                        returned.getReplyText()
                )
        );
    }
}
