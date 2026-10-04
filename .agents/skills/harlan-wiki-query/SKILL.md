---
name: harlan-wiki-query
description: 在 Harlan 的第二大脑中回答学习问题、解释或对比知识，并更新已有主题笔记；不用于纯 Git 操作、Skill 安装或结构审计。
---

# 知识问答

执行根目录 [AGENTS.md](../../../AGENTS.md) 的 Schema，特别是主题对齐、来源标注、写入边界和共享文件协作要求。

1. 先读 wiki/index.md，定位后只深入相关页面；不足时再用 rg 搜文件名、title、aliases、正文标题和局部内容，不先全文扫描 raw/。
2. 对齐本次问题的规范学习主题。相同对象和学习目标更新原页；多个独立主题分别更新；父子主题有独立复习目标时保留并互链。不要按提问措辞或日期新建重复页。
3. 基于已有知识给结论与出处；信息不足时指出缺口，给出可补来源或检索方向。需要外部核查时使用一手来源并保留 URL 与访问日期；不把无依据断言写成事实。
4. 普通问题用正文，比较用表格；演示和趋势按需选用工具。流程图遵循根规则。需要 Obsidian 特殊语法时读取 [obsidian-markdown](../obsidian-markdown/SKILL.md)；新建页面时可读 [页面骨架](../harlan-wiki-ingest/references/page-templates.md)。
5. 将有价值的新结论合并到 outputs/ 对应主题页，更新 updated；已有答案完全覆盖时避免空改。若 Harlan 明确要求只讨论、不落盘，则尊重本次范围，不更新笔记、index、log 或问题队列。
6. 产生可复用原理或操作纠正时同步修订相关 wiki；新增待办疑问按根规则登记 QUESTIONS。若是在回答已登记的问题，结论落盘后再移至“已解决”并注明页面。
7. 完成主题文件后重读共享文件，更新 index、追加 query 日志。审阅 diff、运行 lint，再汇报答案、出处与落盘位置。

若任务变为摄入整份材料，改读 [摄入 Skill](../harlan-wiki-ingest/SKILL.md)；只有确实需要时加载，不在每次问答时预读所有 Skill。
