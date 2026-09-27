"""Day19：继承复用接口，多态让不同对象响应同一个方法。"""

from abc import ABC, abstractmethod
from math import pi


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """所有具体图形都必须实现面积计算。"""


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return pi * self.radius ** 2


def total_area(shapes: list[Shape]) -> float:
    """不关心具体类型，只要求每个对象都提供 area 方法。"""
    return sum(shape.area() for shape in shapes)


def main() -> None:
    shapes: list[Shape] = [Rectangle(3, 4), Circle(2)]
    for shape in shapes:
        print(f"{type(shape).__name__} 面积：{shape.area():.2f}")
    print(f"总面积：{total_area(shapes):.2f}")


if __name__ == "__main__":
    main()

# 练习：增加 Triangle 类，并让 total_area 无需修改即可处理它。
