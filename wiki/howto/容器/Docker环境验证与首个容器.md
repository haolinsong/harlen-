---
title: Docker 环境验证与首个容器
type: howto
tags: [容器/Docker, 入门实验]
aliases: [Docker安装验证, Docker Hello World, 运行第一个Docker容器]
sources: []
created: 2026-09-29
updated: 2026-09-29
verified: ""
env: "macOS/Windows/Linux · Docker Desktop 或 Docker Engine · Docker CLI"
domain_volatility: high
confidence: medium
---

# Docker 环境验证与首个容器

这份操作用一个可安全删除的 `hello-world` 容器验证 CLI、Daemon、Registry、镜像拉取和容器生命周期是否连通。

## 适用环境

- macOS：Docker Desktop，Apple Silicon 或 Intel 均可；应下载与 CPU 架构匹配的安装包。
- Windows：Docker Desktop，学习 Linux 容器时通常使用 WSL 2 或受支持的虚拟化后端。
- Linux：可使用 Docker Engine；也可使用 Docker Desktop，但 Desktop 使用独立 VM 和 `desktop-linux` context。
- 命令均以 Compose v2 所在的现代 Docker CLI 为基线；本实验本身不使用 Compose。

> [!question] 待验证
> 当前知识库执行环境中没有 `docker` 命令，因此以下命令已按 2026-09-29 的官方 CLI 文档静态核对，但尚未在本机实际运行。`verified` 留空，不能把本页视为已完成端到端验证。

## 前置条件

Mac 初次安装者先阅读 [[Docker核心学习笔记]] 开头的「0. 先在 Mac 上安装 Docker」，其中包含 Homebrew 安装、首次启动、基础验收和常用命令。完成后回到本页观察容器生命周期；安装自检使用 `--rm`，本页实验刻意保留容器以便再次启动。

本页不自动安装 Docker，也不修改系统服务。请根据操作系统使用官方安装入口：

