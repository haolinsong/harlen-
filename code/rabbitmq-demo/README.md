# RabbitMQ Spring Boot Demo

这是 `outputs/Java/RabbitMQ入门实战.md` 的配套代码。项目使用 Spring Boot 4.1.1、Java 17+、Spring AMQP 和 RabbitMQ 4.x，演示：

- Direct Exchange、两个业务 Queue 和 Binding
- JSON 消息、publisher confirm 与 publisher return
- 竞争消费与发布/订阅的区别
- 手动 consumer ack、Dead Letter Exchange 和死信 Queue
- 基于事件 ID 的简化幂等处理

## 架构

```text
POST /api/orders/{orderId}/created
                |
                v
          orders.direct
           order.created
            /        \
           v          v
orders.notify.q    orders.audit.q
  manual ack         auto ack
       |
       | nack(requeue=false)
       v
   orders.dlx
       |
       v
orders.notify.dead.q
```

同一事件会分别进入通知 Queue 和审计 Queue，因此两个消费者各收到一份。通知消费者内部可以有多个实例，它们会竞争处理 `orders.notify.q` 中的消息。

## 建议的代码阅读顺序

源码已经加入面向新手的中文 JavaDoc 和关键行注释。建议不要按文件名字母顺序阅读，而是沿着一条消息的生命周期阅读：

1. [`application.yml`](src/main/resources/application.yml)：先看应用如何连接 RabbitMQ，以及 confirm、return、prefetch 等开关。
2. [`RabbitTopology.java`](src/main/java/com/harlan/rabbitmqdemo/config/RabbitTopology.java)：理解 Exchange、Queue、Binding 和 DLX 如何连接。
3. [`OrderCreatedEvent.java`](src/main/java/com/harlan/rabbitmqdemo/model/OrderCreatedEvent.java)：确认生产者与消费者交换的数据结构。
4. [`OrderEventController.java`](src/main/java/com/harlan/rabbitmqdemo/web/OrderEventController.java)：从 HTTP 请求进入消息链路。
5. [`OrderEventPublisher.java`](src/main/java/com/harlan/rabbitmqdemo/service/OrderEventPublisher.java)：观察 `RabbitTemplate` 如何发布消息。
6. [`RabbitPublisherCallbacks.java`](src/main/java/com/harlan/rabbitmqdemo/config/RabbitPublisherCallbacks.java)：区分 publisher confirm 和 return。
7. [`OrderNotificationConsumer.java`](src/main/java/com/harlan/rabbitmqdemo/consumer/OrderNotificationConsumer.java)：重点理解手动 ACK、NACK、死信和幂等。
8. [`OrderAuditConsumer.java`](src/main/java/com/harlan/rabbitmqdemo/consumer/OrderAuditConsumer.java)：理解两个 Queue 各收一份与同一 Queue 竞争消费的区别。
9. [`InMemoryIdempotencyStoreTest.java`](src/test/java/com/harlan/rabbitmqdemo/service/InMemoryIdempotencyStoreTest.java)：通过测试确认幂等记录的行为。

## 环境要求

- Java 17 或更高版本
- Maven 3.6.3 或更高版本，或使用项目自带的 Maven Wrapper
- Docker 与 Docker Compose

## 启动

启动 RabbitMQ：

```bash
docker compose up -d
docker compose ps
```

管理界面：[http://localhost:15672](http://localhost:15672)

- 用户名：`learner`
- 密码：`learner123`

启动应用：

```bash
./mvnw spring-boot:run
```

没有 Maven Wrapper 时也可以使用：

```bash
mvn spring-boot:run
```

健康检查：

```bash
curl http://localhost:8080/actuator/health
```

## 练习

### 1. 正常消息

```bash
curl -i -X POST http://localhost:8080/api/orders/1001/created
```

响应会包含 `eventId`。应用日志中应同时出现 notification 和 audit 两条消费记录。

### 2. 重复消息

使用同一个 `eventId` 连续调用两次：

```bash
curl -i -X POST \
  "http://localhost:8080/api/orders/1002/created?eventId=11111111-1111-1111-1111-111111111111"

curl -i -X POST \
  "http://localhost:8080/api/orders/1002/created?eventId=11111111-1111-1111-1111-111111111111"
```

通知消费者会记录第二条消息为 duplicate，然后直接 ack。

当前幂等存储是内存 `Set`，只适合演示：应用重启后记录会丢失，也无法覆盖跨实例场景。生产环境应改用数据库唯一约束、业务状态机或其他持久化幂等方案，并与业务更新放在同一事务边界内。

### 3. 死信消息

`orderId=fail` 会模拟永久业务失败：

```bash
curl -i -X POST http://localhost:8080/api/orders/fail/created
```

通知消费者会执行 `basicNack(requeue=false)`，消息随后进入 `orders.notify.dead.q`。审计消费者仍会正常处理自己的副本。

查看 Queue 状态：

```bash
docker compose exec rabbitmq \
  rabbitmqctl list_queues name messages_ready messages_unacknowledged
```

### 4. 无法路由的消息

```bash
curl -i -X POST http://localhost:8080/api/orders/1003/unroutable
```

消息使用未绑定的 routing key `order.unknown`。由于开启了 `mandatory` 和 publisher returns，应用日志中应出现 `NO_ROUTE`。

## 测试与打包

```bash
./mvnw test
./mvnw package
```

## 清理

停止容器并保留数据：

```bash
docker compose down
```

停止容器并删除学习数据：

```bash
docker compose down -v
```

## 重要说明

- `QueueBuilder.durable(...)` 默认创建 Classic Queue；单节点学习环境不提供消息副本。
- publisher confirm 只确认 Broker 已接管消息，不代表消费者已经完成业务。
- consumer ack 只确认消息处理结果，不会自动解决数据库更新与 ack 之间的一致性。
- 死信 Queue 必须配套监控、告警和人工或自动补偿流程。
