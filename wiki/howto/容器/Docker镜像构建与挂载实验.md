---
title: Docker 镜像构建与挂载实验
type: howto
tags: [容器/Docker, 镜像构建]
aliases: [Dockerfile构建实验, Docker Volume与Bind Mount实验]
sources: []
created: 2026-09-30
updated: 2026-09-30
verified: 2026-09-30
env: "macOS Docker Desktop 或 Linux Docker Engine · BuildKit · Docker CLI"
domain_volatility: high
confidence: medium
---

# Docker 镜像构建与挂载实验

这份操作用一个两阶段 Nginx 镜像串联 Dockerfile、构建上下文、缓存、命名 Volume 和 Bind Mount，并只清理本实验创建的资源。

## 适用环境

- macOS：Docker Desktop Engine 已启动。
- Linux：Docker Engine 与 BuildKit 可用。
- Windows：可在 WSL 2 Shell 中使用相同的 Linux 命令；PowerShell 路径写法需要相应调整。
- 实验基线：Docker Desktop 4.93.0、Engine/CLI 29.8.1、Buildx 0.37.1、`alpine:3.23`、`nginx:1.31.6-alpine`。

> [!info] 已验证
> 2026-09-30 已在 macOS Docker Desktop 4.93.0 上完成镜像构建、缓存命中、HTTP 请求、命名 Volume 跨容器读取和 readonly Bind Mount 验证。临时容器、实验 Volume 与自定义镜像已清理。

验证时解析到 `alpine:3.23@sha256:85fe1e81...` 与 `nginx:1.31.6-alpine@sha256:df221db8...`；正文保留易读 Tag，后续严格复现时应使用本机重新核对后的完整 Digest。

## 前置条件

从知识库根目录进入实验目录：

```bash
cd code/docker-learning-labs/02-image-and-storage
```

确认 CLI 能连接 Engine：

```bash
docker version
docker buildx version
```

`docker version` 应同时显示 Client 与 Server。只有 Client 时先确认 Docker Desktop Engine 或 Linux Daemon 是否正在运行。

## 目标

1. 从 Dockerfile 构建本地镜像。
2. 观察相同输入的第二次构建复用缓存。
3. 运行镜像并通过 HTTP 验证构建产物。
4. 用两个不同容器证明命名 Volume 独立存在。
5. 用 Bind Mount 让 Nginx 读取宿主机网页。

## 步骤

### 1. 查看实验输入

```bash
ls -la
sed -n '1,120p' Dockerfile
cat .dockerignore
cat message.txt
```

目录应至少包含 `Dockerfile`、`.dockerignore`、`message.txt` 和 `README.md`。构建上下文是当前目录，但 `.dockerignore` 会排除 README、本地 Bind Mount 目录和版本控制文件。

### 2. 构建镜像

```bash
docker build \
  --tag harlan/docker-build-demo:1.0 \
  .
```

预期构建输出依次显示：读取 Dockerfile 和上下文、拉取或读取两个基础镜像、执行 `COPY` 与 `RUN`、从 `build` 阶段复制 `index.html`，最后给镜像设置 Tag。

查看结果和构建历史：

```bash
docker image ls harlan/docker-build-demo
docker image history harlan/docker-build-demo:1.0
```

再次执行完全相同的构建：

```bash
docker build \
  --tag harlan/docker-build-demo:1.0 \
  .
```

多数步骤应显示缓存命中，例如 `CACHED`。具体输出格式由当前 BuildKit 版本决定。

### 3. 运行并验证镜像

```bash
docker run --name docker-build-demo \
  --detach \
  --publish 127.0.0.1:8080:80 \
  harlan/docker-build-demo:1.0
```

验证容器状态和网页：

```bash
docker container ls --filter name=docker-build-demo
curl http://127.0.0.1:8080
```

预期响应：

```text
HELLO FROM HARLAN'S DOCKER BUILD LAB.
```

停止并删除这个容器，保留镜像供后续步骤检查：

