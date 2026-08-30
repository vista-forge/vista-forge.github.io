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

## The theme key is the one duplication that MUST stay in step

Starlight persists the choice under `starlight-theme`; this site uses `theme`.
Both toggles now write **both** keys and both pre-paint scripts read either, so
one click holds across the boundary. Change one and a reader gets a black
landing page and a white reference from a single click — a bug that looks like
a caching problem and is not ([[stale-css-cache-not-a-code-bug]] is the one it
would be mistaken for).

## Nav rule: every item, every width

`.nav--opt` used to hide Tools and Architecture below 860px, making the menu a
function of the viewport. The strip now scrolls sideways instead, and the
reference gets the same items in Starlight's mobile-menu footer (its
`SocialIcons` slot renders in both places, which is why the nav lives there
rather than in a bespoke bar).

⚠️ **`justify-content: flex-end` on an overflowing scroll container is a trap:**
content spilling past the *start* edge cannot be scrolled back to in Chrome, so
the first item silently becomes unreachable. Push the strip right with
`margin-inline-start: auto`, which collapses to 0 once it overflows.
