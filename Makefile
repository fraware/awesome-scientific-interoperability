.PHONY: validate test manifest refresh-manifest links lint all query query-json coverage-audit

validate:
	python scripts/validate_catalog.py
	python scripts/validate_decision_guides.py
	python scripts/validate_problem_index.py
	python scripts/validate_watchlist.py
	python scripts/check_review_freshness.py
	python scripts/check_links.py --offline
	python scripts/verify_manifest.py

coverage-audit:
	python scripts/audit_coverage.py --json-report coverage-audit.json --markdown-report coverage-audit.md

test:
	python -m unittest discover -s tests -v

manifest:
	python scripts/verify_manifest.py

refresh-manifest:
	python scripts/generate_manifest.py

links:
	python scripts/check_links.py

lint:
	npx --yes awesome-lint

query:
	python scripts/query_catalog.py $(if $(SECTION),--section "$(SECTION)",) $(if $(LAYER),--layer "$(LAYER)",) $(if $(DOMAIN),--domain "$(DOMAIN)",) $(if $(CONNECTS),--connects "$(CONNECTS)",) $(if $(EVIDENCE),--evidence "$(EVIDENCE)",) $(if $(REVIEW_TYPE),--review-type "$(REVIEW_TYPE)",) $(if $(ID),--id "$(ID)",)

query-json:
	python scripts/query_catalog.py --format json $(if $(SECTION),--section "$(SECTION)",) $(if $(LAYER),--layer "$(LAYER)",) $(if $(DOMAIN),--domain "$(DOMAIN)",) $(if $(CONNECTS),--connects "$(CONNECTS)",) $(if $(EVIDENCE),--evidence "$(EVIDENCE)",) $(if $(REVIEW_TYPE),--review-type "$(REVIEW_TYPE)",) $(if $(ID),--id "$(ID)",)

all: validate test lint
