"""Day28：观察 PowerPoint 幻灯片的 XML 结构片段，不冒充完整 PPTX。"""

from io import BytesIO
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


PRESENTATION_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"


def build_slide_structure(title: str, points: list[str]) -> bytes:
    """返回教学用 ZIP；完整 PPTX 还需 presentation、master、layout 等部件。"""
    if not title.strip():
        raise ValueError("标题不能为空")
    slide = ET.Element(f"{{{PRESENTATION_NS}}}sld")
    content = ET.SubElement(slide, f"{{{PRESENTATION_NS}}}cSld")
    shapes = ET.SubElement(content, f"{{{PRESENTATION_NS}}}spTree")
    for text in [title, *points]:
        shape = ET.SubElement(shapes, f"{{{PRESENTATION_NS}}}sp")
        text_body = ET.SubElement(shape, f"{{{PRESENTATION_NS}}}txBody")
        paragraph = ET.SubElement(text_body, f"{{{DRAWING_NS}}}p")
        run = ET.SubElement(paragraph, f"{{{DRAWING_NS}}}r")
        ET.SubElement(run, f"{{{DRAWING_NS}}}t").text = text
    output = BytesIO()
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("ppt/slides/slide1.xml", ET.tostring(slide, encoding="utf-8"))
    return output.getvalue()


def read_slide_text(package: bytes) -> list[str]:
    with ZipFile(BytesIO(package)) as archive:
        root = ET.fromstring(archive.read("ppt/slides/slide1.xml"))
    return [node.text or "" for node in root.iter(f"{{{DRAWING_NS}}}t")]


def main() -> None:
    title, points = "学习进度", ["已完成 Day28", "下一步是图像和 PDF"]
    package = build_slide_structure(title, points)
    print("输入：", title, points)
    print("读回幻灯片 XML 文本：", read_slide_text(package))
    print("注意：这是结构片段，不是可在 PowerPoint 打开的完整 PPTX。")


if __name__ == "__main__":
    main()

# 练习：增加第二张 slide2.xml，并让读取函数可选择页码。
