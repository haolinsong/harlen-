"""验证 Day31-40 进阶语法、并发和数据库示例。"""

from __future__ import annotations

import asyncio
import importlib.util
import sqlite3
import sys
import unittest
from contextlib import closing
from pathlib import Path
from types import ModuleType


DEMOS = Path(__file__).resolve().parents[1] / "demos"


def load_demo(relative_path: str) -> ModuleType:
    path = DEMOS / relative_path
    name = "advanced_demo_" + "_".join(path.with_suffix("").parts[-2:])
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 Demo：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class AdvancedAndDatabaseTest(unittest.TestCase):
    def test_iterator_can_restart(self) -> None:
        demo = load_demo("31-迭代器与生成器/01_iterator_protocol.py")
        values = demo.Countdown(3)
        self.assertEqual(list(values), [3, 2, 1])
        self.assertEqual(list(values), [3, 2, 1])

    def test_generator_validates_rows_lazily(self) -> None:
        demo = load_demo("31-迭代器与生成器/02_generator_pipeline.py")
        self.assertEqual(list(demo.long_sessions(demo.parse_events(["甲,20", "乙,45"]), 40)), ["乙: 45 分钟"])
        with self.assertRaisesRegex(ValueError, "第 2 行"):
            list(demo.parse_events(["甲,20", "乙,wrong"]))

    def test_dataclass_validation_and_cents(self) -> None:
        demo = load_demo("32-数据类与模式匹配/01_dataclass_models.py")
        self.assertEqual(demo.total_cents([demo.OrderLine(demo.Product("笔", 125), 3)]), 375)
        with self.assertRaises(ValueError):
            demo.Product("", 100)

    def test_structural_match(self) -> None:
        demo = load_demo("32-数据类与模式匹配/02_structural_matching.py")
        self.assertEqual(demo.describe_command(["delete", "小明"]), "删除 小明 的成绩")
        with self.assertRaises(ValueError):
            demo.describe_command({"action": "add", "name": "小明", "score": 101})

    def test_groupby_requires_sorting(self) -> None:
        demo = load_demo("33-迭代工具/01_itertools_grouping.py")
        self.assertEqual(demo.hours_by_person([("甲", 2), ("乙", 4), ("甲", 3)]), {"甲": 5, "乙": 4})

    def test_thread_results_are_deterministic(self) -> None:
        pool_demo = load_demo("34-线程并发/01_thread_pool.py")
        lock_demo = load_demo("34-线程并发/02_thread_lock.py")
        self.assertEqual(pool_demo.square_waiting_values([3, 1, 2]), [9, 1, 4])
        self.assertEqual(lock_demo.count_total([1] * 100), 100)

    def test_asyncio_gather_preserves_input_order(self) -> None:
        demo = load_demo("35-异步任务/01_asyncio_gather.py")
        self.assertEqual(asyncio.run(demo.run_jobs(["A", "B"])), ["A 已完成", "B 已完成"])

    def test_search_and_stable_sort(self) -> None:
        demo = load_demo("36-搜索与排序/01_search_sort.py")
        self.assertEqual(demo.binary_search([1, 2, 2, 3], 2), 1)
        self.assertIsNone(demo.binary_search([1, 3], 2))
        self.assertEqual(demo.rank_students([("甲", 90), ("乙", 95), ("丙", 90)]), [("乙", 95), ("甲", 90), ("丙", 90)])

    def test_subprocess_receives_only_explicit_value(self) -> None:
        demo = load_demo("37-进程与环境变量/01_subprocess_environment.py")
        self.assertEqual(demo.run_child("安全; 不执行命令"), "安全; 不执行命令")

    def test_sqlite_crud(self) -> None:
        demo = load_demo("38-SQLite基础/01_sqlite_crud.py")
        with closing(sqlite3.connect(":memory:")) as connection:
            demo.create_database(connection)
            book_id = demo.add_book(connection, "SQL", 80)
            self.assertEqual(demo.list_books(connection), [(book_id, "SQL", 80)])

    def test_left_join_keeps_students_without_lessons(self) -> None:
        demo = load_demo("39-关联查询与索引/01_join_and_index.py")
        with closing(sqlite3.connect(":memory:")) as connection:
            demo.prepare_database(connection)
            self.assertEqual(demo.lesson_counts(connection), [("小明", 2), ("小红", 1), ("小刚", 0)])

    def test_transfer_rolls_back_when_receiver_missing(self) -> None:
        demo = load_demo("40-事务与数据库项目/01_transactions.py")
        with closing(sqlite3.connect(":memory:")) as connection:
            demo.create_accounts(connection)
            before = demo.balances(connection)
            with self.assertRaises(ValueError):
                demo.transfer(connection, "甲", "不存在", 30)
            self.assertEqual(demo.balances(connection), before)

    def test_csv_import_rolls_back_whole_batch(self) -> None:
        demo = load_demo("40-事务与数据库项目/02_csv_to_database.py")
        with closing(sqlite3.connect(":memory:")) as connection:
            connection.execute("CREATE TABLE scores (name TEXT PRIMARY KEY, score INTEGER NOT NULL)")
            connection.commit()
            with self.assertRaises(ValueError):
                demo.import_scores(connection, "name,score\n甲,90\n乙,wrong\n")
            self.assertEqual(demo.summary(connection), (0, None))


if __name__ == "__main__":
    unittest.main()
