"""Day06：用循环判断一个整数是否为素数。"""

from math import isqrt


def is_prime(number: int) -> bool:
    """如果 number 是素数则返回 True。"""
    if number < 2:
        return False

    # 如果 number 有大于 sqrt(number) 的因数，它一定还有一个更小的配对因数。
    # 因此只需要检查到整数平方根，减少不必要的循环。
    for divisor in range(2, isqrt(number) + 1):
        if number % divisor == 0:
            return False
    return True


def main() -> None:
    samples = [1, 2, 3, 4, 17, 21, 97]
    for number in samples:
        result = "是素数" if is_prime(number) else "不是素数"
        print(f"{number:>2} {result}")


if __name__ == "__main__":
    main()

# 练习：打印 100 到 200 之间的全部素数。
