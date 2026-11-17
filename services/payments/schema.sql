-- Payments ledger schema. Amounts are integers in minor units (pence).

CREATE TABLE IF NOT EXISTS accounts (
    account_number TEXT PRIMARY KEY,
    customer_id    TEXT NOT NULL,
    opened_on      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id           INTEGER PRIMARY KEY,
    reference    TEXT NOT NULL UNIQUE,
    currency     TEXT NOT NULL,
    amount_minor INTEGER NOT NULL CHECK (amount_minor > 0),
    created_at   TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ledger_entries (
    id             INTEGER PRIMARY KEY,
    payment_id     INTEGER NOT NULL REFERENCES payments(id) ON DELETE CASCADE,
    account_number TEXT NOT NULL REFERENCES accounts(account_number),
    direction      TEXT NOT NULL CHECK (direction IN ('D', 'C')),
    amount_minor   INTEGER NOT NULL CHECK (amount_minor > 0)
);
