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

## [2026-09-29] schema | 新主题会话启动提示词

- 起因：Harlan 希望以后为 Docker 等新学习主题开独立会话时，Agent 主动提醒并给出可复制的启动提示词。
- 规则：当用户表示要开新主题会话时，当前 Agent 必须生成启动提示词；提示词只补充主题范围、会话边界和首次任务，通用规则继续由根目录 `AGENTS.md` 提供。
- 边界：空白新会话在用户发送首条消息前无法主动提醒；新会话不继承其他会话的对话历史。
- 更新：`AGENTS.md`、`README.md`、本文件。

## [2026-09-29] query | Docker 专题第一阶段基础概念

- 范围：按“第一次只生成基础概念”的要求建立 Docker 四周学习路线，但只展开容器与虚拟机、Docker 架构、镜像与容器、生命周期和首个容器实验；Dockerfile、存储、网络、Compose、排障、安全与综合项目留待后续阶段。
- 核验：以 Docker Docs、Docker CLI reference、Docker Engine security、Moby 与 OCI Image/Runtime/Distribution 规范为主要来源；记录 2026-09-29 访问基线和 Docker Desktop 4.93.0 发行说明，不将普通博客作为关键结论依据。
- 新增：[[Docker]]、[[容器与虚拟机]]、[[Docker架构]]、[[Docker镜像与容器]]、[[Docker容器生命周期]]、[[Docker环境验证与首个容器]]、[[Docker学习路径]]、[[Docker核心学习笔记]]。
- 验证：当前环境没有 `docker` 命令，未声称完成容器运行；命令按官方 reference 静态核对，Mermaid 代码块与连接关系人工检查，仓库没有独立 Mermaid 校验器；`python3 scripts/lint.py` 通过，无错误或警告。
- 边界：未修改 `raw/`、`AGENTS.md`、`README.md`、`code/`、`wiki/QUESTIONS.md` 或 `wiki/overview.md`；保留开工前已有未提交修改，仅更新 [[index]] 并在本文件末尾追加本条记录。

## [2026-09-29] query | Docker 笔记前置 Mac 安装步骤

- 触发：Harlan 希望先安装 Docker，再开始学习基础概念。
- 更新：在 [[Docker核心学习笔记]] 开头增加 Mac 安装章节，覆盖 Apple Silicon/Intel 选择、官方 DMG 安装、首次启动、CLI/Server/Compose 验证、hello-world 自检和常见安装问题；同步 [[Docker环境验证与首个容器]] 的前置入口和 [[index]]。
- 核验：参考 Docker 官方 Mac 安装与权限说明；安装自检使用 `--rm`，明确与后续保留容器的生命周期实验区别。本次仅更新文档，未安装 Docker 或执行容器实验。

## [2026-09-29] query | Docker Mac 安装改用 Homebrew

- 触发：Harlan 要求删除芯片与系统要求说明，改用 Brew 命令安装 Docker，并补充常见使用命令。
- 修订：重写 [[Docker核心学习笔记]] 的第 0 章，以 `brew install --cask docker` 安装 Docker Desktop，补充首次启动、环境验证、hello-world、镜像/容器/Compose 常用命令和常见错误；同步 [[Docker环境验证与首个容器]] 与 [[index]]。
- 核验：使用 Homebrew 官方 Docker cask 与 Docker 官方 Mac 安装文档交叉检查；明确 `brew install docker` 只安装 CLI，不能替代 Docker Desktop。本次仅更新文档，没有在用户 Mac 上执行安装。

## [2026-09-29] query | hello-world 容器状态与关闭

- 结论：`docker run --rm hello-world:latest` 会创建并启动容器；其主进程打印信息后立即退出，`--rm` 再自动删除容器，因此命令结束后无需另行停止或删除。
- 更新：在 [[Docker核心学习笔记]] 补充运行中与全部容器的查看和计数方法，并用 Nginx 示例说明 `docker stop`、`docker start` 与 `docker rm` 的区别。
- 安全：常规关闭优先使用 `docker stop`，不把 `docker kill` 或 `docker rm -f` 作为默认方法；本次仅修改文档，没有操作本机 Docker 资源。

## [2026-09-29] query | Mac 后台容器与 Docker Desktop

- 结论：在 Mac 上使用 Docker Desktop 的本地 Engine 时，Desktop 必须运行，但 Dashboard 窗口可以关闭，也无需在每条 CLI 命令前重复启动；`docker run -d` 只脱离终端，不能脱离 Engine。
- 行为：关闭终端不停止后台容器；退出 Docker Desktop 会停止本地 Engine并影响其容器，再次启动时是否自动恢复取决于容器 restart policy。
- 更新：[[Docker架构]]、[[Docker核心学习笔记]]、本文件；补充 Desktop 状态检查、启动、登录时自动启动和 Resource Saver 的使用说明。

## [2026-09-29] query | Mac 关机前的 Docker 停止顺序

- 结论：正常关机不要求先全局停止全部容器再退出 Docker Desktop；有数据库或持续写入服务时，推荐先按容器或 Compose 项目优雅停止，再正常关闭 Mac。
- 操作：区分 `docker compose stop` 的“停止并保留”和 `docker compose down` 的“停止并删除项目容器与网络”；警示 `down -v` 会进一步删除 Volume 数据。
- 边界：不把 `docker stop $(docker ps -q)` 或 `docker system prune` 作为日常关机步骤，避免影响同一 Engine 中的无关项目和资源。
- 更新：[[Docker容器生命周期]]、[[Docker核心学习笔记]]、本文件；依据 Docker 官方 stop 与 Compose stop/down 文档核验。

## [2026-09-30] query | 容器隔离进程与虚拟机 Guest OS

- 结论：容器的主要运行对象是共享外部内核的隔离进程；虚拟机的主要运行对象是拥有独立内核、启动流程和系统服务的 Guest OS。
- 澄清：容器中即使存在 `/bin`、`/etc`、Shell 和系统库，也只是用户态文件，不等于拥有完整操作系统；Guest OS 也不要求必须包含图形桌面。
- 示例：在 Mac 上，macOS 是 Host OS，Docker Desktop 的 Linux VM 是 Guest OS，`hello-world` 或 Nginx 容器是共享该 VM Linux 内核的隔离进程。
- 更新：[[容器与虚拟机]]、[[Docker核心学习笔记]]、本文件。

## [2026-09-30] schema | 流程图统一使用 Mermaid

- 起因：Harlan 要求后续知识库中的流程图统一使用 Mermaid 绘制。
- 规则：步骤流程、状态流转、调用链和数据流均使用 `mermaid` 代码块，不使用 ASCII 字符图；只在 Harlan 明确指定或目标环境无法渲染 Mermaid 时例外并说明。
- 更新：`AGENTS.md`、`README.md`、本文件。

## [2026-09-30] schema | 流程图必须配套详细解释

- 起因：Harlan 要求新增流程图后必须在图下解释完整流程，不能只放一张图。
- 规则：每个流程图下方紧跟文字说明，至少覆盖入口或触发条件、关键节点职责、流转顺序、分支判定和最终输出；说明不得只重复图中标签。
- 更新：`AGENTS.md`、`README.md`、本文件。

## [2026-09-30] query | Docker 镜像层与容器可写层

