"""Day23：在 Python 对象与 JSON 文本之间转换。"""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any


def save_json(path: Path, data: dict[str, Any]) -> None:
    """把字典保存为便于人类阅读的 UTF-8 JSON 文件。"""
    with path.open("w", encoding="utf-8") as file:
        # ensure_ascii=False 保留中文；indent 让嵌套结构更易读。
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_json(path: Path) -> dict[str, Any]:
    """从 JSON 文件读取字典。"""
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, dict):
        raise ValueError("JSON 顶层必须是对象")
    return data


def main() -> None:
    profile = {
        "name": "Harlan",
        "skills": ["Python", "Java"],
        "active": True,
        "completed_days": 23,
    }

    with TemporaryDirectory() as directory:
        path = Path(directory) / "profile.json"
        save_json(path, profile)
        loaded = load_json(path)

        print("保存后的 JSON：")
        print(path.read_text(encoding="utf-8"))
        print(f"读取后仍是字典：{isinstance(loaded, dict)}")
        print(f"已完成天数：{loaded['completed_days']}")


if __name__ == "__main__":
    main()

# 练习：增加一个嵌套的 learning_plan 对象，保存后再读取其中的目标。
