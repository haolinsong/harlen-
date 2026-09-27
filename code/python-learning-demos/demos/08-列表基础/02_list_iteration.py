"""Day08：遍历列表并同时获取索引和值。"""


def average(scores: list[float]) -> float:
    """计算平均值；空列表没有平均值，因此主动报错。"""
    if not scores:
        raise ValueError("scores 不能为空")
    return sum(scores) / len(scores)


def main() -> None:
    scores = [88, 92, 75, 100]

    # enumerate 默认从 0 开始；start=1 更符合人类编号习惯。
    for index, score in enumerate(scores, start=1):
        print(f"第 {index} 门成绩：{score}")

    print(f"最高分：{max(scores)}")
    print(f"最低分：{min(scores)}")
    print(f"平均分：{average(scores):.2f}")


if __name__ == "__main__":
    main()

# 练习：找出所有不低于平均分的成绩。
