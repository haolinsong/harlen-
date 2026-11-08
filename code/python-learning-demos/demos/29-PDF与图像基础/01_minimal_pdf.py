"""Day29：用标准库生成一页最小 PDF，认识对象、偏移表和结束标记。"""

from pathlib import Path
from tempfile import TemporaryDirectory


def build_pdf(text: str) -> bytes:
    """仅演示 ASCII 与内置 Helvetica；中文排版需要嵌入字体及更高层工具。"""
    if not text or not text.isascii():
        raise ValueError("这个最小示例只接受非空 ASCII 文本")
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    contents = f"BT /F1 24 Tf 72 750 Td ({escaped}) Tj ET\n".encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(contents)).encode("ascii") + b" >>\nstream\n" + contents + b"endstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    output = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for number, body in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode("ascii") + body + b"\nendobj\n")
    xref_offset = len(output)
    output.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode("ascii"))
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return bytes(output)


def main() -> None:
    with TemporaryDirectory() as directory:
        path = Path(directory) / "hello.pdf"
        path.write_bytes(build_pdf("Python Day29"))
        print("输入文字：Python Day29")
        print("PDF 文件头：", path.read_bytes()[:8])
        print("文件大小：", path.stat().st_size, "字节")
    print("临时 PDF 已自动清理。")


if __name__ == "__main__":
    main()

# 练习：修改字号与坐标，重新生成后观察页面布局变化。
