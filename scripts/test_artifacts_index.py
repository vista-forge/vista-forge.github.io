"""Tests for artifacts_index: the collection page is a projection of the
folders under artifacts/, and the check fails closed."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import artifacts_index  # noqa: E402


def page(title: str, description: str | None) -> str:
    meta = f'<meta name="description" content="{description}">' if description is not None else ""
    return f"<!doctype html><html><head><title>{title}</title>{meta}</head><body></body></html>"


class ArtifactsIndexTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def add(self, folder: str, title: str, description: str | None) -> None:
        (self.root / folder).mkdir()
        (self.root / folder / "index.html").write_text(page(title, description))

    def test_lists_each_folder_by_name_with_its_title_and_description(self) -> None:
        self.add("zeta", "Zeta", "The last one.")
        self.add("alpha", "Alpha &amp; Co", "The first one.")
        entries = artifacts_index.entries(self.root)
        self.assertEqual(
            [(e.folder, e.title, e.description) for e in entries],
            [("alpha", "Alpha & Co", "The first one."), ("zeta", "Zeta", "The last one.")],
        )
        html = artifacts_index.render(entries)
        self.assertIn('<a href="alpha/">Alpha &amp; Co</a>', html)
        self.assertLess(html.index("alpha/"), html.index("zeta/"))

    def test_a_folder_without_a_page_title_or_description_is_refused(self) -> None:
        self.add("ok", "Fine", "Has both.")
        (self.root / "empty").mkdir()
        with self.assertRaisesRegex(artifacts_index.Refused, "empty/index.html"):
            artifacts_index.entries(self.root)
        (self.root / "empty").rmdir()
        self.add("untitled", "", "No title.")
        with self.assertRaisesRegex(artifacts_index.Refused, "untitled.*title"):
            artifacts_index.entries(self.root)
        (self.root / "untitled" / "index.html").write_text(page("Titled", None))
        with self.assertRaisesRegex(artifacts_index.Refused, "untitled.*description"):
            artifacts_index.entries(self.root)

    def test_check_is_red_when_the_committed_index_differs(self) -> None:
        self.add("one", "One", "The one.")
        (self.root / "index.html").write_text(artifacts_index.render(artifacts_index.entries(self.root)))
        self.assertEqual(artifacts_index.check(self.root), [])
        self.add("two", "Two", "A new one, not yet listed.")
        self.assertEqual(
            artifacts_index.check(self.root),
            ["artifacts/index.html is stale: run `make artifacts` and commit it"],
        )
        (self.root / "index.html").unlink()
        self.assertEqual(
            artifacts_index.check(self.root),
            ["artifacts/index.html is missing: run `make artifacts` and commit it"],
        )


if __name__ == "__main__":
    unittest.main()
