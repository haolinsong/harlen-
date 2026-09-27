"""Day11：字符串的索引、切片、转义和原始字符串。"""


def main() -> None:
    text = "Python学习"
    print(f"完整字符串：{text}")
    print(f"长度：{len(text)}")
    print(f"第一个字符：{text[0]}")
    print(f"最后一个字符：{text[-1]}")
    print(f"前三个字符：{text[:3]}")
    print(f"倒序：{text[::-1]}")

    # 字符串不可变：不能执行 text[0] = 'J'，转换会产生新字符串。
    replaced = text.replace("Python", "编程")
    print(f"替换结果：{replaced}")
    print(f"原字符串仍然是：{text}")

    escaped = "第一行\n第二行\t缩进"
    raw_path = r"C:\new_folder\test.txt"
    print(f"\n转义字符串：\n{escaped}")
    print(f"原始字符串：{raw_path}")


if __name__ == "__main__":
    main()

# 练习：使用切片判断一个字符串是否为回文。
