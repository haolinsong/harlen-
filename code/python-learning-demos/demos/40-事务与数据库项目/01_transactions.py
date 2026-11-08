"""Day40：转账两步必须同成同败，失败时回滚。"""

import sqlite3
from contextlib import closing


def create_accounts(connection: sqlite3.Connection) -> None:
    connection.execute(
        "CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER NOT NULL CHECK(balance >= 0))"
    )
    connection.executemany(
        "INSERT INTO accounts(name, balance) VALUES (?, ?)", [("甲", 100), ("乙", 20)]
    )
    connection.commit()


def transfer(connection: sqlite3.Connection, sender: str, receiver: str, amount: int) -> None:
    if amount <= 0 or sender == receiver:
        raise ValueError("金额必须为正，且收款人与付款人不能相同")
    # 连接上下文在正常退出时提交；异常时回滚，保证两次更新原子化。
    with connection:
        debit = connection.execute(
            "UPDATE accounts SET balance = balance - ? "
            "WHERE name = ? AND balance >= ?", (amount, sender, amount)
        )
        if debit.rowcount != 1:
            raise ValueError("付款账户不存在或余额不足")
        credit = connection.execute(
            "UPDATE accounts SET balance = balance + ? WHERE name = ?", (amount, receiver)
        )
        if credit.rowcount != 1:
            raise ValueError("收款账户不存在")


def balances(connection: sqlite3.Connection) -> list[tuple[str, int]]:
    return connection.execute("SELECT name, balance FROM accounts ORDER BY name").fetchall()


def main() -> None:
    with closing(sqlite3.connect(":memory:")) as connection:
        create_accounts(connection)
        print("转账前：", balances(connection))
        transfer(connection, "甲", "乙", 30)
        print("成功转账 30 后：", balances(connection))
        try:
            transfer(connection, "甲", "不存在", 10)
        except ValueError as error:
            print("失败转账：", error)
        print("失败后余额未变：", balances(connection))


if __name__ == "__main__":
    main()

# 练习：增加转账记录表，并让记录写入和余额变更处于同一事务。
