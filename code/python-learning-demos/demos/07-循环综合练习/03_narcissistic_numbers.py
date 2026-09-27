"""Day07：寻找三位水仙花数。"""


def is_narcissistic(number: int) -> bool:
    """判断一个数是否等于其各位数字的位数次幂之和。"""
    digits = [int(char) for char in str(number)]
    power = len(digits)
    return number == sum(digit ** power for digit in digits)


def narcissistic_numbers(start: int, end: int) -> list[int]:
    return [number for number in range(start, end + 1) if is_narcissistic(number)]


def main() -> None:
    values = narcissistic_numbers(100, 999)
    print(f"三位水仙花数：{values}")

    # 153 = 1^3 + 5^3 + 3^3。
    digits = [1, 5, 3]
    print(f"验证 153：{sum(digit ** 3 for digit in digits)}")


if __name__ == "__main__":
    main()

# 练习：寻找 1 到 9999 之间所有满足定义的数。
