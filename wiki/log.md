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
