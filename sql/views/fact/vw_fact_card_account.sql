-- fact_card_account: 1 linha = 1 conta (grain por account_id do titular)
-- FKs: account_id, card_id (nullable)
SELECT
    a.account_id,
    c.card_id,
    CASE WHEN c.card_id IS NOT NULL THEN 1 ELSE 0 END AS possui_cartao,
    c.type AS card_type
FROM account a
LEFT JOIN disp d
    ON a.account_id = d.account_id
   AND d.type = 'OWNER'
LEFT JOIN card c ON d.disp_id = c.disp_id;
