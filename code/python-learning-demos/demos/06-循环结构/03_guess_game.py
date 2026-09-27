"""Day06：用 while 和分支实现可重复的猜数字流程。"""


def evaluate_guess(secret: int, guess: int) -> str:
    if guess < secret:
        return "太小了"
    if guess > secret:
        return "太大了"
    return "猜中了"


def play_with_guesses(secret: int, guesses: list[int]) -> int | None:
    """依次使用给定猜测，返回猜中的次数；没有猜中则返回 None。"""
    attempts = 0
    for guess in guesses:
        attempts += 1
        result = evaluate_guess(secret, guess)
        print(f"第 {attempts} 次猜 {guess}：{result}")
        if result == "猜中了":
            return attempts
    return None


def main() -> None:
    # 使用固定答案和猜测序列，确保每次运行输出一致，便于学习和测试。
    attempts = play_with_guesses(secret=42, guesses=[20, 60, 35, 42])
    print(f"结果：共尝试 {attempts} 次" if attempts else "没有猜中")

    # 交互版本可以在循环中使用 int(input('请输入数字：')) 获取用户输入。


if __name__ == "__main__":
    main()

# 练习：使用 random.randint(1, 100) 生成随机答案并改成交互版本。
