"""Day01：用最小程序感受 Python 的表达式和输出。"""


def main() -> None:
    print("Hello, Python!")

    # print 可以直接输出表达式的计算结果。
    print("1 + 2 =", 1 + 2)
    print("7 * 8 =", 7 * 8)

    # 字符串可以用 + 拼接，也可以用 * 重复。
    language = "Python"
    print("正在学习：" + language)
    print("加油！" * 3)


if __name__ == "__main__":
    main()

# 练习：把 language 改成你熟悉的另一门语言，然后比较输出。
