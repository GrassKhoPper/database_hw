CREATE SCHEMA IF NOT EXISTS bank;

CREATE TABLE IF NOT EXISTS bank.accounts (
    id SERIAL PRIMARY KEY,
    balance INTEGER NOT NULL DEFAULT 0,
    uuid TEXT NOT NULL UNIQUE,
    phash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bank.transactions (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount INTEGER NOT NULL,
    user_id INTEGER REFERENCES bank.accounts (id) ON DELETE SET NULL,
    account_uuid_snapshot TEXT NOT NULL,

    FOREIGN KEY (user_id) REFERENCES bank.accounts
);

CREATE OR REPLACE VIEW bank.current_balance AS
SELECT
    a.id,
    a.uuid,
    COALESCE(SUM(t.amount), 0) AS balance
FROM bank.accounts AS a
LEFT JOIN bank.transactions AS t ON a.id = t.user_id
GROUP BY a.id, a.uuid;

CREATE OR REPLACE VIEW bank.all_transactions_view AS
SELECT
    t.id,
    t.ts,
    t.amount,
    t.user_id,
    COALESCE(a.uuid, t.account_uuid_snapshot) AS related_account_uuid,
    (a.id IS NULL) AS is_account_deleted
FROM bank.transactions AS t
LEFT JOIN bank.accounts AS a ON t.user_id = a.id;
