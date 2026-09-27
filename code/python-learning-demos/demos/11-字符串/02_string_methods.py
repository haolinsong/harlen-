"""Day11：清理、查找、拆分、连接和格式化字符串。"""


def normalize_tags(raw: str) -> list[str]:
    """把逗号分隔的标签清理为小写列表。"""
    return [part.strip().lower() for part in raw.split(",") if part.strip()]


def main() -> None:
    message = "  Learn Python, Step by Step!  "
    clean = message.strip()
    print(f"去掉两端空白：{clean!r}")
    print(f"转成小写：{clean.lower()}")
    print(f"是否以 Learn 开头：{clean.startswith('Learn')}")
    print(f"Python 的位置：{clean.find('Python')}")
    print(f"替换：{clean.replace('Python', 'Programming')}")

    tags = normalize_tags(" Python, Java,  RabbitMQ, ,Spring ")
    print(f"标签列表：{tags}")
    print(f"重新连接：{' | '.join(tags)}")

    name = "Harlan"
    completed = 12
    print(f"格式化输出：{name:<10} 已完成 {completed:03d} 个练习")


if __name__ == "__main__":
    main()

# 练习：统计一句话中每个单词出现的次数，为 Day13 做准备。
