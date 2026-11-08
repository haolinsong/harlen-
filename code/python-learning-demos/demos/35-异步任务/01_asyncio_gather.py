"""Day35：asyncio 在等待期间切换任务，gather 保持输入顺序。"""

import asyncio


async def read_local_item(name: str, delay: float) -> str:
    # asyncio.sleep 会交还控制权；time.sleep 会阻塞整个事件循环。
    await asyncio.sleep(delay)
    return f"{name} 已完成"


async def run_jobs(names: list[str]) -> list[str]:
    jobs = [read_local_item(name, 0.005) for name in names]
    return list(await asyncio.gather(*jobs))


def main() -> None:
    names = ["任务 A", "任务 B", "任务 C"]
    print("输入：", names)
    print("输出：", asyncio.run(run_jobs(names)))


if __name__ == "__main__":
    main()

# 练习：让每个任务等待不同的时长，观察输出列表是否改变顺序。
