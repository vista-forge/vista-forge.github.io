---
name: site-content-is-unguarded
description: The landing page hand-duplicates the generated org-profile README and links only public repos — both facts drift silently, with no gate.
metadata:
  type: project
---

# The site's content is a hand-copy, and nothing gates it

Two standing hazards in `index.html`, both invisible until someone notices the
site is wrong.

## 1. The repo tables and the numbers are duplicated by hand

`.github/profile/README.md` is the source the page was written from. Its repo
tables are **generated and drift-gated** — `scripts/readme-gen.py --check` renders
them from `ecosystem.json` + each repo's `repo.meta.json` `role` + latest tag, and
red-gates staleness (`make profile-check`, plus the scheduled meta-gate).

**The site gets none of that.** Its tables, the by-the-numbers figures (64 suites ·
1,400+ cases · 3,200+ assertions · 1,300+ Go tests · 21 gated repos · 24 VSL drift
gates), and the version tags are hand-typed. When the profile regenerates, the site
does not, and no gate says so.

If the copy becomes a maintenance problem, the org's own discipline is the answer —
`source-tag → generate → registry → red-gate`: render the site's tables from
`ecosystem.json` into `gen:begin/gen:end` blocks with a `--check` mode, the same
shape `readme-gen.py` already implements. That was considered and deliberately
deferred at build time (2026-07-16) to keep the first pass simple.

## 2. Links are public-only, on purpose

At build time **23 of the 27 repos the profile README links were private**; the org
is on a free plan. A public site that links them serves 404s. So the page links
**only** what is actually public and lists everything else as plain text.

Public then: `tree-sitter-m`, `vista-atlas`, `vista-compass`, and — note the
asymmetry — the **`ghcr.io/vista-forge/vista-iris` container image is public even
though its build repo is private**, which is why the hero can offer a working
`docker pull` at all.

**When a repo goes public, link it.** Don't link ahead of the flip: an
optimistically-added link is a public 404. Check with
`gh api repos/vista-forge/<name> --jq .visibility` rather than assuming.

Related: the page deliberately makes **no licensing claim** while the open-core
split (decided 2026-07-08) is pending attorney review — see
`docs/licensing/open-core-relicense-rollout-tracker.md` in the `docs` repo.
