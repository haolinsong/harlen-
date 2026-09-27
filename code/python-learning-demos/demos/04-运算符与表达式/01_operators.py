"""Day04：算术、比较、逻辑和赋值运算符。"""


def main() -> None:
    left = 17
    right = 5

    print("算术运算：")
    print(f"{left} + {right} = {left + right}")
    print(f"{left} - {right} = {left - right}")
    print(f"{left} * {right} = {left * right}")
    print(f"{left} / {right} = {left / right}")       # 真除法，结果是 float
    print(f"{left} // {right} = {left // right}")     # 向下整除
    print(f"{left} % {right} = {left % right}")       # 余数
    print(f"{right} ** 2 = {right ** 2}")             # 幂运算

    age = 20
    has_ticket = True
    can_enter = age >= 18 and has_ticket
    print(f"\n满足年龄且有票：{can_enter}")
    print(f"年龄不是 18：{age != 18}")

    count = 10
    count += 3  # 等价于 count = count + 3
    count *= 2
    print(f"复合赋值后的 count：{count}")


if __name__ == "__main__":
    main()

# 练习：预测 2 + 3 * 4 和 (2 + 3) * 4 的结果，再运行验证。
