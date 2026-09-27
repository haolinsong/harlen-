package com.harlan.rabbitmqdemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 整个 Spring Boot 应用的启动入口。
 *
 * <p>{@link SpringBootApplication} 同时开启三项核心能力：</p>
 * <ul>
 *     <li>把当前类作为 Java 配置类；</li>
 *     <li>扫描 {@code com.harlan.rabbitmqdemo} 及其子包中的 Spring Bean；</li>
 *     <li>根据 classpath 中的依赖执行自动配置，例如创建 RabbitTemplate 和监听容器。</li>
 * </ul>
 */
@SpringBootApplication
public class RabbitMqDemoApplication {

    public static void main(String[] args) {
        // 创建 Spring ApplicationContext，完成自动配置，然后启动内嵌 Web 服务器。
        SpringApplication.run(RabbitMqDemoApplication.class, args);
    }
}
