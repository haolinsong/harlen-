"""Day26：清洗 CSV，汇总学习时长并生成带原始数据附件的邮件草稿。"""

import csv
import json
import math
import re
from email.message import EmailMessage
from io import StringIO


def build_report(csv_text: str) -> dict[str, object]:
    """读取 student,hours 数据，合并同名学生的学习时长。"""
    reader = csv.DictReader(StringIO(csv_text))
    if reader.fieldnames != ["student", "hours"]:
        raise ValueError("CSV 表头必须是 student,hours")

    hours_by_student: dict[str, float] = {}
    record_count = 0
    for line_number, row in enumerate(reader, start=2):
        # 多余或缺失的列会产生 None 键或 None 值，应立即报告所在行。
        if None in row or row["student"] is None or row["hours"] is None:
            raise ValueError(f"第 {line_number} 行列数不正确")
        student = re.sub(r"\s+", " ", row["student"]).strip()
        if not student:
            raise ValueError(f"第 {line_number} 行缺少姓名")
        try:
            hours = float(row["hours"])
        except ValueError as error:
            raise ValueError(f"第 {line_number} 行学习时长不是数字") from error
        if not math.isfinite(hours) or hours < 0:
            raise ValueError(f"第 {line_number} 行学习时长必须是非负有限数字")
        hours_by_student[student] = hours_by_student.get(student, 0.0) + hours
        record_count += 1

    if record_count == 0:
        raise ValueError("CSV 中没有学习记录")
    return {
        "record_count": record_count,
        "total_hours": round(sum(hours_by_student.values()), 2),
        "hours_by_student": {
            name: round(hours, 2) for name, hours in sorted(hours_by_student.items())
        },
    }


def build_report_draft(csv_text: str) -> EmailMessage:
    """生成本地邮件草稿：正文为 JSON 摘要，附件为原始 CSV。"""
    report = build_report(csv_text)
    message = EmailMessage()
    message["From"] = "teacher@example.com"
    message["To"] = "student@example.com"
    message["Subject"] = "Python 学习时长报告"
    message.set_content(json.dumps(report, ensure_ascii=False, indent=2))
    message.add_attachment(
        csv_text,
        subtype="csv",
        charset="utf-8",
        filename="learning.csv",
    )
    return message


def main() -> None:
    csv_text = "student,hours\n Alice ,2.5\nBob,3\nAlice,1.5\n"
    draft = build_report_draft(csv_text)
    print("输入的 CSV：")
    print(csv_text.strip())
    print(f"\n邮件主题：{draft['Subject']}")
    print("JSON 摘要：")
    print(draft.get_body(preferencelist=("plain",)).get_content().strip())
    print(f"附件名称：{next(draft.iter_attachments()).get_filename()}")


if __name__ == "__main__":
    main()

# 练习：按学习时长降序列出学生，并增加“平均每条记录时长”字段。
