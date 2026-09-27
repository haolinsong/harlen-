"""Day10：比较列表与元组的使用场景。"""


def main() -> None:
    mutable_scores = [80, 90, 100]
    fixed_rgb = (255, 128, 0)

    # list 可变，适合数量或内容需要调整的集合。
    mutable_scores.append(95)
    mutable_scores[0] = 85
    print(f"可修改的成绩列表：{mutable_scores}")

    # tuple 不可变，适合坐标、颜色、数据库一行等固定结构。
    print(f"固定的 RGB 元组：{fixed_rgb}")
    # fixed_rgb[0] = 0  # 取消注释会得到 TypeError。

    # 元组包含的元素如果自身可变，元素内部仍然可以变化。
    container = ([1, 2], "固定标签")
    container[0].append(3)
    print(f"包含列表的元组：{container}")


if __name__ == "__main__":
    main()

# 练习：思考为什么字典的键可以使用元组，却通常不能使用列表。
