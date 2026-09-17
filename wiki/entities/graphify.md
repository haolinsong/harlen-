---
title: graphify
type: entity
tags: [工具/知识图谱, LLM]
aliases: [Graphify]
created: 2026-09-17
updated: 2026-09-17
sources: ["raw/🚀Karpathy知识库工作流终极进化：graphify知识图谱保姆级教程！代码库编译成知识图谱，支持Claude CodeCodexOpenCode.md"]
---

# graphify

**定义**：一个开源工具，以 **skill** 形式集成进 AI 编程助手（Claude Code / Codex / OpenCode / OpenClaw），把 raw 语料编译成知识图谱，供助手做图谱导航式检索，并可导出到 Obsidian。

## 基本档案

| 项 | 内容 |
| --- | --- |
| 类型 | 开源工具 / AI Agent skill |
| 用途 | 把代码库与多模态语料编译成持久化知识图谱 |
| 仓库 | `Graphify-Labs/graphify`（GitHub） |
| 许可证 | Apache-2.0 |
| 语言 | Python（要求 3.10+） |
| 活跃度 | 创建于 2026-04-03；2026-09-17 仍在提交（外部核实） |
| 支持宿主 | Claude Code、Codex、Cursor、Gemini CLI、OpenCode、OpenClaw |
| 安装方式 | `pip install graphifyy && graphify install`（PyPI 包名暂为 `graphifyy`，命令仍是 `graphify`）；或让 Agent 按仓库链接自行安装 |
| 调用形式 | 宿主中的斜杠命令，如 `/graphify .` 加子命令 |

> [!warning] 信息完整度
> **项目本身已核实**（仓库、许可证、活跃度，见下方「外部核实」），但**能力描述仍全部来自单一二手来源（视频转录）**：架构分层、双通道效果、token 节省等说法都还没有第一手验证。缺一个实测。

## 常用子命令

| 子命令 | 作用 |
| --- | --- |
| （无）`.` | 从当前路径全量构建或更新图谱 |
| `query` | 按问题检索，返回文件与行号 |
| `explain` | 解释某段实现，输出流程图与设计决策 |
| `update` | 代码变更后增量更新图谱 |
| `add <URL>` | 追加外部资料（如 arXiv 论文）到图谱 |
| `path` | 追踪两个节点之间的图谱路径 |
| 导出 | 生成 Obsidian 库 |

## 产出物（据官方 README）

运行后在 `graphify-out/` 下生成：

| 文件/目录 | 内容 |
| --- | --- |
| `graph.html` | 交互式图谱，可按社区筛选、搜索节点 |
| `obsidian/` | **可直接作为 Obsidian 库打开** |
| `wiki/` | Wikipedia 风格的文章，供 Agent 导航 |
| `GRAPH_REPORT.md` | 枢纽节点、意外连接、建议追问的问题 |
| `graph.json` | 持久图谱，几周后仍可查询而无需重读原文 |
| `cache/` | SHA-256 缓存，重跑时只处理改动过的文件 |

README 明确说明其起点是 Karpathy 的 `/raw` 工作流，并声称"每次查询比直接读原始文件少 71.5 倍 token"——**这是项目方的自述，未经本库验证**。

## 外部核实（2026-09-17）

以下事实来自 GitHub API 与项目 README，不是来自 raw 来源：

- 仓库：`https://github.com/Graphify-Labs/graphify`
- 许可证 Apache-2.0；Python；创建于 2026-04-03；活跃
- 安装：`pip install graphifyy && graphify install`（PyPI 名 `graphifyy` 是暂时占位）
- 技术标签含 `ast`、`tree-sitter`、`leiden`、`mcp`、`graphrag`——与来源所述"AST + 社区发现"一致

> [!question] 本库的机制缺口
> `sources` 字段按 `AGENTS.md` 定义只装 raw 文件路径，**无法表达"这条结论来自 web 核实"**。本次只能把出处写在正文里。这是 schema 需要补的一处（已记入 `overview.md` 知识缺口）。

## 实现要点

采用 **AST + 语义双通道**（详见 [[知识图谱编译]]）：代码走确定性解析、零 token；文档、论文、图片走并行子代理抽取实体与关系；两者合并成一张图，再经社区发现等分析步骤，最后输出审计报告、可视化与 wiki。

## 相关

- [[知识图谱编译]] — 它实现的方法
- [[2026-09-17 graphify 知识图谱教程（AI超元域）]] — 记录它的来源
