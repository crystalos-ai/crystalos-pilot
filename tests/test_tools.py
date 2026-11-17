import csv
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import export_customers  # noqa: E402
import verify_statements  # noqa: E402

STATEMENTS = REPO_ROOT / "statements"


class VerifyStatementsTest(unittest.TestCase):
    def setUp(self):
        self.manifest = verify_statements.load_manifest()

    def test_every_statement_matches_the_manifest(self):
        files = sorted(STATEMENTS.glob("stmt-*.txt"))
        self.assertEqual(len(files), 60)
        self.assertEqual(sorted(self.manifest), [f.name for f in files])
        for path in files:
            self.assertEqual(verify_statements.verify_file(path, self.manifest, delay=0), "ok")

    def test_changed_statement_is_a_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / "stmt-001.txt"
            shutil.copy(STATEMENTS / "stmt-001.txt", copy)
            copy.write_text(copy.read_text().replace("Closing balance", "Closing balance: 0.00 GBP\n#"))
            self.assertEqual(verify_statements.verify_file(copy, self.manifest, delay=0), "MISMATCH")


class ExportCustomersTest(unittest.TestCase):
    def test_counts_every_customer(self):
        with (REPO_ROOT / "data" / "customers_sample.csv").open(newline="") as f:
            counts = export_customers.count_by_region(csv.DictReader(f))
        self.assertEqual(sum(counts.values()), 40)
        self.assertIn(export_customers.NO_REGION, counts)


if __name__ == "__main__":
    unittest.main()
