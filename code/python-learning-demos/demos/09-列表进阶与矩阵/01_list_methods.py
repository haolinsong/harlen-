"""Day09：常用列表方法会直接修改原列表。"""


def main() -> None:
    tasks = ["阅读", "编码"]
    tasks.append("测试")                 # 在末尾添加一个元素
    tasks.insert(1, "做笔记")           # 在指定位置插入
    tasks.extend(["复盘", "休息"])      # 一次添加多个元素
    print(f"添加后：{tasks}")

    tasks.remove("休息")                 # 按值删除第一个匹配项
    finished = tasks.pop(0)              # 按索引删除并返回元素
    print(f"已完成：{finished}")
    print(f"剩余任务：{tasks}")

    numbers = [3, 1, 4, 1, 5]
    print(f"数字 1 出现 {numbers.count(1)} 次")
    numbers.sort()
    print(f"原地升序排序：{numbers}")
    numbers.reverse()
    print(f"原地反转：{numbers}")


if __name__ == "__main__":
    main()

# 练习：比较 numbers.sort() 与 sorted(numbers) 对原列表的影响。
