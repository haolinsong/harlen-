"""Day32：用数据类集中管理字段与校验，避免位置参数含义不明。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    name: str
    price_cents: int

    def __post_init__(self) -> None:
        if not self.name.strip() or self.price_cents < 0:
            raise ValueError("商品名称不能为空，价格不能为负")


@dataclass(frozen=True)
class OrderLine:
    product: Product
    quantity: int

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("数量必须大于零")

    @property
    def subtotal_cents(self) -> int:
        # 金额用整数分存储，避免浮点小数在累计时出现舍入误差。
        return self.product.price_cents * self.quantity


def total_cents(lines: list[OrderLine]) -> int:
    return sum(line.subtotal_cents for line in lines)


def main() -> None:
    lines = [OrderLine(Product("笔记本", 1250), 2), OrderLine(Product("笔", 350), 3)]
    print("输入订单：", lines)
    print(f"总价：{total_cents(lines) / 100:.2f} 元")


if __name__ == "__main__":
    main()

# 练习：增加一个折扣函数，但不要修改 frozen 数据类中的原价。
