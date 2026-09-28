---
title: 日志
type: log
tags: [系统]
created: 2026-09-13
updated: 2026-09-17
sources: []
---

# 日志

**只追加，不修改历史条目。** 标题格式固定为 `## [YYYY-MM-DD] 动作 | 标题`，便于用 `grep "^## \[" wiki/log.md | tail -5` 取最近 5 条。

动作取值：`scaffold`（搭架构）、`ingest`（摄入来源）、`query`（问答归档）、`lint`（体检）、`schema`（修改本库约定）。

## [2026-09-13] scaffold | 初始化第二大脑架构

- 依据 Andrej Karpathy 的 LLM Wiki 模式（gist: 442a6bf555914893e9891c11519de94f）搭建三层架构：`raw/`（原始资料）、`wiki/`（Agent 维护的知识层）、`AGENTS.md`（schema）。
- 新建：`AGENTS.md`、`raw/README.md`、`raw/assets/`、`wiki/index.md`、`wiki/log.md`、`wiki/overview.md`、`wiki/sources/`、`wiki/concepts/`、`wiki/entities/`。
- Obsidian 附件目录设为 `raw/assets/`。
- 状态：库内暂无任何原始资料与知识页面，等待首次 ingest。

## [2026-09-13] ingest | LLM Wiki（Karpathy）

- 来源：`raw/assets/llm-wiki.md`（Obsidian Web Clipper 抓取；原文为 gist `442a6bf555914893e9891c11519de94f`）
- 新建：[[2026-09-13 LLM Wiki（Karpathy）]]（来源摘要）、[[持久 Wiki 模式]]（概念）
- 更新：[[index]]、[[overview]]、本文件
- 判断：未为作者 Andrej Karpathy 单独建实体页。按 schema 的门槛，它在本来源中仅以作者身份出现，暂不独立成页；若后续来源再次出现则建页。
- 遗留问题：`raw/assets/` 按设计是附件目录，网页剪藏应改存到 `raw/`。本次未移动该文件（agent 不改动 raw）。

## [2026-09-13] schema | 新增面向人类的使用手册

- 新建根目录 `README.md`：把六步循环（投递 → 摄入 → 讨论 → 验收 → 提问 → 体检）、边界与常见问题写成操作手册，面向 Harlan。
- 明确优先级：README 与 `AGENTS.md` 冲突时以 `AGENTS.md` 为准，避免两份文档各说各话。
- 同步更新 `AGENTS.md` 的目录树。

## [2026-09-17] ingest | graphify 知识图谱教程（AI超元域）

- 来源：`raw/🚀Karpathy知识库工作流终极进化：graphify知识图谱保姆级教程！...md`（Web Clipper 抓取；Bilibili BV1G9DiBSEmj，作者 AI超元域）
- 新建：[[2026-09-17 graphify 知识图谱教程（AI超元域）]]（来源摘要）、[[知识图谱编译]]（概念）、[[graphify]]（实体）、[[Andrej Karpathy]]（实体）
- 更新：[[持久 Wiki 模式]]（新增「图谱化演进」一节 + 冲突标注）、[[index]]、[[overview]]、本文件
- 判断 1：**Karpathy 建页的门槛触发**。上次 ingest 记录"若后续来源再次出现则建页"，本次来源正是围绕他的工作流展开，故建页。
- 判断 2：**graphify 建页**。单份来源中出现，但是该来源的核心主体，符合"单份来源中是核心角色"这一条。
- 判断 3：未为 Claude Code / Codex / OpenCode / OpenClaw 建页——它们只是宿主环境，未承担独立论述。
- 冲突处理：图谱路线与持久 Wiki 路线在"维护成本该由谁承担"上不一致，已在 [[持久 Wiki 模式]] 用 `> [!warning] 冲突` 标注，并给出"互补而非替代"的暂定结论，等待第三份来源检验。
- 数据质量：来源是**视频 ASR 转录**，专有名词系统性识别错误（GRAPHY→graphify、CARPY→Karpathy、cloud code→Claude Code、open cloud→OpenClaw 等），已在来源页列出还原对照表。所有能力描述均为二手转述。
- 待办：① 找 graphify 仓库 README 核实能力与成本；② 核实视频 published 日期（2026-04-07）与内容（"最近几天爆火"）的矛盾；③ 确认"AMAC"所指论文。

## [2026-09-17] schema | 剪藏文件归位，raw/ 布局规范化

- 动作：`raw/assets/llm-wiki.md` → `raw/llm-wiki.md`（Harlan 指示执行）。
- 理由：`raw/assets/` 按 `AGENTS.md` 的定义是**附件目录**（图片等），不是文档来源目录。之前 Web Clipper 与附件目录共用同一路径设置，导致网页剪藏落进了 assets。
- 连带修正引用：[[2026-09-13 LLM Wiki（Karpathy）]]（frontmatter + 出处小节）、[[持久 Wiki 模式]]、[[Andrej Karpathy]] 的 `sources` 字段，以及 `README.md` 的状态段。
- 例外说明：这是 raw/ 只读规则的**一次经授权的例外**——由 Harlan 明确指示，且只做移动、不改内容。此后 raw/ 恢复只读。
- 历史条目未改：上一条 ingest 记录里的 `raw/assets/llm-wiki.md` 保持原样，日志只追加不修改，路径变更以本条为准。

## [2026-09-17] schema | 留档建库提示词

- 新建根目录 `建库提示词.md`：逐字保存 2026-09-13 生成本库的原始提示词，附执行信息、要求与落地结果的对照表、以及复用时要注意的三点。
- 归类理由：它是**需求文档而非知识来源**，所以放根目录、与 `AGENTS.md` 并列，不放进 `raw/`（raw 收的是可供提炼的知识材料）。
- 同步更新：`AGENTS.md` 目录树、`README.md` 新增「本库的来历」小节。

