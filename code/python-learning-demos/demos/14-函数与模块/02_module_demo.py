"""Day14：从自定义模块导入函数。"""

# 直接运行本文件时，Python 会把当前脚本目录加入模块搜索路径，
# 因此可以导入同目录下的 math_tools.py。
from math_tools import greatest_common_divisor, is_even, least_common_multiple


def main() -> None:
    left, right = 18, 24
    print(f"最大公约数：{greatest_common_divisor(left, right)}")
    print(f"最小公倍数：{least_common_multiple(left, right)}")
    print(f"{left} 是偶数：{is_even(left)}")


if __name__ == "__main__":
    main()

# 练习：在 math_tools.py 中增加判断奇数的函数并导入使用。
