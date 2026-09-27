"""Day01：认识当前正在使用的 Python 解释器。"""

import platform
import sys


def main() -> None:
    # sys.version 包含完整版本和编译信息，排查环境问题时很有用。
    print("Python 完整版本：")
    print(sys.version)

    # sys.executable 是当前解释器的真实路径。
    # 一台电脑可能同时安装多个 Python，这个值能告诉你到底运行了哪一个。
    print(f"\n解释器路径：{sys.executable}")
    print(f"Python 实现：{platform.python_implementation()}")
    print(f"操作系统：{platform.system()} {platform.release()}")

    major, minor, micro = sys.version_info[:3]
    print(f"拆分后的版本号：major={major}, minor={minor}, micro={micro}")


if __name__ == "__main__":
    # 只有直接运行当前文件时才调用 main；被别的模块导入时不会自动执行。
    main()

# 练习：再打印 platform.machine()，观察当前电脑的 CPU 架构。
