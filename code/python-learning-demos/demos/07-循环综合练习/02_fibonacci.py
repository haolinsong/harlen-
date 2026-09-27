"""Day07：生成斐波那契数列。"""


def fibonacci(count: int) -> list[int]:
    """返回前 count 个斐波那契数，序列从 0、1 开始。"""
    if count < 0:
        raise ValueError("count 不能是负数")

    sequence: list[int] = []
    first, second = 0, 1
    while len(sequence) < count:
        sequence.append(first)
        # 右侧先整体计算，再同时赋值，所以不需要临时变量。
        first, second = second, first + second
    return sequence


def main() -> None:
    print("前 12 个斐波那契数：")
    print(fibonacci(12))


if __name__ == "__main__":
    main()

# 练习：修改函数，让它返回所有小于指定上限的斐波那契数。
