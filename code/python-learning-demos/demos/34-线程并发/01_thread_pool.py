"""Day34：线程池适合等待型任务；map 按输入顺序收集结果。"""

from concurrent.futures import ThreadPoolExecutor
from time import sleep


def fetch_local_value(value: int) -> int:
    # 这里只用短暂等待模拟 I/O，不访问网络，也不声称线程能加速纯计算。
    sleep(0.005)
    return value * value


def square_waiting_values(values: list[int]) -> list[int]:
    with ThreadPoolExecutor(max_workers=3) as pool:
        return list(pool.map(fetch_local_value, values))


def main() -> None:
    values = [3, 1, 4, 2]
    print("输入：", values)
    print("输出：", square_waiting_values(values))


if __name__ == "__main__":
    main()

# 练习：把最大线程数改为 1，比较程序的运行时间。
