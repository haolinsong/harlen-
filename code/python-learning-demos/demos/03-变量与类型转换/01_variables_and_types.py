"""Day03：变量保存值，类型描述值可以进行什么操作。"""


def main() -> None:
    age = 18                 # int：整数
    height = 1.75            # float：浮点数
    name = "Harlan"         # str：字符串
    is_learning = True       # bool：布尔值，只有 True 和 False
    nickname = None          # None：当前没有值

    values = [age, height, name, is_learning, nickname]
    for value in values:
        print(f"值={value!r:<12} 类型={type(value).__name__}")

    # Python 是动态类型语言：变量名没有固定类型，它只是引用某个值。
    score = 95
    print(f"\nscore={score!r}, 类型={type(score).__name__}")
    score = "优秀"
    print(f"score={score!r}, 类型={type(score).__name__}")

    # 推荐使用有意义的 snake_case 名称，不要写成难懂的 a、b、x1。
    completed_lesson_count = 3
    print(f"已完成课程数：{completed_lesson_count}")


if __name__ == "__main__":
    main()

# 练习：添加 complex（复数）和 bytes（字节串）变量并打印类型。
