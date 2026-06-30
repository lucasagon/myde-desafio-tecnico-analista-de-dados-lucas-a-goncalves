-- dim_account: contas (PK: account_id, FK: district_id)
SELECT
    account_id,
    district_id,
    frequency AS statement_frequency,
    date AS account_open_date
FROM account;
