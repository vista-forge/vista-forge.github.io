# vista-forge.github.io

The VistA Forge org site — <https://vista-forge.github.io/>

A **plain static page**: no Jekyll, no Ruby, no Node, no build step. GitHub Pages
serves this repo's `main` branch at root, so a push to `main` is a deploy. The
`.nojekyll` file keeps Pages from running the content through Jekyll.

```
index.html            the whole site — one page
assets/css/site.css   all styling; no framework, no CDN
assets/img/logo.png   the org mark (see "The logo" below)
.nojekyll             serve files as-is
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

## The content is a hand-maintained copy

The page was written from the org profile README (`.github/profile/README.md`) and
**duplicates it by hand**. The profile's repo tables are generated and drift-gated
(`readme-gen.py` against `ecosystem.json`); **this page is not**. When the
profile's repo tables or the by-the-numbers figures change, this page must be
updated to match — nothing checks it for you.

## Repo links: public only

Most of the org is private. The page **links only repos that are actually public**
and lists the rest as plain text, so a visitor never hits a 404. When a repo goes
public, turn its name into a link.

Public today: `tree-sitter-m`, `vista-atlas`, `vista-compass`, and the
`ghcr.io/vista-forge/vista-iris` container image (the image is public even though
its build repo is not).

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
