---
name: a-tailnet-published-origin-cannot-be-embedded
description: A page served from the public internet cannot embed a Funnel-published host from INSIDE the tailnet — the browser refuses silently, and only the operator sees it.
metadata:
  type: project
---

# ⚠️⚠️ The operator is the ONE reader for whom the frames do not work

**Measured 2026-09-19**, on the live site, immediately after the org page
became a shell that frames the three applications published from
`minty.warg-torino.ts.net`.

## What happened

All three framed views showed *"has not answered — most likely offline"* while
the host was up and serving. It was not offline. **The browser never sent the
request:** zero network events, no `requestfailed`, no console entry, no CDP
`loadingFailed` — the iframe simply stayed on `about:blank` forever.

## Why, and why only here

A Funnel hostname resolves **differently depending on who asks**:

| asked from | `minty.warg-torino.ts.net` resolves to |
|---|---|
| this box (MagicDNS, on the tailnet) | `100.117.23.46` — the tailnet address |
| a public resolver (`dig @8.8.8.8`) | `209.177.145.137`, `199.38.181.54` — Tailscale's public ingress |

A page served from `https://vista-forge.github.io` is public. Embedding a host
that resolves to a **private** address is a private-network request, and Chrome
refuses it without asking. Off the tailnet the same name resolves to a public
address and nothing applies.

**So the one reader who sees the frames fail is the operator** — everyone else
gets the public answer. An "it's broken" report from this box is not evidence
about the site, and a green check from this box would not have been either.

## What it is NOT — each checked, not assumed

* **Not a server-side block.** The publish origin
  (`vdb-explorer/tools/publish/origin.py`) sets no `X-Frame-Options` and no
  `frame-ancestors`, and the **public** Funnel ingress, asked directly by IP
  with SNI and Host set, returns the same headers and a 200.
* **Not the shell's code.** From the same live public page, `example.com`
  framed successfully (request made, frame URL committed) in the same tick that
  the Funnel host made no request at all. One variable: the destination address.
* **Not slowness.** Fifteen seconds, zero bytes requested.

## The discriminator, since the page is told nothing

A cross-origin frame reports neither success nor failure to the page around it.
But **a frame that has not navigated is still the embedding page's own
`about:blank`, so reading `contentWindow.location.href` SUCCEEDS; once the
cross-origin document commits, the same read throws.** That one bit separates
*the browser refused to ask* from *the host did not answer*, and the site now
says which. Use it anywhere a cross-origin embed has to degrade loud
([[degrade-loud-or-refuse]]) — a timeout alone will blame the wrong party.

## If the frames are wanted on this box

Nothing in the site can fix it; the choice is the reader's browser. Resolve the
name publicly (a hosts entry pointing at the ingress IP), turn off Chrome's
private-network block, or read the site from a machine that is not on the
tailnet. Otherwise the notice and its direct link are the intended experience
here.

Related: [[two-deployments-one-chrome-ungated]] for what else the framing
exposed, and the org's publish-topology rule (`published-sites-public-repos-private`).
