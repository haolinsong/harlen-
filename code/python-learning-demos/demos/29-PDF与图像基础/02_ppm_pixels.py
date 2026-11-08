"""Day29：用无依赖 PPM 图像理解像素与最近邻缩放。"""

from pathlib import Path
from tempfile import TemporaryDirectory


Pixel = tuple[int, int, int]


def resize_nearest(pixels: list[list[Pixel]], new_width: int, new_height: int) -> list[list[Pixel]]:
    if not pixels or not pixels[0] or new_width <= 0 or new_height <= 0:
        raise ValueError("图像和目标尺寸必须非空且为正")
    if any(len(row) != len(pixels[0]) for row in pixels):
        raise ValueError("所有像素行长度必须相同")
    old_height, old_width = len(pixels), len(pixels[0])
    # 最近邻法直接取源图对应位置；易理解，但放大后会出现明显色块。
    return [
        [pixels[y * old_height // new_height][x * old_width // new_width] for x in range(new_width)]
        for y in range(new_height)
    ]


def write_ppm(path: Path, pixels: list[list[Pixel]]) -> None:
    if not pixels or not pixels[0] or any(len(row) != len(pixels[0]) for row in pixels):
        raise ValueError("像素必须组成非空矩形")
    channels = [channel for row in pixels for pixel in row for channel in pixel]
    if any(not 0 <= channel <= 255 for channel in channels):
        raise ValueError("颜色通道必须在 0～255 之间")
    header = f"P6\n{len(pixels[0])} {len(pixels)}\n255\n".encode("ascii")
    path.write_bytes(header + bytes(channels))


def main() -> None:
    source = [[(255, 0, 0), (0, 255, 0)], [(0, 0, 255), (255, 255, 255)]]
    enlarged = resize_nearest(source, 4, 4)
    with TemporaryDirectory() as directory:
        path = Path(directory) / "pixels.ppm"
        write_ppm(path, enlarged)
        print("输入：2×2 像素；输出：4×4 像素")
        print("左上角像素：", enlarged[0][0])
        print("PPM 文件头：", path.read_bytes().split(b"\n", 3)[:3])
    print("Pillow 可处理 PNG/JPEG 等常见格式；此示例不需要安装它。")


if __name__ == "__main__":
    main()

# 练习：实现灰度变换，再写出另一张 PPM 图像。
