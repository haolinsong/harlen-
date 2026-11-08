"""Day21：使用 pathlib 组合、创建和查找路径。"""

from pathlib import Path
from tempfile import TemporaryDirectory


def find_python_files(root: Path) -> list[str]:
    """递归查找 Python 文件，并返回便于显示的相对路径。"""
    # rglob 会遍历所有子目录。
    # 返回相对路径可避免结果绑定某台电脑的绝对路径。
    return sorted(path.relative_to(root).as_posix() for path in root.rglob("*.py"))


def main() -> None:
    with TemporaryDirectory() as directory:
        project = Path(directory) / "demo_project"
        source_directory = project / "src" / "tools"
        source_directory.mkdir(parents=True)

        (project / "README.md").write_text("# 示例项目\n", encoding="utf-8")
        (project / "src" / "app.py").write_text("print('app')\n", encoding="utf-8")
        (source_directory / "helper.py").write_text("VALUE = 42\n", encoding="utf-8")

        app_path = project / "src" / "app.py"
        print(f"文件名：{app_path.name}")
        print(f"不带扩展名：{app_path.stem}")
        print(f"扩展名：{app_path.suffix}")
        print(f"父目录名：{app_path.parent.name}")
        print(f"找到的 Python 文件：{find_python_files(project)}")


if __name__ == "__main__":
    main()

# 练习：再创建一个 tests/test_app.py，观察递归查找结果的排序。
