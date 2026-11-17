import sqlite3
import unittest

from etl.import_rows import import_rows


def row(customer_id="C-9001", region="North", **overrides):
    values = {
        "customer_id": customer_id,
        "full_name": "Alex Testwell",
        "email": "alex.testwell@example.com",
        "account_number": "MB-TEST-009001",
        "region": region,
        "opened_on": "2024-01-02",
    }
    values.update(overrides)
    return values


class ImportTest(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")

    def tearDown(self):
        self.conn.close()

    def stored(self, customer_id):
        return self.conn.execute(
            "SELECT region, queue FROM customers WHERE customer_id = ?", (customer_id,)
        ).fetchone()

    def test_rows_go_to_their_region_queue(self):
        report = import_rows([row("C-1", "North"), row("C-2", "South")], self.conn)
        self.assertEqual(report.imported, 2)
        self.assertEqual(self.stored("C-1"), ("North", "branch-north"))
        self.assertEqual(self.stored("C-2"), ("South", "branch-south"))

    def test_missing_email_rejected(self):
        report = import_rows([row(email=" ")], self.conn)
        self.assertEqual(report.imported, 0)
        self.assertEqual(report.rejected, [(2, "missing email")])

    def test_unknown_region_rejected(self):
        report = import_rows([row(region="Atlantis")], self.conn)
        self.assertEqual(report.imported, 0)
        self.assertEqual(report.rejected, [(2, "unknown region 'Atlantis'")])

    def test_reimport_updates_customer(self):
        import_rows([row(region="North")], self.conn)
        import_rows([row(region="West")], self.conn)
        self.assertEqual(self.stored("C-9001"), ("West", "branch-west"))

    def test_empty_region_imported(self):
        report = import_rows([row("C-1", "North"), row("C-2", "")], self.conn)
        self.assertEqual(report.imported, 2)
        self.assertEqual(report.rejected, [])
        self.assertEqual(self.stored("C-2"), ("UNASSIGNED", "head-office-review"))


if __name__ == "__main__":
    unittest.main()
