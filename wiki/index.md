---
title: 索引
type: index
tags: [系统]
created: 2026-09-13
updated: 2026-10-04
---

# 索引

全库总目录。Agent 每次 ingest 后必须更新本页；回答问题时**先读本页定位**，再深入具体页面。

分区顺序：概念 → 操作 → 实体 → 来源 → 输出。每区内部按技术栈分组，技术栈顺序：Java / Python / Bash / OS / 容器 / 系统框架 / 通用 / 知识管理。

## 概念（`concepts/`）

回答"为什么、是什么"。

### 知识管理

- [[持久 Wiki 模式]] — 用 LLM 增量维护、持续变厚的知识库模式；含与 RAG 的对比、成立条件与失效模式
- [[知识图谱编译]] — 把语料编译成图谱、沿图导航：AST 确定性通道 + LLM 语义通道
- [[持久 Wiki 实践要点]] — 目录布局、检索选型、Clipper 配置、已知故障清单

### 通用

- [[英语发音与重音]] — 用拼读模式、-ed 清浊音规则、弱读和重音倾向预测发音，并明确例外边界
- [[英语介词的空间模型]] — 用容器、表面、点、方向和路径理解介词，同时区分固定搭配
- [[英语高频动词与短语动词]] — 从核心动词、小品词和三类多词动词结构组织高频表达
- [[英语疑问感叹与倒装结构]] — 区分直接与间接疑问、what/how 感叹句以及部分和完全倒装
- [[英语基本句型与口语造句]] — 用五大句型、SVA/SVOA 和存在结构把中文意图转成可扩展的英语口语骨架
- [[英语人称代词与所有格]] — 从句子角色掌握 I/me/my/mine/myself 等主格、宾格、所有格与反身形式

### 容器

- [[容器与虚拟机]] — 从共享内核、资源开销和隔离边界区分容器与虚拟机
- [[Docker架构]] — 解释 CLI、API、Daemon、Registry、containerd、runc 与容器进程的调用链
- [[Docker镜像与容器]] — 区分镜像、容器、Repository、Tag、Digest、只读层和容器可写层
- [[Docker容器生命周期]] — 用主进程模型解释 create、run、start、stop、kill 与 rm
- [[Docker镜像构建]] — 解释 Dockerfile、构建上下文、BuildKit、缓存与多阶段构建
- [[Docker数据持久化]] — 区分容器可写层、Volume、Bind Mount 及其生命周期

### 系统框架

- [[Kafka核心架构]] — 以 Partition 为核心理解 Topic、Broker、Consumer Group 与 KRaft Controller 的关系
- [[Kafka可靠性与交付语义]] — 用 ACK、ISR、Offset、事务与业务幂等组合分析消息丢失和重复

### Java / Python / Bash / OS

_暂无。_

## 操作（`howto/`）

回答"怎么做"：适用环境 → 步骤 → 验证 → 已知坑。

### 容器

- [[Docker环境验证与首个容器]] — 验证 CLI、Daemon、context、镜像拉取和容器生命周期，并精确清理实验资源
- [[Docker镜像构建与挂载实验]] — 构建两阶段 Nginx 镜像，并验证缓存、Volume 与 Bind Mount

### 系统框架

- [[Kafka KRaft开发环境]] — 用官方 Kafka 4.3.1 容器启动 KRaft 单节点并验证两个 Java 入门实验

### Java / Python / Bash / OS / 通用 / 知识管理

_暂无。_

## 实体（`entities/`）

工具、语言、框架、机构、人物。

- [[graphify]] — 把代码库与多模态语料编译成知识图谱的 skill 型工具；仓库已核实
- [[Andrej Karpathy]] — LLM Wiki 模式的提出者
- [[Apache Kafka]] — 基于 Partition 持久日志、Consumer Group 和 KRaft 元数据仲裁的分布式事件流平台
- [[Docker]] — 用于构建、分发和运行容器化应用的平台与工具集合，区分 Engine、Daemon、CLI、Desktop、Compose 与 OCI

## 来源摘要（`sources/`）

- [[2026-09-13 LLM Wiki（Karpathy）]] — 构想文件：用 LLM 维护持久 wiki 取代查询时检索；本库的方法论出处
- [[2026-09-17 graphify 知识图谱教程（AI超元域）]] — 视频转录：graphify 的架构与实测；ASR 噪声需还原
- [[2026-09-17 LLM Wiki 搭建教程（飞书云文档）]] — 工程化程度最高的规格：三层模型、六操作、七道护栏

## 输出（`outputs/`，第三层）

问答与审计的结论，**给 Harlan 复习学习用**。普通学习笔记按技术栈归类并使用稳定主题名；命中相同主题时持续更新原页，不按日期重复建页。只有维护报告等时间型产物使用日期前缀。

### Java

- [[Java消息队列概览与选型]] — RabbitMQ、Kafka、RocketMQ、Pulsar、ActiveMQ Artemis 的定位、差异与 Java 选型建议
- [[RabbitMQ入门实战]] — RabbitMQ 核心名词与架构、Spring AMQP，以及用 Docker、Spring Boot 跑通收发、路由、确认、死信和幂等的渐进式练习
- [[Maven-Wrapper]] — Maven Wrapper 的定位、文件组成、工作原理、常用命令与版本更新方法

### Python

- [[Python基础学习实战]] — 参考 Python-100-Days 重新编写的 Day01-20 学习项目，包含虚拟环境与 PyCharm 解释器配置、48 个中文注释 Demo、统一运行器和自动化测试

### 系统框架

- [[Apache Kafka学习指南]] — Kafka 4.3.1 与 KRaft 基线下的 12 章学习材料，配套两个含详细注释、开发流程与阅读顺序的 Java 入门实验

### 容器

- [[Docker学习路径]] — 4 周、每周 5～7 小时的渐进路线，当前已展开前三个学习阶段
- [[01-Docker核心学习笔记]] — 第一阶段：从 Mac 安装与常用命令开始，学习 Docker 核心概念和生命周期
- [[02-Dockerfile与镜像构建]] — 第二阶段：学习 Dockerfile 指令、构建上下文、缓存、BuildKit 和多阶段构建
- [[03-Docker数据存储]] — 第三阶段：学习容器可写层、命名 Volume、Bind Mount 与 `COPY` 的边界

### 通用

- [[英语学习笔记]] — 从个人记录纠错重排的英语复习材料，覆盖发音、介词、短语动词、人称代词、语法和机场表达
- [[英语发音学习笔记]] — 持续整理发音规则，以及按“连读组合—中文意思—美式音标—例句”逐行记录的口语训练表

### 知识管理

- [[当前项目工作原理]] — 三层结构、按需 Skill 工作流、规则刷新与上下文开销

---

统计：来源 3 · 概念 17 · 操作 3 · 实体 4 · 输出 12 · 最后更新 2026-10-04
