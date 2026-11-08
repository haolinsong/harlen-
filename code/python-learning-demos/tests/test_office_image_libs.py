"""验证 Day27-29 第三方库实操文件可写入、读回且输入校验有效。"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from zipfile import ZipFile


DEMOS = Path(__file__).resolve().parents[1] / "demos"


def load_demo(relative_path: str) -> ModuleType:
    path = DEMOS / relative_path
    name = "office_demo_" + "_".join(path.with_suffix("").parts[-2:])
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 Demo：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class OfficeImageLibrariesTest(unittest.TestCase):
    def test_openpyxl_round_trip_and_formula(self) -> None:
        demo = load_demo("27-Excel与电子表格/03_openpyxl_report.py")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "report.xlsx"
            demo.create_study_report(path, [("小明", 2.5), ("小红", 3)])
            records, formula = demo.read_study_report(path)
            self.assertEqual(records, [("小明", 2.5), ("小红", 3)])
            self.assertEqual(formula, "=SUM(B2:B3)")
            with ZipFile(path) as archive:
                self.assertIsNone(archive.testzip())
            with self.assertRaises(ValueError):
                demo.create_study_report(path, [("小明", -1)])

    def test_word_report_round_trip(self) -> None:
        demo = load_demo("28-Word与PowerPoint/03_word_report.py")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "report.docx"
            demo.create_word_report(path, "学习周报", ["复习", "练习"])
            self.assertEqual(demo.read_word_report(path), ("学习周报", ["复习", "练习"]))
            with ZipFile(path) as archive:
                self.assertIsNone(archive.testzip())
            with self.assertRaises(ValueError):
                demo.create_word_report(path, "", ["练习"])

    def test_powerpoint_deck_round_trip(self) -> None:
        demo = load_demo("28-Word与PowerPoint/04_powerpoint_deck.py")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "deck.pptx"
            demo.create_learning_deck(path, "文件处理", ["验证输入", "保存文件"])
            self.assertEqual(demo.read_learning_deck(path), ("文件处理", ["验证输入", "保存文件"]))
            with ZipFile(path) as archive:
                self.assertIsNone(archive.testzip())
            with self.assertRaises(ValueError):
                demo.create_learning_deck(path, "文件处理", [])

    def test_reportlab_pdf_round_trip(self) -> None:
        demo = load_demo("29-PDF与图像基础/03_reportlab_pdf.py")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "report.pdf"
            demo.create_pdf_report(path, "Python Report", ["Review files", "Practice"])
            pages, text = demo.read_pdf_report(path)
            self.assertEqual(pages, 1)
            self.assertIn("Python Report", text)
            self.assertIn("Review files", text)
            with self.assertRaises(ValueError):
                demo.create_pdf_report(path, "中文报告", ["Practice"])

    def test_pillow_png_pixels_and_size(self) -> None:
        demo = load_demo("29-PDF与图像基础/04_pillow_image.py")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "card.png"
            demo.create_color_card(path, 10, 5)
            self.assertEqual(
                demo.read_color_card(path),
                ((20, 10), "RGB", (255, 0, 0), (0, 0, 255)),
            )
            with self.assertRaises(ValueError):
                demo.create_color_card(path, 1, 5)


if __name__ == "__main__":
    unittest.main()
