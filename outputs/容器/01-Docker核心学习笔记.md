---
title: 01 Docker 核心学习笔记
type: output
tags: [容器/Docker, 基础]
aliases: [Docker 核心学习笔记, Docker核心学习笔记, Docker基础学习笔记, Docker核心概念, Docker入门笔记]
created: 2026-09-29
updated: 2026-09-30
related: ["[[Docker]]", "[[容器与虚拟机]]", "[[Docker架构]]", "[[Docker镜像与容器]]", "[[Docker容器生命周期]]", "[[Docker环境验证与首个容器]]", "[[Docker学习路径]]"]
---

# 01 Docker 核心学习笔记

这是 Docker 四周学习专题的第一阶段。Mac 用户先完成下面的安装与验证，再学习容器、镜像和生命周期；这些概念是后续 Dockerfile、存储、网络和 Compose 的基础。

## 0. 先在 Mac 上安装 Docker

本节使用 Homebrew 安装 Docker Desktop。Docker Desktop 已包含 Docker CLI、Docker Engine 和 Docker Compose，不需要分别安装这些组件。

### 0.1 使用 Homebrew 安装

先确认终端能使用 Homebrew：

```bash
brew --version
```

如果命令能显示版本，执行：

```bash
brew install --cask docker
```

`--cask` 表示安装 macOS 桌面应用。这里必须安装 Docker Desktop cask；`brew install docker` 安装的只是 Docker CLI，没有负责运行容器的本地 Engine。

日后可以使用以下命令更新 Docker Desktop：

```bash
brew upgrade --cask docker
```

