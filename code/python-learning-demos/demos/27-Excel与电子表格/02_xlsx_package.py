"""Day27：用标准库观察最小 XLSX 的 ZIP/XML 结构，而非代替 openpyxl。"""

from io import BytesIO
from xml.etree import ElementTree as ET
from zipfile import ZIP_DEFLATED, ZipFile


SHEET_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CONTENT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"


def xml_bytes(element: ET.Element) -> bytes:
    return ET.tostring(element, encoding="utf-8", xml_declaration=True)


def build_xlsx(rows: list[list[str]]) -> bytes:
    """创建只含一张工作表、只含文本单元格的教学版 XLSX。"""
    if not rows or any(not row or len(row) > 26 for row in rows):
        raise ValueError("至少一行；每行应有 1～26 个文本单元格")

    types = ET.Element(f"{{{CONTENT_NS}}}Types")
    ET.SubElement(types, f"{{{CONTENT_NS}}}Default", Extension="rels", ContentType="application/vnd.openxmlformats-package.relationships+xml")
    ET.SubElement(types, f"{{{CONTENT_NS}}}Default", Extension="xml", ContentType="application/xml")
    ET.SubElement(types, f"{{{CONTENT_NS}}}Override", PartName="/xl/workbook.xml", ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml")
    ET.SubElement(types, f"{{{CONTENT_NS}}}Override", PartName="/xl/worksheets/sheet1.xml", ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml")

    root_rels = ET.Element(f"{{{PKG_REL_NS}}}Relationships")
    ET.SubElement(root_rels, f"{{{PKG_REL_NS}}}Relationship", Id="rId1", Type=f"{DOC_REL_NS}/officeDocument", Target="xl/workbook.xml")
    workbook = ET.Element(f"{{{SHEET_NS}}}workbook")
    sheets = ET.SubElement(workbook, f"{{{SHEET_NS}}}sheets")
    ET.SubElement(sheets, f"{{{SHEET_NS}}}sheet", name="学习记录", sheetId="1", attrib={f"{{{DOC_REL_NS}}}id": "rId1"})
    workbook_rels = ET.Element(f"{{{PKG_REL_NS}}}Relationships")
    ET.SubElement(workbook_rels, f"{{{PKG_REL_NS}}}Relationship", Id="rId1", Type=f"{DOC_REL_NS}/worksheet", Target="worksheets/sheet1.xml")

    worksheet = ET.Element(f"{{{SHEET_NS}}}worksheet")
    sheet_data = ET.SubElement(worksheet, f"{{{SHEET_NS}}}sheetData")
    for row_number, values in enumerate(rows, start=1):
        row = ET.SubElement(sheet_data, f"{{{SHEET_NS}}}row", r=str(row_number))
        for column, value in enumerate(values):
            cell = ET.SubElement(row, f"{{{SHEET_NS}}}c", r=f"{chr(65 + column)}{row_number}", t="inlineStr")
            inline = ET.SubElement(cell, f"{{{SHEET_NS}}}is")
            ET.SubElement(inline, f"{{{SHEET_NS}}}t").text = value

    # XLSX 是一组有关联的 XML 部件，而不是把 CSV 改名为 .xlsx。
    stream = BytesIO()
    with ZipFile(stream, "w", compression=ZIP_DEFLATED) as archive:
        for name, part in {
            "[Content_Types].xml": types,
            "_rels/.rels": root_rels,
            "xl/workbook.xml": workbook,
            "xl/_rels/workbook.xml.rels": workbook_rels,
            "xl/worksheets/sheet1.xml": worksheet,
        }.items():
            archive.writestr(name, xml_bytes(part))
    return stream.getvalue()


def read_first_sheet(data: bytes) -> list[list[str]]:
    with ZipFile(BytesIO(data)) as archive:
        # 此函数只读自己生成的可信示例，不作为不可信 XLSX 的通用解析器。
        root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    return [
        [cell.findtext(f"{{{SHEET_NS}}}is/{{{SHEET_NS}}}t", default="") for cell in row]
        for row in root.findall(f"{{{SHEET_NS}}}sheetData/{{{SHEET_NS}}}row")
    ]


def main() -> None:
    rows = [["姓名", "时长"], ["小明", "2.5"]]
    data = build_xlsx(rows)
    with ZipFile(BytesIO(data)) as archive:
        print("输入：", rows)
        print("XLSX 内部文件：", archive.namelist())
    print("读回首张工作表：", read_first_sheet(data))


if __name__ == "__main__":
    main()

# 练习：把时长单元格改为数值类型，并观察 XML 中的区别。
