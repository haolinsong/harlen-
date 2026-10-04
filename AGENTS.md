# AGENTS.md — Harlan 第二大脑 · Schema

> 规则来源与操作入口。Agent 动手前完整读取本文件；仅按任务读取 §4 指向的 Skill。
> Schema 版本：2026-10-02.1。修改本文件或项目 Skill 的规则/流程时递增此版本，并在 wiki/log.md 追加 schema 记录；用户操作变化同步 README.md。

## 0. 定位与规则归属

Harlan 的 IT 技术知识库，由 LLM 增量提炼、交叉引用和持续维护持久 Wiki。Harlan 负责选材、提问、方向和验收，Agent 负责整理、归档和记账。

本文件是唯一 Schema 权威；项目 Skill 仅展开本文件授权的操作步骤与正文模板，不另设冲突规则。规则只在所属位置维护一份，README 是使用说明。外部 Skill 提供工具/语法能力，其默认目录、样例字段和写入方式不能覆盖本库约定。用户当前明确要求优先，例如“只讨论，不写入知识库”。

## 1. 架构与归类

| 位置 | 职责 |
| --- | --- |
| raw/ | Harlan 拥有的不可变原始资料；assets/ 为图片附件，personal/ 为个人记录 |
| wiki/ | Agent 维护的知识网络：concepts/、howto/、entities/、sources/ |
| outputs/ | 面向 Harlan、可独立复习的主题活文档；维护报告放 维护/ |
| code/ | 配套实验区，不是第四内容层；项目自带 README、构建配置和适度测试 |
| scripts/ | lint 等确定性工具；Node 工具依赖由 package-lock.json 固定 |
| .agents/skills/ | 本项目按需工作流与外部 Skill，不属于知识内容，不登记成 wiki 页面 |
| README.md / 待落地清单.md | 用户手册 / 已评估暂缓方案及触发条件 |

wiki/index.md 是内容入口，overview.md 是全局判断，QUESTIONS.md 是开放问题队列，log.md 是只追加日志。

concepts/、howto/ 按“知识类型 → 技术栈”分类；outputs/ 只按技术栈。共用 Java、Python、Bash、OS、系统框架、通用、知识管理等目录名。跨栈知识放 通用/。确有新技术栈时可按需新增目录，无需逐次询问；不得创造与现有目录近义的分类。已有分类的大范围重组遵循 §7。

wiki 沉淀细粒度原理与出处，outputs 讲清楚学习主题，通过链接关联，避免长篇重复。code/ 不提交密码、Token、构建产物或本地环境文件。

## 2. 四条铁律

1. **raw/ 永远只读**，包括不向其中新建下载、转录或清洗产物，也不修改、重命名、删除资料。
2. **wiki/ 和 outputs/ 删除页面必须先经 Harlan 同意**。小范围整合/重定向可执行并记账；大规模合并、移动或重命名先说明计划并取得同意。
3. **无来源的断言不写成事实**：推测、待验证、冲突和个人经验分别显式标注。
4. **有价值的结论落盘**到 outputs/ 的已有主题页或新主题页，并维护 index/log。明确只讨论、不落盘时不写文件；已有答案无变化时不制造空改。

## 3. 页面 Schema

### 命名与防重

- 一个知识对象使用一个规范名，其余叫法进 aliases。中文主名，技术专有名词保留原文；文件名与 title 一致，导航文件 index/log/overview/QUESTIONS 沿用现有名称。
- 新文件名不含空格及 `/ \ : * ? " < > | # ^ [ ] %`。示例：JVM垃圾回收.md、SpringBoot自动配置.md。已有历史含空格名称保持原样，未经确认不批量迁移。
- 普通知识页和 outputs 使用稳定主题名，不按问答日期建快照；sources 使用 YYYY-MM-DD-来源名.md，时间性报告使用 outputs/维护/YYYY-MM-DD-主题.md。
- **新建任何页面前**先查 index，再同时检查文件名、title、aliases、正文标题。相同知识对象与学习目标更新原页；同名不同义需明确区分。规范页面名须全库唯一。
- 一次问题含多个独立主题可更新多页，不建临时拼盘。父子主题有独立学习目标或需持续扩展时分别维护并互链。
- 合并时将旧文件名（不含扩展名）加入保留页 aliases，更新 index 与相关链接并追 log；删页仍需确认。页面移动还需检查相对 Markdown 路径，不能仅凭 wikilink 不带目录就认定所有链接安全。
- 对外发布、来源语言以英文为主或重心转向代码/符号时再整体评估英文 slug；不做局部语言迁移。

