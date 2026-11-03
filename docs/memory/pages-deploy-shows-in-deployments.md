---
name: pages-deploy-shows-in-deployments
description: "To see whether a push to this repo is live, read the github-pages deployment's status, not pages/builds/latest, which still reports a build from 2026-08-03; a 404 in the first minute after a push is the deploy still running."
metadata:
  type: project
---

**Measured 2026-09-29**, publishing `artifacts/` (`ad5bb30`).

The site's `build_type` is `legacy` (branch `main`, path `/`), yet
`gh api repos/vista-forge/vista-forge.github.io/pages/builds/latest` answered a
build from **2026-08-03** while the push minutes old was deploying. Every push
does create a `github-pages` **deployment**, and its status is the answer:

    ID=$(gh api "repos/vista-forge/vista-forge.github.io/deployments?per_page=1" --jq '.[0].id')
    gh api "repos/vista-forge/vista-forge.github.io/deployments/$ID/statuses" --jq '.[0].state'

`success` came about 30 s after the push; a WebFetch of the new page in that
window answered **404**, and the same fetch after `success` answered the page.
(Plain `curl https://vista-forge.github.io/…` from the box also works,
measured 2026-11-03.)

**A 404 that lasts is Pages switched OFF, not a deploy.** Measured
2026-11-03: the site 404'd with no push in flight, and
`gh api repos/vista-forge/vista-forge.github.io/pages` answered **404**
(`has_pages: false`), although the 2026-10-23 deploy had succeeded. Nothing
on this box touches the Pages setting (the weekly Actions guard only disables
Actions, which branch Pages does not need), so it was switched off on GitHub
by hand. The fix:

    gh api -X POST repos/vista-forge/vista-forge.github.io/pages \
      -f 'source[branch]=main' -f 'source[path]=/' -f build_type=legacy

The site answered 200 within seconds, serving the last deployment again, with
no new build and no push.

**Why:** a stale builds endpoint reads like a broken deploy, and a 404 right
after a push reads like a wrong path.

**How to apply:** after a push, poll the deployment's status until `success`,
then fetch the page once. A 404 with no push in flight: read the `pages`
endpoint first. Related: [[stale-css-cache-not-a-code-bug]].
