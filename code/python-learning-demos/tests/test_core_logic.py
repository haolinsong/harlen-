"""验证几个具有代表性的纯函数和类。"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from types import ModuleType


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str) -> ModuleType:
    """从任意 Demo 文件加载模块，避免目录名和文件名限制普通 import。"""
    path = PROJECT_ROOT / relative_path
    module_name = "demo_" + "_".join(path.with_suffix("").parts[-3:])
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载模块：{path}")
    module = importlib.util.module_from_spec(spec)
    # dataclass 等功能会通过 sys.modules 查找当前模块。
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class CoreLogicTest(unittest.TestCase):
    def test_temperature_conversion(self) -> None:
        module = load_module("demos/04-运算符与表达式/02_temperature_converter.py")
        self.assertAlmostEqual(module.celsius_to_fahrenheit(0), 32)
        self.assertAlmostEqual(module.fahrenheit_to_celsius(212), 100)

    def test_grade_boundaries(self) -> None:
        module = load_module("demos/05-分支结构/01_grade_level.py")
        self.assertEqual(module.grade_level(90), "A")
        self.assertEqual(module.grade_level(59.9), "E")
        self.assertEqual(module.grade_level(101), "无效成绩")

    def test_prime_and_fibonacci(self) -> None:
        prime = load_module("demos/06-循环结构/02_prime_checker.py")
        fibonacci = load_module("demos/07-循环综合练习/02_fibonacci.py")
        self.assertTrue(prime.is_prime(97))
        self.assertFalse(prime.is_prime(1))
        self.assertEqual(fibonacci.fibonacci(7), [0, 1, 1, 2, 3, 5, 8])

    def test_matrix_transpose(self) -> None:
        module = load_module("demos/09-列表进阶与矩阵/03_matrix.py")
        self.assertEqual(module.transpose([[1, 2, 3], [4, 5, 6]]), [[1, 4], [2, 5], [3, 6]])

    def test_word_frequency(self) -> None:
        module = load_module("demos/13-字典/02_word_frequency.py")
        self.assertEqual(module.word_frequency("Python python Java"), {"python": 2, "java": 1})

    def test_statistics(self) -> None:
        module = load_module("demos/15-函数应用/02_statistics_demo.py")
        self.assertEqual(module.mean([1, 2, 3]), 2)
        self.assertEqual(module.median([1, 4, 2, 3]), 2.5)

    def test_point_distance(self) -> None:
        module = load_module("demos/18-类与对象/03_point.py")
        self.assertEqual(module.Point(0, 0).distance_to(module.Point(3, 4)), 5)

    def test_poker_deck_and_hand(self) -> None:
        module = load_module("demos/20-面向对象综合项目/01_poker_game.py")
        deck = module.Deck()
        hand = deck.deal(5)
        self.assertEqual(len(hand), 5)
        self.assertEqual(len(deck), 47)
        straight = [module.Card("Clubs", rank) for rank in [2, 3, 4, 5, 6]]
        self.assertEqual(module.hand_category(straight), "同花顺")

    def test_payroll_polymorphism(self) -> None:
        module = load_module("demos/20-面向对象综合项目/02_payroll_system.py")
        employee = module.HourlyEmployee("E1", "Tester", hours=170, hourly_rate=10)
        self.assertEqual(employee.monthly_pay(), 1750)


if __name__ == "__main__":
    unittest.main()
