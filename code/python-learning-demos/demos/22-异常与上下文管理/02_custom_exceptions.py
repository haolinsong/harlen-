"""Day22：用自定义异常表达具体的业务失败原因。"""


class InsufficientBalanceError(ValueError):
    """余额不足时抛出，并保留余额与支出金额供调用方判断。"""

    def __init__(self, balance: float, amount: float) -> None:
        self.balance = balance
        self.amount = amount
        shortage = amount - balance
        super().__init__(f"余额不足，还差 {shortage:.2f} 元")


class Wallet:
    def __init__(self, balance: float = 0.0) -> None:
        if balance < 0:
            raise ValueError("初始余额不能为负数")
        self.balance = float(balance)

    def withdraw(self, amount: float) -> float:
        """扣除指定金额并返回剩余余额。"""
        if amount <= 0:
            raise ValueError("支出金额必须大于 0")
        if amount > self.balance:
            raise InsufficientBalanceError(self.balance, amount)
        self.balance -= amount
        return self.balance


def main() -> None:
    wallet = Wallet(100)
    for amount in [35, 80]:
        try:
            balance = wallet.withdraw(amount)
        except InsufficientBalanceError as error:
            print(f"支付 {amount:.2f} 元失败：{error}")
            print(f"异常中记录的当前余额：{error.balance:.2f} 元")
        else:
            print(f"支付 {amount:.2f} 元成功，余额：{balance:.2f} 元")


if __name__ == "__main__":
    main()

# 练习：增加 deposit 方法，并为负数或零充值定义清楚的错误行为。
