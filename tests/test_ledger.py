import unittest

from services.payments import ledger
from services.payments.config import load_config, sqlite_path
from services.payments.maintenance.purge_test_rows import purge


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.conn = ledger.open_ledger(":memory:")
        ledger.open_account(self.conn, "MB-TEST-000001", "C-1", "2024-01-01")
        ledger.open_account(self.conn, "MB-TEST-000002", "C-2", "2024-01-01")

    def tearDown(self):
        self.conn.close()

    def test_payment_moves_money(self):
        ledger.post_payment(self.conn, "P-1", "MB-TEST-000001", "MB-TEST-000002", 2_500)
        self.assertEqual(ledger.balance(self.conn, "MB-TEST-000001"), -2_500)
        self.assertEqual(ledger.balance(self.conn, "MB-TEST-000002"), 2_500)

    def test_zero_amount_refused(self):
        with self.assertRaises(ledger.LedgerError):
            ledger.post_payment(self.conn, "P-1", "MB-TEST-000001", "MB-TEST-000002", 0)

    def test_same_account_refused(self):
        with self.assertRaises(ledger.LedgerError):
            ledger.post_payment(self.conn, "P-1", "MB-TEST-000001", "MB-TEST-000001", 100)

    def test_purge_removes_only_test_rows(self):
        ledger.post_payment(self.conn, "P-1", "MB-TEST-000001", "MB-TEST-000002", 100)
        ledger.post_payment(self.conn, "TEST-0001", "MB-TEST-000002", "MB-TEST-000001", 40)
        self.assertEqual(purge(self.conn), 1)
        self.assertEqual(ledger.balance(self.conn, "MB-TEST-000002"), 100)
        (entries,) = self.conn.execute("SELECT COUNT(*) FROM ledger_entries").fetchone()
        self.assertEqual(entries, 2)


class ConfigTest(unittest.TestCase):
    def test_local_config_is_sqlite(self):
        self.assertEqual(sqlite_path(load_config("local")).name, "payments-local.sqlite3")

    def test_production_config_is_not_opened_locally(self):
        with self.assertRaises(ValueError):
            sqlite_path(load_config("production"))

    def test_production_config_holds_no_password(self):
        settings = load_config("production")
        self.assertRegex(settings["DATABASE_URL"], r"^postgresql://[^:@/]+@")
        self.assertEqual(settings["DATABASE_PASSWORD_ENV"], "PAYMENTS_DB_PASSWORD")


if __name__ == "__main__":
    unittest.main()
