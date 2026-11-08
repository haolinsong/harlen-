"""Day39：用外键、JOIN 和查询计划观察关系数据库的基本操作。"""

import sqlite3
from contextlib import closing


def prepare_database(connection: sqlite3.Connection) -> None:
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
    connection.execute(
        "CREATE TABLE lessons (student_id INTEGER NOT NULL REFERENCES students(id), topic TEXT NOT NULL)"
    )
    connection.executemany(
        "INSERT INTO students(id, name) VALUES (?, ?)", [(1, "小明"), (2, "小红"), (3, "小刚")]
    )
    connection.executemany(
        "INSERT INTO lessons(student_id, topic) VALUES (?, ?)",
        [(1, "文件"), (1, "数据库"), (2, "数据库")],
    )
    connection.commit()


def lesson_counts(connection: sqlite3.Connection) -> list[tuple[str, int]]:
    return connection.execute(
        "SELECT s.name, COUNT(l.topic) FROM students AS s "
        "LEFT JOIN lessons AS l ON l.student_id = s.id "
        "GROUP BY s.id, s.name ORDER BY s.id"
    ).fetchall()


def index_plan(connection: sqlite3.Connection) -> list[str]:
    # 查询计划由 SQLite 和数据量决定；只观察，不硬编码“必定使用索引”。
    return [
        str(row[3])
        for row in connection.execute(
            "EXPLAIN QUERY PLAN SELECT topic FROM lessons WHERE student_id = ?", (1,)
        )
    ]


def main() -> None:
    with closing(sqlite3.connect(":memory:")) as connection:
        prepare_database(connection)
        print("LEFT JOIN 后的学习次数：", lesson_counts(connection))
        print("创建索引前的查询计划：", index_plan(connection))
        connection.execute("CREATE INDEX idx_lessons_student ON lessons(student_id)")
        print("创建索引后的查询计划：", index_plan(connection))


if __name__ == "__main__":
    main()

# 练习：改为 INNER JOIN，观察没有选课的小刚是否还会出现。
