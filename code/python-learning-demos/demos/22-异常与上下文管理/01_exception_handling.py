"""Day22：使用 try/except/else/finally 处理可预期的错误。"""


def parse_score(text: str) -> float:
    """把文本转换为 0～100 的成绩，无效输入时抛出 ValueError。"""
    score = float(text)
    if not 0 <= score <= 100:
        raise ValueError("成绩必须在 0 到 100 之间")
    return score


def describe_score(text: str) -> str:
    """把异常转换成适合展示给用户的结果。"""
    try:
        score = parse_score(text)
    except ValueError as error:
        # 只捕获能够处理的具体异常，不使用会隐藏程序错误的裸 except。
        return f"输入 {text!r} 无效：{error}"
    else:
        # else 只在 try 没有异常时执行，正常路径和错误路径因此更清楚。
        return f"输入 {text!r} 有效，成绩为 {score:.1f}"


def main() -> None:
    for text in ["92.5", "abc", "120"]:
        try:
            print(describe_score(text))
        finally:
            # finally 无论是否发生异常都会执行，
            # 常用于关闭资源或记录结束状态。
            print(f"已处理输入：{text!r}")


if __name__ == "__main__":
    main()

# 练习：让空字符串返回“请输入成绩”，
# 其他格式错误仍显示原异常信息。