## [2026-09-17] ingest | LLM Wiki 搭建教程（飞书云文档）

- 来源：`raw/LLM Wiki 搭建教程 - 飞书云文档.md`（Web Clipper 抓取；飞书原文 AM3ewXySViopPdkE8Gic90BDnRb）
- 新建：[[2026-09-17 LLM Wiki 搭建教程（飞书云文档）]]（来源摘要）、[[持久 Wiki 实践要点]]（概念）
- 更新：[[持久 Wiki 模式]]（新增「外部验证与运维实践」一节）、[[Andrej Karpathy]]（新增「待核实的线索」）、[[index]]、[[overview]]、本文件
- 判断 1：**剪藏严重不完整**——教程的核心正文与提示词全文都缺失，只剩安装四步和评论区。已用 `> [!warning]` 在来源页顶部标注，避免后续会话误把它当成搭建步骤的依据。
- 判断 2：**为"实践要点"单独建概念页**，而不是把运维细节塞进来源页。理由：qmd 包名、Clipper 变量、目录布局这类经验是跨来源复用的，且会随新来源继续累积，属于典型的概念页而非来源页内容。
- 判断 3：**未为教程作者/评论者建实体页**——评论是匿名编号，作者身份不明，不构成实体。
- 重要发现：评论区的故障报告"摄入当天能答对、第二天索引不到、重新摄入又正常"，与 [[持久 Wiki 模式]] 的"索引检索会失效"是同一件事。已在来源页给出根因分析（**会话上下文被误当成持久检索**）并落进 [[持久 Wiki 实践要点]]。这是本库第一次用 schema 设计回答一个真实故障。
- 时间线更正：该教程的评论跨 2026 年 4–9 月，说明这套实践**自 4 月起已在传播**，比本库 9-13 建库早约五个月。本库并非首创，`overview.md` 已相应更新。
- 待办：① 重新剪藏该飞书页面的完整正文（尤其提示词全文与第 2/3 节）；② 查找 Karpathy 关于"HTML 优于 markdown"的原始出处；③ 三条社区未解问题已记入 `overview.md` 知识缺口。

## [2026-09-17] ingest | 重建飞书文档完整正文并重新摄入

- 背景：Harlan 要求重新抓取那份飞书云文档。
- 抓取过程：① 命令行直取失败——未登录会被 302 重定向到 `accounts.feishu.cn` 登录页，这是当初 Clipper 只抓到半截的根本原因；② 公开镜像未找到同一篇；③ Computer Use 权限未授予，无法驱动用户浏览器；④ 改用 Codex 内置浏览器成功打开并读取。
- 技术要点：飞书文档是**虚拟滚动**渲染，DOM 里只保留可视区域（`innerText` 仅 1425 字符，`scrollHeight` 12012→26406 动态增长）；且正文里有内嵌代码块会吃掉滚轮事件，需把滚动光标移到右侧空白处（x≈820）才能滚动外层容器。最终逐屏滚动拼接得到 28836 字符。
- 新建：`raw/LLM Wiki 搭建教程 - 飞书云文档（完整正文重建版）.md`（48KB；含头部失真说明，明确标注它是重建版而非原始剪藏，权威版本仍是原链接）
- 重写：[[2026-09-17 LLM Wiki 搭建教程（飞书云文档）]]——从"半截剪藏"升级为完整规格摘要，新增三层模型、六操作、七道护栏、文档自身的六处矛盾、与本库的对比表
- 更新：[[持久 Wiki 模式]]（新增「工程化扩展」一节 + 回音室风险标注）、[[持久 Wiki 实践要点]]（新增"飞书教程版的额外机制"与逐项对照表）、[[index]]、[[overview]]、本文件
- 重要发现 1：**REFLECT 的 Stage 0**——生成合成结论前先找反驳证据，找不到就标注「回音室风险」。这是本库最缺的一环，且直接适用于本库自身（三份来源同主题、全二手）。
- 重要发现 2：**"个人写作不参与 source_count"** 是防止知识库自证的设计，本库尚无对应机制。
- 重要发现 3：该文档**自身有六处内部矛盾**（REFLECT Stage 1 两处版本不同、QUERY 步骤两处版本不同、章节缺"七"、qmd 包名错、Clipper 变量 `data`/`date`、附件路径归属错），其中两处是评论区读者发现的。结论：长规格文档会自己漂移，schema 越短越可靠。
- 数据质量：重建版会**合并完全相同的重复行**，代码块与目录树中逐字重复的行可能缺失；已在 raw 文件头部与来源页顶部双重标注。
- 判断：**未新建页面**。这批内容属于对既有两个概念页的深化（模式层 → 持久 Wiki 模式；实践层 → 持久 Wiki 实践要点），新开页面会造成重叠。
- 待办：① 是否采纳三个未落地机制（输出落盘 / 开放问题队列 / REFLECT）；② 命名规范中文 vs 英文 slug 需整体取舍，**不许部分迁移**；③ Karpathy 关于 HTML 的原始出处仍未找到。

## [2026-09-17] schema | 写入命名规范、aliases 与链接校验

