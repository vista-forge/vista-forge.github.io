# vista-forge.github.io — the org site.
#
# The `m`/`v` repo tables in index.html are GENERATED from the ecosystem
# registry (see scripts/site-gen.py). Everything else on the page is hand-written.
#
# Two tiers, because this repo is PUBLIC and the registry is not:
#   site-check      offline, no secrets  -> runs in CI on every push
#   site-freshness  live, needs gh auth  -> HOST-ONLY
.PHONY: help check site-check site-sync site-freshness serve

help: ## show this help
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

check: site-check ## the CI gate (offline; what runs on every push)

site-check: ## red-gate index.html's generated blocks against the committed snapshot
	python3 scripts/site-gen.py --check

site-sync: ## HOST-ONLY: re-harvest the org, refresh data/repos.json, rewrite the blocks
	python3 scripts/site-gen.py --harvest
	python3 scripts/site-gen.py

site-freshness: ## HOST-ONLY: red-gate data/repos.json against the live org (new tags, repos gone public)
	python3 scripts/site-gen.py --check-harvest

serve: ## preview at http://127.0.0.1:8000
	python3 -m http.server 8000 --bind 127.0.0.1