- 结论：镜像层不是完整文件系统副本，而是相对下层的文件变化集合；Docker 合并只读层形成统一视图，并为每个容器增加独立可写层。
- 复用：内容相同的基础层可被多个镜像共同引用，拉取新镜像时只获取本地缺失的层；共享的是不可变内容，不会产生跨镜像联动修改。
- 写入：新文件写入容器层；修改下层文件时采用 Copy-on-Write；删除下层文件时记录隐藏标记。容器删除后其可写层数据丢失，持久数据应使用 Volume 或 Bind Mount。
- 更新：[[Docker镜像与容器]]、[[Docker核心学习笔记]]、本文件；新增层复用与两个容器独立写入的 Mermaid 图及完整图后说明。

## [2026-09-30] query | AGENTS.md 自动发现与刷新边界

- 确认：当前任务已重新读取根目录 `AGENTS.md`，识别到流程图必须使用 Mermaid、图后必须详细解释两项新规则。
- 机制：Codex 新建任务时会自动枚举并注入从全局、仓库根目录到当前目录的适用 `AGENTS.md`，因此通常无需额外提醒。
- 边界：官方文档未保证活跃任务会实时热加载中途修改的规则文件；同一任务内刚更新规则时，显式提示重新读取最稳妥，Agent 也可通过工作区文件检查主动刷新。
- 更新：[[当前项目工作原理]]、本文件；使用 OpenAI Docs skill 并核对官方 `AGENTS.md` 发现说明。

## [2026-09-30] schema | 多会话共享工作树协作规则

- 起因：同一 Local 项目的多个会话对话上下文独立，却会共享文件改动，需要防止共享页面被旧快照覆盖或把其他会话的工作误提交。
- 规则：新增开工 Git 基线、主题分区负责、共享热点最后写、并发变化检测、按文件精确暂存和 Worktree 隔离六条协作约定。
- 提交边界：默认不使用 `git add -A`；只有 Harlan 明确要求提交全部变更且 Agent 已审阅范围时才可整体暂存。
- 更新：`AGENTS.md`、`README.md`、本文件。

## [2026-09-30] query | 合并 Docker 第 4.1 与 4.3 节

- 调整：将原“4.3 Tag 不等于版本锁定”合并到“4.1 对象模型、Tag 与 Digest”，让 Registry、Repository、Tag、Digest 的定义、命名格式和固定内容方式连续呈现。
- 保留：4.2 继续独立讲解镜像层、层复用、Copy-on-Write 和容器可写层，避免对象标识与文件系统机制混杂。
- 更新：[[Docker核心学习笔记]]、本文件；未改变技术结论和其他章节编号。

## [2026-09-30] schema | 当前会话规则变更检测与重载提醒

- 起因：Harlan 希望一个会话修改知识库规则后，其他活跃会话能发现变化并提醒刷新当前会话的规则。
- 机制：会话开工时记录 `AGENTS.md` SHA-256；写文件前若发现它在 `git status` 中有变化，重新计算哈希。哈希与基线不同时暂停写入，提醒 Harlan 回复「重新加载项目规则」。
- 重载：固定指令是本库自然语言约定，不是 Codex 内置斜杠命令。Agent 收到后完整重读 `AGENTS.md`、更新哈希、摘要影响当前任务的新规则并复核已做工作；若行为仍显示旧规则，建议重启会话。
- 依据：OpenAI 官方说明 `AGENTS.md` 指令链在会话启动时构建，当指令表现过期时建议重启目标会话。
- 更新：`AGENTS.md`、`README.md`、本文件。

## [2026-09-30] schema | 规则变更检测改为直接比较哈希

- 修正：不再以 `git status` 显示 `AGENTS.md` 未提交为重新计算哈希的前提；每次写文件前都直接将当前 SHA-256 与会话开工基线比较。
- 原因：其他会话提交规则变更后，工作树可能恢复干净，仅检查 `git status` 会漏掉已提交的 `AGENTS.md` 更新。
- 更新：`AGENTS.md`、`README.md`、本文件。

## [2026-09-30] schema | 规则哈希提醒排除本会话预期修改

- 修正：当前会话按 Harlan 明确要求修改 `AGENTS.md` 后，直接完整重读规则并更新哈希基线，不再反向要求 Harlan 输入重载指令。
- 提醒范围：只有非本会话预期产生的 `AGENTS.md` 哈希变化，才暂停写入并提醒「重新加载项目规则」。
- 更新：`AGENTS.md`、`README.md`、本文件。

## [2026-09-30] query | 容器主进程与入口脚本退出

- 结论：容器主进程是由 `ENTRYPOINT`、`CMD` 和运行参数最终启动的容器内 PID 1；Docker 以它作为单次容器运行的生命周期锚点。
- 澄清：入口脚本使用 `command &` 把服务放入后台后自行退出，会导致 PID 1 消失并使容器进入 `Exited`；后台子进程不能替代 PID 1 维持容器状态。
- 正确模式：服务以前台模式运行，入口脚本最后用 `exec` 让服务替换 Shell 成为 PID 1；同时区分容器内 `command &` 与宿主机侧 `docker run -d`。
- 更新：[[Docker容器生命周期]]、[[Docker核心学习笔记]]、本文件；增加错误与正确启动分支的 Mermaid 图、完整图后说明和 Nginx 示例。

## [2026-09-30] query | 澄清 Nginx 前台运行与 Shell 进程控制

- 澄清：`-g 'daemon off;'` 是 Nginx 参数，`&`、`exec` 是 Shell 进程控制方式，`echo` 只负责输出文字，三者不能作为相互对应的写法比较。
- 对照：将错误与正确示例改为使用同一条 Nginx 命令，仅比较行尾 `&` 与前置 `exec` 对 PID 1、容器状态和停止信号的影响。
- 更新：[[Docker核心学习笔记]]、[[Docker容器生命周期]]、本文件；未改动此前讨论中的 6.3 流程图尺寸。

## [2026-09-30] query | 补充 entrypoint.sh 备注

- 说明：`entrypoint.sh` 是常被配置为容器启动入口的普通 Shell 脚本，通常负责准备环境并启动实际服务；该文件名只是惯例，可以自定义。
- 更新：[[Docker核心学习笔记]]、本文件；仅增加简短备注，未扩展新章节。

## [2026-09-30] query | 精简 Docker 核心学习笔记章节

- 删除：移除“Docker 与 OCI 的关系”和“macOS、Windows 与 Linux 的差异”两个完整章节，并清理该页中的 OCI 小结、资料声明和专用来源链接。
- 调整：原第 9～17 节依次改为第 7～15 节，原 10.1 同步改为 8.1；Mac 安装步骤及理解 Docker Desktop VM 所需的平台说明保留。
- 更新：[[Docker核心学习笔记]]、本文件；未删除任何页面。

## [2026-09-30] query | 删除 Docker 笔记模板化收尾章节

- 删除：从 [[Docker核心学习笔记]] 移除原第 8～14 节，包括常见错误与排查、安全提醒、动手练习、验收标准、小结、自测题和答案解析；原“来源”顺延为第 8 节。
- 后续约定：Docker 专题正文不再默认生成上述模板化收尾章节，聚焦概念、原理、命令和直接相关实验；必要风险与易错点改为就近说明。
- 更新：[[Docker核心学习笔记]]、[[Docker学习路径]]、本文件；未删除任何页面。

## [2026-09-30] query | Docker 第二阶段镜像构建与数据存储