- 动作：Harlan 决定采纳「中文主名 + 英文别名」方案，要求把规则写进 `AGENTS.md`。
- `AGENTS.md` §3 新增「命名规范」小节：一个概念一个规范名、其余叫法进 `aliases`、不许中英混用、不许部分迁移、粒度保持一致；并写明重新评估的三个信号（对外发布 / 来源转为英文为主 / 库重心变成代码与符号）。
- `AGENTS.md` §3 frontmatter 模板新增 `aliases` 字段，说明它承担对齐去重、链接补全、承接英文叫法三件事，并要求别名克制（只写真实出现过的）。
- `AGENTS.md` §3 正文结构新增链接书写规则：以规范名为主；`[[英文别名]]` 是否可解析**必须在库内实测确认**，不可解析时改用 `[[规范名|显示文本]]`。
- `AGENTS.md` §4 Ingest 新增第 4 步「对齐检查」并重新编号（9 步）：新建页面前必须按规范名 + aliases 双查。
- `AGENTS.md` §4 Lint 新增「链接完整性」检查，并要求顺带核对两条命名纪律（同概念多页、aliases 为空或堆砌）。
- 为现有页面补 `aliases`：[[持久 Wiki 模式]]、[[知识图谱编译]]、[[持久 Wiki 实践要点]]、[[Andrej Karpathy]]。[[graphify]] 与来源页的规范名本身已是原文，暂不加别名。
- 决策依据：见 [[持久 Wiki 实践要点]] 中「与本库的直接冲突：页面命名」一节——两套方案的去重能力相同，中文主名省掉每次建链的翻译步骤，且降低 Agent 写歪英文 slug 的风险。
- 待办：**实测 `[[英文别名]]` 能否解析到中文页面**（例如 `[[persistent-wiki-pattern]]` 是否落到「持久 Wiki 模式」）。若不能，需在所有别名链接上改用 `[[规范名|显示文本]]` 写法，并据此修正本节规则。

## [2026-09-17] lint | 全库结构审计 + 三项外部核实

- 触发：Harlan 要求对比当前结构与资料，指出可优化处。
- 方法：写了一个只读审计脚本（Codex 的 `work/audit_vault.py`），覆盖 frontmatter 完备性、wikilink 解析（已剔除代码块与行内代码）、孤立页、index 一致性、stub 页、命名纪律与别名冲突、层级完整性、log 格式、来源覆盖率。
- **审计结果：核心结构健康**。19 个 .md（11 wiki + 5 raw + 3 根目录）；断链 0、孤立页 0、index 与实体完全一致、无 stub 页、log 9 条格式 100% 合规、raw 4 份来源全部已摄入（`raw/README.md` 是说明文件，本就不该摄入）。
- **外部核实三项**（用官方文档 / GitHub API / npm registry）：
  ① **Obsidian 的 `aliases` 确实可作为 wikilink 目标**（官方帮助 "Linking notes and files/Aliases"）→ 关闭待验证项，`AGENTS.md` §3 规则成立；同时发现官方禁用字符集含 `# | ^ : %% [[ ]]`，已补进命名规则。
  ② **graphify 仓库确认**：`Graphify-Labs/graphify`，Apache-2.0，Python，创建 2026-04-03，活跃；安装为 `pip install graphifyy && graphify install`；产出含 `obsidian/` 与 `wiki/`。
  ③ **qmd 包名确认** `@tobilu/qmd`（npm 2.8.3，仓库 tobi/qmd，仍在更新）。
- 更新：[[graphify]]（基本档案由"未知"改为已核实事实 + 新增产出物与外部核实两节）、`AGENTS.md`（命名禁用字符）、[[overview]]（关闭待验证项、新增"没有外部核实机制"这一缺口）、本文件。
- 审计中发现的三处可优化点（已向 Harlan 提出，待其决定）：缺 `wiki/outputs/`、缺开放问题队列、没有可重复执行的 lint 脚本。
- 未做：Karpathy 关于"HTML 比 markdown 更适合高密度信息"的说法**仍未找到出处**，搜索受限，保留为待验证。

## [2026-09-17] schema | 主题转向 IT 技术库，落地第一批结构优化

- 背景：Harlan 明确本库主题为 IT 工程（Java / Python / Bash / 操作系统 / 系统框架），并要求落地可立即执行的部分、其余归档待定。
- 确认的三项：① 需要 `howto/` 操作类页面；② 目前无存量资料，不做批量导入；③ 记录以通用原理为主，因此**不强制**标注环境，只在版本敏感处标注。
- 归类方式：一级按**知识类型**（concepts / howto / entities / sources / outputs），二级按**技术栈**（Java / Python / Bash / OS / 系统框架 / 通用，concepts 另有 知识管理）。

**新建**

- `wiki/outputs/` —— 铁律第 4 条：结论必须落盘，不允许只存在于对话里
- `wiki/QUESTIONS.md` —— 开放问题队列（触发词「我想搞清楚…」），摄入时回头检查
- `scripts/lint.py` —— 把今天的审计固化成可重复执行的体检命令（`python3 scripts/lint.py`）
- `raw/personal/` —— 存放 Harlan 自己的排障与学习记录，与外部分开
- `待落地清单.md` —— 8 项已评估但暂不落地的做法，各带触发条件
- `.gitignore` + `git init` —— 版本历史

  > [!question] 未完成：git init 需要 Harlan 手动执行
  > Agent 的沙箱禁止创建 `.git` 目录（实测 `mkdir .git` 返回 Operation not permitted），因此 `git init` 这一步无法由 Agent 完成。`.gitignore` 已备好，Harlan 在库根执行一次 `git init && git add -A && git commit -m "初始化第二大脑"` 即可启用版本历史。

**重写**

