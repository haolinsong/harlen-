"""Day31：自己实现迭代器，理解 for 循环何时停止。"""


class Countdown:
    """每次迭代都创建新游标，因此同一对象可以重复遍历。"""

    def __init__(self, start: int) -> None:
        if start < 0:
            raise ValueError("起点不能为负数")
        self.start = start

    def __iter__(self) -> "CountdownIterator":
        return CountdownIterator(self.start)


class CountdownIterator:
    """游标保存当前位置；耗尽时按协议抛出 StopIteration。"""

    def __init__(self, current: int) -> None:
        self.current = current

    def __iter__(self) -> "CountdownIterator":
        return self

    def __next__(self) -> int:
        if self.current == 0:
            raise StopIteration
        result = self.current
        self.current -= 1
        return result


def main() -> None:
    countdown = Countdown(4)
    print("输入起点：4")
    print("第一次遍历：", list(countdown))
    print("第二次遍历：", list(countdown))


if __name__ == "__main__":
    main()

# 练习：让倒计时可以指定终点，例如 5、4、3 后停止。
