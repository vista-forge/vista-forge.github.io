---
name: the-landing-page-is-for-the-decider
description: The landing page is written for someone deciding, not someone building — three claims with figures, and EVERY technical thing folded at the bottom. Do not re-technicalise it.
metadata:
  type: project
---

# The landing page answers three questions, and the mechanism is an appendix

**Operator, 2026-09-20.** The page opened on the toolchain — continuous
integration, test-driven design, coverage floors, driver seams — all true and
unreadable to anyone who is not already a developer. It is now written for the
person **deciding**, with the person **building** served by a fold at the
bottom.

## The shape, which is the decision

1. **Hero** — what VistA is, what it never had, what Forge adds. No buttons, no
   "see below" note: the operator cut both as filler (2026-09-20) so the claims
   reach the first screen.
2. **The three words as three cards**, each carrying the question it answers —
   *can you prove a change is safe* · *can anyone but a specialist work on it* ·
   *can it move at today's speed*.
3. **One section per claim**: a figure, then three columns — **what it is · how
   it works · what it is worth**.
4. **`#technical`** — ONE fold, shut, holding everything else unedited: the
   numbers, the developer tooling, the stack, why registries, every repository,
   the design principles.

⚠️ **"How does it work" is a technical detail and belongs in the fold.** The
temptation on every future edit is to move a good technical fact up because it
is impressive. That is the state this replaced.

## The figures are HTML, and that is a decision too

Not one drawn image and not a generated one: HTML figures reflow on a phone
(three columns → one at 390px) and stay correct by construction, because the
labels are the page's own text. The operator considered generated infographics
on 2026-09-20 and **chose to keep the HTML ones**.

## Two things the restructure broke, both fixed — expect them again

* **Nested folds need every ANCESTOR opened**, not just the nearest. The router
  walks up from the target opening each one, and opens the target's own fold
  too. Opening only `closest()` leaves an anchor inside a shut outer fold and
  it scrolls to nothing.
* **An unshrinkable flex item does not wrap — it overhangs.**
  `.strata__line-text` was `flex: none`, and its sentence was exactly the 16px
  of horizontal scroll the page had at 390px. Measure the overflowing element;
  do not guess which one it is ([[site-content-is-unguarded]] is the same
  habit applied to prose).

## What is still ungated here

The prose, the figures and the by-the-numbers figures are hand-written and
**rot silently** — only the `m`/`v` repo tables are generated and gated. That
was true before this change and is still true; the restructure moved those
tables without altering a byte, which `make site-check` proves on every run.
