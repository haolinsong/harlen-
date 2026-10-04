# Docker Learning Labs

这是 Docker 四周学习专题的配套实验目录。每个子目录只验证当前阶段需要的 Docker 能力，避免提前混入 Compose、数据库或生产编排。

当前实验：

- `02-image-and-storage/`：使用多阶段 Dockerfile 构建 Nginx 镜像，并验证命名 Volume 与 Bind Mount。

学习入口：

- `outputs/容器/02-Dockerfile与镜像构建.md`
- `outputs/容器/03-Docker数据存储.md`
- `wiki/howto/容器/Docker镜像构建与挂载实验.md`

所有资源都使用明确名称，清理时只处理本实验创建的容器、镜像和 Volume。不要用全局 prune 命令代替精确清理。