- `AGENTS.md` —— 全面重构：三层架构表、四条铁律、按页面类型分档的 frontmatter、三类页面模板（概念/操作/来源）、四个操作（Ingest 含个人记录分支 / Query / Lint / Add-question）、index/log/QUESTIONS 规范。技术专有名词保留原文（`JVM 垃圾回收`、`Spring Boot 自动配置`），时效默认 medium（180 天），版本敏感页面改 high。
- `wiki/index.md` —— 改为 概念 → 操作 → 实体 → 来源 → 输出 五分区，区内按技术栈分组。
- `wiki/overview.md` —— 重新定位为 IT 技术库；三份方法论来源降级为"本库的蓝本"，并明确记录"技术内容为零"是当前最大缺口。
- `README.md` —— 面向 Harlan 的手册：三种投递路径、四句常用话、手动命令、目录速览。
- `raw/README.md` —— 说明 raw / assets / personal 的分工。

**迁移**

- 三个方法论概念页移入 `wiki/concepts/知识管理/`（`持久 Wiki 模式`、`持久 Wiki 实践要点`、`知识图谱编译`）。因全库链接均为纯页面名，移动不影响任何链接。

**归档待定**（详见 `待落地清单.md`）：来源哈希校验、页面模板、二阶合成 REFLECT、英文 slug 迁移、graphify 实测、代码片段库、Karpathy HTML 出处、检索升级（qmd/ripgrep）。

## [2026-09-17] schema | outputs 独立为第三层 + 技术栈目录自建

- 起因：Harlan 提出两点优化——① 技术栈目录缺失时 Agent 应能自建，不必每次请示；② outputs 独立成层，`wiki/` 给 Agent 看、`outputs/` 给 Harlan 复习学习，且 outputs 也要按技术栈分类。
- 判断：两点均采纳。第 ② 点其实**更贴合飞书那份规格**——它的三层正是 Raw / Wiki / Outputs，outputs 本就在 wiki 之外；此前把 outputs 放进 `wiki/` 是本库对那份文档的一次偏离，现纠正。
- 动作：
  - `wiki/outputs/` 整体移至根目录 `outputs/`，按技术栈建子目录（Java / Python / Bash / OS / 系统框架 / 通用 / 知识管理，另加 `维护/` 存体检报告）。
  - `AGENTS.md`：三层改为 Raw / Wiki / Outputs（Schema 定位为横跨三层的配置，不算层）；新增输出页 frontmatter 规范（`type: output` + `related`）与「输出页负责讲清楚、wiki 页负责沉淀」的分工；技术栈目录改为**允许 Agent 按需自建**（约束：专有名词保留原文、不造语义重复的目录）。
  - `scripts/lint.py`：适配 outputs 独立层——检查输出页 `type: output` 与轻量 frontmatter、链接解析、是否在 index 输出区登记。
  - `wiki/index.md`、`README.md`：同步目录说明。
- 影响：输出页不算 wiki 导航页，`lint` 对其要求比 wiki 页轻（`title / type / created` + `related`），但正文少于 100 字仍警告——输出页必须能独立读懂。
- 备注：`git` 仍待 Harlan 手动 `git init`（沙箱禁止 Agent 创建 `.git`）。

## [2026-09-17] schema | 时效默认改为 90 天

- Harlan 决定整体时效定为 90 天（此前默认 180 天）。
- `AGENTS.md`：`domain_volatility` 默认由 `medium` 改为 `high`（90 天复核）；稳定不变的原理页可手动标 `medium`/`low`。
- `scripts/lint.py`：默认阈值同步为 90 天；howto 页的 `verified` 复核窗口也由 180 天改为 90 天。
- 状态：`git` 已由 Harlan 完成 `git init` 并首次提交（commit `184178a`），此前的待办关闭。

## [2026-09-17] schema | 重写 README 为完整使用手册

- Harlan 要求把本库的结构、搭建思路、使用方法完整写入 README，便于理解与使用。
- 重写为一份自包含手册：结构全景图、三层职责、五类页面、归类与命名规则、六步日常流程、常用命令、关键约定、边界、常见问题、设计由来、现状与下一步。
- 定位仍不变：README 面向人（理解+使用），`AGENTS.md` 面向 Agent（规则），冲突时以 `AGENTS.md` 为准。

## [2026-09-17] schema | 新增「整理到笔记中」：摄入 + 复习卡

- 起因：Harlan 希望以后说「整理到笔记中」时，同时更新 wiki 和 outputs——他从别处拿到的知识，既想织进知识网络，也想得到一份能反复复习的成品。
- 判断：合理，已落地为一个独立操作，与普通「摄入」区分开：普通摄入只写 wiki；「整理到笔记中」在完整摄入之外，额外产出一份复习卡到 `outputs/<技术栈>/`。
- 复习卡定稿为四段：一句话结论 / 核心要点 / 怎么用 / 相关（链回 wiki 页）。
- **防漂移的关键约定**：复习卡是**快照**，记录"这次整理时的理解"，不随 wiki 自动更新；wiki 页才是活源头，点复习卡里的链接回找最新版。这条写进了 `AGENTS.md`，避免"每个摄入都复制一份知识"造成的维护债。
- 改动：`AGENTS.md`（新增 §4「整理到笔记」操作、输出页说明补上两种来源、标题由「四个操作」改为「操作」）、`README.md`（第二步新增该触发语）、`持久 Wiki 实践要点`（操作数更新为 5）。

## [2026-09-23] query | 当前项目工作原理

- 触发：Harlan 要求读取当前项目并了解项目工作原理。
- 方法：读取 `AGENTS.md`、`README.md`、`scripts/lint.py`、`wiki/index.md`、`wiki/overview.md`、`wiki/QUESTIONS.md`、`wiki/log.md` 与核心知识管理概念页。
- 结论：本项目是三层结构的持久 Wiki：`raw/` 保存事实来源，`wiki/` 由 Agent 维护知识网络，`outputs/` 保存给 Harlan 复习的问答与审计结论；当前结构已成型，但技术内容仍为零。
- 新建：[[2026-09-23-当前项目工作原理]]（输出页）
- 更新：[[index]]、本文件

