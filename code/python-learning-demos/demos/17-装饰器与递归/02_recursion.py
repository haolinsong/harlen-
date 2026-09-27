"""Day17：递归函数必须包含终止条件和缩小问题规模的步骤。"""


def factorial(number: int) -> int:
    """计算非负整数的阶乘：n! = n * (n-1)!。"""
    if number < 0:
        raise ValueError("阶乘只接受非负整数")
    if number in (0, 1):                 # 终止条件
        return 1
    return number * factorial(number - 1)  # 问题规模从 n 缩小到 n-1


def flatten(values: list[object]) -> list[object]:
    """递归展开任意层级的嵌套列表。"""
    result: list[object] = []
    for value in values:
        if isinstance(value, list):
            result.extend(flatten(value))
        else:
            result.append(value)
    return result


def main() -> None:
    print(f"5! = {factorial(5)}")
    nested: list[object] = [1, [2, [3, 4]], 5]
    print(f"展开 {nested} -> {flatten(nested)}")

    # Python 的递归深度有限；简单循环问题通常优先使用循环。


if __name__ == "__main__":
    main()

# 练习：递归计算 1 + 2 + ... + n，并与循环版本比较。
