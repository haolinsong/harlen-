"""Day21：以字节为单位读写和复制二进制文件。"""

from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory


def copy_binary(source: Path, target: Path, chunk_size: int = 8) -> None:
    """分块复制二进制文件，避免一次把大文件全部读入内存。"""
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")

    with source.open("rb") as source_file, target.open("wb") as target_file:
        while chunk := source_file.read(chunk_size):
            target_file.write(chunk)


def file_digest(path: Path) -> str:
    """返回文件内容的 SHA-256 十六进制摘要。"""
    digest = sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    with TemporaryDirectory() as directory:
        root = Path(directory)
        source = root / "source.bin"
        target = root / "copy.bin"

        # bytes 的每个元素必须是 0～255 的整数。
        # 它适合表示图片、音频等原始字节。
        source.write_bytes(bytes(range(16)) + "Python".encode("utf-8"))
        copy_binary(source, target)

        print(f"源文件大小：{source.stat().st_size} 字节")
        print(f"副本大小：{target.stat().st_size} 字节")
        print(f"内容摘要相同：{file_digest(source) == file_digest(target)}")


if __name__ == "__main__":
    main()

# 练习：把 chunk_size 改成 1、4、1024，确认复制结果是否发生变化。
