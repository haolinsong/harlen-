"""Day16：函数可以作为参数传给另一个函数。"""

from collections.abc import Callable


def apply_to_each(values: list[int], operation: Callable[[int], int]) -> list[int]:
    """对每个值调用 operation，并收集返回结果。"""
    result: list[int] = []
    for value in values:
        result.append(operation(value))
    return result


def square(number: int) -> int:
    return number ** 2


def main() -> None:
    numbers = [1, 2, 3, 4, 5]
    print(f"平方：{apply_to_each(numbers, square)}")

    # map 做转换，filter 做筛选。实际代码中列表生成式往往更易读。
    doubled = list(map(lambda number: number * 2, numbers))
    evens = list(filter(lambda number: number % 2 == 0, numbers))
    print(f"map 翻倍：{doubled}")
    print(f"filter 偶数：{evens}")

    words = ["pear", "watermelon", "fig", "apple"]
    by_length = sorted(words, key=len)
    print(f"按长度排序：{by_length}")


if __name__ == "__main__":
    main()

# 练习：把绝对值函数 abs 传给 apply_to_each。
