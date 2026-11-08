"""Day28：用 python-docx 制作并读回学习报告。"""

from pathlib import Path
from tempfile import TemporaryDirectory

from docx import Document


def create_word_report(path: Path, topic: str, tasks: list[str]) -> None:
    if not topic.strip() or not tasks or any(not task.strip() for task in tasks):
        raise ValueError("主题和每项任务都不能为空")

    document = Document()
    document.add_heading(topic, 0)
    document.add_paragraph("本周学习任务", style="Subtitle")
    table = document.add_table(rows=1, cols=2)
    table.style = "Light Shading Accent 1"
    table.rows[0].cells[0].text = "序号"
    table.rows[0].cells[1].text = "任务"
    for number, task in enumerate(tasks, start=1):
        row = table.add_row()
        row.cells[0].text = str(number)
        row.cells[1].text = task
    # DOCX 要保存为完整文档包；只写 document.xml 并不等于可用文档。
    document.save(path)


def read_word_report(path: Path) -> tuple[str, list[str]]:
    document = Document(path)
    title = document.paragraphs[0].text
    tasks = [row.cells[1].text for row in document.tables[0].rows[1:]]
    return title, tasks


def main() -> None:
    with TemporaryDirectory() as directory:
        path = Path(directory) / "weekly-report.docx"
        create_word_report(path, "Python 学习周报", ["复习函数", "完成文件练习"])
        title, tasks = read_word_report(path)
        print("输入：Python 学习周报，2 项任务")
        print("读回标题：", title)
        print("读回任务：", tasks)


if __name__ == "__main__":
    main()

# 练习：增加一项任务，并在表格后添加一段学习总结。
