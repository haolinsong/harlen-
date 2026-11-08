"""Day29：用 ReportLab 生成 PDF，并用 pypdf 验证页数和文字。"""

from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_pdf_report(path: Path, title: str, items: list[str]) -> None:
    if not title.strip() or not items or any(not item.strip() for item in items):
        raise ValueError("标题和每一项内容都不能为空")
    # 内置 Helvetica 不含中文字形；本例使用 ASCII，中文 PDF 需先注册可用中文字体。
    if not title.isascii() or any(not item.isascii() for item in items):
        raise ValueError("本例仅支持 ASCII 文本；中文需先配置字体")

    page = canvas.Canvas(str(path), pagesize=A4)
    page.setTitle(title)
    page.setFont("Helvetica-Bold", 18)
    page.drawString(50, 790, title)
    page.setFont("Helvetica", 11)
    for index, item in enumerate(items, start=1):
        page.drawString(60, 790 - index * 28, f"{index}. {item}")
    page.showPage()
    page.save()


def read_pdf_report(path: Path) -> tuple[int, str]:
    reader = PdfReader(path)
    return len(reader.pages), reader.pages[0].extract_text()


def main() -> None:
    with TemporaryDirectory() as directory:
        path = Path(directory) / "study-report.pdf"
        create_pdf_report(path, "Python Study Report", ["Practice files", "Review errors"])
        pages, text = read_pdf_report(path)
        print("输入：Python Study Report，2 项内容")
        print("PDF 页数：", pages)
        print("读回文字：", " | ".join(text.splitlines()))


if __name__ == "__main__":
    main()

# 练习：增加一项内容；再尝试输入中文，观察字体检查给出的提示。
