"""Day15：使用 sample 生成不重复的随机号码。"""

import random


def generate_ticket(random_source: random.Random | None = None) -> tuple[list[int], int]:
    """生成一组教学用号码：6 个红球和 1 个蓝球。"""
    source = random_source or random.SystemRandom()
    red_balls = sorted(source.sample(range(1, 34), 6))
    blue_ball = source.randint(1, 16)
    return red_balls, blue_ball


def main() -> None:
    demo_random = random.Random(2026)
    red_balls, blue_ball = generate_ticket(demo_random)
    red_text = " ".join(f"{number:02d}" for number in red_balls)
    print(f"红球：{red_text}  蓝球：{blue_ball:02d}")
    print("这只是 random、sample 和格式化练习，不是预测工具。")


if __name__ == "__main__":
    main()

# 练习：一次生成 5 注，并检查每注红球是否都不重复。
