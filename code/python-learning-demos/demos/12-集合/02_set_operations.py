"""Day12：集合的交集、并集、差集和包含关系。"""


def main() -> None:
    backend = {"Python", "Java", "Go", "SQL"}
    data = {"Python", "SQL", "R", "Statistics"}

    print(f"并集，至少属于一组：{sorted(backend | data)}")
    print(f"交集，同时属于两组：{sorted(backend & data)}")
    print(f"只在后端组：{sorted(backend - data)}")
    print(f"只属于其中一组：{sorted(backend ^ data)}")

    required = {"Python", "SQL"}
    print(f"数据技能是否覆盖必备技能：{required <= data}")
    print(f"data 是否是 required 的超集：{data >= required}")


if __name__ == "__main__":
    main()

# 练习：用集合找出两个班级共同选修某门课程的学生。
