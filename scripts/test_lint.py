"""回归检查：安装 Skill/工具依赖后，外部文档不能冒充知识库链接目标。"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class LinkScopeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="harlan-lint-")
        self.addCleanup(self.temp.cleanup)
        self.vault = Path(self.temp.name)
        for directory in (
            "raw/assets", "raw/personal", "wiki/sources", "wiki/concepts",
            "wiki/howto", "wiki/entities", "outputs", "scripts",
        ):
            (self.vault / directory).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(
            Path(__file__).with_name("lint.py"), self.vault / "scripts/lint.py"
        )
        self.write("wiki/index.md", self.page("index") + "\n- [[测试输出]]\n")
        self.write("wiki/log.md", self.page("log"))
        self.write("outputs/测试输出.md", self.page("output") + "\n[[正文页面]]\n")

    @staticmethod
    def page(kind):
        return (
            "---\ntitle: 测试\ntype: " + kind + "\ntags: []\n"
            "aliases: []\nrelated: []\nsources: []\n"
            "created: 2026-10-01\nupdated: 2026-10-01\n---\n"
        )

    def write(self, name, content):
        path = self.vault / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def lint(self):
        return subprocess.run(
            [sys.executable, str(self.vault / "scripts/lint.py")],
            capture_output=True, text=True, check=False,
        )

    def test_missing_page_is_broken(self):
        result = self.lint()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("断链: [[正文页面]]", result.stdout)

    def test_skill_and_dependency_docs_cannot_satisfy_links(self):
        for prefix in (".agents/skills/example", "scripts/node_modules/example", ".codex"):
            with self.subTest(prefix=prefix):
                self.write(prefix + "/正文页面.md", "仅用于工具的示例")
                result = self.lint()
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("断链: [[正文页面]]", result.stdout)

    def test_real_knowledge_page_satisfies_link(self):
        self.write("wiki/concepts/正文页面.md", self.page("concept") + "真实知识")
        self.write(
            "wiki/index.md",
            self.page("index") + "\n- [[测试输出]]\n- [[正文页面]]\n",
        )
        result = self.lint()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("断链:", result.stdout)


if __name__ == "__main__":
    unittest.main()
