"""Day21：使用明确的编码读写文本文件。"""

from pathlib import Path
from tempfile import TemporaryDirectory


def write_notes(path: Path, notes: list[str]) -> None:
    """覆盖写入多行笔记，并确保文件以换行符结尾。"""
    # encoding="utf-8" 让程序不依赖操作系统的默认编码。
    # with 会在代码块结束时关闭文件，即使中途发生异常也会执行清理。
    with path.open("w", encoding="utf-8") as file:
        for note in notes:
            file.write(note + "\n")


def append_note(path: Path, note: str) -> None:
    """把一条笔记追加到文件末尾，不覆盖已有内容。"""
    with path.open("a", encoding="utf-8") as file:
        file.write(note + "\n")


def read_notes(path: Path) -> list[str]:
    """读取非空行，并去掉每行结尾的换行符。"""
    with path.open("r", encoding="utf-8") as file:
        return [line.rstrip("\n") for line in file if line.strip()]


def main() -> None:
    # 临时目录会在 with 结束后自动删除，Demo 不会在项目中留下练习文件。
    with TemporaryDirectory() as directory:
        notes_path = Path(directory) / "python_notes.txt"
        write_notes(
            notes_path,
            ["文件模式 w 会覆盖旧内容", "读写文本时明确使用 UTF-8"],
        )
        append_note(notes_path, "文件模式 a 会从末尾追加")

        print(f"文件名：{notes_path.name}")
        for index, note in enumerate(read_notes(notes_path), start=1):
            print(f"{index}. {note}")


if __name__ == "__main__":
    main()

# 练习：增加 replace_note 函数，修改指定行后重新写回文件。