- 研究：核对 Docker 官方 Dockerfile reference、构建上下文、BuildKit、构建缓存、多阶段构建、Volume 与 Bind Mount 文档，并核实 Nginx 官方镜像当前实验标签。
- 学习内容：新增 [[Dockerfile与镜像构建]] 与 [[Docker数据存储]]；新术语首次出现时使用两三行注释解释，未添加模板化小结、自测或答案章节。
- 知识网络：新增 [[Docker镜像构建]]、[[Docker数据持久化]] 和 [[Docker镜像构建与挂载实验]]，同步更新 [[Docker学习路径]] 与索引。
- 实验：新增 `code/docker-learning-labs/02-image-and-storage/`，使用多阶段 Dockerfile 生成 Nginx 网页，并提供命名 Volume 与 Bind Mount 的精确验证、停止和清理命令。
- 验证边界：检测到 Docker CLI 29.8.1、Buildx 0.37.1、Compose 5.5.1；Codex 执行环境无权访问 Docker socket，因此只完成官方资料核验和静态检查，未声称镜像已实际构建运行。

## [2026-09-30] query | 英语基本句型与口语造句

- 触发：Harlan 希望把“做什么、是什么、给谁什么、让某人怎么样、哪里有什么”的记忆规则整理进英语知识库，并补充自然例句与其他句式分类。
- 校准：传统五大基本句型通常是 `SV / SVO / SVC / SVOO / SVOC`；`There be` 是独立的存在结构，不是传统第五句型。
- 补充：加入常见的 `SVA / SVOA`、陈述/疑问/祈使/感叹、简单句/并列句/复杂句，以及 dummy `it`、被动语态和从句等扩展框架。
- 口语方法：新增从“最小意思 → 主语和核心动词 → verb pattern → 补充背景 → 否定或疑问”的 Mermaid 造句流程，并提供完整图后说明、易错边界和求助表达。
- 核查：参考 British Council 的 clause structure and verb patterns，以及 Cambridge 的 clauses、objects、complements、`There be`、clause types 和 sentences 资料。
- 更新：[[英语学习笔记]]、[[英语基本句型与口语造句]]、[[index]]、本文件。

## [2026-09-30] query | Docker 第二阶段端到端验证

- 环境：macOS Docker Desktop 4.93.0，Docker Engine/CLI 29.8.1，Buildx 0.37.1，Compose 5.5.1，`linux/arm64` Engine。
- 构建：成功构建 `harlan/docker-build-demo:1.0`；Nginx 返回预期大写文本；连续构建确认 `WORKDIR`、`COPY`、`RUN` 和 `COPY --from` 均命中 BuildKit 缓存。
- 存储：成功验证命名 Volume 被两个不同的一次性容器读写；readonly Bind Mount 成功向 Nginx 提供宿主机文件。
- 镜像：解析到 `alpine:3.23` Digest `sha256:85fe1e81...` 与 `nginx:1.31.6-alpine` Digest `sha256:df221db8...`，完整值保留在实际构建输出中。
- 清理：确认临时容器 `codex-docker-build-check`、`codex-docker-bind-check`，Volume `codex-docker-learning-data` 和自定义镜像均已移除；未执行任何全局 prune。
- 更新：[[Docker镜像构建与挂载实验]] 的 `verified`、[[Dockerfile与镜像构建]]、[[Docker数据存储]]、[[Docker学习路径]] 及实验 README。

## [2026-09-30] query | 删除英语笔记易混动词章节

- 删除：按 Harlan 要求，从 [[英语学习笔记]] 移除原第 6 节“易混动词”及其 `speak/say/talk/tell`、`look/see/watch/view`、`reserve/preserve/conserve` 三组内容。
- 调整：原第 7～10 节顺延为第 6～9 节，并同步更新目录和全部子节编号，避免留下编号空档。
- 边界：未删除相关概念页，也未修改 `raw/`。
- 更新：[[英语学习笔记]]、本文件。

## [2026-09-30] query | Docker 学习笔记阶段编号

- 顺序：明确前三阶段为“Docker 核心概念 → Dockerfile 与镜像构建 → Docker 数据存储”，先学习 `COPY` 再比较运行时挂载。
- 命名：三个稳定学习入口增加 `01`、`02`、`03` 前缀，旧名称保留为 aliases，历史链接仍可解析。
- 同步：更新 [[Docker学习路径]]、索引、相关概念与操作页，以及实验 README 中的页面路径。

## [2026-10-01] schema | 方案 A：项目 Skill 与按需工作流

- 授权：Harlan 选择方案 A，安装 obsidian-markdown、defuddle，并使用现有 skill-creator 创建摄入、问答和治理三个项目 Skill。
- 结构：五个 Skill 放在 .agents/skills/ 随 Git 管理；AGENTS.md 保留唯一 Schema 权威、核心约束和路由，详细步骤、正文骨架与交接提示词按需读取。不迁移知识页面，不改变 raw/wiki/outputs 三层结构。
- 开销：AGENTS.md 从 23,744 字节缩到 12,183 字节，约减少 49%；仅为 UTF-8 规则文本体积对比，未把它等同为模型 Token 或账单降幅。obsidian-markdown 的触发描述收窄到特殊语法处理。
- 刷新：新增 Schema 版本 2026-10-01.1；以后项目 Skill 的规则/流程变化也必须递增根版本。现有会话通过根哈希发现变化，收到“重新加载项目规则”后重读根文件和当前所需 Skill。
- 来源：外部 Skill 固定到 kepano/obsidian-skills 提交 3ccff5338ea700537839b21900aa5358a0402c98，保留 MIT 许可证并记录项目适配；Defuddle 0.19.4 安装在 scripts/node_modules/，package-lock.json 固定依赖树，依赖目录不进 Git。
- 适配：外部样例不覆盖本库字段、链接和权限规则；网页清洗输出只进标准输出或临时目录。澄清无空格命名示例与历史文件兼容方式、移动后的相对链接检查、未实测 howto 不填验证日期。
- 文档：同步 README 与 [[当前项目工作原理]]、[[index]]；待落地清单中的页面骨架已通过 Skill references 落地并移出，不新建 wiki/templates/ 内容分类。
- 验证：五个 Skill 均通过官方 quick_validate；23 处本地 Markdown 引用可解析，Defuddle 声明和锁文件版本一致；Node.js v26.0.0 下成功提取 Obsidian 官方 links 页面。初次联网因沙箱限制失败，经授权重试成功。
- 脚本：lint 排除 .agents/、.codex/ 和 node_modules/，防止示例文档掩盖断链；三项回归测试通过；python3 scripts/lint.py 无错误或警告，git diff --check 通过。未声称完成 Obsidian 界面渲染或客户端自动触发的端到端验收。
- 边界：保留开工前已有的 Docker、英语及规则文档修改；未修改 raw/ 或无关实验项目，未删除知识页面，未提交或推送 Git。

## [2026-10-01] query | 按要求删除 Codex 旧对话排障页

- 授权：Harlan 明确要求删除“Codex旧对话提供商缺失排障”文件。
- 删除：`outputs/通用/Codex旧对话提供商缺失排障.md`；移除索引条目，输出页统计从 12 改为 11。该文件删除前无未提交修改，可从 Git 历史恢复。
- 历史：本日志两处旧链接使用原别名 `2026-09-24-Codex旧对话提供商缺失排障`；页面及其别名已移除，旧链接不再有效。按日志只追加约定保留原条目，不另建占位页或伪造别名目标。
- 范围：仅删除指定文件并维护索引/日志；既有未提交改动保留，未改变 Schema 或体检脚本。

## [2026-10-01] schema | 日常使用说明对齐项目 Skill