## [2026-09-23] query | Java 消息队列概览与选型

- 触发：Harlan 询问 Java 方面有哪些消息队列。
- 方法：先检查 `wiki/index.md`，确认库内没有相关技术页面；随后核对 Spring Boot、RabbitMQ、Apache Kafka、Apache RocketMQ、Apache Pulsar、Apache ActiveMQ Artemis 与 Jakarta Messaging 官方文档。
- 结论：Java 常见选择包括 RabbitMQ、Kafka、RocketMQ、Pulsar 和 ActiveMQ Artemis；选型首先要区分业务任务队列与可回放事件流，并结合路由、吞吐、延时/事务消息、JMS 兼容和运维能力判断。
- 新建：[[2026-09-23-Java消息队列概览与选型]]（输出页）
- 更新：[[index]]、本文件

## [2026-09-23] query | RabbitMQ 入门实战学习文档

- 触发：Harlan 希望按照消息队列学习方案先上手 RabbitMQ，并生成学习文档。
- 方法：基于 RabbitMQ 4.x、Spring Boot 与 Spring AMQP 官方文档，按心智模型、最小收发、工作队列、Exchange 路由、可靠性、死信和幂等逐步组织练习。
- 结论：第一阶段以 Docker + Spring Boot 跑通订单通知链路；第二阶段通过 publisher confirm、publisher return、consumer ack、DLX 和数据库唯一键建立可靠性认知。
- 新建：[[2026-09-23-RabbitMQ入门实战]]（输出页）
- 更新：[[index]]、本文件

## [2026-09-23] query | 补充 RabbitMQ 架构介绍

- 触发：Harlan 要求在 RabbitMQ 入门实战中增加架构介绍。
- 方法：核对 RabbitMQ 4.x 官方 Connections、Channels、Virtual Hosts、Clustering、Classic Queues、Quorum Queues 与 Streams 文档。
- 结论：新增单节点组件图、Connection/Channel 分层、Virtual Host 与元数据、三类消息数据结构、集群复制边界和消息完整生命周期；明确 Cluster 不会自动复制 Classic Queue 消息。
- 更新：[[2026-09-23-RabbitMQ入门实战]]、[[index]]、本文件

## [2026-09-24] query | 创建 RabbitMQ Spring Boot 配套项目

- 触发：Harlan 要求在当前目录新建 `code/` 并生成基于入门实战的 Spring Boot RabbitMQ 项目。
- 方法：使用 Spring Boot 4.1.1、Java 17、Spring AMQP 与 RabbitMQ 4.x，创建独立 Maven 工程和 Docker Compose 环境。
- 结论：项目实现 Direct Exchange、通知与审计双 Queue、JSON 事件、publisher confirm/return、手动 ack、死信队列、失败模拟和内存幂等示例。
- 新建：`code/rabbitmq-demo/`
- 更新：[[2026-09-23-RabbitMQ入门实战]]、本文件

## [2026-09-24] query | Codex旧对话提供商缺失排障

- 只读检查配置、任务数据库和会话元数据，确认四个旧对话仍引用未定义的 deepseek 提供商。
- 输出恢复配置与改用 ChatGPT 的处理路径，未修改应用配置或历史记录。
- 新增：[[2026-09-24-Codex旧对话提供商缺失排障]]；更新：[[index]]、本文件。

## [2026-09-24] query | 验证 RabbitMQ Spring Boot 配套项目

- 使用 IntelliJ IDEA 内置 Maven 编译项目并执行测试，3 个测试全部通过；同时生成 Maven Wrapper 3.9.11。
- 当前环境未安装 Docker，未执行真实 RabbitMQ Broker 联调；项目保留 `compose.yaml` 与完整联调步骤供本地运行。
- 更新：`code/rabbitmq-demo/`、本文件

## [2026-09-24] schema | 新增 code 配套项目目录

- 起因：学习文档开始配套可运行工程，需要明确代码在知识库中的位置与维护边界。
- 约定：`code/` 存放学习与验证项目，不属于 Raw sources、The wiki、Outputs 三层内容；项目应自带运行说明、可复现构建配置和必要测试，不提交秘密信息与构建产物。
- 更新：`AGENTS.md`、`README.md`、本文件

## [2026-09-24] query | Spring AMQP 与 Maven Wrapper

- 触发：Harlan 询问 RabbitMQ 示例项目中 Spring AMQP 与 Maven Wrapper 的定位和用法。
- 方法：对照项目依赖、连接配置、拓扑声明、生产者、消费者与 Wrapper 属性，并核对 Spring Boot、Spring AMQP 和 Apache Maven 官方文档。
- 结论：Spring AMQP 是应用运行时的 RabbitMQ 编程抽象与实现；Maven Wrapper 是构建期的 Maven 版本引导器，两者分别保证消息代码易用和构建环境可复现。
- 新建：[[2026-09-24-Spring-AMQP与Maven-Wrapper]]（输出页）
- 更新：[[index]]、本文件

## [2026-09-24] schema | 输出页改为按主题持续维护

- 起因：日期型、一问一页的输出会让同一学习主题散落在多个文件中，不利于连续学习。
- 新规则：普通输出页使用稳定主题名，不加日期前缀；新问题先按文件名、标题、别名和正文标题做主题对齐，命中就更新原页。一次问题可更新多个独立主题，不创建临时拼盘页；只有体检和阶段审计等时间型维护产物保留日期。
- 迁移：5 篇输出页全部改为主题名；Spring AMQP 内容并入 [[RabbitMQ入门实战]]，Maven Wrapper 独立为 [[Maven-Wrapper]]，其余页面只去除日期前缀。
- 兼容：旧文件名写入 `aliases`，历史 log 链接仍可解析；`scripts/lint.py` 新增普通输出页日期前缀、完整 frontmatter 和输出 aliases 检查。
- 更新：`AGENTS.md`、`README.md`、`scripts/lint.py`、[[index]]、[[当前项目工作原理]]、`code/rabbitmq-demo/README.md`、本文件

