---
name: another-session-may-push-first
description: "Other Claude sessions, cloud ones included, push to this repo's main (the Certo guide, 2026-10-02); fetch before committing, and when the push is rejected here, where merge and rebase are refused, publish from a branch made off origin/main as a fast-forward"
metadata:
  type: project
---

On 2026-10-03 a push of `artifacts/certo-demo/` was rejected: a cloud
session (claude.ai/code) had pushed `artifacts/certo-guide/` to main the
evening before. Both touched the generated `artifacts/index.html`.

**Why:** this repo is a deploy target that more than one session writes,
and `git merge` and `git rebase` are refused by this box's permissions, so
the usual recovery is not available.

**How to apply:**
- `git fetch` and look at `HEAD..origin/main` before committing here.
- If the push is rejected: `git switch -c <name> origin/main`, bring the
  new folder over with `git checkout main -- artifacts/<folder>`, run
  `make artifacts` and `make check` (the index is regenerated, so it never
  needs a hand merge), commit, and `git push origin <name>:main`, a
  fast-forward. Local main is then left a commit apart; realigning it is a
  destructive local step for the operator.
- A new page should link the pages beside it that cover the same thing.
- Confirm the deploy by the `github-pages` deployment's status
  ([[pages-deploy-shows-in-deployments]]).
