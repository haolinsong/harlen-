"""Day18：用 Point 类表示平面上的点。"""

from math import hypot


class Point:
    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y

    def move(self, delta_x: float, delta_y: float) -> None:
        self.x += delta_x
        self.y += delta_y

    def distance_to(self, other: "Point") -> float:
        """计算当前点到另一个点的欧氏距离。"""
        return hypot(self.x - other.x, self.y - other.y)

    def __repr__(self) -> str:
        return f"Point(x={self.x}, y={self.y})"


def main() -> None:
    first = Point(0, 0)
    second = Point(3, 4)
    print(f"两点距离：{first.distance_to(second)}")
    first.move(1, 2)
    print(f"移动后的 first：{first!r}")


if __name__ == "__main__":
    main()

# 练习：增加 midpoint 方法，返回两个点的中点。
