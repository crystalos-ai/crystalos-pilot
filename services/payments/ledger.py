"""Double-entry ledger for the payments service.

Every payment writes one row to `payments` and two rows to `ledger_entries`
(a debit and a credit of the same amount) in one transaction. Amounts are
integers in minor units (pence).
"""

import sqlite3
from pathlib import Path

SCHEMA = Path(__file__).with_name("schema.sql")


class LedgerError(ValueError):
    """A payment that the ledger refuses to post."""


def open_ledger(path):
    """Open (and if needed create) a SQLite ledger at `path`."""
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA.read_text())
    return conn


def open_account(conn, account_number, customer_id, opened_on):
    with conn:
        conn.execute(
            "INSERT INTO accounts (account_number, customer_id, opened_on) VALUES (?, ?, ?)",
            (account_number, customer_id, opened_on),
        )


def post_payment(conn, reference, debit_account, credit_account, amount_minor, currency="GBP"):
    """Move `amount_minor` from `debit_account` to `credit_account`. Returns the payment id."""
    if amount_minor <= 0:
        raise LedgerError("amount must be positive")
    if debit_account == credit_account:
        raise LedgerError("debit and credit account are the same")
    with conn:
        payment_id = conn.execute(
            "INSERT INTO payments (reference, currency, amount_minor) VALUES (?, ?, ?)",
            (reference, currency, amount_minor),
        ).lastrowid
        conn.executemany(
            "INSERT INTO ledger_entries (payment_id, account_number, direction, amount_minor)"
            " VALUES (?, ?, ?, ?)",
            [
                (payment_id, debit_account, "D", amount_minor),
                (payment_id, credit_account, "C", amount_minor),
            ],
        )
    return payment_id


def balance(conn, account_number):
    """Credits minus debits for one account, in minor units."""
    (total,) = conn.execute(
        "SELECT COALESCE(SUM(CASE direction WHEN 'C' THEN amount_minor ELSE -amount_minor END), 0)"
        " FROM ledger_entries WHERE account_number = ?",
        (account_number,),
    ).fetchone()
    return total
