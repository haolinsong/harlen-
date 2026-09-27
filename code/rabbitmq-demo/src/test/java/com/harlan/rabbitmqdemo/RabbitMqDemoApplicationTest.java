package com.harlan.rabbitmqdemo;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

/**
 * 最小 Spring 上下文测试：验证自动配置和项目 Bean 能否一起创建成功。
 *
 * <p>这个测试关注“应用配置能否启动”，并不测试真实 RabbitMQ 收发。</p>
 */
@SpringBootTest(properties = {
        // 测试不需要启动内嵌 Web 服务器，可以减少启动时间和端口占用。
        "spring.main.web-application-type=none",
        // 不启动消息监听容器，因此运行单元测试时不要求本机存在 RabbitMQ。
        "spring.rabbitmq.listener.simple.auto-startup=false"
})
class RabbitMqDemoApplicationTest {

    @Test
    void contextLoads() {
        // 方法体为空是刻意的：Spring 上下文创建过程中没有抛异常，测试就通过。
    }
}
