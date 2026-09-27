"""Day10：元组、打包、解包和交换变量。"""


def point() -> tuple[int, int]:
    # 逗号会把多个值打包成元组，括号很多时候可以省略。
    return 3, 5


def main() -> None:
    coordinates = point()
    x, y = coordinates               # 按位置解包
    print(f"x={x}, y={y}")

    first, *middle, last = [10, 20, 30, 40, 50]
    print(f"first={first}, middle={middle}, last={last}")

    left = "A"
    right = "B"
    left, right = right, left        # 右侧先打包，再解包到左侧
    print(f"交换后：left={left}, right={right}")


if __name__ == "__main__":
    main()

# 练习：用解包取得 (2026, 9, 25) 中的年、月、日。
