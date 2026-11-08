"""Day28：以最小 DOCX 演示 Word 文本位于 ZIP 包的 document.xml 中。"""

from io import BytesIO
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CONTENT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"


def build_docx(paragraphs: list[str]) -> bytes:
    if not paragraphs:
        raise ValueError("至少需要一个段落")
    document = ET.Element(f"{{{WORD_NS}}}document")
    body = ET.SubElement(document, f"{{{WORD_NS}}}body")
    for value in paragraphs:
        paragraph = ET.SubElement(body, f"{{{WORD_NS}}}p")
        run = ET.SubElement(paragraph, f"{{{WORD_NS}}}r")
        ET.SubElement(run, f"{{{WORD_NS}}}t").text = value

    types = ET.Element(f"{{{CONTENT_NS}}}Types")
    ET.SubElement(types, f"{{{CONTENT_NS}}}Default", Extension="rels", ContentType="application/vnd.openxmlformats-package.relationships+xml")
    ET.SubElement(types, f"{{{CONTENT_NS}}}Default", Extension="xml", ContentType="application/xml")
    ET.SubElement(types, f"{{{CONTENT_NS}}}Override", PartName="/word/document.xml", ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml")
    relationships = ET.Element(f"{{{PKG_REL_NS}}}Relationships")
    ET.SubElement(relationships, f"{{{PKG_REL_NS}}}Relationship", Id="rId1", Type=f"{DOC_REL_NS}/officeDocument", Target="word/document.xml")

    output = BytesIO()
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", ET.tostring(types, encoding="utf-8", xml_declaration=True))
        archive.writestr("_rels/.rels", ET.tostring(relationships, encoding="utf-8", xml_declaration=True))
        archive.writestr("word/document.xml", ET.tostring(document, encoding="utf-8", xml_declaration=True))
    return output.getvalue()


def read_paragraphs(data: bytes) -> list[str]:
    with ZipFile(BytesIO(data)) as archive:
        # 只解析自己生成的可信教学文件，不处理任意来源的复杂 DOCX。
        root = ET.fromstring(archive.read("word/document.xml"))
    return [
        "".join(node.text or "" for node in paragraph.iter(f"{{{WORD_NS}}}t"))
        for paragraph in root.findall(f"{{{WORD_NS}}}body/{{{WORD_NS}}}p")
    ]


def main() -> None:
    paragraphs = ["Python 学习报告", "本周学习了文件和数据库。"]
    data = build_docx(paragraphs)
    print("输入段落：", paragraphs)
    print("生成包大小：", len(data), "字节")
    print("从 document.xml 读回：", read_paragraphs(data))


if __name__ == "__main__":
    main()

# 练习：新增第三个段落，并在 read_paragraphs 读回后核对顺序。
