"""验证 Day27-30 零依赖文件格式与本地通信示例。"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from types import ModuleType
from zipfile import ZipFile


DEMOS = Path(__file__).resolve().parents[1] / "demos"


def load_demo(relative_path: str) -> ModuleType:
    path = DEMOS / relative_path
    name = "format_demo_" + "_".join(path.with_suffix("").parts[-2:])
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 Demo：{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class FormatsAndNotificationsTest(unittest.TestCase):
    def test_csv_bom_and_formula_text(self) -> None:
        demo = load_demo("27-Excel与电子表格/01_excel_compatible_csv.py")
        with TemporaryDirectory() as directory:
            path = Path(directory) / "sheet.csv"
            demo.export_csv(path, [("小明", "=1+1")])
            self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))
            self.assertEqual(demo.read_csv(path)[1], ["小明", "'=1+1"])

    def test_xlsx_package_round_trip(self) -> None:
        demo = load_demo("27-Excel与电子表格/02_xlsx_package.py")
        rows = [["姓名", "时长"], ["小明", "2.5"]]
        data = demo.build_xlsx(rows)
        with ZipFile(BytesIO(data)) as archive:
            self.assertIsNone(archive.testzip())
            self.assertIn("xl/workbook.xml", archive.namelist())
        self.assertEqual(demo.read_first_sheet(data), rows)

    def test_docx_round_trip(self) -> None:
        demo = load_demo("28-Word与PowerPoint/01_docx_package.py")
        paragraphs = ["标题", "正文含中文"]
        self.assertEqual(demo.read_paragraphs(demo.build_docx(paragraphs)), paragraphs)

    def test_presentation_fragment_is_not_claimed_as_pptx(self) -> None:
        demo = load_demo("28-Word与PowerPoint/02_pptx_structure.py")
        self.assertEqual(demo.read_slide_text(demo.build_slide_structure("标题", ["第一点"])), ["标题", "第一点"])

    def test_pdf_has_consistent_cross_reference_offset(self) -> None:
        demo = load_demo("29-PDF与图像基础/01_minimal_pdf.py")
        data = demo.build_pdf("Hello PDF")
        self.assertTrue(data.startswith(b"%PDF-1.4\n"))
        self.assertTrue(data.endswith(b"%%EOF\n"))
        start_xref = int(data.split(b"startxref\n")[1].split(b"\n", 1)[0])
        self.assertEqual(data[start_xref:start_xref + 4], b"xref")
        with self.assertRaises(ValueError):
            demo.build_pdf("中文")

    def test_ppm_resize_and_validation(self) -> None:
        demo = load_demo("29-PDF与图像基础/02_ppm_pixels.py")
        pixels = [[(255, 0, 0), (0, 0, 255)]]
        self.assertEqual(demo.resize_nearest(pixels, 4, 1)[0], [pixels[0][0], pixels[0][0], pixels[0][1], pixels[0][1]])
        with TemporaryDirectory() as directory:
            path = Path(directory) / "image.ppm"
            demo.write_ppm(path, pixels)
            self.assertTrue(path.read_bytes().startswith(b"P6\n2 1\n255\n"))

    def test_email_send_uses_local_fake(self) -> None:
        demo = load_demo("30-本地通信模拟/01_email_transport.py")
        transport = demo.FakeMailTransport()
        demo.send_notice(transport, "student@example.invalid", "报告内容")
        self.assertEqual(transport.sent[0].get_content().strip(), "报告内容")

    def test_sms_request_is_not_sent_to_network(self) -> None:
        demo = load_demo("30-本地通信模拟/02_sms_request.py")
        request = demo.build_sms_request("+40123456789", "学习提醒")
        self.assertEqual(demo.fake_gateway(request)["status"], "accepted-locally")


if __name__ == "__main__":
    unittest.main()
