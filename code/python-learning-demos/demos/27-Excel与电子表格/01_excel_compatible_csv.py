"""Day27：生成可供电子表格软件导入的 UTF-8 CSV；CSV 不是 XLSX。"""

import csv
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory


def protect_cell(value: str) -> str:
    """降低文本被当作公式的风险；前导单引号会成为 CSV 内容。"""
    return "'" + value if value.lstrip().startswith(("=", "+", "-", "@")) else value


def export_csv(path: Path, rows: list[tuple[str, str]]) -> None:
    # utf-8-sig 写入 BOM，便于部分电子表格软件识别中文编码。
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["name", "note"])
        writer.writerows((protect_cell(name), protect_cell(note)) for name, note in rows)


def read_csv(path: Path) -> list[list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.reader(stream))


def main() -> None:
    rows = [("小明", "完成练习"), ("小红", "=1+1 不应作为公式执行")]
    with TemporaryDirectory() as directory:
        path = Path(directory) / "learning.csv"
        export_csv(path, rows)
        print("输入：", rows)
        print("读回 CSV：", read_csv(path))
        print("文件开头有 UTF-8 BOM：", path.read_bytes().startswith(b"\xef\xbb\xbf"))


if __name__ == "__main__":
    main()

# 练习：增加 hours 列，并在导入时显式转换成数字。
