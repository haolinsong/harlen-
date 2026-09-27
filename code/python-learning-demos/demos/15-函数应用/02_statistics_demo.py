"""Day15：把数据统计拆成多个小函数。"""

from math import sqrt


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("values 不能为空")
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("values 不能为空")
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return ordered[middle]
    return (ordered[middle - 1] + ordered[middle]) / 2


def population_standard_deviation(values: list[float]) -> float:
    """计算总体标准差，反映数据围绕平均值的离散程度。"""
    average = mean(values)
    variance = sum((value - average) ** 2 for value in values) / len(values)
    return sqrt(variance)


def main() -> None:
    scores = [72, 85, 90, 90, 98]
    print(f"数据：{scores}")
    print(f"平均值：{mean(scores):.2f}")
    print(f"中位数：{median(scores):.2f}")
    print(f"总体标准差：{population_standard_deviation(scores):.2f}")


if __name__ == "__main__":
    main()

# 练习：实现众数 mode，并思考存在多个众数时如何返回。