## [2026-09-24] query | 为 RabbitMQ 示例项目补充新手注释

- 触发：Harlan 希望通过详细代码注释理解 `code/rabbitmq-demo`，当前学习阶段为新手。
- 方法：按消息生命周期为应用入口、拓扑、事件模型、生产者、发布回调、两个消费者、幂等存储、HTTP 接口和测试补充中文 JavaDoc 与关键行注释；同时解释 Maven 依赖、Docker Compose 和 Spring 配置。
- 边界：保留 Maven Wrapper 生成脚本原样，不手工修改工具生成代码；README 新增建议阅读顺序。
- 验证：使用 Maven 完成编译和 3 个测试，全部通过。
- 更新：`code/rabbitmq-demo/`、[[RabbitMQ入门实战]]、本文件

## [2026-09-24] query | RabbitMQ 核心名词详解

- 触发：Harlan 希望详细理解 Broker、Exchange、Queue、Binding 及相关 RabbitMQ 名词。
- 方法：基于 RabbitMQ 官方 AMQP 0-9-1 Model、Exchanges、Queues、Virtual Hosts、Confirms、DLX 与 TTL 文档，按消息生命周期组织概念，并映射到现有 Spring Boot 示例项目。
- 结论：新增 Broker/Node/Cluster、Publisher、Message、Exchange 类型、Routing Key、Binding、Queue 属性与状态、Consumer、ACK/NACK、Prefetch、Confirm/Return、DLX/DLQ、TTL/Policy、Virtual Host/User/Permission 的定义、边界和易混淆对照。
- 更新：[[RabbitMQ入门实战]]、[[index]]、本文件

## [2026-09-24] query | 归档四个DeepSeek旧对话

- 用户要求改用 ChatGPT 并删除四个旧对话；现有接口仅支持归档，已归档全部四个任务并复核状态。
- 永久删除未执行，历史保留；默认模型配置保持不变。
- 更新：[[2026-09-24-Codex旧对话提供商缺失排障]]、本文件。

## [2026-09-25] query | Binding Key 与 Exchange-Queue 映射关系

- 触发：Harlan 询问不同 Exchange 类型如何解释 Binding Key，以及 Exchange 是否固定对应多个 Queue。
- 结论：Binding Key 是 Binding 上的匹配规则；Direct 将其视为完整值，Topic 将其视为模式，Fanout 忽略它，Headers 改用 Binding arguments。Binding 本身就是 Exchange 与 Queue 的映射，双方是可动态配置的多对多关系，不是 Exchange 内置的固定 Queue 列表。
- 补充：同一消息匹配多个不同 Queue 时各写入一份；同一 Queue 的多条 Binding 同时匹配时，该 Queue 仍只写入一份。
- 更新：[[RabbitMQ入门实战]]、本文件。

## [2026-09-25] query | RabbitMQ 拒绝与再次投递

- 触发：Harlan 询问 Consumer 什么时候拒绝消息，以及 Reject、Requeue、Delivery Tag 和 Redelivered 与再次投递的关系。
- 结论：Reject/NACK 是否定当前 Delivery；`requeue=true` 或 Channel、Connection 在手动 ACK 前关闭都会使未确认消息重新入队，并可能交给原 Consumer 或其他 Consumer。Delivery Tag 只标识 Channel 内的一次投递，Redelivered 只表示 Broker 对同一 Queue 消息的重新投递，二者都不能代替业务幂等键。
- 补充：永久失败应进入 DLQ，临时失败应有限重试并退避，已完成的重复事件应 ACK；本项目使用 `basicNack(tag, false, false)` 将模拟永久失败送入死信流程。
- 更新：[[RabbitMQ入门实战]]、本文件。

## [2026-09-25] query | RabbitMQ 消费幂等

- 触发：Harlan 询问什么是幂等。
- 结论：幂等指同一业务请求执行一次和执行多次，最终业务状态与对外副作用相同；它不要求代码只进入一次。RabbitMQ 可能再次投递消息，因此 Consumer 应使用稳定的 `eventId`、数据库唯一约束、处理记录或业务状态机避免重复扣款、扣库存、发货和通知。
- 补充：幂等是目标，去重是实现手段；去重登记与业务更新必须处于同一事务边界。本项目的内存 Set 只用于演示，不能覆盖重启和多实例场景。
- 更新：[[RabbitMQ入门实战]]、本文件。

## [2026-09-25] query | 创建 Python Day01-20 学习项目

- 触发：Harlan 希望参考 `jackfrued/Python-100-Days`，在 `code/` 下创建带详细中文注释的小 Demo 项目学习 Python。
- 范围：建立完整 Day01-100 阶段路线，并实现 Day01-20 Python 基础；参考仓库只用于主题编排，示例代码重新编写。
- 产出：`code/python-learning-demos/` 包含 48 个独立 Demo、统一运行器、项目 README、后续路线和自动化测试，覆盖环境、控制流、容器、函数、装饰器、递归与面向对象综合项目。
- 验证：使用 Python 3.14.7 编译全部文件；9 项核心逻辑测试和逐个运行 48 个 Demo 的冒烟测试全部通过。
- 新增：[[Python基础学习实战]]、`code/python-learning-demos/`；更新：[[index]]、`README.md`、本文件。

## [2026-09-25] query | 优化 Python Demo 目录名称

