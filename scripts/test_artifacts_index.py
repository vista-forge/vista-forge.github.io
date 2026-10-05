"""Tests for artifacts_index: each collection page (artifacts/, prototypes/) is
a projection of the folders under it, and the check fails closed."""

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
        html = artifacts_index.render(entries, artifacts_index.ARTIFACTS)
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

    def test_the_title_is_the_pages_own_not_a_drawings(self) -> None:
        drawing = '<svg role="img"><title>Proposed architecture</title><desc>Boxes.</desc></svg>'
        (self.root / "plan").mkdir()
        (self.root / "plan" / "index.html").write_text(
            page("The Plan", "A page with a drawing in it.").replace("<body>", "<body>" + drawing)
        )
        self.assertEqual([e.title for e in artifacts_index.entries(self.root)], ["The Plan"])
        # A drawing's title never stands in for a missing page title.
        (self.root / "plan" / "index.html").write_text(
            page("", "Only the drawing is titled.").replace("<body>", "<body>" + drawing)
        )
        with self.assertRaisesRegex(artifacts_index.Refused, "plan.*title"):
            artifacts_index.entries(self.root)

    def test_check_is_red_when_the_committed_index_differs(self) -> None:
        c = artifacts_index.ARTIFACTS
        self.add("one", "One", "The one.")
        (self.root / "index.html").write_text(artifacts_index.render(artifacts_index.entries(self.root), c))
        self.assertEqual(artifacts_index.check(self.root, c), [])
        self.add("two", "Two", "A new one, not yet listed.")
        self.assertEqual(
            artifacts_index.check(self.root, c),
            ["artifacts/index.html is stale: run `make artifacts` and commit it"],
        )
        (self.root / "index.html").unlink()
        self.assertEqual(
            artifacts_index.check(self.root, c),
            ["artifacts/index.html is missing: run `make artifacts` and commit it"],
        )

    def test_each_collection_page_names_its_own_collection(self) -> None:
        self.add("one", "One", "The one.")
        listed = artifacts_index.entries(self.root)
        html = artifacts_index.render(listed, artifacts_index.PROTOTYPES)
        self.assertIn("<title>Prototypes · vista-forge</title>", html)
        self.assertIn("<h1>Prototypes</h1>", html)
        self.assertNotIn("Artifacts", html)
        (self.root / "index.html").write_text(artifacts_index.render(listed, artifacts_index.ARTIFACTS))
        # the artifacts page is not the prototypes page, though it lists the same folders
        self.assertEqual(
            artifacts_index.check(self.root, artifacts_index.PROTOTYPES),
            ["prototypes/index.html is stale: run `make artifacts` and commit it"],
        )

    def test_a_collection_folder_that_is_gone_is_refused(self) -> None:
        with self.assertRaisesRegex(artifacts_index.Refused, "nowhere/ is missing"):
            artifacts_index.entries(self.root / "nowhere")

    def test_the_site_has_a_folder_for_every_collection(self) -> None:
        self.assertEqual([c.folder for c in artifacts_index.COLLECTIONS], ["artifacts", "prototypes"])
        for c in artifacts_index.COLLECTIONS:
            self.assertTrue((artifacts_index.SITE / c.folder).is_dir(), c.folder)


if __name__ == "__main__":
    unittest.main()
