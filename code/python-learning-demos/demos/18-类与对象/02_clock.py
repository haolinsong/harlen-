"""Day18：用类表示一个可前进的数字时钟。"""


class Clock:
    def __init__(self, hour: int = 0, minute: int = 0, second: int = 0) -> None:
        if not 0 <= hour < 24 or not 0 <= minute < 60 or not 0 <= second < 60:
            raise ValueError("时间超出有效范围")
        self.hour = hour
        self.minute = minute
        self.second = second

    def tick(self) -> None:
        """让时钟前进一秒，并处理进位。"""
        self.second += 1
        if self.second == 60:
            self.second = 0
            self.minute += 1
        if self.minute == 60:
            self.minute = 0
            self.hour = (self.hour + 1) % 24

    def __str__(self) -> str:
        return f"{self.hour:02d}:{self.minute:02d}:{self.second:02d}"


def main() -> None:
    clock = Clock(23, 59, 57)
    for _ in range(5):
        print(clock)
        clock.tick()


if __name__ == "__main__":
    main()

# 练习：增加 tick_many(seconds) 方法，一次前进指定秒数。
