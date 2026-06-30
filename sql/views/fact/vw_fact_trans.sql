-- fact_trans: 1 linha = 1 transação (FKs: account_id, trans_date)
-- Atenção: ~1M linhas — usar modo Import no Power BI
SELECT
    trans_id,
    account_id,
    date AS trans_date,
    type AS trans_type,
    operation AS trans_operation,
    amount,
    balance,
    k_symbol
FROM trans;
