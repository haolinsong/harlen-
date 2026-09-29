---
title: Docker 学习路径
type: output
tags: [容器/Docker, 学习路径]
aliases: [Docker Learning Path, Docker学习路线, Docker四周学习计划]
created: 2026-09-29
updated: 2026-09-29
related: ["[[Docker]]", "[[容器与虚拟机]]", "[[Docker架构]]", "[[Docker核心学习笔记]]"]
---

# Docker 学习路径

## 一句话结论

用 4 周、每周 5～7 小时，按“理解对象 → 单容器 → 数据与网络 → Compose 与综合排障”的依赖顺序学习；当前只展开第 1 周，后续阶段学到时再增量建设。

## 当前进度

| 阶段 | 状态 | 已有入口 |
| --- | --- | --- |
| 第 1 周：基础模型与首个容器 | 已生成学习材料；本机尚未运行验证 | [[Docker核心学习笔记]]、[[Docker环境验证与首个容器]] |
| 第 2 周：镜像构建与数据 | 仅规划，尚未生成专题正文 | 后续补充 Dockerfile、构建缓存、Volume 与 Bind Mount |
| 第 3 周：网络与 Compose | 仅规划，尚未生成专题正文 | 后续补充 Docker 网络与 Docker Compose |
| 第 4 周：排障、安全与综合项目 | 仅规划，尚未创建综合实验 | 后续补充排障、安全、Registry 与综合实验 |

总预算约 20～28 小时。每周最后至少留 1 小时复盘，不以“看完页面”为完成标准，而以“能解释、能操作、能验证、能清理”为准。

## 第 1 周：先建立正确的容器模型

### 学习目标

- 解释容器解决了环境一致性、依赖交付和进程隔离中的哪些问题。
- 区分容器与虚拟机，知道容器共享内核的收益与安全边界。
- 区分 Docker、Engine、Daemon、CLI、Desktop、Registry 与 OCI。
- 区分镜像、容器、Repository、Tag 与 Digest。
- 解释 `run`、`create`、`start`、`stop`、`kill` 与 `rm` 的生命周期差异。

### 前置知识

- 能打开终端并运行命令。
- 知道进程、端口、文件系统和客户端/服务端的基本含义。
- 不要求 Linux 内核、虚拟化或网络专业知识。

### 核心概念与页面

- [[容器与虚拟机]]
- [[Docker]]
- [[Docker架构]]
- [[Docker镜像与容器]]
- [[Docker容器生命周期]]
- [[Docker环境验证与首个容器]]

### 推荐来源

