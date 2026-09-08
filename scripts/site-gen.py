#!/usr/bin/env python3
"""
site-gen.py — the site's repo tables, generated from the ecosystem registry.

The landing page's `m` and `v` repo tables are OWNED BY THIS TOOL. They are a
projection of the same source the org profile README projects (doc-accuracy D4):

    ecosystem.json  (registry membership + layer, in the .github repo)
      + each repo's committed repo.meta.json `role`
      + its latest version tag
      + its VISIBILITY                        <-- site-specific, see below

Regions of index.html between `<!-- gen:begin block=NAME -->` and
`<!-- gen:end -->` are rendered from that data. Hand-editing them is drift, and
drift is a red gate.

WHY VISIBILITY IS PART OF THE PROJECTION
----------------------------------------
This site is public; most of the org is not. A link to a private repo is a
public 404. So a repo's name is emitted as a LINK only when the repo is actually
public, and as plain text otherwise. That rule used to live in a human's head
(and in a memory file); here it is mechanical — when a repo flips public, a
re-harvest links it, and nothing links it before then.

THE TWO-TIER GATE (and why it is two tiers)
-------------------------------------------
The registry and the roles live in PRIVATE repos, so harvesting them needs a
token with org-wide contents:read. `.github` can hold one (`META_GATE_TOKEN`)
because `.github` is private. **This repo is public** — putting an org-wide read
PAT in its Actions secrets is a much larger blast radius than the gate is worth.
So the harvest and the check are separated:

  tier 1  `--check`          offline. Re-renders from the COMMITTED snapshot
                             (data/repos.json) and diffs index.html. Catches a
                             hand-edited generated block. NO NETWORK, NO SECRETS
                             -> runs in this public repo's CI.

  tier 2  `--check-harvest`  live. Re-harvests and diffs the COMMITTED snapshot.
                             Catches staleness (a new tag, a repo gone public).
                             Needs gh auth -> HOST-ONLY (or a token-bearing job).

Tier 1 alone would let the snapshot rot; tier 2 alone can't run here. Together
the generated HTML can't drift from the snapshot, and the snapshot can't drift
from the org for longer than it takes to run `make site-sync`.

Auth fails LOUD (exit 2), never blind — the meta-gate's lesson: a gate that
silently passes when it cannot see the thing it guards is worse than no gate.

Status prose in a `role` is NOT re-checked here: readme-gen.py already red-gates
that at the source (C1), and the same rule enforced twice drifts twice.

Exit codes: 0 clean · 2 usage/auth/config error · 3 drift.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ORG = "vista-forge"
REGISTRY_REPO = ".github"
REGISTRY_PATH = "ecosystem.json"

HERE = Path(__file__).resolve().parent.parent
INDEX = HERE / "index.html"
SNAPSHOT = HERE / "data" / "repos.json"

BLOCK_RE = re.compile(
    r"(<!--\s*gen:begin\s+block=([\w-]+)\s*-->)\n.*?(\s*<!--\s*gen:end\s*-->)",
    re.DOTALL,
)

# Mirror readme-gen.py so the two projections agree on the same source strings.
_SENTENCE_END = re.compile(r"(?<=\.)\s+")
_VERSION_TAG = re.compile(r"^v\d+(\.\d+)*$")
_CODE_SPAN = re.compile(r"`([^`]+)`")

LAYER_BLOCKS = {"m": "repos-m", "v": "repos-v"}


# --------------------------------------------------------------------------- #
# harvest (live — needs gh auth)
# --------------------------------------------------------------------------- #
def gh(args: list[str], what: str) -> str:
    p = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=60)
    if p.returncode != 0:
        raise OSError(f"{what}: {p.stderr.strip()[:160]}")
    return p.stdout


def preflight() -> None:
    """Fail loud if gh cannot read the registry repo. A harvest that quietly
    yields an empty/partial table is exactly the drift this tool prevents."""
    try:
        gh(["api", f"repos/{ORG}/{REGISTRY_REPO}", "--jq", ".name"],
           "auth preflight")
    except (OSError, subprocess.SubprocessError) as e:
        sys.exit(f"site-gen: cannot read {ORG}/{REGISTRY_REPO} — is `gh` "
                 f"authenticated with org read access?\n  {e}")


def latest_version_tag(tags: list[str]) -> str:
    versioned = [t for t in tags if _VERSION_TAG.match(t)]
    if not versioned:
        return ""
    return max(versioned,
               key=lambda t: tuple(int(p) for p in t.lstrip("v").split(".")))


def load_registry(local: Path | None) -> dict[str, str]:
    """{repo: layer} from ecosystem.json — live from the registry repo's default
    branch (its truth), or a local file when --registry is given."""
    if local:
        raw = local.read_text(encoding="utf-8")
    else:
        raw = gh(["api", "-H", "Accept: application/vnd.github.raw",
                  f"repos/{ORG}/{REGISTRY_REPO}/contents/{REGISTRY_PATH}"],
                 "ecosystem.json fetch")
    return json.loads(raw)["repos"]


def harvest(registry: dict[str, str]) -> dict:
    repos = []
    for name, layer in registry.items():
        if layer not in LAYER_BLOCKS:
            raise ValueError(f"{name}: unknown layer {layer!r} in registry")
        meta = json.loads(gh(
            ["api", "-H", "Accept: application/vnd.github.raw",
             f"repos/{ORG}/{name}/contents/repo.meta.json"],
            f"{name}: repo.meta.json"))
        tags = gh(["api", "--paginate", f"repos/{ORG}/{name}/tags",
                   "--jq", ".[].name"], f"{name}: tags").split()
        vis = gh(["api", f"repos/{ORG}/{name}", "--jq", ".visibility"],
                 f"{name}: visibility").strip()
        repos.append({
            "name": name,
            "layer": layer,
            "role": meta.get("role", ""),
            "tag": latest_version_tag(tags),
            "public": vis == "public",
        })
    return {"org": ORG, "source": f"{ORG}/{REGISTRY_REPO}/{REGISTRY_PATH}",
            "repos": repos}


# --------------------------------------------------------------------------- #
# render (offline — from the snapshot)
# --------------------------------------------------------------------------- #
def cell(text: str) -> str:
    """Escape for HTML, then honour the role's markdown code spans."""
    out = html.escape(text.replace("\n", " ").strip(), quote=False)
    return _CODE_SPAN.sub(r"<code>\1</code>", out)


