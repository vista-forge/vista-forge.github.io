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
External curl is sandbox-denied, so WebFetch is the live check.

**Why:** a stale builds endpoint reads like a broken deploy, and a 404 right
after a push reads like a wrong path.

**How to apply:** after a push, poll the deployment's status until `success`,
then fetch the page once. Related: [[stale-css-cache-not-a-code-bug]].
