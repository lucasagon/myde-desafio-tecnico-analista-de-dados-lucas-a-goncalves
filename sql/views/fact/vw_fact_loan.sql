-- fact_loan: 1 linha = 1 empréstimo (FKs: account_id, district_id, loan_date)
SELECT
    l.loan_id,
    l.account_id,
    a.district_id,
    l.date AS loan_date,
    l.amount,
    l.duration,
    l.payments,
    l.status,
    CASE WHEN l.status IN ('A', 'C') THEN 'bom' ELSE 'mau' END AS status_grupo,
    CASE
        WHEN l.amount < 50000 THEN 'Pequeno'
        WHEN l.amount BETWEEN 50000 AND 150000 THEN 'Médio'
        ELSE 'Grande'
    END AS faixa_valor
FROM loan l
INNER JOIN account a ON l.account_id = a.account_id;
