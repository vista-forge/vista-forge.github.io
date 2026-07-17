# vista-forge.github.io

The VistA Forge org site — <https://vista-forge.github.io/>

A **plain static page**: no Jekyll, no Ruby, no Node, no build step. GitHub Pages
serves this repo's `main` branch at root, so a push to `main` is a deploy. The
`.nojekyll` file keeps Pages from running the content through Jekyll.

```
index.html            the whole site — one page
assets/css/site.css   all styling; no framework, no CDN
assets/img/logo.png   the org mark (see "The logo" below)
scripts/site-gen.py   generates the m/v repo tables from the ecosystem registry
data/repos.json       the committed registry snapshot the tables render from
.nojekyll             serve files as-is
```

## Gates

```
make site-check       offline, no secrets — the CI gate on every push
make site-sync        HOST-ONLY — re-harvest the org and rewrite the tables
make site-freshness   HOST-ONLY — is the snapshot stale vs the live org?
```

## Editing

Open `index.html` and edit. To preview, open the file in a browser directly, or
serve the directory (`python3 -m http.server`) if you want paths to resolve the
same way they do in production.

The palette is **semantic, not decorative** — keep the mapping intact when adding
sections:

| Token | Means |
|---|---|
| `--ember` | the `v` layer — VistA-specific |
| `--cyan` | the `m` layer — engine-neutral |

Both light and dark themes are supported via `prefers-color-scheme`; a change to
one needs a check against the other.

## What is generated, and what is not

**Generated — do not hand-edit.** The `m` and `v` repo tables live between
`<!-- gen:begin block=repos-m -->` / `<!-- gen:end -->` markers and are owned by
`scripts/site-gen.py`. They are a projection of the same source the org profile
README projects: `ecosystem.json` (registry membership + layer) + each repo's
committed `repo.meta.json` `role` + its latest version tag + **its visibility**.
Editing a block by hand is drift, and `make site-check` red-gates it.

**Hand-written — keep it honest yourself.** Everything else: the prose, the
by-the-numbers figures, and the "M standard & corpora" / "Editor extensions" /
"Shared foundations" tables (those repos are not in the registry, so there is
nothing to project them from — the same boundary `readme-gen.py` draws for the
profile README).

### Why two tiers of gate

The registry and the roles are in **private** repos, so harvesting them needs a
token with org-wide `contents:read`. `.github` can hold one (`META_GATE_TOKEN`)
because `.github` is private. **This repo is public**, where that token's blast
radius is far larger than the gate is worth. So:

| Tier | Command | Network | Catches |
|---|---|---|---|
| 1 | `make site-check` | none — **runs in CI** | a hand-edited generated block |
| 2 | `make site-freshness` | live `gh` — **host-only** | a stale snapshot (new tag, repo gone public) |

Tier 1 alone would let `data/repos.json` rot; tier 2 alone can't run in a public
repo's CI. Together, the HTML can't drift from the snapshot and the snapshot can't
drift from the org for longer than it takes to run `make site-sync`.

## Repo links: public only, mechanically

Most of the org is private, and a link to a private repo is a **public 404**. So a
repo's name is emitted as a link **only when it is actually public**, and as plain
text otherwise. This is not a rule to remember — `site-gen.py` harvests visibility,
so a re-harvest links a repo the moment it goes public, and nothing links it
before. Run `make site-sync` after any repo flips.

Public today: `tree-sitter-m`, `vista-atlas`, `vista-compass`, and the
`ghcr.io/vista-forge/vista-iris` container image (the image is public even though
its build repo is not). Every repo in the registry is currently private, so the
generated tables emit no links at all.

## The logo

`assets/img/logo.png` is the org avatar, used **unmodified, on its white plate** —
rounded and ringed by CSS (`.logo-tile`, `.brand__mark`) so it reads as a product
mark.

It is deliberately **not** background-removed. The mark is a 3D render whose
brightest chrome facets are the same pure white as its backdrop and connect to it,
so every automated knockout either leaves the drop shadow behind or eats notches
out of the V's bevels. If a transparent version is ever wanted, re-export it from
the original render with an alpha channel rather than post-processing this PNG.
See `docs/memory/org-logo-treatment.md`.

## Licensing

The page makes **no licensing claim**, by decision: the open-core split (`m-*`
Apache / `v-*` AGPL + commercial, decided 2026-07-08) is still pending attorney
review, and each repo's `LICENSE` is the source of truth in the meantime. Revisit
once `docs/licensing/open-core-relicense-rollout-tracker.md` lands in the `docs`
repo.
