"""Day19：实例方法、类方法和静态方法的职责不同。"""


class Product:
    tax_rate = 0.20  # 类属性，由所有实例共享

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def price_with_tax(self) -> float:
        """实例方法使用当前对象的数据，也能访问类属性。"""
        return self.price * (1 + self.tax_rate)

    @classmethod
    def from_text(cls, text: str) -> "Product":
        """类方法常用作替代构造器，cls 表示当前类。"""
        name, price_text = text.split(":", maxsplit=1)
        return cls(name=name, price=float(price_text))

    @staticmethod
    def is_valid_price(price: float) -> bool:
        """静态方法与对象状态无关，只是逻辑上属于 Product。"""
        return price >= 0


def main() -> None:
    product = Product.from_text("Keyboard:100")
    print(f"{product.name} 含税价：{product.price_with_tax():.2f}")
    print(f"价格 -1 是否有效：{Product.is_valid_price(-1)}")


if __name__ == "__main__":
    main()

# 练习：修改 Product.tax_rate，观察已有对象计算结果是否变化。
