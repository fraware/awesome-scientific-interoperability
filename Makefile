.PHONY: validate test links lint all

validate:
	python scripts/validate_catalog.py
	python scripts/check_links.py --offline

test:
	python -m unittest discover -s tests -v

links:
	python scripts/check_links.py

lint:
	npx --yes awesome-lint

all: validate test lint
