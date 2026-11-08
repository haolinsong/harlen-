"""Day24：用 re.sub 清理空白并统一日期的书写格式。"""

import re


DATE_WITH_SLASHES = re.compile(r"\b(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})\b")


def clean_note(text: str) -> str:
    """压缩连续空白，并把 YYYY/MM/DD 的分隔符改成连字符。"""
    compact = re.sub(r"\s+", " ", text).strip()
    # 替换函数使用命名分组，避免手写切片下标。
    return DATE_WITH_SLASHES.sub(
        lambda match: (
            f"{match.group('year')}-{match.group('month')}-{match.group('day')}"
        ),
        compact,
    )


def main() -> None:
    raw = "  Python 学习\n  复习日期：2026/10/24   计划：正则表达式  "
    print(f"原始输入：{raw!r}")
    print(f"清理结果：{clean_note(raw)}")
    print("提示：这里只统一日期格式，没有检查日期是否真实存在。")


if __name__ == "__main__":
    main()

# 练习：把连续逗号和空格改成一个中文逗号，注意别误删普通文字。
