"""Day09：列表生成式用于简洁地“遍历、筛选、转换”。"""


def main() -> None:
    numbers = list(range(1, 11))

    # 阅读顺序：对 numbers 中的每个 number，如果它是偶数，就计算平方。
    even_squares = [number ** 2 for number in numbers if number % 2 == 0]
    print(f"偶数的平方：{even_squares}")

    names = ["alice", "bob", "charlie"]
    upper_names = [name.upper() for name in names]
    print(f"转换为大写：{upper_names}")

    # 两层 for 可以生成笛卡尔组合，但太复杂时普通循环会更易读。
    coordinates = [(x, y) for x in range(2) for y in range(3)]
    print(f"坐标组合：{coordinates}")


if __name__ == "__main__":
    main()

# 练习：生成 1 到 20 中能被 3 整除的数字字符串。
