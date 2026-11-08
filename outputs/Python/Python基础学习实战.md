---
title: Python基础学习实战
type: output
tags: [Python/基础, Python/实战]
aliases: []
created: 2026-09-25
updated: 2026-10-24
related: []
---

# Python 基础学习实战

本学习项目参考 [Python-100-Days](https://github.com/jackfrued/Python-100-Days) 的知识顺序，用重新编写的小 Demo 学习 Python 基础语法、常用数据结构、函数、面向对象编程，以及文件与结构化数据处理。

## 项目入口

- [项目 README](../../code/python-learning-demos/README.md)
- [Day21-100 学习路线](../../code/python-learning-demos/docs/learning-roadmap.md)
- [全部 Demo](../../code/python-learning-demos/demos)
- [自动化测试](../../code/python-learning-demos/tests)

## 当前内容

项目包含 90 个可独立运行的 Demo：

| 阶段 | 主题 |
| --- | --- |
| Day01-07 | 环境、输入输出、变量、运算符、分支、循环和基础算法 |
| Day08-13 | 列表、元组、字符串、集合和字典 |
| Day14-17 | 函数、模块、高阶函数、Lambda、偏函数、装饰器和递归 |
| Day18-20 | 类、属性、类方法、继承、多态、扑克和工资结算项目 |
| Day21 | 文本与二进制文件、UTF-8 编码、临时目录和 `pathlib` |
| Day22 | 异常处理、自定义异常和上下文管理器 |
| Day23 | JSON、CSV，以及 CSV 生成 JSON 成绩报告的综合练习 |
| Day24 | 正则表达式匹配、查找和文本清理 |
| Day25 | 本地邮件消息、CSV 附件与解析 |
| Day26 | 清洗 CSV 并生成带原始数据附件的学习报告草稿 |
| Day27-30 | 电子表格与 Office/PDF/图像文件实操，以及本地通信模拟 |
| Day31-33 | 迭代器、生成器、数据类、模式匹配和迭代工具 |
| Day34-37 | 线程、异步任务、搜索排序、子进程与环境变量 |
| Day38-40 | SQLite 增删改查、关联查询、索引、事务与 CSV 导入 |

每个脚本都包含中文说明、关键行注释和一个可继续修改的练习。示例默认不等待键盘输入，因此既可以逐个运行，也能一次执行全部脚本。文件类示例使用临时目录，运行结束后自动清理，不会把练习数据留在项目中。

## Day21-23 学习重点

### Day21：文件与路径

- 文本文件需要明确编码；本项目统一使用 `encoding="utf-8"`，避免依赖操作系统默认值。
- `r`、`w`、`a` 分别表示读取、覆盖写入和末尾追加；二进制模式在其后增加 `b`。
- 大文件应分块读写，避免一次性占用过多内存；复制是否正确可以比较内容或摘要。
- `pathlib.Path` 用 `/` 组合路径，并提供 `name`、`stem`、`suffix`、`parent`、`rglob` 等操作。

### Day22：异常与上下文管理

- `try` 中只放可能失败的操作，`except` 捕获能够处理的具体异常。
- `else` 表示没有异常时的正常路径，`finally` 用于无论成功失败都必须执行的清理工作。
- `raise` 主动拒绝无效状态；自定义异常可以携带余额、金额等业务上下文。
- `with` 通过 `__enter__` 和 `__exit__` 管理资源，确保文件在正常结束或异常退出时都被关闭。

### Day23：JSON 与 CSV

- JSON 保存嵌套对象、列表、数字和布尔值，适合配置和系统间交换数据。
- CSV 是文本表格；读取后的字段默认都是字符串，需要按业务含义显式转换类型。
- 生成报告时按照“读取 → 校验 → 转换 → 统计 → 序列化”拆分步骤，错误数据应尽早给出具体行号。
- `ensure_ascii=False` 可以让 JSON 文件直接保留中文，`newline=""` 可以避免 CSV 跨平台空行问题。

## Day24-26 学习重点

### Day24：正则表达式

- 正则模式建议写成原始字符串，例如 `r"\s+"`，让反斜线交给正则引擎解释。
- `fullmatch` 适合检查整个输入的格式，`finditer` 适合取得每次匹配的文本和位置。
- `re.sub` 可替换重复空白或统一日期分隔符；统一格式不等于验证日期有效性。
- 固定格式的编号使用 `[0-9]` 明确要求 ASCII 数字，配合命名分组让结果易读。

### Day25：邮件消息

- `EmailMessage` 将收件人、主题、正文与附件组织成一封结构化邮件。
- `as_bytes()` 可把邮件序列化，`BytesParser` 可将字节解析回邮件对象。
- 给 CSV 文本附件显式设置 `charset="utf-8"`；解析 `text/csv` 后，`get_content()` 返回文本，可直接读取中文。
- 这两个 Demo 只创建和解析本地邮件，不执行网络发送。

### Day26：综合报告

- CSV 的 `student,hours` 字段先校验列数和数值，再把姓名中的多余空白压缩、合并同名记录。
- 学习时长拒绝负数与 `nan` 等非有限值，错误信息包含数据行号，便于定位输入问题。
- 将 JSON 摘要放入邮件正文，原始 CSV 作为附件；收件人可以同时看到统计结果与原始数据。
- 运行 `python run_demo.py 26-数据清洗与报告/01_weekly_report.py` 可观察完整输入和输出。

以上 API 细节参考 [Python 3.14 `re` 文档](https://docs.python.org/3.14/library/re.html) 与 [Python 3.14 `email.message` 文档](https://docs.python.org/3.14/library/email.message.html)，核查日期为 2026-10-24。

## Day27-30 学习重点与边界

- Day27 先区分 CSV 文本与 XLSX 的 ZIP/XML 包，再用 `openpyxl` 写出真实 XLSX：姓名列是文本、学习时长列是数字，合计单元格保存 `SUM` 公式。**写入公式不等于算出结果**；`openpyxl` 不计算公式，结果需要电子表格软件重算。
- Day28 先观察最小 DOCX 和幻灯片 XML 片段，再分别用 `python-docx` 生成含任务表格的 DOCX、用 `python-pptx` 生成完整的双页 PPTX，并重新打开检查标题和内容。原有 `pptx_structure` 仍只是结构片段，不能当完整 PPTX 使用。
- Day29 先用最小 PDF 和 PPM 理解文件结构与像素，再用 ReportLab 生成 PDF、用 `pypdf` 读回文字，并用 Pillow 创建、缩放、读回 PNG 色卡。PDF 示例仍只使用 ASCII；中文 PDF 需注册支持中文字形的字体。
- Day30 将邮件内容与传输动作分开，并构造短信 API 请求；两个传输端都由本地替身模拟，**没有发送真实邮件或短信**，也不需要账号或密钥。

这些第三方库只安装到项目 `.venv`。首次运行 Day27-29 实操或执行全部 Demo 前，先在已激活的虚拟环境中执行 `python -m pip install -r requirements-docs.txt`。可以按 `02_xlsx_package.py` → `03_openpyxl_report.py` 的顺序比较底层格式与库的抽象，再运行 `04_powerpoint_deck.py`、`03_reportlab_pdf.py` 和 `04_pillow_image.py`。所有文件写入临时目录，结束后自动清理；想观察实际文件，可自行把目标路径改为固定的练习目录。

以上库用法与边界参考 [openpyxl 教程](https://openpyxl.readthedocs.io/en/3.1/tutorial.html)、[python-docx 快速入门](https://python-docx.readthedocs.io/en/latest/user/quickstart.html)、[python-pptx 快速入门](https://github.com/scanny/python-pptx/blob/master/docs/user/quickstart.rst)、[Pillow 图像 API](https://pillow.readthedocs.io/en/stable/reference/Image.html) 与 [ReportLab 用户指南](https://docs.reportlab.com/reportlab/userguide/ch2_graphics/)，核查日期为 2026-10-24。文件结构另参考 [Microsoft 的最小工作簿结构](https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/structure-of-a-spreadsheetml-document)、[WordprocessingML 结构](https://learn.microsoft.com/en-us/office/open-xml/word/structure-of-a-wordprocessingml-document)及 [Adobe PDF Reference 1.7](https://opensource.adobe.com/dc-acrobat-sdk-docs/pdfstandards/pdfreference1.7old.pdf)。

## Day31-40 学习重点

- Day31-33：迭代器自己保存位置并在耗尽时抛出 `StopIteration`；生成器用 `yield` 逐条交出数据；数据类把字段和校验放在一起；`groupby` 只合并相邻同键记录，因此示例先排序。
- Day34-35：线程池演示等待型任务，锁保护共享计数的“读—改—写”；`asyncio.sleep` 在等待时让出控制权，`gather` 的结果保持输入顺序。不要把示例里的短暂等待理解为真实性能测试。
- Day36-37：二分查找依赖升序输入，稳定排序保持同分记录原顺序；调用子进程时传参数列表与独立的环境变量，不把用户文本交给 Shell 解释。
- Day38-40：SQLite 使用 `?` 占位符绑定参数；`LEFT JOIN` 保留没有选课的学生；索引可通过 `EXPLAIN QUERY PLAN` 观察，但是否采用索引由数据库决定；转账与 CSV 批量导入用事务保证失败时回滚。这里是本地 SQLite 教学，**不是 MySQL 实操**。

建议依次修改 [生成器流水线](../../code/python-learning-demos/demos/31-迭代器与生成器/02_generator_pipeline.py)、[关联查询与索引](../../code/python-learning-demos/demos/39-关联查询与索引/01_join_and_index.py) 和 [CSV 导入数据库](../../code/python-learning-demos/demos/40-事务与数据库项目/02_csv_to_database.py) 文件末尾的练习，再运行对应 Demo 和测试。API 行为参考 [Python `asyncio` 文档](https://docs.python.org/3.14/library/asyncio-task.html)、[Python `subprocess` 文档](https://docs.python.org/3.14/library/subprocess.html) 与 [Python `sqlite3` 文档](https://docs.python.org/3.14/library/sqlite3.html)，核查日期为 2026-10-24。

## 使用方法

当前电脑的系统 `/usr/bin/python3` 是 3.9.6，不支持 `match/case`；Homebrew Python 是 3.14.7，因此使用下面的解释器：

```bash
cd code/python-learning-demos
/opt/homebrew/bin/python3 -m venv .venv
source .venv/bin/activate
python --version
which python
```

虚拟环境继承创建它的解释器版本，并不会自动升级系统 Python。首次创建后，每次新开终端只需进入项目并执行 `source .venv/bin/activate`；完成学习后执行 `deactivate` 退出。

激活后使用虚拟环境中的 `python` 运行项目：

```bash
python run_demo.py --list
python run_demo.py 21-文件与路径/01_text_files.py
python run_demo.py 23-JSON与CSV/03_score_report.py
python run_demo.py 26-数据清洗与报告/01_weekly_report.py
python -m pip install -r requirements-docs.txt
python run_demo.py 27-Excel与电子表格/03_openpyxl_report.py
python -m unittest discover -s tests -v
```

项目最低要求 Python 3.10。`.venv/` 已加入 `.gitignore`，不会提交到 Git；安装依赖时使用 `python -m pip install -r requirements-docs.txt`，可以避免误装到系统 Python。

### PyCharm 运行按钮仍使用旧版本

终端执行 `source .venv/bin/activate` 只会修改当前终端进程的 `PATH`。PyCharm 代码左侧的绿色运行按钮使用项目中单独保存的 Python Interpreter 或 Run Configuration，所以终端使用 3.14、按钮仍使用 3.9 并不矛盾。

本项目当前的 `.idea` 配置仍记录着 `Python 3.9`。在 PyCharm 的 `Settings > Project: python-learning-demos > Python Interpreter` 中添加已有解释器，并选择：

```text
/Users/sjj/learn/codex知识库/Harlan的第二大脑/code/python-learning-demos/.venv/bin/python
```

如果项目解释器修改后按钮仍使用 3.9，再到 `Run > Edit Configurations`，把脚本配置的 `Python interpreter` 改为 `Project Default` 或 `.venv`。运行 `01_python_info.py` 后，`sys.executable` 指向 `.venv/bin/python` 才表示配置生效。

设置生效后，即使在终端执行 `deactivate`，PyCharm 运行按钮仍会使用 Python 3.14。原因是 `deactivate` 只恢复当前终端的 `PATH`，不会修改 PyCharm 持久保存的项目解释器；PyCharm 会直接执行 `.venv/bin/python` 的绝对路径。只有在终端输入 `python ...` 时，是否激活虚拟环境才会决定命令解析到哪个解释器。

## 学习建议

1. 先运行 Demo，不看代码预测主题和输出。
2. 阅读注释，逐行确认变量如何变化。
3. 修改示例数据并再次运行。
4. 完成文件结尾的练习。
5. 每完成一天，用自己的话解释三个最重要的知识点。

学习重点不是记住所有方法，而是能够把问题拆成变量、分支、循环、函数和对象，并通过运行结果验证自己的判断。

## 验证结果

- 本机验证解释器：Python 3.14.7。
- `run_demo.py --list` 发现 90 个 Demo。
- 冒烟测试逐个启动 90 个 Demo，全部成功退出。
- 46 项关键逻辑测试和 1 项全量冒烟测试全部通过。

## 后续阶段

按[学习路线](../../code/python-learning-demos/docs/learning-roadmap.md)的 Day01-100 规划，截至 2026-10-24 已有 Day01-40 的可运行示例，后续还有 Day41-100 共 60 个规划日。Day41-45 属于当前“进阶语法、Linux 与数据库”阶段，重点补全 Linux 终端与 MySQL 实操；其后依次是 Web 开发 20 个、数据分析 15 个、机器学习 10 个、综合实践 10 个规划日。

如果继续每批完成 2～3 个规划日，且一批不跨阶段，Day41-100 预计还需 **22～29 批**。这只是规划日数量估算，不等于 Demo 数量或日历天数。Day27-29 的 Office、PDF、Pillow 基础实操已补齐；中文 PDF 排版与真实通信仍未做。后续涉及新依赖或账号的内容，需要在开始前确定范围和环境。

## 相关

- [Python-100-Days](https://github.com/jackfrued/Python-100-Days) — 本项目参考的学习主题路线。
- [Python 官方教程](https://docs.python.org/3/tutorial/) — 查询 Python 语言行为与标准用法。
- [Python `re` 官方文档](https://docs.python.org/3.14/library/re.html) — 正则表达式语法与匹配接口。
- [Python `email.message` 官方文档](https://docs.python.org/3.14/library/email.message.html) — 邮件对象与附件接口。