### Frontmatter

所有知识页面包含 `title`、`type`、`tags`、`created`、`updated`；日期为 YYYY-MM-DD，tags 不超过两层。

| type | 额外必需字段 | 正文职责 |
| --- | --- | --- |
| source | sources | 一份外部资料的出处、核心论点、细节、局限 |
| concept | aliases、sources | 一句定义、核心要点、相邻概念区别；版本敏感时写前提 |
| entity | aliases、sources | 工具/语言/框架/机构/人物；至少出现于两份来源或是一份来源的核心角色才建页 |
| howto | aliases、sources、verified、env | 目标、可复制步骤、验证、已知坑；版本敏感时写适用环境 |
| output | aliases、related | 独立可读的主题复习/综合结论 |
| overview / index / log | 无 | 全局综述 / 内容索引或问题队列 / 变更日志 |

列表字段可为空；sources 记录库根相对 raw 路径，不编造不存在的文件。外部核查 URL 与访问日期写入正文。related 使用加引号的 wikilink 列表，如 `["[[页面名]]"]`。

howto 的 verified 是最后实际验证通过日期；未实测时留空并说明，不能用检索日期代替。env 在版本敏感时不得为空。concept/entity/howto 可设 domain_volatility：high=90 天（默认）、medium=180 天、low=365 天。confidence 用于 concept/entity：1 个外部来源→low、3+→medium、5+且无重大矛盾→候选 high，须 Harlan 确认；个人记录不计入数量。

正文骨架按需读取 [.agents/skills/harlan-wiki-ingest/references/page-templates.md](.agents/skills/harlan-wiki-ingest/references/page-templates.md)，不要在每轮启动时全部加载。

### 链接与表达

- 知识页内部链接使用规范名 `[[页面名]]`；raw 引用和配置/脚本链接使用从当前文件出发的相对 Markdown 路径。
- 内容页末尾设“## 相关”，关联 2–5 个最相关页面；不要为凑数量编造页面。导航与日志沿用其专用结构。
- 步骤流程、状态流转、调用链和数据流等**流程图一律使用 mermaid 代码块**，不用 ASCII 替代。仅 Harlan 明确要求其他格式或目标环境不支持 Mermaid 时例外并说明。
- **每张流程图下方紧跟详细解释**：入口/触发条件、关键节点职责、先后与流转关系、分支条件、结束状态或输出，不能只重复节点标签。
- 连续解释多个同一语境的新名词时，只用一个“新名词” callout；在框内为每个名词分别加粗标名并解释，保留各自定义。被正文、代码或图表隔开的解释，以及不同主题的名词，不强行合并。
- 使用 Obsidian callout：`[!warning] 冲突`（保留双方出处，不静默覆盖）、`[!question] 待验证`、`[!info] 推测`、`[!info] 个人经验`（与外部结论分开）。

## 4. 按需操作路由

执行对应任务前读取下表的 SKILL.md。已经读过且规则未变化时复用当前上下文；不要每轮重读全部 Skill、README、log、raw 或脚本实现。客户端未发现 Skill 时直接打开表中的文件；缺文件时报告缺口，不猜流程。

| 任务 | 读取路径 | 主要结果 |
| --- | --- | --- |
| 摄入来源、个人记录、整理到笔记 | [.agents/skills/harlan-wiki-ingest/SKILL.md](.agents/skills/harlan-wiki-ingest/SKILL.md) | 对齐更新 wiki；明确要复习成品时再更新 outputs |
| 学习问答、解释、对比 | [.agents/skills/harlan-wiki-query/SKILL.md](.agents/skills/harlan-wiki-query/SKILL.md) | index-first 检索，有价值结论并入稳定主题页 |
| 体检、结构/规则/脚本维护、新主题交接 | [.agents/skills/harlan-wiki-governance/SKILL.md](.agents/skills/harlan-wiki-governance/SKILL.md) | 维护或审计报告；或可复制的新会话提示词 |
| Obsidian 特殊语法 | [.agents/skills/obsidian-markdown/SKILL.md](.agents/skills/obsidian-markdown/SKILL.md) | 正确使用 wikilink、properties、callout 等 |
| 普通公开网页正文清洗 | [.agents/skills/defuddle/SKILL.md](.agents/skills/defuddle/SKILL.md) | 用项目本地 CLI 去除网页杂项；临时产物不写 raw |
| PDF | 当前环境已有 PDF Skill | 按需读取与查看页面，不重复安装 |

