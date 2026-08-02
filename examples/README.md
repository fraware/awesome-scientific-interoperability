# Examples

## catalog.json consumer

`catalog_json_consumer.py` is a minimal downstream smoke test for published catalog dumps.

```bash
python scripts/export_catalog.py
python examples/catalog_json_consumer.py dist/catalog.json
python examples/catalog_json_consumer.py dist/catalog.json --evidence public-validator
```

After a release or Pages deploy, the same script can point at a downloaded `catalog.json` without cloning this repository's YAML shards.
