"""Day02：学习 print、单行注释和多行文档字符串。"""


def main() -> None:
    # sep 决定多个值之间用什么连接，默认是空格。
    print("Python", "Java", "Go", sep=" | ")

    # end 决定输出结尾，默认是换行符 \n。
    print("这一行还没有结束", end=" -> ")
    print("现在结束")

    # \n 是换行转义字符，\t 是制表符。
    print("姓名：Harlan\n方向：软件开发\n工具：\tPython")


if __name__ == "__main__":
    main()

# 练习：尝试把 sep 改成逗号，把 end 改成两个换行符。