外部 Skill 的来源和适配见 scripts/skill-sources.json。内置 skill-creator/skill-installer 仅用于创建或安装时，不在日常问答中加载。Skill 不共享会话历史，也不替代用户的任务范围。

## 5. 索引、日志与问题队列

- **index**：按“概念 / 操作 / 实体 / 来源 / 输出”分区，再按技术栈分组；条目为 `- [[页面名]] — 一句话摘要`，底部更新统计。新增/合并/重命名/内容摘要变化时维护；回答前先读它。
- **log**：只在末尾追加，标题 `## [YYYY-MM-DD] 动作 | 标题`；动作限定 scaffold / ingest / query / lint / schema。最近记录可用 `tail -80 wiki/log.md` 查看，不为普通问答读整份历史。保留原条目和历史日期。
- **Add-question**：Harlan 说“我想搞清楚…”或“add question”时，在 QUESTIONS 的“待解决”追加 `- [ ] 问题（opened YYYY-MM-DD）`，更新 updated 并记 query 日志。
- 摄入必须回看问题队列；来源回答了开放问题时先提示并经确认执行 Query，再移至“已解决”，保留结论页链接。已解决项不删除。

## 6. 语言与验证

默认中文，技术专有名词保留原文；结论先行、页面自洽，命令配置可直接复制。修改后检查 git diff，并运行 `python3 scripts/lint.py`；区分本次问题与已有问题，不修无关学习内容。验证时直接运行确定性脚本，仅在修改或排障时读实现。

## 7. 权限、多会话与规则刷新

同一本地工作目录共享文件，不共享对话历史。按主题分工，跨会话事实以文件和 Git 为准。

1. **开工基线**：运行 `git status --short` 和 `shasum -a 256 AGENTS.md`，记住现有修改与规则哈希；已有改动属于 Harlan 或其他会话，不覆盖。
2. **写前复核**：每次开始写文件前检查 Git 状态、目标差异和 AGENTS.md 哈希，不以 Git 是否显示规则未提交为前提。目标出现其他会话的新改动时先重读并最小合并；无法安全判断则停止该文件写入并请 Harlan 决定。
3. **共享热点最后写**：index、log、QUESTIONS、overview 在主题文件完成后更新，写前重读磁盘最新版，不用旧快照覆盖。log 始终追加。
4. **提交范围**：默认仅精确暂存本会话确认的文件，不用 git add -A。Harlan 明确要求提交全部且已审阅范围时才整体暂存；提交后复查状态。本会话没有提交请求时不自动提交或推送。
5. **重叠任务**：同一主题页串行编辑或由 Harlan 指定交接顺序；大量重叠或需独立提交时优先 Worktree，再通过提交、合并或 Handoff 交接。
6. **大改动**：大规模重命名、移动、合并、目录重构前说明计划并等待确认；不修改无关主题和代码项目。已明确批准的方案可以按批准范围实施。
7. **规则刷新**：发现非本会话预期产生的 AGENTS.md 哈希变化，暂停新写入，提醒：“检测到项目规则变化，请回复：重新加载项目规则。”这是项目自然语言约定，不是内置斜杠命令。
8. 收到重载指令后完整重读 AGENTS.md、更新哈希，重新读取当前任务对应 Skill 及所需 references，说明变化并复核已做/待做工作。新规则与未完工作冲突时说明重做范围，等 Harlan 确认后继续。
9. 本会话按 Harlan 授权修改 Schema 后直接重读并更新哈希，无需反向要求重载。**修改项目 Skill 的规则/流程也必须递增根 Schema 版本**，使仍按旧版根哈希检测的会话能发现变化。
10. 不宣称活跃会话保证热加载根规则；Skill 发现异常时重新打开/新建项目任务。准备开新主题会话时按治理 Skill 主动给可复制提示词；新任务首轮默认只读初始化并等待具体问题。
