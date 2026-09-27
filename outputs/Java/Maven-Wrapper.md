---
title: Maven Wrapper
type: output
tags: [Java/Maven, 构建工具]
aliases: []
created: 2026-09-24
updated: 2026-09-24
related: ["[[RabbitMQ入门实战]]"]
---

# Maven Wrapper

## 一句话结论

Maven Wrapper 是随项目提交的 Maven 启动脚本：它让开发者和 CI 使用项目指定的 Maven 版本执行构建，而不依赖机器上碰巧安装的版本。

## 它解决什么问题

直接运行 `mvn test` 时，使用的是操作系统 `PATH` 中的 Maven；运行 `./mvnw test` 时，脚本读取项目指定的版本，必要时先下载，再调用这个固定版本执行同一个 Maven Goal。

它不会替代以下内容：

- 不替代 `pom.xml`：依赖、插件和构建规则仍由 `pom.xml` 定义。
- 不替代 JDK：机器上仍须安装符合项目要求的 Java。
- 不把项目依赖提交进仓库：依赖仍会下载到 Maven 本地仓库。

## 文件组成

以 [`rabbitmq-demo`](../../code/rabbitmq-demo/README.md) 为例：

```text
rabbitmq-demo/
├── mvnw                                  # macOS / Linux 启动脚本
├── mvnw.cmd                              # Windows 启动脚本
└── .mvn/wrapper/maven-wrapper.properties # Wrapper 与 Maven 版本配置
```

当前配置是：

```properties
wrapperVersion=3.3.4
distributionType=only-script
distributionUrl=https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/3.9.11/apache-maven-3.9.11-bin.zip
```

这表示使用 Maven Wrapper 3.3.4 的 `only-script` 方式，引导下载并运行 Maven 3.9.11。该方式不需要在仓库中提交 `maven-wrapper.jar`。

## 怎么用

先进入含有 `mvnw` 和 `pom.xml` 的项目根目录：

```bash
cd "/Users/sjj/learn/codex知识库/Harlan的第二大脑/code/rabbitmq-demo"
```

macOS / Linux：

```bash
./mvnw -v                 # 查看实际使用的 Maven 与 Java
./mvnw test               # 编译并运行测试
./mvnw package            # 测试并打包 JAR
./mvnw spring-boot:run    # 启动 Spring Boot
./mvnw dependency:tree    # 查看依赖树
./mvnw clean              # 删除 target 构建产物
```

Windows：

```powershell
mvnw.cmd -v
mvnw.cmd test
mvnw.cmd spring-boot:run
```

第一次运行通常需要联网下载指定的 Maven 和项目依赖，之后会使用本地缓存。团队脚本与 CI 应优先使用 Wrapper，从而让构建入口和 Maven 版本保持一致。

## 更新版本

Wrapper 已经存在时，可以用它更新自身配置：

```bash
./mvnw wrapper:wrapper -Dmaven=3.9.11
```

更新后提交 `mvnw`、`mvnw.cmd` 和 `.mvn/wrapper/` 的变化，并重新验证：

```bash
./mvnw clean test
```

对供应链校验要求较高的项目，可以在 `maven-wrapper.properties` 中配置 `distributionSha256Sum`，用于校验下载的 Maven 压缩包。

## 常见问题

### 为什么不用本机的 mvn？

可以使用，但 `mvn` 的版本取决于本机环境。仓库已经提供 Wrapper 时，优先使用 `./mvnw` 更容易复现团队和 CI 的构建结果。

### Wrapper 应该提交到 Git 吗？

应该提交 Wrapper 脚本和 `.mvn/wrapper/` 中的配置。下载到用户目录的 Maven、项目依赖和 `target/` 构建产物不应提交。

### mvnw 没有执行权限怎么办？

在 macOS 或 Linux 上执行：

```bash
chmod +x mvnw
```

然后把执行权限变化一起提交到 Git。

## 相关

- [[RabbitMQ入门实战]] — 本库中使用 Maven Wrapper 的示例项目
- [Apache Maven Wrapper 官方文档](https://maven.apache.org/tools/wrapper/)
