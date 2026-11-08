"""Day27：用 openpyxl 写入数值和公式，再读回真实 XLSX。"""

from math import isfinite
from pathlib import Path
from tempfile import TemporaryDirectory

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill


def create_study_report(path: Path, records: list[tuple[str, float]]) -> None:
    """将姓名和学习时长写入电子表格。"""
    if not records or any(not name.strip() or not isfinite(hours) or hours < 0 for name, hours in records):
        raise ValueError("至少提供一条记录；姓名不能为空，时长须为非负有限数")

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "学习时长"
    sheet.append(["姓名", "时长（小时）"])
    for name, hours in records:
        # 保留数字类型，电子表格才能继续计算，而不是把时长当作文本。
        sheet.append([name, hours])

    total_row = len(records) + 2
    sheet.cell(total_row, 1, "合计")
    sheet.cell(total_row, 2, f"=SUM(B2:B{total_row - 1})")
    for cell in sheet[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="2563EB")
    sheet.column_dimensions["A"].width = 18
    sheet.column_dimensions["B"].width = 18
    workbook.save(path)


def read_study_report(path: Path) -> tuple[list[tuple[str, float]], str]:
    """读回数据与公式；openpyxl 本身不计算公式结果。"""
    workbook = load_workbook(path, data_only=False)
    sheet = workbook["学习时长"]
    records = [(sheet.cell(row, 1).value, sheet.cell(row, 2).value) for row in range(2, sheet.max_row)]
    formula = sheet.cell(sheet.max_row, 2).value
    workbook.close()
    return records, formula


def main() -> None:
    records = [("小明", 2.5), ("小红", 3.0)]
    with TemporaryDirectory() as directory:
        path = Path(directory) / "study-report.xlsx"
        create_study_report(path, records)
        loaded, formula = read_study_report(path)
        print("输入：", records)
        print("读回：", loaded)
        print("合计公式：", formula)
        print("Python 计算的合计：", sum(hours for _, hours in loaded))
        print("说明：公式结果需由 Excel 等电子表格软件重新计算。")


if __name__ == "__main__":
    main()

# 练习：增加一名同学，并把合计公式改成计算平均时长。
