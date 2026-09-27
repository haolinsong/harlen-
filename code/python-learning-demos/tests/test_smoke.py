"""逐个启动 Demo，确保所有示例都能独立运行。"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEMOS_ROOT = PROJECT_ROOT / "demos"


class DemoSmokeTest(unittest.TestCase):
    def test_every_demo_exits_successfully(self) -> None:
        demos = sorted(DEMOS_ROOT.glob("[0-9][0-9]-*/[0-9][0-9]_*.py"))
        self.assertGreaterEqual(len(demos), 40, "Demo 数量异常，可能有文件未被发现")

        failures: list[str] = []
        for demo in demos:
            completed = subprocess.run(
                [sys.executable, str(demo)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            if completed.returncode != 0:
                relative = demo.relative_to(PROJECT_ROOT)
                failures.append(f"{relative}\n{completed.stderr}")

        self.assertEqual(failures, [], "\n\n".join(failures))


if __name__ == "__main__":
    unittest.main()
