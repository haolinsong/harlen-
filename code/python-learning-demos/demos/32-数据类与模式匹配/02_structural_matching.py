"""Day32：match/case 匹配结构，适合区分形状不同的输入。"""


def describe_command(command: object) -> str:
    match command:
        case {"action": "add", "name": str(name), "score": int(score)} if 0 <= score <= 100:
            return f"添加 {name}：{score} 分"
        case {"action": "list"}:
            return "列出全部成绩"
        case ["delete", str(name)]:
            return f"删除 {name} 的成绩"
        case _:
            raise ValueError("不支持的命令结构或分数")


def main() -> None:
    commands: list[object] = [
        {"action": "add", "name": "小明", "score": 88},
        {"action": "list"},
        ["delete", "小明"],
    ]
    for command in commands:
        print("输入：", command, "→ 输出：", describe_command(command))


if __name__ == "__main__":
    main()

# 练习：增加 {"action": "top", "count": 3} 命令，并拒绝非正数 count。
