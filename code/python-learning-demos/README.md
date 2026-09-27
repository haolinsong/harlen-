# Python Learning Demos

这是一个面向 Python 新手的可运行示例项目。学习主题参考
[jackfrued/Python-100-Days](https://github.com/jackfrued/Python-100-Days) 的 Day01-20，
示例代码、注释和练习均为本项目重新编写。

项目目标不是堆积语法，而是让每个知识点都有一个小程序可以运行、修改和观察。

## 环境要求

- Python 3.10 或更高版本，因为 Day05 会演示 `match/case`。
- Day01-20 只使用 Python 标准库，不需要安装第三方依赖。
- 当前电脑已验证的解释器是 `/opt/homebrew/bin/python3`，版本为 Python 3.14.7。

先确认解释器版本：

```bash
/opt/homebrew/bin/python3 --version
```

## 创建虚拟环境

虚拟环境不会自动把旧 Python 升级成新版本，它会使用创建它的解释器。因此本机要明确使用
Homebrew 的 Python 3.14.7 创建 `.venv`：

```bash
# 1. 进入项目目录
cd "/Users/sjj/learn/codex知识库/Harlan的第二大脑/code/python-learning-demos"

# 2. 使用新版 Python 创建虚拟环境；只需要创建一次
/opt/homebrew/bin/python3 -m venv .venv

# 3. 在当前 zsh 终端中激活虚拟环境
source .venv/bin/activate

# 4. 验证当前 python 已经来自项目的 .venv
python --version
which python
```

验证时应看到 Python 3.14.7，并且 `which python` 的结果以
`python-learning-demos/.venv/bin/python` 结尾。激活后，终端提示符前面通常会出现
`(.venv)`，后续命令直接使用 `python` 即可。

每次新开终端，只需重新进入项目并激活，不需要再次创建：

```bash
cd "/Users/sjj/learn/codex知识库/Harlan的第二大脑/code/python-learning-demos"
source .venv/bin/activate
```

学习结束后退出虚拟环境：

```bash
deactivate
```

`.venv/` 已被 `.gitignore` 忽略，不会提交到 Git。如果以后更换了 Python 大版本，应删除旧的
`.venv`，再用目标解释器重新创建；虚拟环境不适合在不同 Python 版本之间直接复用。

### 在 PyCharm 中使用 `.venv`

激活虚拟环境只会修改当前终端的 `PATH`。代码左侧 `main` 附近的绿色运行按钮由 PyCharm
直接启动项目解释器，因此还要在 IDE 中单独选择 `.venv`：

1. 打开 `PyCharm > Settings`（macOS 也可以按 `Command + ,`）。
2. 进入 `Project: python-learning-demos > Python Interpreter`。
3. 点击 `Add Interpreter`，选择 `Add Local Interpreter`。
4. 选择已有环境 `Existing`，解释器路径填写：

   ```text
   /Users/sjj/learn/codex知识库/Harlan的第二大脑/code/python-learning-demos/.venv/bin/python
   ```

5. 确认后把它选为当前项目的解释器，再点击 `Apply` 和 `OK`。
6. 再次点击代码左侧的绿色运行按钮，输出的 `sys.executable` 应指向 `.venv/bin/python`。

此后即使在终端执行 `deactivate`，PyCharm 的绿色运行按钮仍会使用 Python 3.14，这是预期行为。
`deactivate` 只恢复当前终端的 `PATH`；PyCharm 已经把 `.venv/bin/python` 保存为项目解释器，
运行时会直接调用这个绝对路径。两套设置互不控制。

如果仍然显示 Python 3.9，打开 `Run > Edit Configurations`，找到当前脚本的运行配置，
把 `Python interpreter` 改成 `Project Default` 或刚添加的 `.venv`。也可以删除旧的临时运行
配置，再从代码左侧重新运行，让 PyCharm 按新的项目解释器创建配置。

在已激活的终端中，可以用下面的命令取得需要填写到 IDE 的准确路径：

```bash
python -c "import sys; print(sys.executable)"
```

## 快速开始

列出全部 Demo：

```bash
python run_demo.py --list
```

运行一个 Demo，参数可以是列表中路径的一部分：

```bash
python run_demo.py 03-变量与类型转换/01_variables_and_types.py
```

运行全部 Demo：

```bash
python run_demo.py --all
```

运行自动化测试：

```bash
python -m unittest discover -s tests -v
```

以上命令假设已经激活 `.venv`。安装第三方依赖时也建议写成 `python -m pip install 包名`，
确保依赖安装到当前虚拟环境，而不是系统 Python。

## 学习方式

每个 Demo 都遵循相同节奏：

1. 先直接运行，观察输出。
2. 阅读文件顶部说明和行内中文注释。
3. 修改变量或参数，再运行一次。
4. 完成文件末尾给出的练习建议。
5. 不理解时先打印变量的值和 `type(...)`，再定位问题。

不要急着背语法。能够预测程序下一行输出什么，比记住所有 API 更重要。

## 01-20 目录导航

| 目录 | Demo |
| --- | --- |
| `01-Python环境与运行` | `python_info`、`hello_python` |
| `02-基础语法与输入输出` | `hello_world`、`input_and_output` |
| `03-变量与类型转换` | `variables_and_types`、`type_conversion` |
| `04-运算符与表达式` | `operators`、`temperature_converter`、`circle_calculator` |
| `05-分支结构` | `grade_level`、`triangle`、`command_match` |
| `06-循环结构` | `loops`、`prime_checker`、`guess_game` |
| `07-循环综合练习` | `primes_under_100`、`fibonacci`、`narcissistic_numbers` |
| `08-列表基础` | `list_basics`、`list_iteration` |
| `09-列表进阶与矩阵` | `list_methods`、`list_comprehension`、`matrix` |
| `10-元组` | `tuple_unpacking`、`tuple_vs_list` |
| `11-字符串` | `string_basics`、`string_methods` |
| `12-集合` | `set_basics`、`set_operations` |
| `13-字典` | `dictionary_basics`、`word_frequency` |
| `14-函数与模块` | `function_basics`、`module_demo` |
| `15-函数应用` | `verification_code`、`statistics_demo`、`lottery` |
| `16-高阶函数` | `higher_order_functions`、`lambda_and_partial` |
| `17-装饰器与递归` | `decorators`、`recursion` |
| `18-类与对象` | `class_basics`、`clock`、`point` |
| `19-面向对象进阶` | `properties`、`class_and_static_methods`、`inheritance` |
| `20-面向对象综合项目` | `poker_game`、`payroll_system` |

## 目录结构

```text
python-learning-demos/
├── demos/             # 按“序号-主题”组织的独立可运行脚本
├── docs/              # 后续 Day21-100 路线图
├── tests/             # 冒烟测试和关键逻辑测试
├── run_demo.py        # Demo 列表与统一运行入口
└── pyproject.toml     # Python 版本和工具配置
```

## 后续路线

Day21-100 暂时只建立路线，不提前引入大量依赖。完成基础阶段后，再依次增加文件处理、
数据库、Web 开发、数据分析、机器学习和自动化测试。详见
[`docs/learning-roadmap.md`](docs/learning-roadmap.md)。
