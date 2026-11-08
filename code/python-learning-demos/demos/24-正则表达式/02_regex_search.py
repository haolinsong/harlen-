"""Day24：用 finditer 找到文本中所有匹配项及其位置。"""

import re


TICKET = re.compile(r"\b(?P<kind>BUG|TASK)-(?P<number>[0-9]{3})\b")


def find_tickets(text: str) -> list[tuple[str, int, int]]:
    """按出现顺序返回编号、起始位置和结束位置。"""
    # finditer 返回 Match 对象；除了匹配文本，还能取得 span 位置信息。
    return [
        (match.group(), *match.span())
        for match in TICKET.finditer(text)
    ]


def main() -> None:
    text = "今天修复 BUG-007，并开始 TASK-024；BUG-12 还不是三位编号。"
    print(f"输入：{text}")
    for ticket, start, end in find_tickets(text):
        print(f"编号 {ticket} 位于 [{start}, {end})，切片结果：{text[start:end]}")


if __name__ == "__main__":
    main()

# 练习：为编号再增加 IDEA 类型，并尝试用 match.group("kind") 取出类别。
