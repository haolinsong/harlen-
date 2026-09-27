"""Day16：Lambda 适合短小表达式，partial 用来预先固定参数。"""

from functools import partial


def power(base: int, exponent: int) -> int:
    return base ** exponent


def main() -> None:
    students = [
        {"name": "Alice", "score": 88},
        {"name": "Bob", "score": 95},
        {"name": "Carol", "score": 82},
    ]

    # lambda 没有名字，适合只在这里使用一次的简单排序规则。
    ordered = sorted(students, key=lambda student: student["score"], reverse=True)
    print(f"按成绩降序：{ordered}")

    # partial 不会立刻执行 power，而是生成一个固定了部分参数的新函数。
    square = partial(power, exponent=2)
    cube = partial(power, exponent=3)
    print(f"5 的平方：{square(5)}")
    print(f"5 的立方：{cube(5)}")

    # int 的第二个参数是进制，固定 base=2 后得到二进制转换函数。
    binary_to_int = partial(int, base=2)
    print(f"二进制 101101 = {binary_to_int('101101')}")


if __name__ == "__main__":
    main()

# 练习：使用 partial 创建固定 exponent=4 的 fourth_power 函数。
