---
title: Docker 数据持久化
type: concept
tags: [容器/Docker, 数据存储]
aliases: [Docker Storage, Docker Volume, Docker Bind Mount, Docker挂载]
sources: []
created: 2026-09-30
updated: 2026-09-30
domain_volatility: high
confidence: medium
---

# Docker 数据持久化

Docker 数据持久化通过 Volume 或 Bind Mount 把重要数据放在容器可写层之外，使数据生命周期不再绑定某一个容器。

## 核心要点

- 未挂载路径的写入进入容器可写层；删除容器时，该层随容器删除。
- Volume 由 Docker 创建和管理，可在容器删除后继续存在，也可被新的容器重新挂载。
- Bind Mount 直接连接 Daemon 主机上的指定路径，宿主机与容器可以看到并修改同一份文件。
- `--mount` 用显式字段声明 `type`、`src` 和 `dst`，通常比 `-v` 更易读；Bind Mount 源路径不存在时默认报错。
- 挂载到容器中已有内容的路径时，挂载内容会遮住该路径原有的镜像文件；底层镜像没有被修改。
- 删除 Volume 是数据删除操作；`docker volume prune` 可能影响其他项目，不应作为单项目实验的常规清理方式。

## 与相邻概念的区别

- **Volume 与容器可写层**：Volume 生命周期独立于容器；可写层只属于一个容器。
- **Volume 与 Bind Mount**：Volume 的宿主机存储位置由 Docker 管理；Bind Mount 的来源路径由用户明确选择，并与主机目录结构耦合。
- **`COPY` 与挂载**：`COPY` 把文件固化进镜像；挂载只在容器运行时改变指定路径所呈现的内容。
- **停止与删除**：停止容器通常保留容器可写层；删除容器才移除该层。两者默认都不会删除命名 Volume。

## 前提与适用范围

Docker Desktop 的 Daemon 位于 Linux VM 中，但 Desktop 会处理 macOS/Windows 原生路径到 Linux 容器的 Bind Mount 共享。性能、权限和大小写行为仍受宿主文件系统与 Desktop 设置影响，应在目标环境验证。

参考：

- [Docker storage](https://docs.docker.com/engine/storage/)
- [Volumes](https://docs.docker.com/engine/storage/volumes/)
- [Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)

## 相关

- [[Docker镜像与容器]] — 可写层与 Copy-on-Write
- [[Docker镜像构建]] — `COPY` 和镜像生成
- [[Docker镜像构建与挂载实验]] — Volume 与 Bind Mount 验证
- [[03-Docker数据存储]] — 面向学习的详细说明