- 触发：Harlan 反馈 `day01`、`day02` 等目录无法直接看出学习内容。
- 调整：将 20 个 Demo 目录统一改为“二位序号-主题”，例如 `01-Python环境与运行`、`05-分支结构`、`14-函数与模块`。
- 同步：更新 Demo 发现规则、测试路径、项目 README 和复习文档中的运行示例。
- 更新：[[Python基础学习实战]]、`code/python-learning-demos/`、本文件。

## [2026-09-26] query | Python 项目虚拟环境操作

- 触发：Harlan 希望避开 macOS 自带的较低版本 Python，为学习项目创建虚拟环境。
- 结论：虚拟环境继承创建它的解释器版本，因此应使用 `/opt/homebrew/bin/python3 -m venv .venv` 创建，再通过 `source .venv/bin/activate` 激活；不能依靠 `venv` 自动升级 Python。
- 补充：README 增加创建、激活、验证、退出和重新进入步骤；项目命令统一演示为激活后使用 `python`，依赖安装使用 `python -m pip`。
- 更新：[[Python基础学习实战]]、`code/python-learning-demos/README.md`、[[index]]、本文件。

## [2026-09-26] query | PyCharm 运行按钮解释器不一致

- 触发：Harlan 激活 `.venv` 后，终端运行使用 Python 3.14，但代码左侧运行按钮仍使用 Python 3.9。
- 定位：项目 `.idea/misc.xml` 与模块配置仍绑定 `Python 3.9`；终端激活只影响该终端的 `PATH`，不会修改 PyCharm 的项目 SDK 或已有 Run Configuration。
- 解决：在 PyCharm 中将 Existing Interpreter 设置为项目 `.venv/bin/python`；若旧运行配置覆盖项目默认值，再把其解释器改为 `Project Default` 或删除后重建。
- 更新：[[Python基础学习实战]]、`code/python-learning-demos/README.md`、[[index]]、本文件。

## [2026-09-26] query | deactivate 与 PyCharm 项目解释器

- 触发：Harlan 发现终端执行 `deactivate` 后，PyCharm 运行按钮仍使用 Python 3.14。
- 结论：这是正常行为；`deactivate` 只恢复当前终端的 `PATH`，不会更改 PyCharm 持久保存的项目解释器。PyCharm 运行按钮会继续直接调用 `.venv/bin/python` 的绝对路径。
- 更新：[[Python基础学习实战]]、`code/python-learning-demos/README.md`、本文件。

## [2026-09-26] ingest | 英语个人学习记录

- 触发：Harlan 要求摄入 `raw/personal/English.md`，梳理并重新编辑排版输出。
- 处理：按个人记录流程摄入，不创建客观来源摘要页，也不把个人记录计入置信度来源数量；原始文件保持只读。
- 梳理：将 865 行增量记录重组为发音、介词、核心动词、短语动词、句型语法和机场表达六条主线，合并重复条目并修正明显的拼写、翻译和规则错误。
- 核查：使用 British Council 和 Cambridge Dictionary 的公开资料复核重音、地点与时间介词、how/what 感叹、否定副词倒装和多词动词结构；原笔记引用的 Bilibili 视频未作为独立来源摄入。
- 新增：[[英语学习笔记]]、[[英语发音与重音]]、[[英语介词的空间模型]]、[[英语高频动词与短语动词]]、[[英语疑问感叹与倒装结构]]；更新：[[index]]、本文件。

## [2026-09-26] ingest | 强化英语笔记的技巧与例句

- 触发：Harlan 希望输出文档更明显地体现原始记录中的英语学习技巧，并尽量提供准确例句。
- 调整：新增技巧总览与章节内提示框，明确保留容器/表面/点、箭头与受益区、二维/三维路径、小品词方向感，以及 `take/set/turn/break/cut` 的核心动作模型。
- 例句：为主要短语动词、易混词、数字界面操作和原记录中的实用句子补充完整例句，并增加语体或语境提示。
- 核查：补充 Cambridge 的使役结构、`get`、`as/like` 资料和 British Council 的短语动词资料；纠正无法自然迁移的字面助记。
- 更新：[[英语学习笔记]]、本文件。

## [2026-09-26] query | 优化英语发音拼读与重音

- 触发：Harlan 希望核查 `ai/ay`、`ee/ea/ie`、`oa/oe`、`oi/oy`、`ou/ow`、`oo/ue/ui` 等读音总结，并优化发音章节。
- 结论：`oi/oy → /ɔɪ/` 相对最稳定；`ai/ay`、`ee/ea`、`oa/oe` 可作为起始映射但需记录例外；`ei/ey`、`ie`、`ou/ow`、`oo/ue/ui` 都不能压缩成单一读音。
- 扩充：新增 17 组字母组合对照、相对稳定性、位置倾向、六组朗读句、重音符号、schwa 示例和新词六步判断法。
- 核查：参考 University of Florida Literacy Institute、Reading Rockets、British Council 与 Cambridge Dictionary 的课程、拼读说明和词典音标。
- 更新：[[英语学习笔记]]、[[英语发音与重音]]、本文件。

## [2026-09-28] query | Kafka 前半阶段学习指南与两个 Java 实验

