"""Day13：字典使用键查找值。"""


def main() -> None:
    student = {
        "name": "Harlan",
        "age": 20,
        "skills": ["Java", "Python"],
    }

    print(f"姓名：{student['name']}")
    print(f"城市：{student.get('city', '暂未填写')}")

    student["city"] = "Bucharest"     # 新键会被添加
    student["age"] = 21               # 已有键会被更新
    student["skills"].append("RabbitMQ")

    for key, value in student.items():
        print(f"{key:<8} -> {value}")

    removed_city = student.pop("city")
    print(f"删除的城市：{removed_city}")
    print(f"剩余键：{list(student.keys())}")


if __name__ == "__main__":
    main()

# 练习：增加一个 courses 字典，键是课程名，值是分数。