- 起因：方案 A 已加入 Skill 说明，但 README 的“日常怎么用”仍保留旧版六步流程，未完整说明新入口和处理边界。
- 更新：按场景列出摄入、复习整理、学习问答、问题队列和治理入口，并提供可复制提示词；补充直接提供网页/文本、Defuddle 临时清洗、个人记录与 PDF 的处理方式。
- 对齐：说明已有明确重点不重复确认、普通摄入与主题复习的区别、仅讨论不落盘、避免空改，以及体检诊断与执行修复的范围；同步手册中的结论落盘说明。
- 范围：仅修改 README 与追加本日志；这是对现有 AGENTS.md 和 Skill 的说明同步，未新增规则或更改 Skill 行为，Schema 版本保持 2026-10-01.1。未新增知识页面，index 无需改动。
- 验证基线：本次开工时 lint 已报告 1 项历史日志断链，来自此前经授权删除的排障页；本次文档同步不处理该已有问题。

## [2026-10-01] lint | 知识库内部体检

- 存放：按 Harlan 本次明确要求，将完整结果保存在 wiki 内部，不生成 outputs 报告，不主动展开给使用者。采用本日志追加记录，不新增目录、页面类型或永久规则；治理 Skill 的默认报告路径未修改。
- 范围：检查当前工作树中的 30 个 wiki 页面、11 个输出页，以及规则、README、待落地清单、问题队列和 lint 实现；仅列出 raw 文件并核对引用路径，不修改原始资料。开工有多项既有未提交修改，检查对象不是纯 HEAD 快照。
- 基线：Schema 2026-10-01.1；AGENTS.md SHA-256 为 `af527a0f59974ef9973652ce99926935b78d0568846e4f6be64e3a536e606dd4`，写前未变化。最近提交为 `2e776f3`、`1da2108`、`403b8bd`、`184178a`；本次不提交或推送。

### 确定性检查与正向结果

- `python3 scripts/lint.py`：1 项错误、0 项警告；错误是既有历史日志断链，不是本次新增。开工记录数为 77，本条追加后为 78；知识页数量不变。
- `python3 scripts/test_lint.py`：3 项回归测试通过，覆盖不存在的页面、工具文档不能冒充知识页、真实知识页可解析三种情况；不代表 lint 已覆盖完整 Schema。
- 当前知识页均已收录索引，来源 3、概念 16、操作 3、实体 4、输出 11，与索引统计一致。文件名无完全重名，忽略空格、连字符、下划线及大小写后，文件名、title、一级正文标题各自也未发现重复；lint 未报告别名冲突。该结果不是对所有语义近义重复的绝对排除。
- 普通内联相对 Markdown 链接的目标文件扫描未发现缺失；不包含锚点有效性、全部 Markdown 语法或外部 URL 可访问性验证。检查到 14 个 Mermaid 图块，图后均有解释文字；未实际渲染图，也未据此认定每段解释都完整覆盖分支。

### 待治理问题

1. **优先：删除页与历史日志校验缺少配套约定。** 本日志第 223、272 行仍引用已获准删除页面的原别名 `2026-09-24-Codex旧对话提供商缺失排障`；同一目标被 lint 按文件去重为 1 项错误。影响是合法删除后体检持续失败，但日志又禁止改写。建议后续设计显式删除登记，只对有删除证据的历史 log 链接给予可追踪的处理，实时知识页仍严格检查；不要全面跳过日志或创建伪知识页。需同步 Schema、脚本和回归测试，本次仅记录，不执行。

2. **优先：三页 sources 引用了不存在的 raw 文件。** `raw/LLM Wiki 搭建教程 - 飞书云文档.md` 当前不存在，却仍出现在 [[持久 Wiki 实践要点]]、[[Andrej Karpathy]]、[[2026-09-17 LLM Wiki 搭建教程（飞书云文档）]] 的 sources 中；来源页正文还把它列作原始剪藏版本。实际存在的是带“（完整正文重建版）”的文件，不能仅凭相似名称就判定内容可替代。影响是来源可追溯性不实，当前 lint 只统计引用，未检查目标存在。建议核对 Git 历史与重建版内容后，再修正这三页的来源记录、明确缺失版本；不在 raw 中补造文件，不擅自将两个版本合并为一个来源。

3. **优先：全局现状与部分说明滞后。** [[overview]] 仍称“技术内容仍是零”“最大的缺口：没有技术内容”，但索引已有容器概念 6 页、系统框架概念 2 页和操作 3 页；“3 份来源摘要仍都是方法论资料”不等于“没有技术内容”。它还称外部核实机制不存在，而根 Schema 已规定 URL 与访问日期写正文。[[当前项目工作原理]] 的“当前状态”保留截至 2026-09-24 的旧统计，应视为注明日期的历史快照而非伪事实，但容易被当成当前值。飞书来源摘要中“本库则把 Schema 单列为第三层”的比较也已过时。建议单独刷新 overview 和本库现状比较，保留来源原观点及历史日志；动态数量尽量由 index 提供，避免多处复制。成本是少量治理文字更新，不需要改写技术内容。

4. **一般：18 页 title 与文件名不一致，属于命名规则漂移，不是发现 18 组重复页。** 差异主要是空格和连字符；导航标题已按例外排除，历史文件名含空格本身不算违规。范围如下：
   - 容器概念：`Docker容器生命周期`、`Docker数据持久化`、`Docker架构`、`Docker镜像与容器`、`Docker镜像构建`。
   - 系统框架概念：`Kafka可靠性与交付语义`、`Kafka核心架构`。
   - 操作页：`Docker环境验证与首个容器`、`Docker镜像构建与挂载实验`、`Kafka KRaft开发环境`。
   - 输出页：`Java消息队列概览与选型`、`Maven-Wrapper`、`RabbitMQ入门实战`、`01-Docker核心学习笔记`、`02-Dockerfile与镜像构建`、`03-Docker数据存储`、`Docker学习路径`、`Apache Kafka学习指南`。
   建议优先评估将 title 对齐现有文件名，确有检索价值的显示变体放 aliases，以减少路径迁移；批量处理前确认范围并检查别名冲突。README“归类与命名规则”仍以带空格名称作规范名示例，且“不许中英混用”的字面表达与保留技术专有名词的例子不一致，建议同步澄清新命名与历史兼容，不批量重命名历史文件。

5. **一般：lint 的覆盖小于完整 Schema，不能把仅有 1 项机器错误理解为全库只剩 1 个问题。** `scripts/lint.py` 第 81 行以文件名构建字典，跨目录同名会被覆盖；第 90 行 howto 必需字段未含 env；尚无 title/文件名一致性、sources 路径存在性、相对 Markdown 目标和日志动作枚举校验。建议先增加低歧义规则及对应测试，再考虑复杂语义检查；遗留不一致应有明确迁移计划，不能靠自动重写全库消除。扩展脚本是后续治理任务，本次不实施。

### 语义抽查与验证边界

