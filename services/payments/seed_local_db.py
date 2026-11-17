"""Build the local payments database from synthetic rows.

Opens one account for each customer in data/customers_sample.csv, funds it
from the bank's settlement account, and adds a few `TEST-` payments between
customers. Run from the repository root:

    python3 -m services.payments.seed_local_db
"""

import csv
import random

from services.payments import ledger
from services.payments.config import REPO_ROOT, load_config, sqlite_path

SETTLEMENT_ACCOUNT = "MB-TEST-SETTLE"
CUSTOMERS = REPO_ROOT / "data" / "customers_sample.csv"
TEST_PAYMENTS = 12


def seed(path):
    if path.exists():
        path.unlink()
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = ledger.open_ledger(path)
    rng = random.Random(7)
    ledger.open_account(conn, SETTLEMENT_ACCOUNT, "MERIDIAN", "2020-01-01")
    with CUSTOMERS.open(newline="") as f:
        customers = list(csv.DictReader(f))
    for row in customers:
        ledger.open_account(conn, row["account_number"], row["customer_id"], row["opened_on"])
        ledger.post_payment(
            conn, f"SEED-{row['customer_id']}", SETTLEMENT_ACCOUNT,
            row["account_number"], rng.randrange(10_000, 500_000),
        )
    for n in range(1, TEST_PAYMENTS + 1):
        debit, credit = rng.sample(customers, 2)
        ledger.post_payment(
            conn, f"TEST-{n:04d}", debit["account_number"],
            credit["account_number"], rng.randrange(100, 5_000),
        )
    conn.close()
    return len(customers)


def main():
    path = sqlite_path(load_config("local"))
    count = seed(path)
    print(f"seeded {count} accounts and {TEST_PAYMENTS} test payments into {path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
