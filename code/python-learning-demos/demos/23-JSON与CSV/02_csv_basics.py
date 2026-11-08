"""Day23：使用 csv 模块读写结构统一的表格数据。"""

import csv
from pathlib import Path
from tempfile import TemporaryDirectory


FIELDNAMES = ["name", "language", "hours"]


def write_records(path: Path, records: list[dict[str, object]]) -> None:
    """写入带表头的 CSV；newline='' 可避免跨平台出现多余空行。"""
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)


def read_records(path: Path) -> list[dict[str, object]]:
    """读取 CSV，并把 hours 从文本显式转换为整数。"""
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return [
            {
                "name": row["name"],
                "language": row["language"],
                "hours": int(row["hours"]),
            }
            for row in reader
        ]


def main() -> None:
    records: list[dict[str, object]] = [
        {"name": "Alice", "language": "Python", "hours": 12},
        {"name": "Bob", "language": "Java", "hours": 8},
    ]

    with TemporaryDirectory() as directory:
        path = Path(directory) / "learning.csv"
        write_records(path, records)
        loaded = read_records(path)

        print("CSV 文件内容：")
        print(path.read_text(encoding="utf-8").strip())
        print(f"读取后的记录：{loaded}")
        print(f"总学习时长：{sum(record['hours'] for record in loaded)} 小时")


if __name__ == "__main__":
    main()

# 练习：增加 completed 字段，并在读取时把 true/false 文本转换为 bool。
