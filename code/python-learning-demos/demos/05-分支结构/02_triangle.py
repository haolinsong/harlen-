"""Day05：判断三条边能否构成三角形并计算面积。"""

from math import sqrt


def is_valid_triangle(a: float, b: float, c: float) -> bool:
    """任意两边之和必须大于第三边，而且边长必须为正。"""
    return a > 0 and b > 0 and c > 0 and a + b > c and a + c > b and b + c > a


def triangle_metrics(a: float, b: float, c: float) -> tuple[float, float]:
    """返回三角形的周长和面积；边长无效时抛出 ValueError。"""
    if not is_valid_triangle(a, b, c):
        raise ValueError("三条边不能构成三角形")
    perimeter = a + b + c
    half = perimeter / 2
    # 海伦公式：area = sqrt(s * (s-a) * (s-b) * (s-c))。
    area = sqrt(half * (half - a) * (half - b) * (half - c))
    return perimeter, area


def main() -> None:
    sides = (3.0, 4.0, 5.0)
    perimeter, area = triangle_metrics(*sides)
    print(f"边长：{sides}")
    print(f"周长：{perimeter:.2f}，面积：{area:.2f}")


if __name__ == "__main__":
    main()

# 练习：测试 (1, 2, 3) 为什么不能构成三角形。
