"""Day14：函数、参数、返回值和作用域。"""


def calculate_total(price: float, quantity: int = 1, discount: float = 0.0) -> float:
    """计算折扣后的总价，discount 使用 0 到 1 的小数。"""
    subtotal = price * quantity
    return subtotal * (1 - discount)


def join_words(*words: str, separator: str = " ") -> str:
    """*words 收集任意数量的位置参数，separator 是仅限关键字参数。"""
    return separator.join(words)


def build_profile(name: str, **attributes: object) -> dict[str, object]:
    """**attributes 收集任意数量的关键字参数。"""
    return {"name": name, **attributes}


def main() -> None:
    print(f"默认数量：{calculate_total(20):.2f}")
    print(f"关键字参数：{calculate_total(price=20, quantity=3, discount=0.1):.2f}")
    print(join_words("Python", "函数", "很好用", separator="-"))
    print(build_profile("Harlan", age=20, city="Bucharest"))

    # 函数内部的 subtotal 是局部变量，函数外部不能直接访问。


if __name__ == "__main__":
    main()

# 练习：为 calculate_total 增加税率参数，并校验折扣范围。
