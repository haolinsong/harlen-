"""Day23：综合 CSV、异常处理和 JSON 生成成绩统计报告。"""

import csv
import json
from io import StringIO
from typing import Any


def build_score_report(csv_text: str) -> dict[str, Any]:
    """读取 CSV 文本，校验成绩并生成可以直接序列化的报告。"""
    reader = csv.DictReader(StringIO(csv_text))
    if reader.fieldnames != ["name", "score"]:
        raise ValueError("CSV 表头必须是 name,score")

    records: list[tuple[str, float]] = []
    for line_number, row in enumerate(reader, start=2):
        name = row["name"].strip()
        if not name:
            raise ValueError(f"第 {line_number} 行缺少姓名")
        try:
            score = float(row["score"])
        except ValueError as error:
            raise ValueError(f"第 {line_number} 行成绩不是数字") from error
        if not 0 <= score <= 100:
            raise ValueError(f"第 {line_number} 行成绩超出 0～100")
        records.append((name, score))

    if not records:
        raise ValueError("CSV 中没有成绩记录")

    top_name, top_score = max(records, key=lambda item: item[1])
    average = sum(score for _, score in records) / len(records)
    return {
        "student_count": len(records),
        "average": round(average, 2),
        "passed_count": sum(score >= 60 for _, score in records),
        "top_student": {"name": top_name, "score": top_score},
    }


def main() -> None:
    csv_text = """name,score
Alice,92
Bob,78
Carol,55
"""
    report = build_score_report(csv_text)

    print("输入的 CSV：")
    print(csv_text.strip())
    print("\n生成的 JSON 报告：")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

# 练习：在报告中增加最高分、最低分和及格率，
# 并为并列最高分设计返回结构。
