---
title: "The VistA Documentation Library on the org site"
status: accepted — ruled by the operator 2026-11-07
phase: building
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

Built: the admission, the service, the menu entry and the frame route. Two steps need the
operator, because they need credentials this session does not hold:

- the org mirror `github.com/vista-forge/vdocs-web` (private, Actions disabled and vulnerability
  alerts deleted before the first push, as for vdb-explorer), which `workspace/repos.txt` names;
- the Funnel path: `sudo tailscale funnel --bg --set-path /vdocs http://127.0.0.1:8146`
  (`tailscale serve` changes need root on this host).

Until the Funnel path exists the frame shows the site's own notice with the direct link. From
inside the tailnet the frame never loads, as for the other two hosted applications
(`docs/memory/a-tailnet-published-origin-cannot-be-embedded.md`); check it from outside.
