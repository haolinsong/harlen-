"""Day02：理解输入、函数参数和格式化输出。"""


def build_greeting(name: str, goal: str) -> str:
    """根据名字和学习目标生成问候语。"""
    # f-string 可以把变量直接嵌入字符串，可读性通常比字符串拼接更好。
    return f"你好，{name}！今天继续学习：{goal}。"


def main() -> None:
    # 为了让自动测试不会停下来等待输入，Demo 使用预设值。
    name = "Harlan"
    goal = "Python 基础"

    # 实际交互程序可以改成下面两行：
    # name = input("请输入你的名字：")
    # goal = input("请输入今天的学习目标：")
    print(build_greeting(name, goal))


if __name__ == "__main__":
    main()

# 练习：增加一个 hours 参数，并在问候语中显示计划学习多少小时。
