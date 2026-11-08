"""Day24：用正则表达式检查一整段课程编号。"""

import re


# r 前缀使反斜线留给正则表达式解释，避免与 Python 字符串转义混淆。
# 命名分组让每一段的含义比数字下标更容易看懂。
COURSE_CODE = re.compile(
    r"(?P<subject>[A-Z]{2})-(?P<year>[0-9]{4})-(?P<lesson>[0-9]{2})"
)


def parse_course_code(text: str) -> dict[str, str | int]:
    """解析形如 PY-2026-24 的编号；格式不符时抛出 ValueError。"""
    # fullmatch 要求整个输入符合格式；search 只要找到其中一段就会成功。
    match = COURSE_CODE.fullmatch(text.strip())
    if match is None:
        raise ValueError("编号格式应为两个大写字母-四位年份-两位课号")
    return {
        "subject": match.group("subject"),
        "year": int(match.group("year")),
        "lesson": int(match.group("lesson")),
    }


def main() -> None:
    for text in ["PY-2026-24", "前缀 PY-2026-24", "Py-2026-24"]:
        try:
            print(f"输入：{text!r} → {parse_course_code(text)}")
        except ValueError as error:
            print(f"输入：{text!r} → {error}")


if __name__ == "__main__":
    main()

# 练习：允许三位课号，并观察修改正则后旧编号是否仍能通过。
