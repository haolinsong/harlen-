---
title: Docker 网络
type: concept
tags: [容器/Docker, 网络]
aliases: [Docker Networking, Docker容器网络, Docker Bridge网络, Docker容器通信]
sources: []
created: 2026-11-01
updated: 2026-11-01
domain_volatility: high
confidence: medium
---

# Docker 网络

Docker 网络为容器提供独立的网络视图，并通过网络连接、名称解析和端口发布控制容器之间以及容器与宿主机之间的通信路径。

## 核心要点

- 每个普通容器都有自己的网络环境；容器内的 `127.0.0.1` 只指向该容器本身，不指向宿主机或其他容器。
- 未指定 `--network` 时，容器会连接到默认 `bridge`；默认 bridge 上的容器可以通过 IP 通信，但不能直接用容器名互相解析。
- 用户自定义 bridge 网络会为同一网络中的容器提供名称解析。应用应通过容器名或网络别名寻找依赖，不应依赖可能变化的容器 IP。
- 同一 bridge 网络内的容器可直接访问彼此监听的端口，不需要先发布到宿主机。
- `--publish HOST_IP:HOST_PORT:CONTAINER_PORT` 用于让宿主机或宿主机外部的客户端访问容器端口；它与容器之间的内部通信不是一回事。
- `EXPOSE` 只记录镜像预期监听的端口，不会自动创建宿主机端口映射。

## 通信方向

| 发起方 | 目标 | 常用地址 | 是否需要 `--publish` |
| --- | --- | --- | --- |
| 同一自定义网络中的容器 | 另一个容器 | `容器名:容器端口` | 不需要 |
| 宿主机 | 容器 | `127.0.0.1:宿主机端口` | 需要 |
| Docker Desktop 中的容器 | macOS/Windows 宿主机服务 | `host.docker.internal:宿主机端口` | 宿主机服务不使用 Docker 的 `--publish` |
| 容器 | 自身进程 | `127.0.0.1:容器端口` | 不需要 |

## 默认 bridge 与自定义 bridge

| 对比 | 默认 `bridge` | 用户自定义 bridge |
| --- | --- | --- |
| 加入方式 | 未写 `--network` 时自动加入 | `--network NETWORK` 明确加入 |
| 按容器名通信 | 默认不支持 | 支持 Docker DNS 名称解析 |
| 项目隔离 | 所有未指定网络的容器混在一起 | 可以按项目创建独立网络 |
| 推荐用途 | 简单兼容场景 | 单机多容器应用与学习实验 |

用户自定义 bridge 的范围是单个 Docker Engine；跨多台 Docker 主机的通信不属于本阶段，应由其他网络驱动或编排系统处理。

## 与相邻概念的区别

- **容器端口与宿主机端口**：应用监听的是容器端口；`--publish` 另选一个宿主机入口，再把流量转发到容器端口。
- **`EXPOSE` 与端口发布**：`EXPOSE 80` 是镜像元数据；`--publish 127.0.0.1:8080:80` 才创建实际访问入口。
- **容器名与容器 IP**：容器名是同一自定义网络中的稳定访问入口；容器重建后 IP 可能改变。
- **网络与 Volume**：网络连接进程之间的请求；Volume 保存需要跨容器生命周期保留的数据。

## 前提与适用范围

本文以单个 Docker Engine 上的 Linux 容器和 bridge 网络为主。Docker Desktop 在 macOS/Windows 上通过 Linux VM 和后端转发实现容器网络，因此宿主机通常通过已发布端口访问容器，而不是直接依赖容器内部 IP。

参考（访问日期 2026-11-01）：

- [Networking overview](https://docs.docker.com/engine/network/)
- [Port publishing and mapping](https://docs.docker.com/engine/network/port-publishing/)
- [Docker Desktop networking how-tos](https://docs.docker.com/desktop/features/networking/networking-how-tos/)
- [Dockerfile reference: EXPOSE](https://docs.docker.com/reference/dockerfile/#expose)

## 相关

- [[Docker架构]] — 网络对象由 Docker Daemon 创建和管理
- [[Docker镜像与容器]] — 容器身份与运行时边界
- [[Docker数据持久化]] — 与网络并列的运行时资源
- [[04-Docker网络与容器通信]] — 面向学习的命令、图示和实验
- [[Docker学习路径]] — 本阶段在四周学习路线中的位置
