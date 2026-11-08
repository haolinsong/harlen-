"""Day36：二分查找要求有序输入；排序稳定性保留相同分数的原顺序。"""


def binary_search(numbers: list[int], target: int) -> int | None:
    # 教学用排序检查便于报错；它本身有额外开销，实际二分查找通常把“已排序”作为前提。
    if numbers != sorted(numbers):
        raise ValueError("二分查找要求输入升序排列")
    left, right = 0, len(numbers)
    while left < right:
        middle = (left + right) // 2
        if numbers[middle] < target:
            left = middle + 1
        else:
            right = middle
    # 返回第一次出现的位置，重复值也有确定结果。
    return left if left < len(numbers) and numbers[left] == target else None


def rank_students(students: list[tuple[str, int]]) -> list[tuple[str, int]]:
    # Python 的排序是稳定的；相同分数维持输入顺序。
    return sorted(students, key=lambda student: student[1], reverse=True)


def main() -> None:
    numbers = [2, 4, 4, 7, 9]
    students = [("小明", 90), ("小红", 95), ("小刚", 90)]
    print("升序数字：", numbers, "查找 4：", binary_search(numbers, 4))
    print("输入学生：", students)
    print("按分数降序：", rank_students(students))


if __name__ == "__main__":
    main()

# 练习：将二分查找改为返回“最后一次出现的位置”。
