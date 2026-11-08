"""Day37：安全地启动子进程，并用显式环境变量传入配置。"""

import os
import subprocess
import sys


def run_child(message: str) -> str:
    environment = os.environ.copy()
    environment["DEMO_MESSAGE"] = message
    # 参数列表不会经过 Shell 解析，避免把用户输入当作命令执行。
    completed = subprocess.run(
        [sys.executable, "-c", "import os; print(os.environ['DEMO_MESSAGE'])"],
        env=environment,
        capture_output=True,
        text=True,
        check=True,
        timeout=5,
    )
    return completed.stdout.strip()


def main() -> None:
    message = "你好，子进程"
    before = os.environ.get("DEMO_MESSAGE")
    print("父进程输入：", message)
    print("子进程输出：", run_child(message))
    print("父进程环境保持不变：", os.environ.get("DEMO_MESSAGE") == before)


if __name__ == "__main__":
    main()

# 练习：让子进程再打印自己的进程号，并与父进程的 os.getpid() 比较。
