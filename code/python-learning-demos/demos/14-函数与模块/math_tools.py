"""Day14 的辅助模块：集中保存可复用的数学函数。"""


def greatest_common_divisor(a: int, b: int) -> int:
    """使用欧几里得算法计算最大公约数。"""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def least_common_multiple(a: int, b: int) -> int:
    """计算最小公倍数；任一参数为 0 时结果为 0。"""
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // greatest_common_divisor(a, b)


def is_even(number: int) -> bool:
    return number % 2 == 0