def render_table(repos: list[dict], org: str) -> str:
    rows = []
    for r in repos:
        delivers = _SENTENCE_END.split(r["role"])[0].rstrip(".")
        name = html.escape(r["name"], quote=False)
        # public -> a link a visitor can follow; private -> plain text, never a 404
        label = (f'<a href="https://github.com/{org}/{name}">{name}</a>'
                 if r["public"] else f"<strong>{name}</strong>")
        tag = r["tag"] or "—"
        cls = "tag tag--has" if r["tag"] else "tag"
        rows.append(f'          <tr><td>{label}</td><td>{cell(delivers)}</td>'
                    f'<td class="{cls}">{tag}</td></tr>')
    return "\n".join(rows)


def render_blocks(data: dict) -> dict[str, str]:
    out = {}
    for layer, block in LAYER_BLOCKS.items():
        repos = [r for r in data["repos"] if r["layer"] == layer]
        out[block] = render_table(repos, data["org"])
    return out


def replace_blocks(text: str, rendered: dict[str, str]) -> tuple[str, list[str]]:
    found: list[str] = []

    def sub(m: re.Match) -> str:
        name = m.group(2)
        found.append(name)
        if name not in rendered:
            return m.group(0)
        return f"{m.group(1)}\n{rendered[name]}\n{m.group(3).lstrip(chr(10))}"

    return BLOCK_RE.sub(sub, text), found


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true",
                    help="offline: verify index.html matches the committed snapshot (exit 3 on drift)")
    ap.add_argument("--harvest", action="store_true",
                    help="live: refresh data/repos.json from the org (needs gh auth)")
    ap.add_argument("--check-harvest", action="store_true",
                    help="live: verify the committed snapshot matches the org (exit 3 on drift)")
    ap.add_argument("--registry", type=Path,
                    help="read ecosystem.json from this path instead of the registry repo")
    args = ap.parse_args()

    # ---- live tiers -------------------------------------------------------- #
    if args.harvest or args.check_harvest:
        if not args.registry:
            preflight()
        try:
            data = harvest(load_registry(args.registry))
        except (OSError, ValueError, json.JSONDecodeError) as e:
            sys.exit(f"site-gen: harvest failed — {e}")

        fresh = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        if args.check_harvest:
            have = SNAPSHOT.read_text(encoding="utf-8") if SNAPSHOT.exists() else ""
            if have != fresh:
                print("site-gen: data/repos.json is STALE vs the live org.",
                      file=sys.stderr)
                for line in _diff(have, fresh, "data/repos.json"):
                    print(line, file=sys.stderr)
                print("\n  fix: make site-sync", file=sys.stderr)
                return 3
            print("site-gen: snapshot matches the live org.")
            return 0
        SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
        SNAPSHOT.write_text(fresh, encoding="utf-8")
        print(f"site-gen: harvested {len(data['repos'])} repos -> "
              f"{SNAPSHOT.relative_to(HERE)}")
        return 0

    # ---- offline tiers ----------------------------------------------------- #
    if not SNAPSHOT.exists():
        sys.exit(f"site-gen: {SNAPSHOT.relative_to(HERE)} missing — run `make site-sync`")
    data = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    src = INDEX.read_text(encoding="utf-8")
    rendered = render_blocks(data)
    new, found = replace_blocks(src, rendered)

    missing = set(rendered) - set(found)
    if missing:
        sys.exit(f"site-gen: index.html has no block(s) for: {', '.join(sorted(missing))}")

    if args.check:
        if new != src:
            print("site-gen: index.html generated blocks are STALE.", file=sys.stderr)
            for line in _diff(src, new, "index.html"):
                print(line, file=sys.stderr)
            print("\n  fix: make site-sync  (do not hand-edit a gen block)",
                  file=sys.stderr)
            return 3
        print(f"site-gen: {len(found)} generated block(s) in sync.")
        return 0

    if new != src:
        INDEX.write_text(new, encoding="utf-8")
        print(f"site-gen: rewrote {len(rendered)} block(s) in index.html")
    else:
        print("site-gen: index.html already current")
    return 0


def _diff(a: str, b: str, name: str) -> list[str]:
    import difflib
    return list(difflib.unified_diff(a.splitlines(), b.splitlines(),
                                     f"{name} (committed)", f"{name} (expected)",
                                     lineterm="", n=1))[:40]


if __name__ == "__main__":
    sys.exit(main())
