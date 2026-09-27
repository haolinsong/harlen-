"""Day05：使用 Python 3.10+ 的 match/case 匹配命令。"""


def describe_command(command: str) -> str:
    """把简短命令转换成人类可读的说明。"""
    # match/case 类似其他语言的 switch，但还支持更强的结构模式匹配。
    match command.strip().lower():
        case "start" | "run":
            return "启动程序"
        case "stop":
            return "停止程序"
        case "status":
            return "查看状态"
        case "help" | "?":
            return "显示帮助"
        case "":
            return "没有输入命令"
        case unknown:
            return f"未知命令：{unknown}"


def main() -> None:
    for command in ["start", "STATUS", "?", "deploy", ""]:
        print(f"{command!r:<10} -> {describe_command(command)}")


if __name__ == "__main__":
    main()

# 练习：增加 restart 命令，并让它返回“重新启动程序”。
