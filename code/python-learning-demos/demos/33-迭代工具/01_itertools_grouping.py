"""Day33：itertools.groupby 只合并相邻同键元素，先排序再分组。"""

from itertools import groupby


def hours_by_person(records: list[tuple[str, int]]) -> dict[str, int]:
    if any(minutes < 0 for _, minutes in records):
        raise ValueError("时长不能为负数")
    # 如果不排序，分散在列表两端的同一个人会形成两个分组。
    ordered = sorted(records, key=lambda record: record[0])
    return {
        person: sum(minutes for _, minutes in group)
        for person, group in groupby(ordered, key=lambda record: record[0])
    }


def main() -> None:
    records = [("小明", 30), ("小红", 20), ("小明", 45)]
    print("输入：", records)
    print("按人汇总：", hours_by_person(records))


if __name__ == "__main__":
    main()

# 练习：使用 itertools.islice 只读取生成器的前两条结果。
