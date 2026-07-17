# vista-forge.github.io — per-repo memory index

One line per memory file. Content lives in the files, not here. Per the Increment
Protocol keep-test, this store holds **durable lessons only** — per-increment
journals belong in git history, not here.

- [org-logo-treatment](org-logo-treatment.md) — **The org mark can't be background-removed and shouldn't be tried again.** Its bright chrome bevels are neutral ≥250 — the same pure white as the paper backdrop, and connected to it — so every border-seeded flood fill either leaves the cast shadow (~222 at bottom-left) as a smudge or chews notches out of the V's arms; edge-limited growing kills the shadow but still bites the bevels. Measured 2026-07-16 across `lum>=240/246/250`. The site uses the PNG **unmodified on its white plate** (`.logo-tile` / `.brand__mark` = radius + 1px ring). A transparent mark must come from a re-export of the original render with alpha, not from post-processing the PNG.
- [site-content-is-unguarded](site-content-is-unguarded.md) — **The landing page hand-duplicates the org profile README, and nothing gates the copy.** The profile's repo tables are generated from `ecosystem.json` via `readme-gen.py --check`; the site's copies of those tables and the by-the-numbers figures are hand-written and drift silently. The page also links **only public repos** (23 of 27 are private) — a link added before its repo opens is a public 404.
