---
title: Docker
type: entity
tags: [容器/Docker, 开发工具]
aliases: [Docker平台, Docker Platform]
sources: []
created: 2026-09-29
updated: 2026-09-29
domain_volatility: high
confidence: medium
---

# Docker

Docker 是一套用于构建、分发和运行容器化应用的平台与工具集合；它不是容器技术本身，也不是某一个单独的后台进程。

## 核心要点

| 名称 | 主要职责 | 不应混同为 |
| --- | --- | --- |
| Docker Engine | 提供 Docker API，并管理镜像、容器、网络和数据卷 | Docker Desktop 的全部功能 |
| Docker Daemon（`dockerd`） | 接收 API 请求并执行容器与镜像管理 | 用户输入命令的终端程序 |
| Docker CLI（`docker`） | 把命令转换为 API 请求，可连接本地或远程 Daemon | 容器运行时本身 |
| Docker Desktop | macOS、Windows、Linux 上的桌面产品，打包 Engine、CLI、Compose 等能力 | Docker Engine 的同义词 |
| Docker Compose | 用声明式配置管理一组相关容器 | Kubernetes 或生产集群调度器 |
| Docker Hub / Registry | 保存和分发镜像 | 运行容器的主机 |

- Docker 采用 Client–Server 架构：CLI 和 Compose 是客户端，Daemon 是主要服务端。
- Docker Engine 使用 `containerd` 管理容器生命周期；默认由 `runc` 一类底层运行时创建容器进程。普通入门操作不需要直接使用这两个组件。
- Docker 的开源上游与 Moby 项目关系紧密；Docker 产品在这些开源组件上提供面向开发者的完整体验。
- Docker 使用并扩展 OCI（Open Container Initiative）定义的镜像格式、运行时和分发规范，因此 OCI 与 Docker 是“行业规范与具体实现/产品”的关系。
- Docker Desktop 在 macOS、Windows 上通过 Linux 虚拟机运行 Linux 容器；Docker Desktop for Linux 也使用独立虚拟机和 `desktop-linux` context，不能把它与宿主机上单独安装的 Docker Engine 当成同一个实例。

## 与相邻概念的区别

- **Docker 与容器**：Docker 是工具和平台；容器是被隔离运行的进程及其配置、文件系统视图和资源边界。
- **Docker 与虚拟机**：Docker 可以运行在虚拟机内。macOS、Windows 上的 Docker Desktop 正是常见例子。
- **Docker 与 Kubernetes**：Docker 聚焦镜像构建与单机容器工作流；Kubernetes 负责跨节点编排，二者不在同一抽象层。
- **Docker 与 OCI**：OCI 规定可互操作的格式和行为；Docker 是实现并使用这些规范的产品生态之一。

## 前提与适用范围

本页基于 2026-09-29 访问的官方资料。当天 Docker Desktop 最新发行说明为 4.93.0；具体安装要求、许可和组件版本会变化，应以官方当前页面为准，而不是把本页版本号当作安装约束。

参考：

- [What is Docker?](https://docs.docker.com/get-started/docker-overview/)
- [Docker Desktop](https://docs.docker.com/desktop/)
- [Alternative container runtimes](https://docs.docker.com/engine/daemon/alternative-runtimes/)
- [Moby 项目](https://github.com/moby/moby)
- [OCI Release Notices](https://opencontainers.org/release-notices/overview/)
- [Docker Desktop release notes](https://docs.docker.com/desktop/release-notes/)

## 相关

- [[Docker架构]] — CLI、Daemon、Registry 与运行时的调用关系
- [[容器与虚拟机]] — 隔离方式与平台差异
- [[Docker镜像与容器]] — Docker 管理的两个核心对象
- [[Docker核心学习笔记]] — 面向初学者的第一阶段复习入口