- [What is Docker?](https://docs.docker.com/get-started/docker-overview/)
- [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
- [What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/)
- [Running containers](https://docs.docker.com/engine/containers/run/)
- [OCI Release Notices](https://opencontainers.org/release-notices/overview/)

### 动手任务与用时

| 任务 | 预计用时 |
| --- | ---: |
| 阅读基础模型并手绘一次组件关系 | 1.5 小时 |
| 比较容器与 VM，写出各自适用场景 | 0.5 小时 |
| 安装或确认 Docker 环境 | 1～2 小时 |
| 完成 `hello-world` 生命周期实验 | 1 小时 |
| 用 `inspect`、`ps -a`、`image ls` 解释观察结果 | 1 小时 |
| 自测、纠错和复述 | 1 小时 |

### 完成标准

- 不看笔记，能画出 CLI → API → Daemon → containerd/runc → 容器，以及 Daemon ↔ Registry。
- 能用一句话区分镜像与容器、停止与删除、Engine 与 Desktop。
- 能运行并安全清理明确命名的 `hello-world` 容器。
- 能解释为什么 `hello-world` 打印完后显示 `Exited (0)` 不是故障。
- 能说明 `latest` 是普通可变 Tag，Digest 才是内容不可变标识。

### 常见误区

- 把容器理解为轻量虚拟机。
- 只验证 `docker --version`，就认为 Daemon 已经可用。
- 把 Docker Desktop、Docker Engine、Docker CLI 当成同一个程序。
- 把停止容器当成删除容器，或把删除容器当成删除镜像。
- 认为 `latest` 自动表示最新版或稳定版。

### 复习题

1. 为什么 Linux 容器不能脱离兼容内核运行？
2. CLI 可以正常输出版本时，为什么 `docker run` 仍可能失败？
3. 同一个镜像能否创建多个容器？这些容器共享什么、不共享什么？
4. `docker start` 与再次执行 `docker run` 有什么本质差别？
5. Tag 和 Digest 分别适合解决什么问题？

答案要点见 [[Docker核心学习笔记]] 的“自测答案与解析”。

## 第 2 周：构建自己的镜像并理解数据去向

### 学习目标

- 能读写基础 Dockerfile，区分 `RUN`、`CMD`、`ENTRYPOINT`、`COPY`、`ARG` 与 `ENV`。
- 理解构建上下文、`.dockerignore`、镜像层和缓存失效顺序。
- 使用 BuildKit 与多阶段构建减小运行镜像并提高构建效率。
- 区分容器可写层、Volume、Bind Mount，以及 `COPY` 与运行时挂载。

### 前置知识

完成第 1 周；能独立运行、检查和删除容器。

### 核心概念与后续页面

计划建设：Dockerfile 与镜像构建、Docker 构建缓存、Docker 存储。当前不创建空页，学到本阶段时再落盘。

### 推荐来源

- [Dockerfile overview](https://docs.docker.com/build/concepts/dockerfile/)
- [Build cache](https://docs.docker.com/build/cache/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker storage](https://docs.docker.com/engine/storage/)

### 动手任务与用时

- 容器化一个只返回文本或 JSON 的简单 Web 服务：2 小时。
- 调整 Dockerfile 指令顺序并观察缓存命中：1.5 小时。
- 改为多阶段构建并比较镜像大小：1 小时。
- 分别用 Volume 与 Bind Mount 保存/共享数据：1.5 小时。
- 自测与清理：1 小时。

### 完成标准

- 能预测修改依赖文件和源码文件分别会让哪些构建层失效。
- 能解释 `COPY` 在构建时写入镜像，Bind Mount 在运行时覆盖容器路径。
- 能证明删除容器后命名 Volume 中的数据仍然存在。
- 能给 Dockerfile 选择正确的主进程启动方式。

### 常见误区

- 把镜像层当作可以原地修改的目录。
- 将密码写入 `ARG`、`ENV` 或镜像层。
- 把依赖安装和源码复制混在同一缓存边界。
- 认为挂载路径会自动把镜像内原文件复制到宿主机。

### 复习题

1. 为什么频繁变化的文件通常应在 Dockerfile 后面复制？
2. `RUN`、`CMD` 和 `ENTRYPOINT` 分别发生在构建期还是运行期？
3. Volume 与 Bind Mount 的生命周期和控制方有何不同？

## 第 3 周：让多个容器可靠通信

### 学习目标

- 理解默认 bridge、自定义网络、服务发现和端口发布。
- 区分容器内 `localhost`、宿主机 `localhost` 与其他容器的服务名。
- 使用 Compose v2 描述服务、网络、数据卷、环境变量和健康检查。
- 区分 `docker compose up`、`run` 与 `exec`。

### 前置知识

完成第 2 周；知道应用端口、持久数据和镜像构建流程。

### 核心概念与后续页面

计划建设：Docker 网络、Docker Compose。Compose 文件只描述期望配置，不替代镜像和容器的基础模型。

### 推荐来源

- [Docker networking](https://docs.docker.com/engine/network/)
- [Port publishing](https://docs.docker.com/engine/network/port-publishing/)
- [Compose overview](https://docs.docker.com/compose/)
- [Compose Specification](https://compose-spec.io/)

### 动手任务与用时

- 在自定义网络中让两个容器通过名称通信：1.5 小时。
- 发布 Web 端口并从宿主机验证：1 小时。
- 把 Web 服务与数据库写成 `compose.yaml`：2 小时。
- 增加命名 Volume、健康检查和启动依赖：1.5 小时。
- 自测与清理：1 小时。

### 完成标准

- 能从宿主机和容器内分别解释 `localhost` 指向谁。
- 能在不硬编码容器 IP 的情况下，用 Compose 服务名访问依赖。
- 能运行 `docker compose config` 检查解析后的配置。
- 能在不删除命名 Volume 的前提下停止并重建服务。

### 常见误区

- 认为 `EXPOSE` 会自动把端口开放到宿主机。
- 在应用配置中用 `localhost` 访问另一个容器。
- 用固定容器 IP 代替服务名和 Docker DNS。
- 把 `depends_on` 当作业务已经可用的完整保证。

### 复习题

1. `EXPOSE 8080` 与 `-p 8080:8080` 的效果有何不同？
2. 为什么同一 Compose 网络中的服务应该通过服务名通信？
3. `docker compose run` 和 `docker compose exec` 分别创建什么？

## 第 4 周：从“能运行”走向“能维护”

### 学习目标

- 使用 logs、inspect、stats、events 和容器内检查定位常见故障。
- 识别启动失败、端口冲突、DNS、挂载、权限、健康检查和平台不匹配问题。
- 理解最小镜像、非 root、只读文件系统、最小权限、Digest 固定和秘密管理等基础实践。
- 掌握 Registry 的基本 pull/tag/push 模型，但不在本任务中登录或推送真实仓库。
- 完成一个 Web 服务 + 持久化服务的 Compose 综合实验。

### 前置知识

完成前三周；能构建镜像并解释网络、挂载和 Compose 配置。

### 核心概念与后续页面

计划建设：Docker 故障排查、Docker 安全与最佳实践、Docker 综合实验。综合项目将在本机具备 Docker 后再执行端到端验证。

### 推荐来源

- [Docker Engine security](https://docs.docker.com/engine/security/)
- [Docker CLI reference](https://docs.docker.com/reference/cli/docker/)
- [Docker Scout](https://docs.docker.com/scout/)
- [Docker Hub repositories](https://docs.docker.com/docker-hub/repos/)

### 动手任务与用时

- 制造并修复 4 类故障：端口占用、错误环境变量、数据库不可达、挂载权限：2 小时。
- 为容器补充健康检查、资源限制和非 root 用户：1.5 小时。
- 完成综合项目验收与持久化验证：2 小时。
- 复盘开发配置与生产配置差异：1 小时。

### 完成标准

- 面对失败时先收集状态、日志、配置和网络证据，不靠反复重启猜测。
- 能解释开发环境“能跑”为什么不等于生产环境“安全可靠”。
- 能只清理综合实验创建的容器、网络和数据卷，并明确数据丢失边界。
- 能列出后续 CI/CD、镜像供应链、容器编排和 Kubernetes 的学习顺序。

### 常见误区

- 默认使用 `--privileged` 或把 Docker socket 挂进容器解决问题。
- 在运行中容器里手工修复，然后把它当成可复现部署。
- 使用浮动 Tag 却期望每次部署内容完全一致。
- 用 `docker system prune -a --volumes` 作为日常排障第一步。

### 复习题

1. 一个容器不断重启时，最先应该保留哪些证据？
2. 为什么 root 容器、可写根文件系统和过多 capabilities 会扩大风险？
3. 使用 Digest 固定镜像后，安全更新流程为何仍不能省略？

## 后续方向

完成 4 周后再考虑：在 CI/CD 中构建与扫描镜像、软件物料清单与签名证明、远程 Registry 权限、Rootless、容器运行时深入、Kubernetes。Kubernetes 不是学习 Docker 基础的前置条件。

## 怎么用

每次只推进一周：先读对应输出页，再进入概念页理解原理，最后按 howto 或 `code/` 实验验证。下一阶段开始前，把上一阶段的完成标准逐条演示一遍；做不到的条目先回补，不用靠“继续看更多”掩盖模型缺口。

## 相关

- [[Docker核心学习笔记]] — 第 1 周当前学习正文
- [[Docker环境验证与首个容器]] — 第一个可复现实验
- [[Docker架构]] — 组件依赖主线
- [[Docker镜像与容器]] — 后续构建、存储与 Compose 的对象基础
