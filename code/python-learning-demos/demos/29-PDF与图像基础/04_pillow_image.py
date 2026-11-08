"""Day29：用 Pillow 创建、缩放并读回一张 PNG 图像。"""

from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image, ImageDraw


def create_color_card(path: Path, width: int = 80, height: int = 40) -> None:
    if width < 2 or height < 1:
        raise ValueError("宽度至少为 2，高度至少为 1")

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width // 2 - 1, height - 1), fill="red")
    draw.rectangle((width // 2, 0, width - 1, height - 1), fill="blue")
    # 最近邻缩放保留明确的左右色块，便于初学者观察像素变化。
    image = image.resize((width * 2, height * 2), Image.Resampling.NEAREST)
    image.save(path, format="PNG")


def read_color_card(path: Path) -> tuple[tuple[int, int], str, tuple[int, ...], tuple[int, ...]]:
    with Image.open(path) as image:
        image.load()
        return image.size, image.mode, image.getpixel((0, 0)), image.getpixel((image.width - 1, 0))


def main() -> None:
    with TemporaryDirectory() as directory:
        path = Path(directory) / "color-card.png"
        create_color_card(path)
        size, mode, left, right = read_color_card(path)
        print("输入尺寸：80 × 40")
        print("输出尺寸与模式：", size, mode)
        print("左上、右上像素：", left, right)


if __name__ == "__main__":
    main()

# 练习：将右侧改为绿色，再把缩放方式换成 BILINEAR，对比边缘像素。
