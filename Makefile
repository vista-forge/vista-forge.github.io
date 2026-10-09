# vista-forge.github.io — the org site.
#
# The page is hand-written. The repo tables that were generated from the
# ecosystem registry left with their section (operator, 2026-10-07), and
# site-gen.py, its snapshot and its two gates went with them.
.PHONY: help check artifacts artifacts-check serve

help: ## show this help
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

check: artifacts-check ## THE gate — local, reaches no network (no CI; run before every push)

artifacts: ## regenerate artifacts/, prototypes/ and proposals/ index.html from the folders under each
	python3 scripts/artifacts_index.py

artifacts-check: ## red-gate artifacts/, prototypes/ and proposals/ index.html against their folders (and the tests)
	python3 -m unittest scripts/test_artifacts_index.py
	python3 scripts/artifacts_index.py --check

serve: ## preview at http://127.0.0.1:8000
	python3 -m http.server 8000 --bind 127.0.0.1