- Docker、Kafka 的概念页、操作页与主题输出职责总体可区分，未据标题相近就判定为应合并。Java、Python 已有输出，但对应概念/操作区仍空；这是按复用需求逐步补充的知识网络缺口，不要求现在拆出每个术语。优先在后续重复提问时识别可独立复用的对象，再查重建页。
- [[Docker容器生命周期]] 的图后说明偏向状态定义，转换条件与结束行为部分散落后文；下次相关主题编辑时，可将必要的触发、重启与删除分支就近解释，不据此开展全库流程图改写。
- 3 个 howto 均有 env；其中 2 个 verified 留空，不应以本次体检日期冒充实测日期。网页来源写在正文、sources 留空本身不违反当前 Schema；未逐条联网核查技术断言、时效、访问日期与置信度，也未重跑 Docker、Kafka、Python、Java 实验或客户端 Skill 自动触发。
- 未发现必须立即引入全文检索、知识图谱或新内容类型的证据；既有暂缓方案继续以待落地清单中的触发条件评估，不为本次检查扩建架构。
- 执行边界：仅追加本条内部报告，未修改学习页、README、Schema、Skill、脚本或 raw，未执行任何删除、重命名和批量修复。无新页面、合并或摘要变化，index 无需空改。后续修复须单独授权并重新检查工作树与规则哈希。

## [2026-10-02] lint | 内部体检收尾验证

- 续接：完成上一日体检的写后验证，详细发现保留在上一条记录，不生成 outputs 报告，也不改写历史检查结果。
- 并发变化：续接时发现开工基线之外的新文件 `outputs/通用/english-speaking-patterns.md`，输出页数量由 11 增至 12；这不是本次体检创建的文件，未修改、删除或代为补齐。
- 当前校验：`python3 scripts/lint.py` 报告 2 项错误、1 项警告。除原有历史日志断链外，新文件缺少 frontmatter，且未登记到 index；保留原文件，待其所属学习任务完成或另行授权处理，不将其计作本次审计新增缺陷。
- 完整性：按写入前 63,735 字节及 SHA-256 核验，先前日志内容完整保留，体检报告只在末尾追加；AGENTS.md 哈希与上次基线一致。`git diff --check` 通过，3 项 lint 回归测试通过，但全库 lint 尚未通过。
- 边界：本次仅追加内部检查记录，不改 Schema、Skill、索引或学习内容，不提交或推送。上次的页面统计是当时快照；本条记录续接时的新增状态。
- 写后快照：复跑期间最初的 `english-speaking-patterns.md` 路径已不存在，lint 的新增报错路径变为 `outputs/通用/Speaking.md`，仍为缺 frontmatter 和未登记索引；不能仅据路径变化确认是重命名。这说明相关工作区仍有并发变动，上述结果只代表检查时点，本次不追改其他任务进行中的页面。

## [2026-10-02] schema | 连续新名词解释合并为单个框

- 起因：Harlan 指出 [[02-Dockerfile与镜像构建]] 中四个紧挨着的“新名词”分别显示为四个框，阅读上过于分散。
- 规则：同一语境下连续解释多个新名词时，用一个“新名词” callout，框内逐项加粗名词并保留各自定义；中间有正文、代码、图表或主题变化时不强行合并。
- 示例：将该页“基础镜像 / 构建阶段 / Alpine Linux / 语法指令”四个 callout 合成一个，原有解释和顺序保留；仅做呈现调整，未改技术结论。
- 同步：更新 `AGENTS.md` Schema 版本至 2026-10-02.1，并在 `README.md` 的使用约定中说明；页面名称、索引摘要和统计未变化，`wiki/index.md` 无需改动。
- 范围：保留开工前已有的未提交修改与其他主题页面；未改项目 Skill、脚本或 raw，未提交或推送 Git。

## [2026-10-02] query | 排查并合并 Docker 连续新名词解释

- 排查：检查当前 Docker 输出页中的全部“新名词” callout；截图所示四个名词已由 Schema 更新同步合并。
- 调整：在 [[02-Dockerfile与镜像构建]] 中继续合并 Dockerfile/构建、ARG/ENV、构建上下文/`.dockerignore`、构建缓存/缓存失效、多阶段构建/构建产物五组连续解释。
- 调整：在 [[03-Docker数据存储]] 中合并数据持久化/挂载、Volume/Bind Mount 两组连续解释。
- 边界：被正文、命令、代码或图表隔开的独立名词解释保持不动；技术结论与索引摘要未变化，因此未修改 index。

## [2026-10-02] query | 英语人称代词与所有格

- 新增：[[英语人称代词与所有格]]，系统整理 `I/me/my/mine/myself` 等主格、宾格、物主限定词、名词性物主代词与反身代词。
- 补充：记录 `you` 的单复数、dummy `it`、单数 `they`、代词与一般现在时动词一致，以及 `its/it's`、`I/me` 和反身代词的常见错误。
- 练习：在 [[英语学习笔记]] 第 6 节加入速查表、自然例句和人物轮换练习，强调换代词时同步调整动词形式。
- 核查：参考 Cambridge Grammar 与 British Council 的 personal、possessive 和 reflexive pronoun 资料，访问日期为 2026-10-02。
- 更新：[[英语学习笔记]]、[[英语人称代词与所有格]]、[[index]]、本文件；未修改 `raw/` 或 Speaking 文档。

## [2026-10-02] query | Docker build 执行目录与末尾点号

- 结论：`docker build --tag harlan/docker-build-demo:1.0 .` 应在 `code/docker-learning-labs/02-image-and-storage/` 执行。
- 解释：`1.0` 是镜像标签；末尾 `.` 是独立的路径参数，表示以当前目录作为构建上下文，并非标签的一部分。
- 更新：在 [[02-Dockerfile与镜像构建]] 增加明确的 `cd` 命令，并拆解 `docker build`、`--tag` 与构建上下文参数；索引摘要未变化。

## [2026-10-02] query | Docker run 实验命令解释

- 解释：拆分 `docker run`、`--name`、`--detach`、`--publish` 与镜像引用，说明该命令会创建并后台启动容器。
- 端口：明确 `127.0.0.1:8080:80` 表示从 Mac 本地 8080 端口转发到容器 80 端口，默认仅本机可访问。
- 格式：说明行末反斜杠只是 Shell 续行符，不应写成 `\--detach`，并补充等价单行命令、状态检查与清理边界。
- 更新：[[02-Dockerfile与镜像构建]]；索引摘要未变化。

## [2026-10-02] query | 删除容器后镜像仍存在与 image ls 输出

- 区分：`docker rm` 只删除容器，不删除其镜像；需要时使用 `docker image rm harlan/docker-build-demo:1.0` 单独删除实验镜像。
- 截图：实验容器删除后，自定义镜像仍在但 `U` 消失；`nginx:latest` 的 `U` 表示另有现存容器引用该镜像，且它与实验使用的 `nginx:1.31.6-alpine` ID 不同。
- 列说明：解释 Docker CLI 29 的 `IMAGE`、`ID`、`DISK USAGE`、`CONTENT SIZE` 和 `EXTRA`；`U` 表示 In Use，包括运行中或已停止但尚未删除的容器引用。
- 纠错：截图第一次使用 `docher-build-demo`，因名称拼写错误而提示不存在；第二次使用正确名称后删除成功。
- 核查：参考 Docker 官方 `docker image rm` 文档与 docker/cli #5560，访问日期 2026-10-02；更新 [[02-Dockerfile与镜像构建]]，索引摘要未变化。

## [2026-10-02] query | 在 Dockerfile 指令前补充 build 与 run 命令

