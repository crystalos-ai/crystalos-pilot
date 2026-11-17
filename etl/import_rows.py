"""Nightly customer import.

Reads the customer extract from core banking (CSV) and loads it into the
customer store. Each customer is routed to the work queue of its region.

Rules:
- customer_id, full_name, email and account_number are required. A row
  without one of them is rejected and listed in the report.
- region is optional. A customer with no region is imported with region
  UNASSIGNED and routed to the head-office review queue.
- A region that is not in QUEUE_BY_REGION is rejected.

Run from the repository root:

    python3 -m etl.import_rows data/customers_sample.csv [--db var/customers.sqlite3]
"""

import argparse
import csv
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

REQUIRED_FIELDS = ("customer_id", "full_name", "email", "account_number")
UNASSIGNED_REGION = "UNASSIGNED"
QUEUE_BY_REGION = {
    "North": "branch-north",
    "South": "branch-south",
    "East": "branch-east",
    "West": "branch-west",
    "Central": "branch-central",
    UNASSIGNED_REGION: "head-office-review",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id    TEXT PRIMARY KEY,
    full_name      TEXT NOT NULL,
    email          TEXT NOT NULL,
    account_number TEXT NOT NULL,
    region         TEXT NOT NULL,
    queue          TEXT NOT NULL
)
"""


@dataclass
class ImportReport:
    imported: int = 0
    rejected: list = field(default_factory=list)  # (line number, reason)


def import_rows(rows, conn):
    """Load CSV rows (dicts) into `conn`. Line numbers count the header as line 1."""
    report = ImportReport()
    conn.execute(SCHEMA)
    for line_no, row in enumerate(rows, start=2):
        missing = [name for name in REQUIRED_FIELDS if not (row.get(name) or "").strip()]
        if missing:
            report.rejected.append((line_no, "missing " + ", ".join(missing)))
            continue
        region = (row.get("region") or "").strip()
        queue = QUEUE_BY_REGION.get(region)
        if queue is None:
            report.rejected.append((line_no, f"unknown region {region!r}"))
            continue
        conn.execute(
            "INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?, ?, ?)",
            (row["customer_id"].strip(), row["full_name"].strip(), row["email"].strip(),
             row["account_number"].strip(), region, queue),
        )
        report.imported += 1
    conn.commit()
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Nightly customer import.")
    parser.add_argument("extract", type=Path)
    parser.add_argument("--db", type=Path, default=Path("var/customers.sqlite3"))
    args = parser.parse_args(argv)
    args.db.parent.mkdir(parents=True, exist_ok=True)
    with args.extract.open(newline="") as f, sqlite3.connect(args.db) as conn:
        report = import_rows(csv.DictReader(f), conn)
    print(f"imported {report.imported}, rejected {len(report.rejected)}")
    for line_no, reason in report.rejected:
        print(f"  line {line_no}: {reason}")


if __name__ == "__main__":
    main()
