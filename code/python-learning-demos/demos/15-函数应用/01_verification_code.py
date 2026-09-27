"""Day15：生成由数字和字母组成的随机验证码。"""

import random
import string


def generate_code(length: int = 6, *, random_source: random.Random | None = None) -> str:
    """生成验证码；可注入随机数对象，使测试结果可重复。"""
    if length <= 0:
        raise ValueError("length 必须大于 0")
    source = random_source or random.SystemRandom()
    alphabet = string.ascii_uppercase + string.digits
    return "".join(source.choice(alphabet) for _ in range(length))


def main() -> None:
    # 固定 seed 只为了让教学输出稳定；真实验证码不要使用可预测的 seed。
    demo_random = random.Random(2026)
    print(f"演示验证码：{generate_code(6, random_source=demo_random)}")


if __name__ == "__main__":
    main()

# 练习：增加 exclude_ambiguous 参数，排除 0/O、1/I 等易混字符。