- 顺序：在原 `RUN`、`CMD` 与 `ENTRYPOINT` 章节之前新增终端命令基础章节，后续原第 3～9 节顺延为第 4～10 节。
- 语法：解释 Option、位置参数、可选项、占位符，以及 `docker build [OPTIONS] PATH` 和 `docker run [OPTIONS] IMAGE [COMMAND] [ARG...]` 的参数位置。
- 参数：整理当前学习阶段需要的构建标签、Dockerfile、构建参数、目标阶段、缓存、平台，以及容器名称、后台运行、端口、环境变量、挂载、网络、交互和资源限制等常用选项。
- 衔接：明确区分终端命令 `docker run`、`docker build` 与 Dockerfile 指令 `RUN`、`CMD`、`ENTRYPOINT`，并用三个可复制命令说明镜像名之后的命令参数。
- 核查：参考 Docker 官方 `docker buildx build`、`docker container run` 与 Running containers 文档，访问日期 2026-10-02；更新 [[02-Dockerfile与镜像构建]]，索引摘要未变化。

## [2026-10-02] query | Docker 镜像引用名称拆分

- 纠正：`harlan/docker-build-demo:1.0` 不是“镜像名 `harlan` 加标签 `docker-build-demo:1.0`”。
- 拆分：`harlan` 是命名空间，`docker-build-demo` 是仓库名，`1.0` 是冒号后的标签；`harlan/docker-build-demo` 合起来通常称为镜像名或仓库路径。
- 边界：本地使用 `harlan` 命名不会自动上传镜像，也不验证同名 Registry 账号是否存在。
- 更新：[[02-Dockerfile与镜像构建]] 的构建命令解释；索引摘要未变化。

## [2026-10-02] query | 调整镜像引用解释位置

- 移动：按 Harlan 指定位置，将 `harlan/docker-build-demo:1.0` 的命名空间、仓库名和标签解释移动到 `--build-arg` 安全提醒之后。
- 去重：原位置不再保留同一组解释，技术内容未变化；更新 [[02-Dockerfile与镜像构建]]，索引无需修改。

## [2026-10-02] query | 细化 ENTRYPOINT 与 CMD 参数执行过程

- 拆解：逐项解释 `python`、`-m`、`http.server`、端口和 `--directory` 参数的含义，并展示 Docker 最终交给操作系统的完整参数数组。
- 覆盖：明确镜像名后的运行参数会整组替换 `CMD`，再追加到 Exec form 的 `ENTRYPOINT`，不是只替换默认参数中的某一项。
- 边界：补充容器监听端口与宿主机端口发布的区别，并对比 Exec form、Shell form 及其主进程和信号处理差异。
- 核查：参考 Docker 官方 Dockerfile reference 与 Running containers 文档，访问日期 2026-10-02；更新 [[02-Dockerfile与镜像构建]]，索引摘要未变化。

## [2026-10-04] query | 规则动词 -ed 词尾发音

- 规则：在 [[英语发音与重音]] 与 [[英语学习笔记]] 中区分规则动词 `-ed` 的 `/t/`、`/d/`、`/ɪd/` 三种读音，强调依据原形的最后一个音而不是最后一个字母。
- 原理：补充清辅音后读 `/t/`、元音或浊辅音后读 `/d/`、`/t/` 或 `/d/` 后增加音节读 `/ɪd/`，并用声带振动解释发音动作。
- 边界：说明 `/ɪd/` 才增加音节；自然语流中的弱化不等于基础形式改变；`naked`、`crooked` 和表示“博学的”`learned` 等词汇化形容词需要查词典。
- 练习：新增 `look → looked`、`play → played`、`want → wanted` 三组递进口语练习，以及 `looked‿at`、`played‿it` 的元音前连接。
- 核查：参考 Cambridge Grammar、BBC Learning English、British Council 与 Cambridge Dictionary，访问日期为 2026-10-04；[[英语发音与重音]] 的 confidence 由 low 更新为 medium。
- 更新：[[英语学习笔记]]、[[英语发音与重音]]、[[index]]、本文件；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 新建英语发音学习笔记

- 触发：Harlan 希望把 `-ed` 发音放入独立文档，并在后续持续增加更多发音知识。
- 新增：[[英语发音学习笔记]]，作为稳定的发音专题复习入口；首章完整收录 `-ed` 三种读音、清浊音原理、音节变化、固定形容词例外、语流连接、听辨与口语肌肉训练。
- 分层：[[英语学习笔记]] 只保留三类读音速查表和专题链接；[[英语发音与重音]] 只保留声音同化原理、音节结论和外部来源，减少长篇重复。
- 后续：新的发音复习内容优先继续更新 [[英语发音学习笔记]]；可复用的原理仍同步维护在对应概念页，不为每次提问新建近义页面。
- 更新：[[英语发音学习笔记]]、[[英语学习笔记]]、[[英语发音与重音]]、[[index]]、本文件；未删除页面，未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | turn out to be 句型

- 句型：在 [[英语学习笔记]] 的 `turn` 词族中补充 `主语 + turn out + to be + 表语`，并拆解 `The party turned out to be very fun.` 的主语、谓语、不定式结构和表语。
- 扩展：整理 `turn out to be + 形容词/名词短语`、`turn out + 形容词/副词` 与 `It turns/turned out that + 从句` 三类常用表达，并补充自然例句。
- 区分：`turn out to be` 强调真相或结果后来显现，`turn into` 强调实际发生变化；说明非正式英语中的形容词 `fun` 可用于 `very fun`，也可说 `a lot of fun`。
- 核查：参考 Cambridge Dictionary 与 Oxford Learner's Dictionaries，访问日期为 2026-10-04；[[英语高频动词与短语动词]] 的 confidence 由 low 更新为 medium。
- 更新：[[英语学习笔记]]、[[英语高频动词与短语动词]]、本文件；页面名称与索引摘要未变化，因此未修改 index；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | is 连读训练第一批

- 格式：在 [[英语发音学习笔记]] 建立固定的“连读组合｜连读音标｜练习例句”表格；后续连读材料按批次追加，每个连读占一行。
- 内容：整理 `What is`、`Where is`、`When is`、`Which is`、`name is`、`time is`、`there is`、`each is` 八组英式目标音和自然例句。
- 校准：按 Cambridge Dictionary 将 `/ɪz/` 记为 `is` 的完整/强式，而非弱读；另行区分 `/z/`、`/s/` 弱式和 `what's/where's/there's` 缩约形式。
- 原理：在 [[英语发音与重音]] 补充辅音接元音的连读、非卷舌英式口音中的 linking r，以及连读、弱读与缩约的边界。
- 来源：本批来自 Harlan 提供的抖音博主“Sara 老师英语小灶”视频摘要；因未提供原视频链接，不视为逐字转录。另参考 British Council、BBC Learning English 与 Cambridge Dictionary 核查，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、[[index]]、本文件；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 基础代词与 be 连读训练第二批

- 内容：在 [[英语发音学习笔记]] 追加 `it is`、`that is`、`these are`、`those are` 的连读音标和练习例句；`which is` 已在第一批收录，不重复建行。
- 校准：`it is`、`that is` 保留完整 `is /ɪz/`，并提示常见缩约 `it's /ɪts/`、`that's /ðæts/`。
- 强弱式：区分 `are` 的英式强式 `/ɑː/`、弱式 `/ə/` 与美式强式 `/ɑːr/`、弱式 `/ɚ/`；将资料中的美式 `/ər/` 规范为 r-coloured schwa `/ɚ/`。
- 原理：在 [[英语发音与重音]] 补充 `these/those + are` 中辅音到元音的连读与 `are` 弱读可能同时发生。
- 核查：参考 Cambridge Dictionary 的 `are`、`these`、`those` 发音资料，访问日期为 2026-10-04；索引摘要仍然准确，无需修改 index。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 优化连读训练表结构