Homebrew 当前安装命令见 [docker cask](https://formulae.brew.sh/cask/docker)，Docker Desktop 的首次启动流程见 [官方 Mac 安装说明](https://docs.docker.com/desktop/setup/install/mac-install/)。如果 Mac 还没有 Homebrew，先按照 [Homebrew 官方安装说明](https://docs.brew.sh/Installation)完成安装，再回到这里。

### 0.2 验证 Docker 环境

打开一个新的终端窗口，在任意目录依次执行：

```bash
docker --version
docker version
docker compose version
```

| 命令 | 验证什么 | 成功标准 |
| --- | --- | --- |
| `docker --version` | 终端是否能找到 Docker CLI | 显示 Docker 客户端版本 |
| `docker version` | 客户端是否能连接容器引擎 | 同时显示 **Client** 与 **Server** 部分 |
| `docker compose version` | Compose 插件是否可用 | 显示 Compose 版本 |

版本号以实际安装结果为准，不必与笔记中的发行说明完全相同。尤其要检查 `docker version`：只有 Client、没有 Server，说明还没有完成引擎连接验证。

#### 每次使用 Docker 都要打开 Docker Desktop 吗

在 Mac 上使用 Docker Desktop 提供的本地 Engine 时，**Docker Desktop 必须处于运行状态**，但不需要一直打开 Dashboard 窗口，也不需要在每条 `docker` 命令之前重复启动它。

可以这样理解：

- Docker CLI 是遥控器，Docker Desktop 中的 Engine 是实际工作的机器；只有遥控器、没有运行中的 Engine，无法创建或管理本地容器。
- 关闭终端不会停止以 `-d` 方式运行的容器，因为容器由 Engine 管理。
- 关闭 Docker Desktop 的 Dashboard 窗口通常不等于退出应用；菜单栏中的 Docker 图标仍显示 Engine 正在运行即可。
- 真正退出 Docker Desktop 会停止本地 Engine，后台容器也不能继续运行。再次启动 Desktop 后，容器是否自动启动取决于它的 restart policy；默认不会自动恢复运行。
- `docker run -d` 中的 `-d` 只表示容器与当前终端分离，不表示它能够脱离 Docker Engine 或 Docker Desktop 独立运行。

可以随时检查状态：

```bash
docker desktop status
docker version
```

需要时启动 Docker Desktop：

```bash
docker desktop start
```

也可以在“应用程序”中点击 Docker，或使用 `open -a Docker`。如果不想每次登录 Mac 后手动启动，可在 Docker Desktop 的 **Settings → General** 中开启 **Start Docker Desktop when you sign in to your computer**。Docker Desktop 默认的 Resource Saver 会在没有容器运行时减少资源占用，并在需要运行容器时自动唤醒，因此通常无需为了节省空闲资源而频繁退出应用。

参考：[Docker Desktop CLI](https://docs.docker.com/desktop/features/desktop-cli/)、[Docker Desktop 设置](https://docs.docker.com/desktop/settings-and-maintenance/settings/)和 [Resource Saver](https://docs.docker.com/desktop/use-desktop/resource-saver/)。

#### 关闭 Mac 前要先停止全部容器吗

不需要形成“每次关机都先停止全部容器，再退出 Docker Desktop”的固定动作。正常关闭 Mac 时可以让系统退出 Docker Desktop；但如果正在运行数据库、消息队列或会持续写数据的应用，推荐先按项目优雅停止，让进程有机会刷新数据和完成清理。

按下面三种情况处理：

- **没有运行中的容器**：可以直接正常关机。
- **一次性的无状态学习容器**：通常可以直接正常关机；若希望下次状态清晰，也可以先停止它。
- **数据库或 Compose 多服务项目**：先在项目目录执行 `docker compose stop`，确认停止后再正常关机。

推荐的关机前检查流程：

```bash
# 1. 查看当前有哪些容器正在运行
docker ps

# 2A. 停止一个明确命名的容器
docker stop web-demo

# 2B. 如果是 Compose 项目，在含 compose.yaml 的目录中停止整个项目
docker compose stop

# 3. 确认没有仍需处理的运行中容器
docker ps
```

`docker compose stop` 只停止项目容器，不删除它们，下次可以在相同目录使用 `docker compose start`。如果实验已经结束、希望同时删除项目容器和网络，则使用：

```bash
docker compose down
```

普通 `docker compose down` 默认不会删除命名 Volume；**不要随意添加 `-v`**，因为 `docker compose down -v` 会删除项目 Volume，其中的数据库数据可能永久丢失。

完成上述停止后，可以直接正常关闭 Mac；没有必要再把“手动退出 Docker Desktop”作为强制步骤。如果想完全确认 Desktop 已停止，也可以从菜单退出，但这只是可选操作。不要使用 `docker stop $(docker ps -q)` 作为日常关机流程，因为它会停止当前 Engine 中所有项目的容器；也不要执行 `docker system prune`，它属于资源清理而不是关机步骤。

官方行为说明：[docker stop](https://docs.docker.com/reference/cli/docker/container/stop/) 会先给进程优雅退出机会；[docker compose stop](https://docs.docker.com/reference/cli/docker/compose/stop/) 停止但保留容器；[docker compose down](https://docs.docker.com/reference/cli/docker/compose/down/) 会移除项目容器和网络，只有增加 `-v` 才会进一步删除 Volume。

### 0.3 运行第一个容器

保持 Docker Desktop 运行，在同一个终端执行：

```bash
docker run --rm hello-world:latest
```

这条命令首次执行时通常需要联网下载官方教学镜像。看到 **`Hello from Docker!`**，且命令正常结束，就完成了从客户端到引擎、镜像拉取和容器执行的基本验证。

1. 本地没有 `hello-world:latest` 时，Docker 先拉取镜像。
2. Docker 从镜像创建容器并启动容器主进程。
3. 主进程打印欢迎信息，然后正常退出。
4. 容器随主进程退出而停止；`--rm` 随即自动删除这个容器。

本次检查不开放服务端口，也不挂载 Mac 文件夹。镜像保留在本地，无需执行全局清理命令。更完整的观察与清理练习见 [[Docker环境验证与首个容器]]。

#### 查看当前有多少个容器

“当前开了多少个”可能指正在运行的容器，也可能指仍保留在 Docker 中的全部容器，需要分别查看：

```bash
# 列出正在运行的容器
docker ps

# 列出全部仍然存在的容器，包括已经停止的容器
docker ps -a

# 只统计正在运行的容器数量（macOS/Linux）
docker ps -q | wc -l

# 统计全部仍然存在的容器数量（macOS/Linux）
docker ps -aq | wc -l
```

`docker ps` 与 `docker container ls` 等价；`-q` 只输出容器 ID，便于计数。由于 `hello-world` 主进程很快退出，而且本次使用了 `--rm`，命令结束后它通常不会出现在 `docker ps` 或 `docker ps -a` 中。

#### 如何关闭一个容器

先用 `docker ps` 找到容器的名称或 ID，再执行 `docker stop`。下面用一个持续运行的 Nginx 容器演示完整过程：

```bash
# 创建并在后台启动名为 web-demo 的容器
docker run --name web-demo -d nginx:latest

# 确认它正在运行
docker ps

# 优雅停止它
docker stop web-demo

# 确认它已停止但仍然存在
docker ps -a
```

`docker stop web-demo` 只是结束容器进程，不会删除容器；以后可以用 `docker start web-demo` 再次启动。如果确定不再需要它，停止后再删除：

```bash
docker rm web-demo
```

正常关闭优先使用 `docker stop`，不要把 `docker kill` 或 `docker rm -f` 当作常规操作；后两者会跳过或缩短应用的正常退出过程。如果容器创建时使用了 `--rm`，那么它被停止或自然退出后会自动删除，无需再执行 `docker rm`。

### 0.4 Docker 常见命令

#### 查看环境

| 命令 | 作用 |
| --- | --- |
| `docker --version` | 查看 Docker CLI 版本 |
| `docker version` | 查看 Client 与 Server 版本，并验证两者能否连接 |
| `docker info` | 查看当前 Engine、存储驱动和资源概况 |
| `docker context show` | 查看 CLI 当前连接的 Docker context |
| `docker compose version` | 查看 Compose 插件版本 |
| `docker COMMAND --help` | 查看某个命令的帮助，例如 `docker run --help` |

#### 管理镜像

| 命令 | 作用 |
| --- | --- |
| `docker pull nginx:latest` | 从 Registry 拉取镜像 |
| `docker image ls` | 列出本地镜像 |
| `docker image inspect nginx:latest` | 查看镜像的详细元数据 |
| `docker image history nginx:latest` | 查看镜像层和构建历史 |
| `docker image rm nginx:latest` | 删除未被容器使用的本地镜像 |

#### 管理容器

| 命令 | 作用 |
| --- | --- |
| `docker run --name web-demo -d -p 8080:80 nginx:latest` | 创建并后台运行 Nginx，把 Mac 的 8080 端口映射到容器的 80 端口 |
| `docker container ls` | 列出正在运行的容器；短写是 `docker ps` |
| `docker container ls -a` | 列出运行中和已停止的全部容器 |
| `docker logs web-demo` | 查看容器日志；加 `-f` 可持续跟踪 |
| `docker exec -it web-demo sh` | 在正在运行的容器中启动交互式 Shell |
| `docker inspect web-demo` | 查看容器的配置、状态、网络和挂载信息 |
| `docker stop web-demo` | 优雅停止容器，容器对象仍然保留 |
| `docker start web-demo` | 重新启动已有的停止容器 |
| `docker restart web-demo` | 重启已有容器 |
| `docker rm web-demo` | 删除已经停止的容器 |

运行 `web-demo` 后，可以访问 `http://localhost:8080` 验证 Nginx。结束练习时执行：

```bash
docker stop web-demo
docker rm web-demo
```

这两条命令只停止并删除名为 `web-demo` 的实验容器，`nginx:latest` 镜像仍保留在本地。

#### 管理 Compose 项目

以下命令需要在包含 `compose.yaml` 的项目目录中运行：

| 命令 | 作用 |
| --- | --- |
| `docker compose config` | 解析并检查 Compose 配置 |
| `docker compose up -d` | 创建并在后台启动项目服务 |
| `docker compose ps` | 查看项目中的容器状态 |
| `docker compose logs -f` | 持续查看项目服务日志 |
| `docker compose down` | 停止并删除该 Compose 项目的容器和默认网络 |

常见参数：`-d` 表示后台运行，`--name` 指定容器名，`-p 主机端口:容器端口` 发布端口，`-it` 启用交互式终端，`--rm` 表示容器退出后自动删除。


### 0.5 安装验收

- [x] `brew install --cask docker` 安装成功，Docker Desktop 能正常启动。
- [x] `docker version` 同时显示 Client 和 Server。
- [x] `docker compose version` 能返回版本。
- [x] `docker run --rm hello-world:latest` 输出欢迎信息并正常结束。

以后开始学习前先确保 Docker Desktop 的 Engine 处于运行状态，再打开终端执行命令。关闭终端通常不会停止后台容器；退出 Docker Desktop 会影响它管理的本地容器环境。



> [!info] 资料基线
> 本页根据 2026-09-29 访问的 Docker 官方文档、CLI reference 和 Moby 项目资料编写。当天 Docker Desktop 最新发行说明为 4.93.0；概念不依赖单一补丁版本，实际安装要求和组件版本应以官方当前页面为准。

> [!question] 运行验证状态
> 2026-09-30 已确认 Docker CLI 29.8.1 能连接 Docker Desktop 4.93.0 的 Engine 29.8.1，并实际运行了第二阶段构建与存储实验。本页的首容器完整验证步骤集中在 [[Docker环境验证与首个容器]]。

## 一句话结论

Docker 把应用及其用户态依赖做成不可变镜像，再由 Daemon 按运行配置创建受隔离的容器进程；镜像不是容器，容器不是虚拟机，CLI 也不是实际运行容器的服务端。

## 本章目标

学完后，你应该能：

1. 解释容器解决什么问题，以及它解决不了什么问题。
2. 区分容器与虚拟机的内核、开销和隔离边界。
3. 画出 Docker CLI、Daemon、Registry、镜像和容器的关系。
4. 区分 Docker Engine、Docker Desktop、Docker CLI 与 Docker Daemon。
5. 区分镜像（Image）、容器（Container）、仓库（Repository）、标签（Tag）和摘要（Digest）。
6. 解释 `run`、`create`、`start`、`stop`、`kill` 和 `rm`。
7. 完成一个可安全清理的首容器实验，并能解释每个观察结果。

## 1. 容器解决什么问题

### 1.1 从“在我机器上能跑”到可交付环境

传统交付经常把应用代码和环境准备拆开：开发者交付代码，另一台机器再单独安装运行时、系统库和工具。版本、路径、权限或配置一旦不同，就会出现环境漂移。

容器镜像把应用所需的用户态文件、二进制、库和默认运行配置一起打包。开发、测试和部署可以从同一镜像内容创建容器，减少“重新解释环境”的次数。


## 2. 容器与虚拟机

容器（Container）共享运行它的内核；虚拟机（Virtual Machine）拥有自己的 Guest OS 内核。这个区别同时解释了容器为何轻量，以及为何不能把容器默认当成与 VM 等价的安全边界。

| 维度   | 容器                      | 虚拟机              |
| ---- | ----------------------- | ---------------- |
| 运行对象 | 隔离进程                    | 完整 Guest OS      |
| 内核   | 共享宿主机或 Desktop VM 内核    | 每台 VM 独立内核       |
| 启动   | 通常接近进程启动                | 需要启动操作系统         |
| 打包   | 应用和用户态依赖                | OS、驱动、应用和依赖      |
| 隔离   | namespaces、cgroups、安全策略 | Hypervisor 与独立内核 |
| 典型组合 | 可运行在 VM 内               | VM 内可运行多个容器      |

### 2.1 “运行对象”是什么意思

“运行对象”指启动、停止和分配资源时，主要被管理的东西：

- **容器的运行对象是隔离进程**：运行 Nginx 容器，本质上是在一个已经运行的 Linux 内核上启动 Nginx 进程，再用 namespaces、cgroups、独立文件系统和网络配置把它隔离起来。容器可以有多个进程，但没有自己的内核，也没有完整的操作系统开机过程。
- **虚拟机的运行对象是完整 Guest OS**：Guest OS 中文常称“客体操作系统”或“来宾操作系统”，是运行在虚拟硬件中的另一套操作系统。它会启动自己的内核、初始化系统、系统服务，最后才运行应用。

不要根据目录和命令的外观判断：容器内可能有 `/bin`、`/etc`、Shell 和包管理器，看起来很像一套 Linux，但这些只是用户态文件；容器仍然借用外部 Linux 内核，所以不是完整 Guest OS。“完整”也不代表必须有图形界面，最小化 Ubuntu 只要有自己的内核和启动过程，仍然是 Guest OS。

在当前 Mac 环境中的实际层级是：

```text
Mac 硬件
└── macOS（Host OS）
    └── Docker Desktop 的 Linux VM（有自己的 Linux 内核，是 Guest OS）
        └── hello-world / Nginx 容器（共享该 Linux 内核的隔离进程）
```

因此表格中的一句话可以展开为：**容器隔离并运行应用进程；虚拟机启动并运行一套拥有独立内核的操作系统。**


## 3. Docker 的组件边界

### 3.1 关系图

这张图回答“终端输入 `docker run` 后，请求经过哪些组件”。从用户向右阅读控制流；Registry 与 Daemon 之间是镜像分发，最右侧才是实际容器进程。

```mermaid
flowchart LR
    User[用户] --> CLI[Docker CLI]
    User --> Compose[Docker Compose]
    CLI --> API[Docker API]
    Compose --> API
    API --> Daemon[Docker Daemon]
    Registry[Registry] <--> Daemon
    Daemon --> Images[本地镜像存储]
    Daemon --> Containerd[containerd]
    Containerd --> Runc[runc]
    Runc --> Kernel[Linux 内核]
    Kernel --> Process[容器主进程]
```

图后逐步解释：

1. 用户操作 CLI 或 Compose；它们是客户端。
2. 客户端通过 Docker API 连接某个 Daemon。
3. Daemon 管理镜像、容器、网络和数据卷；本地缺少镜像时访问 Registry。
4. Engine 使用 containerd 管理容器生命周期，默认借助 runc 创建底层运行环境。
5. 内核最终调度的仍是普通进程，只是它看到受隔离的环境。

关键结论：CLI 关闭通常不会让后台容器停止；一条命令操作哪台机器，取决于当前 Docker context 指向哪个 Daemon。


## 4. 镜像、容器、Registry、Tag 与 Digest

### 4.1 对象模型、Tag 与 Digest

| 对象            | 定义                     | 关键性质                         |
| ------------- | ---------------------- | ---------------------------- |
| 镜像（Image）     | 创建容器所需的只读、分层应用包        | 不运行；内容变化会形成新镜像内容             |
| 容器（Container） | 镜像加运行配置、可写层和进程状态形成的实例  | 可运行、停止、再次启动或删除               |
| Registry      | 保存和分发镜像内容的服务           | Docker Hub 是默认公共 Registry 之一 |
| Repository    | Registry 中同一名称下的一组镜像引用 | 例如 `library/nginx`           |
| Tag           | 人类可读、可移动的引用            | 例如 `1.29`、`latest`           |
| Digest        | 基于内容的加密摘要              | 例如 `sha256:...`，内容不变则标识不变    |

镜像名的一般形式：

```text
[REGISTRY_HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]
```

`nginx` 通常等价于 `docker.io/library/nginx:latest`。这里的 `latest` 只是默认 Tag；维护者可以让它指向不同内容，Docker 也不会判断它是否比别的 Tag 更新。因此 Tag 适合提供易读名称，但不能单独保证内容永远不变。

需要固定镜像内容时使用 Digest：

```bash
docker pull IMAGE@sha256:DIGEST
```

Digest 根据内容计算；内容不变时标识不变，因此能固定到同一份镜像内容。但固定 Digest 不会自动包含以后发布的漏洞修复，仍然需要主动评估、测试并更新到新的 Digest。

深入理解见 [[Docker镜像与容器]]。

### 4.2 镜像为什么分层

镜像层记录文件系统变化。不同镜像可以复用相同层，下载时只需获取本地缺失的层。容器创建时不会修改镜像层，而是在其上增加属于该容器的可写层。

先把“层”理解为一张张叠加的只读透明片。每张透明片只记录相对下面各层发生的变化，叠起来才得到容器最终看见的完整文件系统。例如：

| 层 | 只记录这一阶段的变化 |
| --- | --- |
| 基础层 | 加入最基本的 Linux 用户态文件 |
| Python 层 | 加入 Python 可执行文件和标准库 |
| 依赖层 | 加入 Flask 等第三方依赖 |
| 应用层 | 加入自己的 `app.py` |

应用层本身不需要再复制 Python 和基础 Linux 文件。Docker 读取时把这些层合并起来，所以在容器中可以同时看到所有层提供的文件。

下面的图同时说明“镜像之间复用”和“容器之间隔离”。箭头表示“在前一份只读内容之上增加自己的变化”，不是文件在运行时沿箭头移动。

```mermaid
flowchart TB
    Base[基础 Linux 层] --> Python[Python 运行时层]
    Python --> Web[Web 应用层]
    Python --> Worker[Worker 应用层]
    Web --> ContainerA[容器 A 的可写层]
    Web --> ContainerB[容器 B 的可写层]
```

流程从基础层开始：基础 Linux 层提供公共用户态文件，Python 层在其上增加运行时。随后出现两个分支：Web 镜像和 Worker 镜像都复用前两层，但分别保存自己的应用变化。如果已经拉取 Web 镜像，再拉取使用相同基础内容的 Worker 镜像，Docker 可以直接使用本地的基础层和 Python 层，只获取缺失的 Worker 应用层。

从 Web 镜像创建容器 A 和容器 B 时，两者继续共享 Web 镜像的全部只读层，但分支末端各自增加一层独立的可写层。最终每个容器看到的是“公共只读层 + 自己的可写层”合并后的目录树，而不是一份完整镜像副本。

运行时对文件的操作可以这样判断：

| 容器内的操作 | 实际发生的位置 | 是否改变镜像 |
| --- | --- | --- |
| 读取 `/usr/bin/python` | 从镜像层读取 | 否 |
| 新建 `/tmp/result.txt` | 写入本容器可写层 | 否 |
| 修改镜像自带的 `/app/app.py` | 先复制到可写层，再修改副本 | 否 |
| 删除镜像自带的文件 | 在可写层记录隐藏标记 | 否，底层原文件仍存在 |

这就是 Copy-on-Write：平时共享只读内容，只有真正修改时才在当前容器的可写层产生副本。删除容器时，这层私人修改也会被删除；另一个基于相同镜像创建的容器完全不受影响。

因此：
- 同一镜像可以创建多个容器。
- 每个容器拥有自己的运行配置和可写层。
- 删除一个容器不会删除镜像，也不会删除其他容器。
- 容器可写层不适合保存必须持久化的业务数据。

Dockerfile 指令如何产生层、构建缓存如何命中，会在第 2 周展开。

## 5. `docker run` 到底做了什么

这张图回答首次运行为什么会出现下载，而再次运行可能直接启动。按条件分支阅读：先检查本地镜像，再创建并启动容器。

```mermaid
flowchart TD
    Run[docker run IMAGE] --> Local{本地已有匹配镜像吗}
    Local -->|否| Pull[从 Registry 拉取清单与缺失层]
    Local -->|是| Create[创建容器配置与可写层]
    Pull --> Create
    Create --> Network[准备网络与挂载]
    Network --> Start[启动镜像默认或指定命令]
    Start --> Running{主进程仍在运行吗}
    Running -->|是| Up[容器 Running]
    Running -->|否| Exited[容器 Exited]
```

图后讲解：

1. `run` 的命令形式是 `docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]`。
2. 若本地没有符合拉取策略的镜像，Daemon 从 Registry 获取内容。
3. Daemon 创建容器：镜像不变，新的容器获得配置和可写层。
4. 网络与挂载按参数准备好后，容器主进程启动。
5. 主进程结束，容器进入 Exited；使用 `--rm` 时，退出后容器还会被自动删除。

关键结论：`run` 不等于“启动镜像”，而是“以镜像为模板创建并启动新容器”。镜像永远不会自己运行。

## 6. 容器生命周期

### 6.1 状态图

这张图用于区分停止与删除。Created、Running、Paused 和 Exited 都表示容器对象仍存在；Removed 才表示对象消失。

```mermaid
flowchart LR
    Image[Image] -->|create| Created[Created]
    Created -->|start| Running[Running]
    Running -->|pause| Paused[Paused]
    Paused -->|unpause| Running
    Running -->|进程退出或 stop| Exited[Exited]
    Exited -->|start| Running
    Exited -->|rm| Removed[Removed]
    Running -.->|rm -f| Removed
```

图后讲解：

- `docker create` 只创建，不运行。
- `docker start` 启动已有容器。
- `docker run` 常用但会创建新容器；反复执行会产生多个容器。
- `docker stop` 先给主进程优雅退出机会，超时才强制终止。
- `docker kill` 默认直接强制终止，正常维护应优先 `stop`。
- `docker rm` 删除容器对象；停止本身不会删除。

关键结论：容器寿命跟主进程绑定。这里的主进程是容器内部的 PID 1；一个 Web 服务如果被入口脚本放到后台，而作为 PID 1 的入口脚本随后退出，Docker 就会把容器标记为停止。具体过程见 6.3。

### 6.2 常用命令的精确差异

| 命令 | 是否创建新容器 | 是否要求容器运行 | 结果 |
| --- | ---: | ---: | --- |
| `docker create IMAGE` | 是 | 否 | 新容器处于 Created |
| `docker run IMAGE` | 是 | 否 | 新容器被创建并启动 |
| `docker start NAME` | 否 | 否 | 已有停止容器再次运行 |
| `docker stop NAME` | 否 | 是 | 主进程收到终止信号，容器保留 |
| `docker kill NAME` | 否 | 是 | 默认立即强制终止，容器保留 |
| `docker rm NAME` | 否 | 否，默认需先停止 | 容器对象被删除，镜像保留 |
| `docker exec NAME CMD` | 否 | 是 | 在现有运行容器中增加一个进程 |

### 6.3 主进程、PID 1 与信号

#### 什么是容器主进程

Docker 根据镜像的 `ENTRYPOINT`、`CMD` 和 `docker run` 末尾指定的命令，启动容器中的第一个进程。这个进程在容器自己的进程编号空间中是 **PID 1**，Docker 把它当作容器生命周期的锚点。

主进程不一定是 Docker Daemon，也不表示容器只能有一个进程。例如：

- `docker run ... java -jar app.jar`：Java 进程可以直接成为 PID 1。
- 镜像先执行 `/entrypoint.sh`：入口脚本先成为 PID 1，再由它准备环境并启动真正的服务。
- 主进程可以创建 Worker 等子进程；只要 PID 1 仍在，容器仍可以保持 `Running`。

> [!note] `entrypoint.sh` 是什么
> 它是一个普通 Shell 脚本，常被设置为容器启动后首先执行的入口，用来准备环境并启动实际服务；文件名可以自定义，并非 Docker 规定必须叫这个名字。

#### 为什么入口脚本退出会停止容器

下面的图从 `docker run` 开始，对比入口脚本启动 Web 服务时的错误分支与正确分支。判断点不是“容器里是否还出现过其他进程”，而是 PID 1 是否仍然存活。

```mermaid
flowchart TD
    Run[docker run 启动容器] --> Entry[entrypoint.sh 成为 PID 1]
    Entry --> Choice{入口脚本如何启动 Web 服务}
    Choice -->|使用 web-server 后台运行且脚本结束| ScriptExit[入口脚本退出即 PID 1 退出]
    ScriptExit --> Exited[容器进入 Exited]
    Choice -->|使用 exec 启动前台服务| Replace[Web 服务替换 Shell 并成为 PID 1]
    Replace --> Alive{Web 服务是否仍在运行}
    Alive -->|是| Running[容器保持 Running]
    Alive -->|否| Exited
```

入口是 `docker run`：Docker 根据镜像配置启动 `entrypoint.sh`，因此脚本最初是 PID 1。随后根据脚本的写法产生两个分支。错误分支把 Web 服务放入脚本后台，然后脚本走到末尾；PID 1 随即退出，Docker 将这次容器运行标记为 `Exited`，其他后台子进程不能代替它维持容器生命周期。正确分支使用 `exec` 启动前台 Web 服务；`exec` 不会再创建一层长期存在的 Shell，而是让 Web 服务替换 Shell 成为 PID 1。只要服务仍存活，容器就是 `Running`；服务正常完成或异常退出时，容器才进入 `Exited`。

以 Nginx 为例，先把命令中的几个部分拆开。它们不属于同一层，不能把 `-g` 与 `&` 或 `echo` 当成互相替代的写法：

| 写法 | 由谁解释 | 作用 |
| --- | --- | --- |
| `nginx` | Shell | 启动 Nginx 程序 |
| `-g 'daemon off;'` | Nginx | `-g` 用来传入全局配置；`daemon off;` 要求 Nginx 不要自行转入后台 |
| `&` | Shell | 把前面的命令作为后台任务启动，Shell 不等它结束，立即执行下一行 |
| `echo "Nginx started"` | Shell | 只打印一行文字；打印完就结束，不负责维持容器运行 |
| `exec` | Shell | 不再创建一个需要 Shell 等待的子进程，而是用 Nginx 替换当前 Shell 进程 |

为了只比较 `&` 与 `exec`，两个例子应使用完全相同的 Nginx 参数。下面的写法有问题：

```sh
#!/bin/sh
nginx -g 'daemon off;' &
```

它按以下顺序执行：

1. Docker 启动 `entrypoint.sh`，Shell 成为容器内的 PID 1。
2. Shell 启动 Nginx。`daemon off;` 让 Nginx 本身不进行 daemon 化，但行尾的 `&` 又让 Shell 把这个 Nginx 进程当作自己的后台任务。
3. 因为使用了 `&`，Shell 不等待 Nginx；脚本已经没有下一条命令，于是 Shell 立即退出。
4. PID 1 退出后，Docker 判定这次容器运行已经结束，容器进入 `Exited`；留下的 Nginx 进程也会随容器停止而被终止。

更适合容器的写法是：

```sh
#!/bin/sh
exec nginx -g 'daemon off;'
```

它的执行过程不同：

1. Shell 最初仍然是 PID 1。
2. `exec` 用 Nginx 替换 Shell，而不是让 Shell 在后台再启动一个 Nginx。替换完成后，原来的 PID 1 现在就是 Nginx。
3. `daemon off;` 同时保证 Nginx 不再自行派生一个后台 daemon 后退出；Nginx 会一直占据 PID 1。
4. 只要 Nginx 还在运行，容器就保持 `Running`；Nginx 退出时，容器才进入 `Exited`。执行 `docker stop` 时，停止信号也能直接送到作为 PID 1 的 Nginx。


> [!info] 两种“后台”不要混淆
> `docker run -d IMAGE` 是让整个容器脱离宿主机当前终端，容器中的 PID 1 仍然运行；入口脚本里的 `command &` 是让某个命令成为脚本的后台子进程。如果脚本随后退出，容器仍会停止。


## 7. 第一个动手实验

完整步骤、预期结果、清理和故障处理见 [[Docker环境验证与首个容器]]。核心命令如下：

```bash
docker version
docker context show
docker run --name docker-basics-hello hello-world:latest
docker container ls -a --filter name=docker-basics-hello
docker image ls hello-world
docker start --attach docker-basics-hello
docker rm docker-basics-hello
```

应该观察到：

1. Client 与 Server 都可用。
2. 首次运行会拉取镜像，后续本地已有层可复用。
3. `hello-world` 打印完成后退出码为 0，容器处于 Exited。
4. `start` 再次运行的是原容器，不创建第二个容器。
5. `rm` 后容器消失，镜像仍在。

## 8. 来源

- [Docker：What is Docker?](https://docs.docker.com/get-started/docker-overview/) — 平台、架构、对象定义。
- [Docker：What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) — 容器与 VM 的入门模型。
- [Docker：What is an image?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/) — 镜像不可变性与分层。
- [Docker：Running containers](https://docs.docker.com/engine/containers/run/) — 容器进程与 `docker run`。
- [Docker CLI：container create](https://docs.docker.com/reference/cli/docker/container/create/) — create 与 run/start 的边界。
- [Docker CLI：container stop](https://docs.docker.com/reference/cli/docker/container/stop/) — 停止信号与超时强制终止。
- [Docker CLI：image pull](https://docs.docker.com/reference/cli/docker/image/pull/) — Tag、Digest 和内容寻址。
- [Docker Engine security](https://docs.docker.com/engine/security/) — namespaces、cgroups 与 Daemon 攻击面。
- [Moby Project](https://github.com/moby/moby) — Moby 与 Docker Engine 的关系。
## 相关

- [[Docker学习路径]] — 四周顺序、任务和完成标准
- [[Docker]] — 平台、产品和生态边界
- [[容器与虚拟机]] — 共享内核与隔离差异
- [[Docker架构]] — Client–Server 与运行时调用链
- [[Docker镜像与容器]] — 对象、层、Tag 与 Digest
- [[Docker容器生命周期]] — 状态与命令的精确关系
- [[Docker环境验证与首个容器]] — 可复制的第一个实验
