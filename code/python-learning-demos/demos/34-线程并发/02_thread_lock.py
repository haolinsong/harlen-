"""Day34：多个线程更新同一份状态时，用锁保护读-改-写整体。"""

from concurrent.futures import ThreadPoolExecutor
from threading import Lock


class SafeCounter:
    def __init__(self) -> None:
        self.value = 0
        self._lock = Lock()

    def add(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("本示例只接受非负增量")
        # value += amount 包含读取和写回；锁保护的是整个逻辑操作。
        with self._lock:
            self.value += amount


def count_total(amounts: list[int]) -> int:
    counter = SafeCounter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(counter.add, amounts))
    return counter.value


def main() -> None:
    amounts = [1, 2, 3, 4, 5]
    print("输入增量：", amounts)
    print("最终计数：", count_total(amounts))


if __name__ == "__main__":
    main()

# 练习：增加 subtract 方法，并考虑计数不能低于零时如何检查。
