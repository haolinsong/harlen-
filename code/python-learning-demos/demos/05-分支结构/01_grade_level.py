"""Day05：使用 if/elif/else 完成多分支判断。"""


def grade_level(score: float) -> str:
    """把百分制成绩转换成等级。"""
    if not 0 <= score <= 100:
        return "无效成绩"
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "E"


def main() -> None:
    for score in [95, 82, 76, 60, 41, 120]:
        print(f"{score:>3} 分 -> {grade_level(score)}")


if __name__ == "__main__":
    main()

# 练习：把等级改成“优秀、良好、中等、及格、不及格”。
