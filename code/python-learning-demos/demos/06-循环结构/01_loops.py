"""Day06：for、while、break 和 continue。"""


def main() -> None:
    # range(1, 6) 生成 1、2、3、4、5，不包含右边界 6。
    total = 0
    for number in range(1, 6):
        total += number
    print(f"1 到 5 的和：{total}")

    # continue 跳过本轮剩余代码，下面只打印奇数。
    odds: list[int] = []
    for number in range(10):
        if number % 2 == 0:
            continue
        odds.append(number)
    print(f"10 以内的奇数：{odds}")

    # while 适合循环次数事先不明确、由条件决定结束的场景。
    countdown = 3
    while countdown > 0:
        print(f"倒计时：{countdown}")
        countdown -= 1

    # break 会立刻结束当前循环。
    for number in range(1, 100):
        if number % 7 == 0 and number % 5 == 0:
            print(f"第一个同时被 5 和 7 整除的正整数：{number}")
            break


if __name__ == "__main__":
    main()

# 练习：计算 1 到 100 之间所有偶数的和。