```bash
docker stop docker-build-demo
docker rm docker-build-demo
```

### 4. 验证命名 Volume 的生命周期

```bash
docker volume create docker-learning-data

docker run --rm \
  --mount type=volume,src=docker-learning-data,dst=/data \
  alpine:3.23 \
  sh -c 'printf "saved in volume\n" > /data/message.txt'

docker run --rm \
  --mount type=volume,src=docker-learning-data,dst=/data \
  alpine:3.23 \
  cat /data/message.txt
```

第二个容器应输出 `saved in volume`。两个一次性容器都已经删除，但 Volume 仍可通过下面的命令看到：

```bash
docker volume inspect docker-learning-data
```

### 5. 验证 Bind Mount

```bash
mkdir -p bind-content
printf '<h1>Hello from Bind Mount</h1>\n' > bind-content/index.html

docker run --name docker-bind-demo \
  --rm \
  --detach \
  --publish 127.0.0.1:8081:80 \
  --mount type=bind,src="$(pwd)/bind-content",dst=/usr/share/nginx/html,readonly \
  nginx:1.31.6-alpine

curl http://127.0.0.1:8081
```

预期响应包含 `Hello from Bind Mount`。本次没有重新构建镜像；Nginx 直接读取宿主机 `bind-content/`。

停止容器：

```bash
docker stop docker-bind-demo
```

`--rm` 会在停止后自动删除容器，不会删除宿主机的 `bind-content/`。

## 验证

用下面的读取操作核对最终状态：

```bash
docker image ls harlan/docker-build-demo
docker container ls -a --filter name=docker-build-demo
docker container ls -a --filter name=docker-bind-demo
docker volume inspect docker-learning-data
cat bind-content/index.html
```

预期状态：实验镜像存在；两个实验容器均不存在；命名 Volume 存在；宿主机 Bind Mount 文件存在。

## 清理与回滚

确认不再需要实验数据后，精确删除本实验创建的 Volume 和镜像：

```bash
docker volume rm docker-learning-data
docker image rm harlan/docker-build-demo:1.0
```

`bind-content/` 是本地学习文件，可保留用于后续修改。若要删除，应由 Harlan 明确决定；本实验不会自动删除宿主机文件。

> [!warning] 数据影响
> `docker volume rm docker-learning-data` 会永久删除该 Volume 内的数据。不要用 `docker volume prune`、`docker builder prune` 或 `docker system prune` 代替精确清理，它们可能影响其他项目。

## 已知坑

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `docker version` 只有 Client | Engine 未运行、context 错误或 socket 权限不足 | 先恢复 Server 连接再构建 |
| `COPY message.txt` 找不到文件 | 命令不在实验目录运行，或上下文选择错误 | 确认末尾 `.` 指向包含该文件的目录 |
| 8080 或 8081 端口占用 | 宿主机已有进程监听 | 只修改冒号左侧宿主机端口，例如 `18080:80` |
| Bind Mount 源路径不存在 | `--mount` 默认不自动创建源目录 | 先执行 `mkdir -p bind-content` |
| 镜像中的网页被“覆盖” | Bind Mount 挂在 Nginx 默认网页目录 | 这是挂载遮蔽行为；停止容器后镜像内容仍在 |
| `volume is in use` | 仍有容器引用该 Volume | 用 `docker ps -a --filter volume=docker-learning-data` 精确定位 |

参考：

- [Dockerfile overview](https://docs.docker.com/build/concepts/dockerfile/)
- [Build context](https://docs.docker.com/build/concepts/context/)
- [Docker build cache](https://docs.docker.com/build/cache/)
- [Volumes](https://docs.docker.com/engine/storage/volumes/)
- [Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)

## 相关

- [[Docker镜像构建]] — Dockerfile、BuildKit 与缓存原理
- [[Docker数据持久化]] — Volume 与 Bind Mount 的生命周期
- [[02-Dockerfile与镜像构建]] — 第二阶段学习笔记
- [[03-Docker数据存储]] — 第三阶段学习笔记
