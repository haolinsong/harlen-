---
name: harlan-wiki-governance
description: 治理 Harlan 的第二大脑结构、规则、命名与链接，执行体检、维护脚本或生成新主题会话交接提示词；普通学习问答不触发。
---

# 知识库治理

执行根目录 [AGENTS.md](../../../AGENTS.md) 的 Schema。治理范围是结构、规则和流程；学习主题只在暴露结构问题且与当前任务有关时涉及。

## 按任务选择流程

- 体检/审计：先执行下方体检流程。
- 修改 Schema、Skill 或脚本：执行下方维护流程；只验证本次影响范围，不自动开展全库内容改写。
- 新主题会话交接：只读 [交接提示词](references/session-handoff.md)。
- 用户只要讨论或诊断：给证据与建议，不将讨论理解为执行修复的授权；明确“不要落盘”时不改文件。

## 体检

1. 先运行 `python3 scripts/lint.py`。它做确定性检查；先看输出，仅在诊断或修改脚本时读取实现。
2. 补充脚本无法判断的语义检查：同义重复、结论矛盾、被新来源推翻的内容、反复出现却无独立页面的概念、缺失交叉引用及知识空白。区分结构问题与单篇内容问题。
3. 报告写入 outputs/维护/YYYY-MM-DD-体检.md；同日同主题更新原报告。写清证据、影响、具体可执行建议及未验证部分，不只列抽象评分。
4. 重读共享文件后登记 index、追加 lint 日志。修改后的收尾 lint 是验证，不再递归新建一份体检报告。

## 维护

1. 阅读当前规则、README、待落地清单、index 与最近日志，核对 Git 基线；仅加载任务相关主题和脚本。优先小范围、可验证的改进，说明原因、影响与迁移成本。
2. 修改规则时更新 AGENTS.md；若详细步骤位于项目 Skill 或其 references，修改对应唯一位置，并递增根文件的 Schema 版本，保证其他会话能通过根规则哈希发现更新。
3. 面向使用者的变化同步 README；持久化说明优先更新现有 outputs/知识管理/当前项目工作原理.md，避免再造近义介绍页。审计报告才使用日期页。
4. 暂不值得实施的方案记入待落地清单，写明触发条件；已落地条目移出清单并追 schema 日志。大范围迁移和删页执行根文件确认要求。
5. 共享热点最后重读并最小合并；index 登记内容页面，Skill/脚本使用普通路径，不列作知识页面。追加 schema 日志，说明保留的开工前修改和验证边界。
6. 完成后检查 git diff 并运行 `python3 scripts/lint.py`。修改 lint 的扫描范围时运行 `python3 scripts/test_lint.py`；新 Skill 使用可用的 skill-creator 校验器，至少核对 frontmatter、引用路径及真实触发场景。脚本按风险实测，不虚报通过。

## 外部 Skill 维护

安装来源、固定提交和本地适配记录在项目根 scripts/skill-sources.json。升级时审阅上游差异，保留本库路径和权限适配，更新许可证与锁定记录；不要用上游默认目录覆盖本库 Schema。Defuddle 依赖由 scripts/package-lock.json 固定；用 `npm ci --prefix scripts --ignore-scripts --no-audit --no-fund` 恢复。
