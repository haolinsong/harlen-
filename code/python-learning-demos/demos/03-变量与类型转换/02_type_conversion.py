"""Day03：字符串、整数和浮点数之间的显式转换。"""


def main() -> None:
    # input 的结果永远是 str。这里用字符串模拟用户输入。
    age_text = "20"
    price_text = "19.90"

    age = int(age_text)
    price = float(price_text)
    total = price * 2

    print(f"明年年龄：{age + 1}")
    print(f"两件商品总价：{total:.2f}")
    print(f"数字重新转成字符串：{str(total)!r}")

    # 注意：bool 判断的是对象是否为空，而不是字符串看起来像不像 False。
    print(f"bool('False') = {bool('False')}，因为它是非空字符串")
    print(f"bool('') = {bool('')}，因为它是空字符串")

    # int('3.14') 会报错；需要先转成 float，再按需求取整。
    decimal_text = "3.14"
    print(f"int(float('3.14')) = {int(float(decimal_text))}")


if __name__ == "__main__":
    main()

# 练习：尝试转换 'abc'，观察 ValueError，并在 Day21 学习异常处理。