- [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/)
- [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/)
- [Docker Engine for Linux](https://docs.docker.com/engine/install/)
- [Docker Desktop for Linux](https://docs.docker.com/desktop/setup/install/linux/)

Docker Desktop 的商用许可、系统要求和支持范围会变化，安装前应阅读当前官方页面。Linux 不应为了省事直接执行来源不明的远程安装脚本。

## 目标

完成后应能证明：

1. Docker CLI 已安装。
2. CLI 能连接到预期的 Docker Daemon。
3. Daemon 能从 Registry 拉取官方 `hello-world` 镜像。
4. 容器主进程完成后，容器停止但没有自动消失。
5. 同一容器可以再次启动，删除容器不会自动删除镜像。

## 步骤

### 1. 区分客户端、服务端与 Compose

以下命令只读取版本和当前连接信息，不创建资源：

```bash
docker --version
docker version
docker compose version
docker context show
docker context ls
```

- `docker --version` 只能证明 CLI 可执行。
- `docker version` 同时显示 Client 与 Server；缺少 Server 部分通常表示 Daemon 未启动、权限不足或 context 指错。
- `docker compose version` 验证 Compose v2 插件；推荐命令形式是 `docker compose`，不是旧的 `docker-compose`。
- `docker context show` 显示当前 CLI 的连接目标。Linux 同时安装 Engine 与 Desktop 时尤其需要核对。

可进一步读取 Daemon 信息：

```bash
docker info
```

预期结果是命令成功返回 Server、Storage Driver、当前容器和镜像数量等信息。不要把输出中的内部路径、Registry 凭据配置或企业代理信息随意公开。

### 2. 创建并运行一次性输出程序

在任意普通工作目录运行：

```bash
docker run --name docker-basics-hello hello-world:latest
```

参数解释：

- `docker run`：需要时先拉取镜像，然后创建并启动一个新容器。
- `--name docker-basics-hello`：为本实验容器指定唯一名称，方便精确检查和清理。
- `hello-world:latest`：Docker Official Image 的默认教学 Tag；Tag 可变，只适合这个入门验证，不代表生产固定版本方案。

第一次运行通常会显示本地找不到镜像、逐层下载、创建容器以及 `Hello from Docker!`。程序打印完成后主进程退出，因此容器会停止；这不是启动失败。

### 3. 分别观察镜像和已停止容器

```bash
docker container ls
docker container ls -a --filter name=docker-basics-hello
docker image ls hello-world
docker container inspect \
  --format '{{.State.Status}} exit={{.State.ExitCode}} image={{.Config.Image}}' \
  docker-basics-hello
```

预期现象：

- `docker container ls` 不显示该容器，因为它已经停止。
- 加 `-a` 后能看到 `docker-basics-hello`，状态为 `Exited`。
- 镜像列表仍有 `hello-world`。
- `inspect` 应显示类似 `exited exit=0 image=hello-world:latest`；具体大小写和格式以本机版本为准。

### 4. 启动同一个容器

```bash
docker start --attach docker-basics-hello
```

`start` 不会创建新容器，而是重新启动原来的容器。`--attach` 把本次标准输出连接到当前终端，因此应再次看到欢迎信息；程序结束后容器再次进入 `Exited`。

检查是否仍然只有一个同名容器：

```bash
docker container ls -a --filter name=docker-basics-hello
```

### 5. 精确清理本实验容器

确认容器已经停止后执行：

```bash
docker rm docker-basics-hello
```

验证容器已经删除、镜像仍然存在：

```bash
docker container ls -a --filter name=docker-basics-hello
docker image ls hello-world
```

第一条命令应不再返回该容器；第二条仍可显示镜像。这正是“删除容器不等于删除镜像”。

## 验证

逐项确认：

- [ ] `docker version` 同时显示 Client 和 Server。
- [ ] 当前 context 是预期的本地 Docker Engine 或 Docker Desktop。
- [ ] `docker run` 能拉取 `hello-world` 并打印欢迎信息。
- [ ] `docker container ls -a` 能看到退出码为 0 的停止容器。
- [ ] `docker start --attach` 再次运行同一个容器，没有创建第二个容器。
- [ ] `docker rm docker-basics-hello` 后只删除实验容器，镜像仍在。

只有全部完成，才能把本页 `verified` 更新为实际日期。

## 清理与回滚

常规清理只需要删除这个明确命名的实验容器：

```bash
docker rm docker-basics-hello
```

如果容器意外仍在运行，先优雅停止，再删除：

```bash
docker stop docker-basics-hello
docker rm docker-basics-hello
```

可选：确认没有其他任务依赖 `hello-world:latest` 后再删除本地镜像：

```bash
docker image rm hello-world:latest
```

> [!warning] 数据影响
> 不要为这个实验执行 `docker system prune`、`docker image prune -a` 或批量删除命令。它们可能清理与本任务无关的容器、镜像、网络或构建缓存。上面的命令只针对 `docker-basics-hello` 和可选的 `hello-world:latest`。

## 已知坑

| 现象 | 常见原因 | 处理方向 |
| --- | --- | --- |
| `command not found: docker` | CLI 未安装或不在 `PATH` | 使用对应平台官方安装文档；不要猜测安装命令 |
| `Cannot connect to the Docker daemon` | Desktop/Daemon 未启动，context 错误或权限不足 | 启动预期的 Docker 产品，检查 `docker context ls` 和 `docker version` |
| 只有 Client、没有 Server | CLI 正常但服务端不可达 | 不要重复安装 CLI；先检查 Daemon 与 context |
| `Conflict. The container name ... is already in use` | 上一次实验容器仍存在 | 用 `docker container ls -a` 核对后，只删除同名实验容器 |
| 拉取超时或 TLS/代理错误 | 网络、代理、证书或 Registry 访问受限 | 检查 Docker Daemon/Desktop 的代理配置，不只检查终端代理 |
| `no matching manifest` / `exec format error` | 镜像不支持当前 OS/CPU，或跨架构模拟失败 | 用 `docker image inspect` 核对平台；选择支持的镜像变体 |
| Linux `permission denied` | 当前用户无权访问 Docker socket | 按官方 Rootless 或权限文档处理；不要盲目 `chmod 666 /var/run/docker.sock` |
| Windows 命令存在但 Linux 容器不可用 | Desktop 后端、WSL 2 或容器模式不匹配 | 检查 Docker Desktop 状态与当前容器模式 |

## 安全提醒

- Docker API/Daemon 控制权限很高，只让可信用户访问。
- 不把 Docker socket 挂载进不可信容器。
- 不为解决普通权限问题默认使用 `sudo docker ...` 或开放 socket 权限。
- 拉取镜像前核对发布者、Tag、支持平台和维护状态；生产环境还应使用 Digest、签名/证明和漏洞扫描。
- `hello-world:latest` 是学习验证，不是生产部署模板。

参考：

- [hello-world Docker Official Image](https://hub.docker.com/_/hello-world)
- [docker container run](https://docs.docker.com/reference/cli/docker/container/run/)
- [docker container create](https://docs.docker.com/reference/cli/docker/container/create/)
- [docker container stop](https://docs.docker.com/reference/cli/docker/container/stop/)
- [docker container rm](https://docs.docker.com/reference/cli/docker/container/rm/)

## 相关

- [[Docker架构]] — 为什么要分别验证 Client、Server 和 context
- [[Docker镜像与容器]] — 镜像、容器、Tag 与 Digest
- [[Docker容器生命周期]] — `run`、`start`、`stop`、`rm` 的区别
- [[Docker核心学习笔记]] — 基础概念、练习和自测
