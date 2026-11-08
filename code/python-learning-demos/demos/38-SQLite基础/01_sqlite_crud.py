"""Day38：用内存 SQLite 练习建表、增删改查与参数绑定。"""

import sqlite3
from contextlib import closing


def create_database(connection: sqlite3.Connection) -> None:
    connection.execute(
        "CREATE TABLE books (id INTEGER PRIMARY KEY, title TEXT NOT NULL, pages INTEGER NOT NULL CHECK(pages > 0))"
    )
    connection.commit()


def add_book(connection: sqlite3.Connection, title: str, pages: int) -> int:
    if not title.strip() or pages <= 0:
        raise ValueError("书名不能为空，页数必须大于零")
    # 占位符让数据库驱动绑定值；不要用 f-string 拼接用户输入。
    cursor = connection.execute(
        "INSERT INTO books(title, pages) VALUES (?, ?)", (title, pages)
    )
    connection.commit()
    return int(cursor.lastrowid)


def list_books(connection: sqlite3.Connection) -> list[tuple[int, str, int]]:
    return connection.execute("SELECT id, title, pages FROM books ORDER BY id").fetchall()


def main() -> None:
    with closing(sqlite3.connect(":memory:")) as connection:
        create_database(connection)
        book_id = add_book(connection, "Python 入门", 180)
        connection.execute("UPDATE books SET pages = ? WHERE id = ?", (200, book_id))
        connection.commit()
        print("输入：Python 入门，180 页；更新为 200 页")
        print("查询结果：", list_books(connection))
        connection.execute("DELETE FROM books WHERE id = ?", (book_id,))
        connection.commit()
        print("删除后：", list_books(connection))


if __name__ == "__main__":
    main()

# 练习：增加根据最低页数筛选书籍的函数，仍使用 SQL 占位符。
