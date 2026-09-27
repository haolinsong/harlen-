"""列出并运行 demos 目录中的学习示例。"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent
DEMOS_ROOT = PROJECT_ROOT / "demos"


def discover_demos() -> list[Path]:
    """返回按路径排序的 Demo 脚本，不把辅助模块当成独立 Demo。"""
    # 目录名采用“序号-主题”，列表输出时不打开文件也能知道每组学什么。
    return sorted(DEMOS_ROOT.glob("[0-9][0-9]-*/[0-9][0-9]_*.py"))


def display_name(path: Path) -> str:
    """把绝对路径转换成适合复制到命令中的相对路径。"""
    return path.relative_to(DEMOS_ROOT).as_posix()


def select_demo(selector: str, demos: list[Path]) -> Path:
    """按完整相对路径或唯一的路径片段选择 Demo。"""
    normalized = selector.replace("\\", "/")
    exact_matches = [path for path in demos if display_name(path) == normalized]
    if exact_matches:
        return exact_matches[0]

    partial_matches = [path for path in demos if normalized in display_name(path)]
    if len(partial_matches) == 1:
        return partial_matches[0]
    if not partial_matches:
        raise ValueError(f"没有找到 Demo：{selector}")

    candidates = "\n".join(f"  - {display_name(path)}" for path in partial_matches)
    raise ValueError(f"匹配到多个 Demo，请提供更完整的路径：\n{candidates}")


def run_demo(path: Path) -> int:
    """使用当前 Python 解释器运行脚本，并返回进程退出码。"""
    # flush=True 保证标题先于子进程输出显示，重定向终端时也不会错序。
    print(f"\n{'=' * 72}\n运行 {display_name(path)}\n{'=' * 72}", flush=True)
    completed = subprocess.run([sys.executable, str(path)], cwd=PROJECT_ROOT, check=False)
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="列出或运行 Python 学习 Demo")
    parser.add_argument("selector", nargs="?", help="Demo 相对路径或唯一的路径片段")
    parser.add_argument("--list", action="store_true", help="列出全部 Demo")
    parser.add_argument("--all", action="store_true", help="依次运行全部 Demo")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    demos = discover_demos()

    if args.list:
        for path in demos:
            print(display_name(path))
        print(f"\n共 {len(demos)} 个 Demo")
        return 0

    if args.all:
        failed: list[str] = []
        for path in demos:
            if run_demo(path) != 0:
                failed.append(display_name(path))
        if failed:
            print("\n以下 Demo 运行失败：")
            for name in failed:
                print(f"  - {name}")
            return 1
        print(f"\n全部 {len(demos)} 个 Demo 运行成功。")
        return 0

    if not args.selector:
        print("请传入 Demo 路径，或使用 --list / --all。")
        return 2

    try:
        selected = select_demo(args.selector, demos)
    except ValueError as error:
        print(error)
        return 2
    return run_demo(selected)


if __name__ == "__main__":
    raise SystemExit(main())
