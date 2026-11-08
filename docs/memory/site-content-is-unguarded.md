---
name: site-content-is-unguarded
description: Every word and figure on the landing page is hand-written and ungated (the generated repo tables were dropped 2026-10-07); re-measure figures from the tree, never copy the profile README.
metadata:
  type: project
---

# The landing page is hand-written, and nothing checks it

Until 2026-10-07 the `m`/`v` repo tables were generated from the registry by
`scripts/site-gen.py` and drift-gated; the operator dropped that section, and
the generator, its snapshot and its gates went with it (git history has them).
**Do not link a private repo**: the site is public, and that link is a public
404 — with the generator gone, nothing does this for you.

## The hand-written page

The prose and the by-the-numbers figures are typed by hand and **nothing checks
them**. Same for the "M standard & corpora" / "Editor extensions" / "Shared
foundations" tables — those repos aren't in `ecosystem.json`, so there is nothing to
project them from (the same boundary `readme-gen.py` draws for the profile README's
own Shared-foundations table).

Because nothing checks them, they rot silently: at the 2026-08-14 re-measure every
figure was low, some by more than half (3,200+ → 5,445 assertions, 1,300+ → 2,857 Go
tests, 21 → 34 repos), and the M-test row still said "MSL + VSL" months after
f-stdlib existed. (It says "MSL + VSL" again since 2026-09-08, for the opposite
reason: f-stdlib is retired. A hand-written figure is wrong in both directions
— the row was stale when the band arrived and stale again when it left.) The
same retirement left "69 modules, 579 entry points" and "three standard libraries"
on the page until 2026-11-08, two months after the band was gone.

**Re-measure, don't copy the profile README** — it is hand-written too, and its
numbers carry the same staleness. The counting method, validated against
`m-stdlib/test-results.json` (it reproduces STDARGSTST's 28 cases / 37 assertions
exactly):

| Figure | How |
|---|---|
| suites | `*TST.m` files under the three stdlibs, excluding `dist/` + `kids/` |
| test cases | `grep -c ';@TEST'` across those files |
| assertions | count of `^STDASSERT` **less** the `start^`/`report^` pair per file |
| Go tests | `^func Test[A-Z_]` in `*_test.go`, grouped by `repo.meta.json` `layer` |
| examples | files in `<stdlib>/examples/programs/`; tags = `@example` in `src/` |
| gated repos | repos whose `Makefile` has a `check:` target |
| layer-bearing | repos carrying a `layer` field in `repo.meta.json` |
| VSL drift gates | prerequisites of v-stdlib's `gates:` target |
| library modules, entry points | `modules` and the sum of each module's `labels` in `m-stdlib/dist/stdlib-manifest.json` + `v-stdlib/dist/vsl-manifest.json` (published labels only; each repo's `manifest-check` holds them to source) — 38 + 25 = 63 modules, 347 + 233 = 580 entry points on 2026-11-08 |

⚠️ **A committed measurement artifact can be stale.** `m-stdlib/test-results.json`
reports 33 suites against 43 `*TST.m` files on disk — it is one run's output, not a
census. Count the tree; use the JSON only to validate the method.

Related: the page makes **no licensing claim** while the open-core split (decided
2026-07-08) is pending attorney review — see
`docs/licensing/open-core-relicense-rollout-tracker.md` in the `docs` repo.

## The VistA Documentation Library's page and menu entry (2026-11-08)

`vdocs-library/index.html` and the Docs menu's description carry hand-written figures measured from
the published `~/data/vdocs/index.db` (read-only `sqlite3 -readonly`), and nothing checks them:

| Figure | How |
|---|---|
| listings, applications, VA catalog sections, lifecycle, format, dispositions | `v_inventory`: `count(*)`, `count(DISTINCT app_code)`, `GROUP BY section` / `app_status` / `format` / `disposition` |
| "about 6,100 documents" | listings less `disposition = 'covered-by-other-format'` (a Word + PDF pair is two listings) |
| current manuals, applications, domains, kinds, audiences | `v_documents WHERE is_latest = 1`: `count(*)`, `app_code`, `function_category`, `doc_type` grouped by `v_vocab` kind `doc_type_family`, `doc_user` |
| sections, words, figures of the current manuals | `v_sections` joined to `is_latest = 1`; `sum(word_count)`, `sum(image_count)` |
| index totals | `v_documents`, `v_sections`, `v_chunks`, `v_entities` (`GROUP BY type`), `v_inventory` counts, all versions |

**Not** the user's round numbers: "8,000+ documents, 180 applications" were offered on 2026-11-08
and measured as 9,080 listings and 197 applications (178 have an active listing). The pipeline row
is `vdocs`'s `cli/app.py:build_stages` (16 stages); the MCP tools are `src/vdocs/server/mcp.py` —
both in the vdocs project repo, which the page describes but never links (private).