- 分类：移除“第一批”“第二批”编号标题，改为“疑问词及常用名词 + `is`”和“代词、指示词 + `be`”两个内容型小标题。
- 表格：统一增加“中文意思”列，形成“连读组合｜中文意思｜连读音标｜练习例句”的固定顺序，并为现有 12 个连读组合补充语境化释义。
- 表达：将正文中的“本批”“第一批”等说法改成“本组”或具体小节名称，后续内容按语言现象归类，不再按提交顺序编号。
- 更新：[[英语发音学习笔记]]、[[index]]、本文件；发音结论未变化，因此无需修改概念页；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 连读表统一为美式强弱读

- 音标：[[英语发音学习笔记]] 的连读训练表只保留美式音标，移除表中的英式音标。
- 格式：继续使用单个“连读音标（美式）”列，在同一单元格内依次展示强读与弱读，不拆成两列。
- 缩约：对 `what's`、`where's`、`it's`、`that's` 等常用形式同时标明弱读音标和书写形式；`which is`、`each is` 不硬造不常用的更短形式。
- 强弱式：为 `these are`、`those are` 同时列出美式 `are` 的强式与弱式，并保留中文意思和原练习例句。
- 呈现：连读章节中的音标集中放入表格，规则和资料来源也改用表格呈现；索引摘要同步为“美式强弱读”。
- 核查：参考 Cambridge Dictionary 的 `is`、`are`、相关单词发音和 Contractions 语法页，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[index]]、本文件；概念页继续保留英美差异作为原理参考，未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 连读训练表仅保留美式强读

- 取舍：Harlan 决定当前阶段只记清晰的强读；从 [[英语发音学习笔记]] 的连读训练表删除全部弱读和缩约音标。
- 格式：音标列统一为“连读音标（美式强读）”，每个组合只保留一个美式强读音标，中文意思和练习例句不变。
- 范围：删除 `is` 的缩约读法以及 `are` 的弱式，仅保留 `What is`、`these are` 等完整组合的美式强读。
- 导航：[[index]] 摘要由“美式强弱读”调整为“美式强读”；概念页仍保留弱读作为客观发音原理，不进入当前练习表。
- 更新：[[英语发音学习笔记]]、[[index]]、本文件；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 动词加 it 连读训练

- 内容：在 [[英语发音学习笔记]] 新增“动词 + `it`”小节，收录 `get/take/make/have/give/leave/say/know/put/let + it` 十个高频组合。
- 格式：继续按“连读组合｜中文意思｜连读音标（美式强读）｜练习例句”逐行整理，不加入自然语流弱读。
- 校准：视频把美式 flap t 写成 `/d/` 只是近似听感；精确语音实现应记为 voiced alveolar flap `[ɾ]`，而基本音位仍是 `/t/`。
- 纠错：`let it` 的词界是 `/t/ + /ɪ/`，不是两个 `/t/` 相遇；`take/make + it`、`have/give/leave + it`、`say/know + it` 也分别属于不同的词界声音组合，不能全部套用 flap t。
- 分层：练习表只保留清晰强读；[[英语发音与重音]] 增加 flap t 的适用环境、音位与具体语音实现的区别，供听辨时参考。
- 核查：参考 Cambridge University Press、Iowa State University 与 Washington State Board for Community and Technical Colleges 的美式 flapping 资料，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；索引摘要仍然准确，无需修改 index；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | of 与 to 高频语块发音训练

- 内容：在 [[英语发音学习笔记]] 新增“数量、范围表达 + `of`”和“动词 + `to`”两组表格，收录 15 个高频语块的中文意思、美式强读和练习例句。
- 格式：继续只记录美式强读；`of` 使用 `/ɑːv/`，`to` 使用 `/tuː/`，不把 `kinda`、`wanna`、`gonna`、`gotta` 等弱化或缩约读法写入练习表。
- 校准：`of /əv/` 属于弱读；`to` 以辅音 `/t/` 开头，所以“动词 + `to`”并不是“辅音 + 元音”连读，而可能涉及弱读、同化或口语缩约。
- 纠错：`used to` 的清晰读法保留 `/s/` 和 `/t/`，不是 `justa`；`hafta`、`sposta`、`needa`、`comea` 不作为标准拼写或固定强读记录。
- 核查：参考 Cambridge Dictionary 的 `of`、`to`、`wanna`、`gonna`、`gotta`、`supposed` 和 Oxford Learner's Dictionaries 的 `used to`，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；索引摘要仍然准确，无需修改 index；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 更正 of 语块为自然弱读

- 更正：Harlan 指出 `of` 系列用于连读训练时应体现 schwa；将 `lots of`、`one of`、`some of`、`kind of`、`sort of`、`couple of`、`out of` 中的 `of` 由强式 `/ɑːv/` 改为日常非重读语流中的 `/əv/`。
- 区分：`/ɑːv/` 仍是美式英语中强调或单独读 `of` 时的强式，但不适合作为这一组自然口语训练的目标读法。
- 格式：`of` 表头明确标为“美式自然弱读”；其他既有表格继续保留美式强读，`to` 组仍使用 `/tuː/`。
- 导航：同步调整 [[index]] 摘要，不再概括为所有训练表均只含美式强读。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、[[index]]、本文件；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | to 语块改为美式日常读法

- 规则：[[英语发音学习笔记]] 后续按材料实际训练的美式日常读法记录，不再机械地把每组音标统一为强式；资料音标有误时先核查、校正。
- 修改：将“动词 + `to`”表改为日常弱化读法，记录 `want to /ˈwɑːnə/`、`have to /ˈhæftə/`、`going to /ˈɡɑːnə/`、`need to /ˈniːdə/`、`used to /ˈjuːstə/`、`supposed to /səˈpoʊstə/`、`got to /ˈɡɑːt̬ə/`。
- 纠错：资料中的 `/ɒ/`、`/əʊ/` 改为对应的美式 `/ɑː/`、`/oʊ/`；`come to` 通常保留 `/t/`，因此记作 `/kʌm tə/`，不记成 `/ˈkʌmə/`。
- 边界：表格保留标准拼写；`wanna`、`gonna`、`hafta`、`needa` 等只用于解释口语听感，不替代正式书写，具体弱化仍受语速、重音和说话人影响。
- 核查：参考 Cambridge Dictionary、Oxford Learner's Dictionaries、VOA Learning English、Pronuncian，以及 Lorenz 与 Tizón-Couto 的美式 `V-to-Vinf` 语料研究，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；[[index]] 摘要仍然准确，无需修改；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 情态动词加 have 的自然弱读

- 内容：在 [[英语发音学习笔记]] 新增“情态动词 + `have`”小节，收录 `should/could/would/might/may/must + have` 六个组合的中文意思、美式日常读法和练习例句。
- 发音：保留材料中的自然弱读，将非重读助动词 `have` 记作 `/əv/`；补全 `must have /mʌst‿əv/`。
- 语义：补充 `should have` 的“本应做却未做／按理应该已经”、`could have` 的“未实现能力或机会／过去可能性”两类常见用法，并区分 `may/might have`、`must have` 与 `would have`。
- 拼写：说明 `'ve` 的读音虽然与弱读 `of` 相同，标准书写仍是 `have` 或 `'ve`，不能写成 `should of`、`could of`、`would of`。
- 核查：参考 Cambridge Dictionary、Oxford Learner's Dictionaries 与 British Council 的发音和过去情态结构资料，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；[[index]] 摘要仍然准确，无需修改；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 疑问词与代词加 are 的日常读法

