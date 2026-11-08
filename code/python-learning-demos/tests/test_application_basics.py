"""验证 Day21-26 文件、文本、邮件和数据处理示例的核心逻辑。"""

from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from email import policy
from email.parser import BytesParser
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_module(relative_path: str) -> ModuleType:
    """从包含中文目录名的 Demo 路径加载模块。"""
    path = PROJECT_ROOT / relative_path
    module_name = "application_demo_" + "_".join(path.with_suffix("").parts[-3:])
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载模块：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class ApplicationBasicsTest(unittest.TestCase):
    def test_text_file_round_trip(self) -> None:
        module = load_module("demos/21-文件与路径/01_text_files.py")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "notes.txt"
            module.write_notes(path, ["第一条", "第二条"])
            module.append_note(path, "第三条")
            self.assertEqual(module.read_notes(path), ["第一条", "第二条", "第三条"])

    def test_binary_copy_keeps_content(self) -> None:
        module = load_module("demos/21-文件与路径/02_binary_files.py")
        with TemporaryDirectory() as directory:
            source = Path(directory) / "source.bin"
            target = Path(directory) / "target.bin"
            source.write_bytes(bytes(range(64)))
            module.copy_binary(source, target, chunk_size=7)
            self.assertEqual(source.read_bytes(), target.read_bytes())
            self.assertEqual(module.file_digest(source), module.file_digest(target))

    def test_pathlib_finds_nested_python_files(self) -> None:
        module = load_module("demos/21-文件与路径/03_pathlib_paths.py")
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "package").mkdir()
            (root / "main.py").write_text("", encoding="utf-8")
            (root / "package" / "tool.py").write_text("", encoding="utf-8")
            (root / "README.md").write_text("", encoding="utf-8")
            self.assertEqual(module.find_python_files(root), ["main.py", "package/tool.py"])

    def test_score_validation(self) -> None:
        module = load_module("demos/22-异常与上下文管理/01_exception_handling.py")
        self.assertEqual(module.parse_score("92.5"), 92.5)
        with self.assertRaises(ValueError):
            module.parse_score("101")
        with self.assertRaises(ValueError):
            module.parse_score("not-a-number")

    def test_custom_exception_exposes_context(self) -> None:
        module = load_module("demos/22-异常与上下文管理/02_custom_exceptions.py")
        wallet = module.Wallet(50)
        with self.assertRaises(module.InsufficientBalanceError) as raised:
            wallet.withdraw(70)
        self.assertEqual(raised.exception.balance, 50)
        self.assertEqual(raised.exception.amount, 70)
        self.assertEqual(wallet.balance, 50)

    def test_json_round_trip(self) -> None:
        module = load_module("demos/23-JSON与CSV/01_json_basics.py")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "data.json"
            expected = {"title": "Python 学习", "days": [21, 22, 23]}
            module.save_json(path, expected)
            self.assertEqual(module.load_json(path), expected)

    def test_csv_score_report(self) -> None:
        module = load_module("demos/23-JSON与CSV/03_score_report.py")
        report = module.build_score_report("name,score\nAlice,90\nBob,50\n")
        self.assertEqual(report["student_count"], 2)
        self.assertEqual(report["average"], 70.0)
        self.assertEqual(report["passed_count"], 1)
        self.assertEqual(report["top_student"], {"name": "Alice", "score": 90.0})

    def test_regex_requires_whole_course_code(self) -> None:
        module = load_module("demos/24-正则表达式/01_regex_basics.py")
        self.assertEqual(
            module.parse_course_code("PY-2026-24"),
            {"subject": "PY", "year": 2026, "lesson": 24},
        )
        for invalid in ["前缀 PY-2026-24", "Py-2026-24", "PY-2026-2"]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                module.parse_course_code(invalid)

    def test_email_attachment_survives_serialization(self) -> None:
        module = load_module("demos/25-邮件消息/02_csv_attachment.py")
        csv_text = "name,hours\n小明,2.5\n"
        message = module.build_message_with_csv(csv_text)
        parsed = BytesParser(policy=policy.default).parsebytes(message.as_bytes())
        attachments = list(parsed.iter_attachments())
        self.assertEqual(len(attachments), 1)
        self.assertEqual(attachments[0].get_filename(), "learning.csv")
        self.assertEqual(attachments[0].get_content(), csv_text)

    def test_weekly_report_merges_names_and_rejects_invalid_hours(self) -> None:
        module = load_module("demos/26-数据清洗与报告/01_weekly_report.py")
        csv_text = "student,hours\n Alice ,2.5\nBob,3\nAlice,1.5\n"
        report = module.build_report(csv_text)
        self.assertEqual(report["record_count"], 3)
        self.assertEqual(report["total_hours"], 7.0)
        self.assertEqual(report["hours_by_student"], {"Alice": 4.0, "Bob": 3.0})
        for invalid in ["-1", "nan", "wrong"]:
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                module.build_report(f"student,hours\nAlice,{invalid}\n")

    def test_weekly_report_draft_contains_summary_and_source(self) -> None:
        module = load_module("demos/26-数据清洗与报告/01_weekly_report.py")
        csv_text = "student,hours\nAlice,2\n"
        draft = module.build_report_draft(csv_text)
        parsed = BytesParser(policy=policy.default).parsebytes(draft.as_bytes())
        body = parsed.get_body(preferencelist=("plain",)).get_content()
        self.assertEqual(json.loads(body)["total_hours"], 2.0)
        attachment = next(parsed.iter_attachments())
        self.assertEqual(attachment.get_content(), csv_text)


if __name__ == "__main__":
    unittest.main()
