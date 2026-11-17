# Payments service

The ledger behind Meridian Bank's retail payments.

| File | What it is |
|---|---|
| `ledger.py` | Opens accounts, posts double-entry payments, reads balances. |
| `schema.sql` | Tables: `accounts`, `payments`, `ledger_entries`. |
| `config.py` | Reads `db.<name>.conf` settings. |
| `db.local.conf` | The local SQLite database under `var/`. |
| `db.production.conf` | The production PostgreSQL database (platform team). |
| `seed_local_db.py` | Builds the local database from synthetic rows. |
| `maintenance/` | Runbooks and scripts for the local database. |

Build the local database:

```sh
python3 -m services.payments.seed_local_db
```

The production password is never stored here. The platform deployment reads
it from the environment variable named in `db.production.conf`.