- 内容：在 [[英语发音学习笔记]] 新增“疑问词、代词 + `are`”小节，整理 `what/where/there/how/when/you/we + are` 七个高频组合的中文意思、美式日常读法和练习例句。
- 弱读：疑问词和 `there` 后的非重读 `are` 采用美式弱式 `/ɚ/`；`where are`、`there are` 中相邻的卷舌成分在快速语流中会紧密融合。
- 闪音：`what are` 记录常见美式读法 `/ˈwɑːt̬ɚ/`，其中 `/t/` 在重读元音与非重读元音之间可能实现为 flap。
- 缩约：代词组合采用日常更常见的 `you are → you're /jɚ/` 与 `we are → we're /wɪr/`，并保留标准缩约拼写。
- 核查：参考 Cambridge Dictionary 的 `are`、`you're`、`we're` 以及 Rachel's English 的 `are` 弱读讲解，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；[[index]] 摘要仍然准确，无需修改；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 统一 are 系列的宽式弱读

- 更正：上一版把 `are /ɚ/` 的弱读、`what are` 的可选 flap 以及 `you are / we are` 的缩约混在同一组，训练层级不一致。
- 音标：将 `what are` 从 `/ˈwɑːt̬ɚ/` 改为宽式 `/wɑːt‿ɚ/`；整组统一表达“保留前词 + 弱读 `are /ɚ/`”。
- 范围：将 `you are → you're /jɚ/`、`we are → we're /wɪr/` 改回原词组合 `you are /juː‿ɚ/`、`we are /wiː‿ɚ/`。
- 分层：flap `[ɾ]` 和 `you're / we're` 继续作为快速语流中可能出现的现象保留在 [[英语发音与重音]]，但不再混入本组练习表。
- 核查：参考 Cambridge Dictionary 的美式 `what /wɑːt/`、`are /ɚ/` 及相关单词读音，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；[[index]] 摘要仍然准确，无需修改；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 动词加 on 的美式连读

- 内容：在 [[英语发音学习笔记]] 新增“动词 + `on`”小节，收录 `put/go/get/take/turn/hold + on` 六个组合的中文意思、美式日常读法和练习例句。
- 音标：将资料中的英式 `/ɒn/`、`/ɡəʊ/`、`/həʊld/`、`/tɜːn/` 校正为美式 `/ɑːn/`、`/ɡoʊ/`、`/hoʊld/`、`/tɝːn/`；用 `‿` 标示词界处的连续发音。
- 分层：本组使用宽式音标表达稳定的练习目标，不混入 `put on`、`get on` 在特定语速和重音下可能出现的其他语音细节；`go on` 属于元音之间的顺畅过渡。
- 例句：将不自然的 `I hold on a second.` 改为表示“稍等一下”的祈使句 `Hold on a second.`；将 `go on a trip` 作为整体搭配理解。
- 核查：参考 Cambridge Dictionary 的 `on` 读音及六个相关词条，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；[[index]] 摘要仍然准确，无需修改；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 动词加 over 的美式连读

- 内容：在 [[英语发音学习笔记]] 新增“动词 + `over`”小节，收录 `get/turn/come/take/hand/pull + over` 六个高频短语的中文意思、美式日常读法和练习例句。
- 音标：统一按美式 `over /ˈoʊ.vɚ/` 记录，并用 `‿` 标示前词末尾辅音与 `/oʊ/` 之间的连续发音；不把两个单词写成一个词。
- 例句：将 `turn over the page` 调整为更自然的可分结构 `Turn the page over.`；将 `pull over the car` 调整为司机自己靠边停车时使用的 `Please pull over.`。
- 语法：在 [[英语发音与重音]] 补充短语动词的连读与可分性不是同一问题，并区分 `pull over` 的不及物用法和警察让另一辆车停车的 `pull the car over`。
- 核查：参考 Cambridge Dictionary 的 `over` 美式发音与六个相关词条，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；[[index]] 摘要仍然准确，无需修改；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | t、d 结尾词加 you 的合音

- 内容：在 [[英语发音学习笔记]] 新增“`/t/`、`/d/` 结尾词 + `you`”小节，整理 `won't/don't/can't/could/would + you`，并补充 `should you`、`did you` 与对照项 `can you`。
- 合音：`/t/ + /j/` 在自然语流中常融合为 `/tʃ/`，`/d/ + /j/` 常融合为 `/dʒ/`；非重读 `you` 同时常弱化为 `/jə/`，因此记录 `don't you /doʊntʃə/`、`would you /wʊdʒə/` 等美式日常读法。
- 对照：`can you` 不符合 `/t/`、`/d/` 合音条件，记录常见弱读 `/kən‿jə/`，避免把所有“动词 + `you`”机械套用成 `/tʃ/` 或 `/dʒ/`。
- 边界：合音会受语速、强调和口音影响；慢速或强调时可保留 `/t j/`、`/d j/` 和强式 `you /juː/`，标准拼写不写成 `doncha`、`couldja`。
- 核查：参考 British Council、BBC Learning English、Pronuncian 与 Cambridge Dictionary 的合音、弱读及单词读音资料，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；[[index]] 摘要仍然准确，无需修改；未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | you 合音组保留 u 音

- 更正：Harlan 提供的视频截图将 `don't you` 标为 `/ˈdoʊntʃu/`；该读法中的 `/t + j/` 已融合为 `/tʃ/`，但 `you` 保留 `/u/`，属于正确的美式合音读法。
- 修改：[[英语发音学习笔记]] 的本组跟随截图，统一将 `won't/don't/can't + you` 记为 `/tʃu/` 结尾，将 `could/would/should/did + you` 记为 `/dʒu/` 结尾；对照项改为 `can you /kən‿ju/`。
- 重音：表中的 `ˈ` 表示语块单独跟读时重读第一个音节，不代表真实句子的信息重音永远固定在此处。
- 分层：原先的 `/doʊntʃə/`、`/wʊdʒə/` 不是错误，而是 `you` 进一步弱化为 schwa 的更快语流形式；当前练习表只保留截图采用的 `/u/` 版本。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；[[index]] 摘要无需修改，未修改 `raw/` 或 Speaking 文档。

## [2026-10-04] query | 助动词加 he 的 h 脱落

- 内容：在 [[英语发音学习笔记]] 新增“助动词 + `he`”小节，整理 `did/was/does/is/has/will/would + he` 七个组合的中文意思、美式日常读法和练习例句。
- 原理：非重读 `he` 可以由 `/hiː/` 弱化为省略 `/h/` 的 `/i/`，让前词末尾的 `/d/`、`/z/`、`/l/` 直接衔接 `/i/`；这属于弱读和 `/h/` 脱落，不是辅音合音。
- 校正：资料中的 `was he /wɒzi/` 使用英式 `/ɒ/`，按本页美式音标约定改为 `/wʌzi/`；其他给定音标可用于本组较清楚的跟读练习。
- 例句：将 `Has he finished homework?` 调整为更自然的 `Has he finished his homework?`。
- 语法：不把 `would he` 简单归为将来时；它常用于假设、意愿或过去视角的将来。
- 核查：参考 Cambridge Dictionary 的 `he` 强弱式及 `was`、`does`、`has`、`will`、`would` 读音，访问日期为 2026-10-04。
- 更新：[[英语发音学习笔记]]、[[英语发音与重音]]、本文件；[[index]] 摘要仍然准确，无需修改；未修改 `raw/` 或 Speaking 文档。
