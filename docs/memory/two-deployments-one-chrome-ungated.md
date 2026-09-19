---
name: two-deployments-one-chrome-ungated
description: The org site and forge-reference are one visual product built by two toolchains, so the palette, the nav items and the theme key are restated by hand in both — and nothing gates the agreement.
metadata:
  type: project
---

# ⚠️ One chrome, two toolchains, no gate between them

**2026-08-30.** The reference site was restyled to be a *wing* of this one
rather than a separate product: same mark, same wordmark, same palette, same
five nav items, same two-state dark/light button. It is still a **separate
deployment built by Starlight**, so every one of those is *restated*, not
shared.

## What is duplicated, and where

| here | there (`forge-reference` repo) |
|---|---|
| `assets/css/site.css` token block | `site/src/styles/forge.css` — same values, mapped onto Starlight's `--sl-color-*` |
| the five `<nav class="nav">` items in `index.html` | `site/src/components/OrgNav.astro` |
| the `.brand` / `.brand__mark` markup | `site/src/components/SiteTitle.astro` |
| `.theme-toggle` markup + CSS | `site/src/components/ThemeToggle.astro` + the same rules in `forge.css` |
| `assets/img/{mark,favicon-32,logo-180}.png` | vendored copies in `site/public/` |

**No gate compares any row.** A token changed on one side and not the other
drifts silently and looks like nothing — the same blind spot as
[[site-content-is-unguarded]], one boundary out: each stylesheet is internally
fine, and a reader is the only thing that sees both.

**Why not share the stylesheet.** A `<link>` to this origin from the reference
would be an off-host load, which that repo's `make offline-check` forbids
outright — and it would not survive an airgapped read either. Vendoring the
values is the deliberate cost of the offline guarantee, not an oversight.

## ⚠️ 2026-09-19: the drift is now in ONE VIEWPORT, and the theme trick does not reach the third copy

The landing page became a **shell**: a permanent banner of three menus over
either the landing content or a **frame** holding one of the three published
applications, the reference among them. Two things this table said were
*invisible* stopped being invisible, and one thing it said was *solved* turned
out to be solved only for one of two copies.

**The nav row is now read side by side, by everyone.** The reference is shown
*inside* the Docs view, so its `OrgNav` renders directly under this banner —
one brand, two disagreeing bars, in one screenshot. The row above stopped being
a drift nobody can see and became the first thing a reader of that view sees.
(Its links still resolve: they are bare anchors, and the shell's router reads
`#repos` as a section of the landing page. That back-compat is deliberate — the
router must keep accepting bare anchors for exactly this reason.)

**The theme key holds across the two ORIGINS it was written for, and no
further.** `localStorage` is per-origin. Writing both `theme` and
`starlight-theme` works because the Pages copy of the reference is served from
`vista-forge.github.io` — the *same* origin as the landing page. The copy that
the Docs view actually frames is served from the Funnel host, a **third
origin**, which shares no storage with either. So a framed reference is always
on its own default, whatever the reader chose in the banner above it, and
nothing in this repo can change that.

⚠️ **The two copies of the reference are not interchangeable.** Measured
2026-09-19: the Funnel copy carries `concepts/`, `errors/` and `guides/`
directories the Pages copy does not (240 vs 262 HTML files, different vintages).
Picking whichever is same-origin to get the theme back would silently serve
different documentation.

**Also measured:** the publish origin (`vdb-explorer`'s `tools/publish/origin.py`)
sets no `X-Frame-Options` and no `frame-ancestors`, and the Funnel passes its
headers through unchanged — which is the only reason any of this frames at all.
A security header added there blanks three views here, with no error on this
side.

## The theme key is the one duplication that MUST stay in step

Starlight persists the choice under `starlight-theme`; this site uses `theme`.
Both toggles now write **both** keys and both pre-paint scripts read either, so
one click holds across the boundary. Change one and a reader gets one ground on
the landing page and the other on the reference from a single click — a bug that
looks like a caching problem and is not ([[stale-css-cache-not-a-code-bug]] is
the one it would be mistaken for).

⚠️ **Both defaults must agree, and each site states its own.** Light became the
default on 2026-08-30; the reference expresses that in the head script that
seeds `starlight-theme`, which must stay ahead of Starlight's own inline
ThemeProvider — that one falls back to `prefers-color-scheme`, so a dark-OS
reader would land dark on a site whose default is light.

## Nav rule: every item, every width

`.nav--opt` used to hide Tools and Architecture below 860px, making the menu a
function of the viewport. The strip then scrolled sideways instead, and the
reference gets the same items in Starlight's mobile-menu footer (its
`SocialIcons` slot renders in both places, which is why the nav lives there
rather than in a bespoke bar).

⚠️ **`justify-content: flex-end` on an overflowing scroll container is a trap:**
content spilling past the *start* edge cannot be scrolled back to in Chrome, so
the first item silently becomes unreachable. Push the strip right with
`margin-inline-start: auto`, which collapses to 0 once it overflows.

⚠️ **The sideways scroll had to go when the flat links became menus, and not
for the reason it looks like.** Three items fit at any width, so the scroll was
merely unnecessary — but it was also *fatal*: a scroll container clips its
descendants, **absolutely-positioned ones included**, so a dropdown panel
inside it is sliced off at the banner's edge. A menu cannot live inside an
`overflow-x: auto` strip at all.
