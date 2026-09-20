# vista-forge.github.io

The VistA Forge org site — <https://vista-forge.github.io/>

A **plain static page**: no Jekyll, no Ruby, no Node, no build step. GitHub Pages
serves this repo's `main` branch at root, so a push to `main` is a deploy. The
`.nojekyll` file keeps Pages from running the content through Jekyll.

```
index.html            the banner, the landing content, and the frame shell
assets/css/site.css   all styling; no framework, no CDN
assets/img/logo.png   the org mark (see "The logo" below)
scripts/site-gen.py   generates the m/v repo tables from the ecosystem registry
data/repos.json       the committed registry snapshot the tables render from
.nojekyll             serve files as-is  ⚠️ load-bearing: Astro's _astro/ dies without it
forge-docs/           DEPLOYED ARTIFACT — do not hand-edit
```

## One address, two views

The banner is permanent. Everything under it is one of two views, chosen by the
**hash route** — never by navigating away, so the address bar always reads
`vista-forge.github.io`, the back button steps one view at a time, and any view
can be linked to:

| Route | What shows |
|---|---|
| `#/architecture` (the default) | the landing content, in the page itself |
| `#/architecture/<section>` | the same, scrolled to that section, fold opened |
| `#/explore/vdb-explorer` | the dd-bundle browser, in a frame |
| `#/explore/cprs-configuration` | the CPRS configuration dashboard, in a frame |
| `#/docs/forge-reference` | the generated `m`/`v` surface reference, in a frame |
| `#<section>` | a bare legacy anchor — read as `#/architecture/<section>` |

That last row is load-bearing: the published reference's own nav links back here
with bare anchors (`#repos`, `#stack`), and so do older links. They keep working.

**The landing content is still in `index.html`, not in a frame.** Only the three
applications are framed. Two reasons, and both are the point: the page a crawler
and a reader get at the root URL is the same document it always was, and
`site-gen.py`'s generated repo tables stay where the gate looks for them.

### The frames

The three applications are served from the project's own machine over a public
Tailscale Funnel (`minty.warg-torino.ts.net`), and are shown under this banner
rather than linked away to theirs. Consequences worth knowing before changing
anything here:

* **A new frame is built for every view, never `iframe.src = …` on a live one.**
  Re-pointing a frame that has already loaded pushes a session-history entry, so
  the reader's next Back press undoes the *frame's* navigation instead of
  returning to the view they came from. The first load of a freshly inserted
  frame replaces instead of pushing. Measured here; it is not the obvious
  one-liner.
* **Nothing sits between the banner and the application.** The framed view has
  no strip of its own: the banner already says which view this is and the
  application says its own name, so a bar repeating both was chrome charged
  against the thing it framed. A word appears over the empty frame while it
  loads, and a notice appears only when something is wrong.
* **The wait is bounded, and names WHICH failure.** A cross-origin frame reports
  neither success nor failure to the page around it, so the two are told apart
  by asking the frame whether it ever navigated: a frame that has not is still
  this page's own `about:blank` and its location reads back; once the
  cross-origin document commits, the same read throws. Still same-origin after
  6 s means the browser refused to send the request (see below); navigated but
  unfinished after 20 s means the host is slow or down. Both carry the direct
  link. A timeout alone blames the wrong party — it did, on the first day.
* ⚠️ **From inside the tailnet, the frames do not load, and nothing here can fix
  that.** `minty.warg-torino.ts.net` resolves to a tailnet address on this
  network and to Tailscale's public ingress everywhere else, and a page served
  from the public internet may not embed a host that resolves to a private
  address. The operator is the only reader affected — which also means a result
  from this box is not evidence about the published site. Measured, with the
  four alternatives ruled out, in
  `docs/memory/a-tailnet-published-origin-cannot-be-embedded.md`.
* **A cross-origin frame cannot be styled or read from here**, so anything the
  framed page must do differently is the framed page's own job. The reference
  used to render its own copy of this banner directly under it; since
  2026-09-19 it detects being framed (`window.self !== window.top`, pre-paint)
  and hides its banner entirely, having first moved its search box and its
  theme control into a left rail that also carries the page's headings and the
  site tree. Under this banner it is two panes and nothing else. That is a
  change in the `forge-docs` repo and a republish, never an edit to the
  deployed copy here.
* **The light/dark choice does not cross the origin boundary**, because
  `localStorage` is per-origin. The framed reference is on its own default
  until the reader uses the control in its rail — which is why that control had
  to survive the move rather than go with the banner.
* **Nothing here sets `X-Frame-Options` or a `frame-ancestors` policy**, on
  either side. If the publish origin ever grows one, these views go blank.

Without JavaScript the landing page is unchanged, the menus fall back to
hover/focus, and a `<noscript>` note links the three applications directly.

## `forge-docs/` — a deployed copy, not source

That directory is the built `v` surface reference, served at
<https://vista-forge.github.io/forge-docs/>. It is **generated in the
`forge-docs` repo and copied here**; nothing in this repo produces it and
no gate here grades it. To refresh it, follow that repo's
`docs/guides/publishing.md` — never edit these files in place.

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

**Light is the default; dark is an explicit opt-in** via the header toggle
(2026-08-30 — it was the other way round from 2026-08-14). Neither is inferred
from `prefers-color-scheme`: the choice is the reader's, persisted in
`localStorage` and applied pre-paint by an inline script on every page. The
light values live on bare `:root` and the dark ones under
`:root[data-theme="dark"]`, so a change to one needs a check against the other.

Dark is **dark, not black**. The ground was `#000` with the elevated surfaces
barely above it, which made every card edge a hairline against a void; the ramp
now starts one step up, at the same hue and saturation.

### The palette is restated in `forge-docs`

The reference site is a wing of this one and wears the same chrome, but it is a
separate deployment built by Starlight — there is no shared stylesheet, and a
`<link>` across origins would be an off-host load its `offline-check` forbids.
So the same token values are restated in `forge-docs/site/src/styles/forge.css`
(in the `forge-docs` repo), mapped onto Starlight's own `--sl-color-*` names.

**Nothing gates the agreement.** A change to a token here is a change there as
well, and the only way to see a drift is to look at the two pages side by side.
The same goes for the header: that repo's `src/components/OrgNav.astro` mirrors
this one's, and both toggles write both theme keys (`theme` here,
`starlight-theme` there) so one click holds across the boundary.

⚠️ **The two navs no longer agree, and the drift is now hidden rather than
reconciled.** This banner is three menus (Architecture / Explore / Docs);
`OrgNav.astro` is still the five flat links it mirrored before. Inside the Docs
view that nav is not rendered at all — the whole banner it sits in is hidden
(see the frames section above) — so a reader never sees the two disagree. They
still disagree for anyone who opens the reference directly, and its links still
point at bare anchors this router happens to accept. Reconciling them is a
change in the `forge-docs` repo; not rendering one of them is not the same
thing.

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