- 触发：Harlan 希望系统学习 Kafka；确认先只生成两个项目，并把原 23 章计划收缩为可覆盖当前项目的前半阶段内容，后续只登记不展开。
- 基线：核验 Apache Kafka 4.3.1、Java 21 与 KRaft Only；ZooKeeper 仅作为旧集群迁移背景。
- 文档：[[Apache Kafka学习指南]] 当前包含 12 章，覆盖基础架构、Topic/Partition、KRaft 部署、Producer、Consumer、存储、副本、可靠性、Java 开发与两个实战；第 12 章记录 Python、Connect、Streams、Schema、安全、监控、排障、调优、Kubernetes 和生产架构等后续清单。
- 代码：新增 `code/kafka-learning-labs/`，当前只保留 `01-hello-world-java` 与 `02-log-pipeline-java`；包括官方 Kafka 4.3.1 Compose、Topic 脚本、详细注释和单元测试。
- 验证：项目已配置独立 Maven Wrapper，两个模块从零编译成功，4 项测试全部通过；`compose.yaml` 通过 YAML 语法检查并按 Apache Kafka 官方单节点示例复核。当前环境未安装 `docker` 命令，因此 Broker 联调暂未验证。
- 新增：[[Apache Kafka]]、[[Kafka核心架构]]、[[Kafka可靠性与交付语义]]、[[Kafka KRaft开发环境]]、[[Apache Kafka学习指南]]；更新：[[index]]、本文件。

## [2026-09-28] query | 补充 Kafka 整体架构与核心名词关系

- 解释：在指南 2.1 节补充控制面、数据面和客户端的职责，以及从 Producer 到 Leader、Follower、Consumer 和 Offset 的流转链路。
- 关系：在 2.2 节增加 Broker、Topic、Partition、Replica、Leader、Follower、Producer、Consumer、Consumer Group 与 Offset 的层级图和七条关系。
- 纠正：Broker 物理上保存的是多个 Topic 的 Partition Replica，不能简化为每个 Broker 都包含完整 Topic。
- 更新：[[Apache Kafka学习指南]]、本文件。

## [2026-09-28] query | 解释 Kafka Consumer Group 分工与消费进度

- 空闲：用 4 个 Partition 和 6 个 Consumer 说明同组有效并行度的上限，以及空闲成员在 Rebalance 后接管 Partition 的可能。
- 进度：明确 Committed Offset 以 `Consumer Group + Topic + Partition` 为键独立保存，表示该 Group 在该 Partition 下一条要读的位置。
- 分工：区分 Group 内负载均衡与 Group 间独立订阅；“读取全部消息”指 Group 整体而非每个 Consumer，并受起始 Offset 和 Retention 限制。
- 更新：[[Apache Kafka学习指南]]、本文件。

## [2026-09-28] query | 进一步解释 Kafka KRaft

- 定位：将 KRaft 解释为 Kafka 内置的元数据管理与共识机制，明确它取代 ZooKeeper，但不存放或中转普通业务消息。
- 机制：补充 Active Controller、Standby Controller、Metadata Log、Raft 多数派提交、Broker 元数据同步和 Controller 故障选举流程。
- 区分：明确 Active Controller 与 Partition Leader 的职责和数量不同，并介绍 Broker-only、Controller-only 和 Combined Mode。
- 更新：[[Apache Kafka学习指南]]、本文件。

## [2026-09-28] query | 补充 Kafka 消息 Key 定义

- 命名：将指南 3.1 节从“从 key 到 Partition”改为“消息 Key 如何决定 Partition”，避免缺少上下文。
- 定义：补充 Kafka Record 结构、Producer 主动指定 Key 的语义，以及 Java `ProducerRecord<K, V>` 中 `K` 和 `V` 的含义。
- 用途：说明 Key 参与 Partition 映射、实体内顺序和 Log Compaction，并明确 Key 不是全局唯一主键。
- 更新：[[Apache Kafka学习指南]]、本文件。

## [2026-09-28] query | Codex 长会话与上下文管理

- 结论：当前会话已较长且经过上下文压缩，但仍可正常工作；无法从任务内部精确读取剩余上下文百分比。
- 建议：同一目标优先使用 `/status` 和 `/compact`（客户端提供时）；主题变化时新建任务，需继承历史分叉时使用 Fork。
- 落盘：本库依靠 `AGENTS.md`、`wiki/index.md`、主题输出页和 `wiki/log.md` 保存状态，因此新会话不会丢失已归档的学习内容。
- 更新：[[当前项目工作原理]]、本文件。

## [2026-09-28] query | 区分 Partition Leader 与 Leader Replica

- 结论：Partition Leader 与 Leader Replica 指向同一个副本，前者从 Partition 角度命名，后者从 Replica 角度命名；`Replica Leader` 不是推荐的常用表述。
- 层级：一个 Partition 拥有一组 Replica，其中一个承担 Leader，其余承担 Follower；不是一个 Replica 内部包含 Leader 和 Follower。
- 更新：[[Apache Kafka学习指南]]、本文件。

## [2026-09-28] query | Kafka 学习项目新手注释与开发流程

- 触发：Harlan 希望以新手视角阅读 `kafka-learning-labs`，要求为代码增加详细注释，并在 README 说明开发流程和阅读顺序。
- 源码：为两个 Java 实验的配置、Admin、Producer、Consumer、事件契约、JSON 编解码和测试补充类级、方法级与关键步骤中文注释；同时解释 Maven、Compose 和 Topic 脚本中的关键配置。
- 文档：根 README 按版本与环境、Topic、最小闭环、结构化事件、失败场景和验证方式还原开发流程；两个实验 README 分别增加逐文件阅读顺序、输出解读、练习和教学边界。
- 学习路径：明确先读环境与配置，再沿 `serialize -> produce -> partition -> poll -> process -> commit` 追踪消息，最后用 Consumer Group CLI 验证 Offset 与 Lag。
- 验证：Java 21 下两个 Maven 模块编译成功，4 项单元测试全部通过；Shell 脚本语法、Git whitespace 检查和知识库 lint 均通过。当前环境没有 `docker` 命令，因此未重复执行 Broker 联调。
- 更新：`code/kafka-learning-labs/`、[[Apache Kafka学习指南]]、[[index]]、本文件。
