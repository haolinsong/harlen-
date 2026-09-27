"""Day04：根据半径计算圆的周长和面积。"""

from math import pi


def circle_metrics(radius: float) -> tuple[float, float]:
    """返回二元组：(周长, 面积)。"""
    circumference = 2 * pi * radius
    area = pi * radius ** 2
    return circumference, area


def main() -> None:
    radius = 3.0
    circumference, area = circle_metrics(radius)
    print(f"半径：{radius}")
    print(f"周长：{circumference:.2f}")
    print(f"面积：{area:.2f}")


if __name__ == "__main__":
    main()

# 练习：把半径改为 0 和负数，思考函数是否应该主动校验参数。
