# 实验 02：镜像构建与数据存储

本实验用一个很小的静态网页说明四件事：Dockerfile 如何生成镜像、BuildKit 如何复用缓存、多阶段构建如何只保留运行产物，以及 Volume 与 Bind Mount 的数据分别保存在哪里。

## 文件结构

```text
02-image-and-storage/
├── Dockerfile       # 两阶段构建：生成网页，再复制进 Nginx
├── .dockerignore    # 从构建上下文排除无关文件
├── message.txt      # 构建输入
└── README.md        # 本说明
```

> **BuildKit**：Docker 当前使用的镜像构建后端，负责解析 Dockerfile、计算缓存并输出镜像。

> **多阶段构建**：一个 Dockerfile 使用多个 `FROM`。前一阶段负责生成文件，最终阶段只复制运行所需产物。

## 构建与运行

确保 Docker Desktop Engine 已启动，然后在本目录执行：

```bash
docker build --tag harlan/docker-build-demo:1.0 .

docker run --name docker-build-demo \
  --detach \
  --publish 127.0.0.1:8080:80 \
  harlan/docker-build-demo:1.0

curl http://127.0.0.1:8080
```

预期返回：

```text
HELLO FROM HARLAN'S DOCKER BUILD LAB.
```

停止并删除容器：

```bash
docker stop docker-build-demo
docker rm docker-build-demo
```

Volume 与 Bind Mount 的完整验证和清理步骤见 `wiki/howto/容器/Docker镜像构建与挂载实验.md`。

## 已知限制

- 本实验只提供静态网页，不包含数据库、Compose 和自定义网络；这些属于下一学习阶段。
- 基础镜像 Tag 会继续更新。本文档记录的是 2026-09-30 核验可用的标签，长期复现还应记录 Digest。
- 2026-09-30 已在 macOS Docker Desktop 4.93.0、Engine 29.8.1 上完成构建、HTTP、缓存、Volume 和 Bind Mount 验证；临时实验资源已清理。
