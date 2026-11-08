"""Day22：理解上下文管理器如何保证资源被释放。"""

from pathlib import Path
from tempfile import TemporaryDirectory
from types import TracebackType


class ManagedTextFile:
    """教学用上下文管理器：进入时打开文件，退出时关闭文件。"""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.file = None

    def __enter__(self):
        print("进入 with：打开文件")
        self.file = self.path.open("w", encoding="utf-8")
        return self.file

    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        print("离开 with：关闭文件")
        if self.file is not None:
            self.file.close()
        # 返回 False 表示不吞掉异常，调用方仍然能看到真正的问题。
        return False


def main() -> None:
    with TemporaryDirectory() as directory:
        path = Path(directory) / "message.txt"
        with ManagedTextFile(path) as file:
            file.write("上下文管理器会负责清理资源。\n")
            print(f"with 内文件是否关闭：{file.closed}")

        print(f"with 外文件是否关闭：{file.closed}")
        print(f"文件内容：{path.read_text(encoding='utf-8').strip()}")


if __name__ == "__main__":
    main()

# 练习：在 with 内主动抛出 ValueError，确认 __exit__ 仍会关闭文件。
