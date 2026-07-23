---
name: stale-css-cache-not-a-code-bug
description: A "section X doesn't show up" report after a CSS-only deploy is almost always a stale browser CSS cache, not a code bug. Prove it with a live-asset fetch + an isolated-profile headless render before touching code.
metadata:
  type: project
---

# "It doesn't show up in <browser>" after a CSS change = stale cache first, code bug last

When someone reports that a section of the live site "doesn't show up" **shortly
after a CSS-only push**, the overwhelmingly likely cause is a **stale browser CSS
cache**, not a code defect. The browser refetched the changed `index.html` but is
still styling it with the **old, cached `assets/css/site.css`** — so new markup
(e.g. `.vfm` classes) renders unstyled/collapsed and appears to vanish. GitHub
Pages serves user assets with roughly a **10-minute cache**, and an already-open
browser holds the old CSS for that window.

- **Fix for the reporter:** hard-reload — **Ctrl+Shift+R** (Firefox/Chrome). It
  also self-heals on its own within ~10 min.
- Verified real case 2026-07-23: the v-f-m stack diagram "didn't show up in
  Firefox." Code was fine; it was the cache.

## Prove it fast — the two checks (and their gotchas)

1. **Confirm the deploy actually shipped the new bytes.** `curl` to external hosts
   is **sandbox-denied here** — use **WebFetch** on the live URLs
   (`https://vista-forge.github.io/assets/css/site.css`, `/index.html`) and check
   the new selectors/text are present. If the live CSS already has the new rules,
   the problem is downstream of the deploy = the client cache.

2. **Render your ACTUAL files in real Firefox headless** to rule out a genuine
   browser-specific bug (don't trust only the Chromium Playwright render):

   ```
   firefox --headless --new-instance --profile <tmpdir> \
     --window-size=1000,900 --screenshot out.png "file://$PWD/index.html"
   ```

   **Gotcha:** the user's Firefox is usually already running, so a plain
   `firefox --headless --screenshot` dies with *"Firefox is already running, but is
   not responding."* The `--new-instance --profile <tmpdir>` (a throwaway profile)
   is what lets a second instance launch. To isolate one component, write a tiny
   harness HTML into the scratchpad that `<link>`s the real `site.css` and contains
   only that section's markup, then screenshot that.

## Robustness option (considered, not taken)

A `?v=<version>` cache-bust on the CSS `<link href>` would force a fresh CSS fetch
on every deploy and kill this class of report — but it needs a **manual version
bump on every CSS edit** (forget it and the 10-min stale window returns anyway).
Offered to the operator rather than imposed. HTML-only changes don't need it (the
cached CSS is already correct). See [[site-content-is-unguarded]] for what on the
page is gated vs hand-written.
