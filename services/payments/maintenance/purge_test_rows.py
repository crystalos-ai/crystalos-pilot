"""Delete `TEST-` payments (and their ledger entries) from the local database.

    python3 -m services.payments.maintenance.purge_test_rows [--dry-run]

Works on the local SQLite database only: `config.sqlite_path` refuses any
other database.
"""

import argparse

from services.payments import ledger
from services.payments.config import load_config, sqlite_path

TEST_PREFIX = "TEST-"


def purge(conn, dry_run=False):
    (count,) = conn.execute(
        "SELECT COUNT(*) FROM payments WHERE reference LIKE ?", (TEST_PREFIX + "%",)
    ).fetchone()
    if not dry_run:
        with conn:
            conn.execute("DELETE FROM payments WHERE reference LIKE ?", (TEST_PREFIX + "%",))
    return count


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--config", default="local", help="config name (default: local)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    path = sqlite_path(load_config(args.config))
    conn = ledger.open_ledger(path)
    count = purge(conn, args.dry_run)
    conn.close()
    print(f"{'would delete' if args.dry_run else 'deleted'} {count} test payments from {path.name}")


if __name__ == "__main__":
    main()
