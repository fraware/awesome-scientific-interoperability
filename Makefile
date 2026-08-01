.PHONY: validate test manifest refresh-manifest links lint all

validate:
	python scripts/validate_catalog.py
	python scripts/check_links.py --offline
	python scripts/verify_manifest.py

test:
	python -m unittest discover -s tests -v

manifest:
	python scripts/verify_manifest.py

refresh-manifest:
	python scripts/generate_manifest.py

links:
	python scripts/check_links.py

lint:
	npm install --no-save --package-lock=false awesome-lint@2.3.0
	node scripts/run_awesome_lint.mjs

all: validate test lint
