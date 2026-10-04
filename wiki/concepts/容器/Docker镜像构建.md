---
title: Docker 镜像构建
type: concept
tags: [容器/Docker, 镜像构建]
aliases: [Docker Build, Dockerfile构建, Docker构建缓存]
sources: []
created: 2026-09-30
updated: 2026-09-30
domain_volatility: high
confidence: medium
---

# Docker 镜像构建

Docker 镜像构建是 BuildKit 根据 Dockerfile 和构建上下文生成不可变镜像的过程，并通过依赖关系与缓存减少重复工作。

## 核心要点

- Dockerfile 提供有序构建指令；构建上下文限定 `COPY`、`ADD` 等步骤能访问的文件。
- `.dockerignore` 在上下文交给构建器前排除无关文件，减少传输和误包含风险。
- `RUN` 在构建时执行并保存结果；`CMD` 与 `ENTRYPOINT` 定义容器启动行为，不会在构建时运行应用。
- `ARG` 主要用于构建期输入；`ENV` 会保存在镜像配置中并成为容器默认环境。二者都不适合传递秘密。
- BuildKit 为每个步骤计算可复用结果；某一步缓存失效时，其后依赖步骤需要重新处理。
- 多阶段构建使用多个 `FROM` 分离构建环境与运行环境，并用 `COPY --from` 只传递所需构建产物。

## 与相邻概念的区别

- **构建与运行**：构建把 Dockerfile 和项目文件变成镜像；运行从镜像创建容器并启动进程。
- **Dockerfile 与镜像**：Dockerfile 是构建说明，镜像是构建结果；同一 Dockerfile 在基础镜像或输入改变后可能产生不同镜像内容。
- **镜像层与构建缓存**：镜像层属于最终镜像内容；构建缓存是构建器为了复用步骤保存的结果，两者有关联但不是同一个管理对象。
- **`COPY` 与 Bind Mount**：`COPY` 在构建时把上下文文件写入镜像；Bind Mount 在运行时把宿主机路径接入容器，不改变镜像。
- **`CMD` 与 `ENTRYPOINT`**：`CMD` 常用作可覆盖的默认命令或参数；Exec form 的 `ENTRYPOINT` 常用作稳定的主程序，运行参数会追加在后面并替换 `CMD` 默认值。

## 前提与适用范围

本页以现代 Docker 的 BuildKit 构建后端为基线。具体 Dockerfile 语法能力受所选语法版本、BuildKit 和 Docker Engine/Desktop 版本影响；版本敏感功能应查当前官方 reference。

参考：

- [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
- [Build context](https://docs.docker.com/build/concepts/context/)
- [Docker build cache](https://docs.docker.com/build/cache/)
- [BuildKit](https://docs.docker.com/build/buildkit/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## 相关

- [[Docker镜像与容器]] — 镜像层和容器可写层
- [[Docker数据持久化]] — 运行期数据位置
- [[Docker镜像构建与挂载实验]] — 可复制的构建步骤
- [[02-Dockerfile与镜像构建]] — 面向学习的详细串联
