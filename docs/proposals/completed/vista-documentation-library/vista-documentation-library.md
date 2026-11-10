---
title: "The VistA Documentation Library on the org site"
status: completed — accepted, ruled by the operator 2026-11-07
phase: landed
---

# The VistA Documentation Library on the org site

The operator asked, 2026-11-07, for vdocs-web — the navigator over the VA's own VistA manuals,
built in `~/projects` — to be published on <https://vista-forge.github.io> and to appear in the
Docs menu as **VistA Documentation Library**. This page records the rulings that made that
possible, because the site may not depend on a `~/projects` repo.

## Rulings

- **VL-D1. vdocs-web joins the org as a non-waterline member** (operator, 2026-11-07), the same
  standing as vdb-explorer (VD-D93). It moved to `~/vista-forge/vdocs-web`, its module to
  `github.com/vista-forge/vdocs-web`, and it is listed in `workspace/repos.txt` and the org
  `go.work`. It carries no `m`/`v` layer tag and no `ecosystem.json` entry, reaches no engine, and
  the dependency runs one way, `~/data/vdocs` → vdocs-web: nothing in the org may come to depend
  on it. Its `make check` carries the org docs gate and vulnerability scan; the eight build-time
  advisories the scan still found after updating within range are accepted until 2026-12-07, by
  operator ruling, in its `web/` and `extension/osv-scanner.toml`. The producer, `vdocs`, stays in
  `~/projects`: vdocs-web reads its published `index.db` from `~/data/vdocs`, a data release, not
  code.
- **VL-D2. It is served live from the project's host, public, at
  `https://minty.warg-torino.ts.net/vdocs/`** (operator, 2026-11-07). GitHub Pages serves static
  files only, and the navigator is a server over a 363 MB `index.db` (GitHub refuses any file over
  100 MB), so it cannot be a copy in this repo the way the reference is. vdocs-web runs as a user
  service (`vdocs-web/tools/publish/vdocs-web.service`, loopback port 8146, a published copy of the
  binary, read-only hardening) behind its own Tailscale Funnel path: vdb-explorer's publish origin
  serves static directories only, so a live server cannot be one of them. vdocs-web works under a
  path because every request and asset it loads is relative.
- **VL-D3. The Docs menu lists it as "VistA Documentation Library", framed at `#/docs/vdocs`**
  (operator, 2026-11-07), after the reference's entry in the menu's left column. The `<noscript>`
  note links it directly.

## State

Landed 2026-11-07. The org mirror `github.com/vista-forge/vdocs-web` exists (private, Actions
disabled and vulnerability alerts deleted before the first push, as for vdb-explorer), the operator
added the Funnel path (`sudo tailscale funnel --bg --set-path /vdocs http://127.0.0.1:8146`), and
the site push `c0dd6fa0` deployed. Checked through Tailscale's public ingress, as a reader off the
tailnet resolves the name: `https://minty.warg-torino.ts.net/vdocs/` answers 200 with no header
that refuses framing, its relative `./_app/` assets and its API (`api/meta`, `api/suggest`) answer,
and `/` still serves the other applications. The live site carries the menu entry and the
`#/docs/vdocs` route.

2026-11-08, at the operator's request: the menu entry opens an orientation page, this site's own
`/vdocs-library/` (same origin, so it loads anywhere), drawing what the Inventory and the Library hold
and how the web app and the MCP server read one index; its two links open the app at
`#/docs/vdocs/library` and `#/docs/vdocs/inventory`. The menu's note under the VistA Forge stack was
removed. The page's figures are hand-written, measured from the published index that day.
Later that day the operator simplified the menu to two entries with plain generic names, *VistA
Forge Docs* and *VistA Docs*; the page is titled *VistA Documentation*, names the VA Software Document
Library (VDL) once as the source, and calls it the catalog after that.

From inside the tailnet the app's frame never loads, as for the other two hosted applications
(`docs/memory/a-tailnet-published-origin-cannot-be-embedded.md`); the frame itself was not viewed
from off the tailnet.
