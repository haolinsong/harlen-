"""Day28：用 python-pptx 创建可重新打开的双页演示文稿。"""

from pathlib import Path
from tempfile import TemporaryDirectory

from pptx import Presentation


def create_learning_deck(path: Path, title: str, points: list[str]) -> None:
    if not title.strip() or not points or any(not point.strip() for point in points):
        raise ValueError("标题和每个要点都不能为空")

    presentation = Presentation()
    cover = presentation.slides.add_slide(presentation.slide_layouts[0])
    cover.shapes.title.text = title
    cover.placeholders[1].text = "Python 学习记录"

    content = presentation.slides.add_slide(presentation.slide_layouts[1])
    content.shapes.title.text = "本周要点"
    frame = content.placeholders[1].text_frame
    frame.clear()
    for index, point in enumerate(points):
        # clear 后保留第一个段落，后续要点再增加段落，避免空白首行。
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = point
        paragraph.level = 0
    presentation.save(path)


def read_learning_deck(path: Path) -> tuple[str, list[str]]:
    presentation = Presentation(path)
    title = presentation.slides[0].shapes.title.text
    frame = presentation.slides[1].placeholders[1].text_frame
    return title, [paragraph.text for paragraph in frame.paragraphs]


def main() -> None:
    with TemporaryDirectory() as directory:
        path = Path(directory) / "learning-deck.pptx"
        create_learning_deck(path, "文件处理", ["先验证输入", "再保存文件"])
        title, points = read_learning_deck(path)
        print("输入：文件处理，2 个要点")
        print("读回封面：", title)
        print("读回要点：", points)


if __name__ == "__main__":
    main()

# 练习：添加第三个要点，再尝试增加一页“下周计划”。
