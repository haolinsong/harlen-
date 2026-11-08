"""Day40 综合练习：把 CSV 成绩导入 SQLite，整批失败时不留半成品。"""

import csv
import sqlite3
from contextlib import closing
from io import StringIO


def import_scores(connection: sqlite3.Connection, csv_text: str) -> int:
    reader = csv.DictReader(StringIO(csv_text))
    if reader.fieldnames != ["name", "score"]:
        raise ValueError("CSV 表头必须是 name,score")
    count = 0
    with connection:
        for line_number, row in enumerate(reader, start=2):
            if None in row or row["name"] is None or row["score"] is None:
                raise ValueError(f"第 {line_number} 行列数不正确")
            name = row["name"].strip()
            try:
                score = int(row["score"])
            except ValueError as error:
                raise ValueError(f"第 {line_number} 行分数不是整数") from error
            if not name or not 0 <= score <= 100:
                raise ValueError(f"第 {line_number} 行姓名或分数无效")
            connection.execute(
                "INSERT INTO scores(name, score) VALUES (?, ?)", (name, score)
            )
            count += 1
    return count


def summary(connection: sqlite3.Connection) -> tuple[int, float | None]:
    return connection.execute("SELECT COUNT(*), ROUND(AVG(score), 2) FROM scores").fetchone()


def main() -> None:
    with closing(sqlite3.connect(":memory:")) as connection:
        connection.execute(
            "CREATE TABLE scores (name TEXT PRIMARY KEY, score INTEGER NOT NULL CHECK(score BETWEEN 0 AND 100))"
        )
        connection.commit()
        csv_text = "name,score\n小明,90\n小红,80\n"
        print("输入 CSV：\n" + csv_text.strip())
        print("导入条数：", import_scores(connection, csv_text))
        print("数据库摘要（人数、均分）：", summary(connection))


if __name__ == "__main__":
    main()

# 练习：在 CSV 中加入一个无效分数，验证导入后数据库仍为空。
