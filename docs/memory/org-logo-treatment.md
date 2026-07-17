---
name: org-logo-treatment
description: The vista-forge org mark cannot be background-removed — its bright chrome facets are the same pure white as its backdrop — so the site uses it unmodified on its white plate.
metadata:
  type: project
---

# The org logo — use it on its plate, don't knock it out

The mark (a chromed **V** with circuit-trace inlay standing on a steel **anvil**
bearing an **M** — VistA on the anvil) is the GitHub org avatar. Canonical source:
`https://avatars.githubusercontent.com/u/287217332` — there is **no logo file
committed anywhere in the org**; the site vendors it at
`vista-forge.github.io/assets/img/logo.png`.

**Do not try to make it transparent with a threshold/flood-fill.** Measured
2026-07-16, not guessed:

- The render sits on white paper (254) **plus a soft cast shadow** that reaches
  ~222 at bottom-left. So there is no single luminance cut: a threshold tight
  enough to spare the metal leaves the shadow as a gray smudge.
- The V's **bevels and the anvil's top faces are specular white** — neutral and
  ≥250, i.e. *identical in value to the paper*, and **connected to it**. Any
  border-seeded flood fill therefore leaks through the bevel and chews visible
  notches out of the V's arms. Confirmed at `lum>=240/246/250` with
  `chroma<=8/6/5`; the leak persists at every setting that also removes the paper.
- Edge-limited region growing (Sobel gradient < 40, grow only through smooth
  neutral pixels) *does* kill the shadow cleanly — but still bites the bevels,
  because the bevel's interior is smooth as well as white.

**Conclusion: the white background is not separable from the subject by any
value-based rule.** The site therefore uses the PNG **unmodified**, presented on
its own plate — `border-radius` + a 1px ring (`.logo-tile` for the hero,
`.brand__mark` for the header/footer) — which reads as a deliberate app-icon mark
on both the dark and light themes.

If a transparent mark is ever genuinely needed, the fix is upstream: **re-export
from the original 3D render with an alpha channel**, or have it redrawn as vector.
Post-processing this PNG is a dead end — don't spend the iterations again.
