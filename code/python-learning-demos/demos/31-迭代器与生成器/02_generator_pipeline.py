"""Day31：用生成器逐条处理日志，而不是先建立多份中间列表。"""

from collections.abc import Iterable, Iterator


def parse_events(lines: Iterable[str]) -> Iterator[tuple[str, int]]:
    for line_number, line in enumerate(lines, start=1):
        pieces = line.strip().split(",")
        if len(pieces) != 2:
            raise ValueError(f"第 {line_number} 行应为 用户,分钟数")
        name = pieces[0].strip()
        if not name:
            raise ValueError(f"第 {line_number} 行缺少用户名")
        try:
            minutes = int(pieces[1])
        except ValueError as error:
            raise ValueError(f"第 {line_number} 行分钟数不是整数") from error
        if minutes < 0:
            raise ValueError(f"第 {line_number} 行分钟数不能为负数")
        # yield 每次只交出一条记录；输入可以是文件迭代器，不必一次读完。
        yield name, minutes


def long_sessions(events: Iterable[tuple[str, int]], minimum: int) -> Iterator[str]:
    for name, minutes in events:
        if minutes >= minimum:
            yield f"{name}: {minutes} 分钟"


def main() -> None:
    lines = ["小明,25", "小红,50", "小明,40"]
    print("输入：", lines)
    print("不少于 40 分钟：", list(long_sessions(parse_events(lines), 40)))


if __name__ == "__main__":
    main()

# 练习：增加一个生成器，只保留指定用户的记录。
