"""Day07：综合使用循环和分支找出 100 以内的素数。"""

from math import isqrt


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for divisor in range(2, isqrt(number) + 1):
        if number % divisor == 0:
            return False
    return True


def primes_below(limit: int) -> list[int]:
    """返回所有严格小于 limit 的素数。"""
    result: list[int] = []
    for number in range(2, limit):
        if is_prime(number):
            result.append(number)
    return result


def main() -> None:
    primes = primes_below(100)
    print("100 以内的素数：")
    print(primes)
    print(f"一共有 {len(primes)} 个")


if __name__ == "__main__":
    main()

# 练习：把 limit 改成 1000，比较运行时间和结果数量。
