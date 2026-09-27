---
title: Python基础学习实战
type: output
tags: [Python/基础, Python/实战]
aliases: []
created: 2026-09-25
updated: 2026-09-26
related: []
---

# Python 基础学习实战

本学习项目参考 [Python-100-Days](https://github.com/jackfrued/Python-100-Days) 的 Day01-20 主题顺序，用重新编写的小 Demo 学习 Python 基础语法、常用数据结构、函数和面向对象编程。

## 项目入口

- [项目 README](../../code/python-learning-demos/README.md)
- [Day21-100 后续路线](../../code/python-learning-demos/docs/learning-roadmap.md)
- [全部 Demo](../../code/python-learning-demos/demos)
- [自动化测试](../../code/python-learning-demos/tests)

## 当前内容

项目包含 48 个可独立运行的 Demo：

| 阶段 | 主题 |
| --- | --- |
| Day01-07 | 环境、输入输出、变量、运算符、分支、循环和基础算法 |
| Day08-13 | 列表、元组、字符串、集合和字典 |
| Day14-17 | 函数、模块、高阶函数、Lambda、偏函数、装饰器和递归 |
| Day18-20 | 类、属性、类方法、继承、多态、扑克和工资结算项目 |

每个脚本都包含中文说明、关键行注释和一个可继续修改的练习。示例默认不等待键盘输入，因此既可以逐个运行，也能一次执行全部脚本。

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
python run_demo.py 03-变量与类型转换/01_variables_and_types.py
python -m unittest discover -s tests -v
```

项目最低要求 Python 3.10。`.venv/` 已加入 `.gitignore`，不会提交到 Git；安装依赖时使用 `python -m pip install 包名`，可以避免误装到系统 Python。

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
- `run_demo.py --list` 发现 48 个 Demo。
- 冒烟测试逐个启动 48 个 Demo，全部成功退出。
- 9 项关键逻辑测试和 1 项全量冒烟测试全部通过。

## 后续阶段

Day21-100 已在路线文档中按阶段规划，但没有提前安装第三方依赖。完成基础阶段后，再依次增加文件处理、数据库、Web 开发、数据分析、机器学习和综合项目。

## 相关

- [Python-100-Days](https://github.com/jackfrued/Python-100-Days) — 本项目参考的学习主题路线。
- [Python 官方教程](https://docs.python.org/3/tutorial/) — 查询 Python 语言行为与标准用法。
