"""Day08：创建列表，并学习索引、切片和成员判断。"""


def main() -> None:
    languages = ["Python", "Java", "Go", "Rust"]
    print(f"完整列表：{languages}")
    print(f"第一个元素：{languages[0]}")
    print(f"最后一个元素：{languages[-1]}")
    print(f"前两个元素：{languages[:2]}")
    print(f"从第二个开始：{languages[1:]}")
    print(f"Python 是否存在：{'Python' in languages}")

    # 列表是可变对象，可以直接修改某个位置。
    languages[2] = "Kotlin"
    print(f"修改后：{languages}")

    # 切片返回新列表，不会改变原列表。
    copied = languages[:]
    copied.append("TypeScript")
    print(f"原列表：{languages}")
    print(f"副本：{copied}")


if __name__ == "__main__":
    main()

# 练习：使用步长切片 languages[::-1] 得到倒序副本。
