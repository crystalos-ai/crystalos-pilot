Fictional sample code for product demonstrations. All data is synthetic.

# Meridian Bank: retail banking services

A small Python monorepo for Meridian Bank's retail back office. It holds four
pieces:

| Folder | What it does |
|---|---|
| `services/payments/` | The payments ledger: double-entry bookkeeping, on SQLite for local work. |
| `screening/` | Sanctions name-match screening for outgoing payments. |
| `etl/` | The nightly customer import from the core-banking extract. |
| `tools/`, `statements/` | Customer reports and the monthly statement checks. |

Synthetic sample data lives in `data/` and `statements/`.

## Requirements

Python 3.10 or later. The code uses the standard library only, so there is
nothing to install.

## Run the tests

From the repository root:

```sh
python3 -m unittest discover -s tests
```

## Common tasks

```sh
# Build the local payments database (var/payments-local.sqlite3) from synthetic rows
python3 -m services.payments.seed_local_db

# Run the nightly import against the sample extract
python3 -m etl.import_rows data/customers_sample.csv

# Write a customer count by region to out/customers_by_region.csv
python3 tools/export_customers.py

# Check one statement file against statements/MANIFEST.sha256
python3 tools/verify_statements.py statements/stmt-001.txt
```

See `CONTRIBUTING.md` for code style and the change process.
