---
name: site-content-is-unguarded
description: The site's m/v repo tables are generated + drift-gated from ecosystem.json; the prose and the by-the-numbers figures are still hand-written and ungated. Know which half you're editing.
metadata:
  type: project
---

# Half the landing page is gated. Know which half.

## Generated — `scripts/site-gen.py` owns it

The `m` and `v` repo tables in `index.html` sit between
`<!-- gen:begin block=repos-m -->` / `<!-- gen:end -->` and are a projection of
the same source the org profile README projects: `ecosystem.json` (membership +
layer) + each repo's committed `repo.meta.json` `role` + latest version tag +
**visibility**. Hand-editing a block is drift; `make site-check` red-gates it.

**Visibility is part of the projection on purpose.** The site is public and most
of the org is not, so a link to a private repo is a public 404. The generator
emits a link only for a public repo and plain text otherwise — so "link it when it
goes public" is mechanical, not a thing anyone has to remember. Run
`make site-sync` after a repo flips.

## The two-tier gate — and why it is two

The registry and the roles live in **private** repos; harvesting them needs
org-wide `contents:read`. `.github` holds such a PAT (`META_GATE_TOKEN`) because
`.github` is private. **This repo is public** — an org-wide read token in its
Actions secrets is a far bigger blast radius than the gate is worth. So the
harvest and the check are split:

| Tier | Command | Network | Catches |
|---|---|---|---|
| 1 | `make site-check` | none — runs in CI | a hand-edited generated block |
| 2 | `make site-freshness` | live `gh` — host-only | a stale snapshot (new tag, repo gone public) |

Tier 1 alone lets `data/repos.json` rot; tier 2 alone can't run here. **If the site
repo ever goes private, collapse them** — a single live `--check` in CI is simpler
and strictly better once the token is safe to hold.

The snapshot deliberately carries **no harvest timestamp**: a timestamp would churn
every run and make a real diff invisible among the noise.

## Still ungated — the hand-written half

The prose, and the by-the-numbers figures (64 suites · 1,400+ cases · 3,200+
assertions · 1,300+ Go tests · 21 gated repos · 24 VSL drift gates), are typed by
hand from the profile README and **nothing checks them**. Same for the "M standard
& corpora" / "Editor extensions" / "Shared foundations" tables — those repos aren't
in `ecosystem.json`, so there is nothing to project them from (the same boundary
`readme-gen.py` draws for the profile README's own Shared-foundations table).

## Proof the generation was worth it

The first live harvest (2026-07-16) immediately caught real drift: **m-driver-sdk
was `v0.11.0` live while both the hand-copy and `profile/README.md` said
`v0.9.0`.** The profile's own generated block was stale — i.e. `make profile-sync`
had not been run in `.github` since the tag. If the site's tables and the profile's
disagree, suspect the profile is stale before assuming the site is.

Related: the page makes **no licensing claim** while the open-core split (decided
2026-07-08) is pending attorney review — see
`docs/licensing/open-core-relicense-rollout-tracker.md` in the `docs` repo.
