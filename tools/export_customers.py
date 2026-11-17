"""Write a customer count by region to out/customers_by_region.csv.

Reads data/customers_sample.csv. The report stays on this machine.

    python3 tools/export_customers.py [--source FILE] [--out FILE]
"""

import argparse
import csv
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
NO_REGION = "(none)"


def count_by_region(rows):
    return Counter((row["region"] or "").strip() or NO_REGION for row in rows)


def write_report(counts, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["region", "customers"])
        writer.writerows(sorted(counts.items()))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Customer count by region.")
    parser.add_argument("--source", type=Path, default=REPO_ROOT / "data" / "customers_sample.csv")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "out" / "customers_by_region.csv")
    args = parser.parse_args(argv)
    with args.source.open(newline="") as f:
        counts = count_by_region(csv.DictReader(f))
    write_report(counts, args.out)
    print(f"wrote {sum(counts.values())} customers in {len(counts)} regions to {args.out}")


if __name__ == "__main__":
    main()
