-- fact_agg_carteira: fato agregada (grain: district × mês × status × faixa)
SELECT
    a.district_id,
    DATE_FORMAT(l.date, '%Y-%m-01') AS periodo_mes,
    l.status,
    CASE
        WHEN l.amount < 50000 THEN 'Pequeno'
        WHEN l.amount BETWEEN 50000 AND 150000 THEN 'Médio'
        ELSE 'Grande'
    END AS faixa_valor,
    COUNT(*) AS qtd_emprestimos,
    SUM(l.amount) AS valor_total,
    ROUND(AVG(l.amount), 2) AS valor_medio,
    ROUND(
        100.0 * SUM(CASE WHEN l.status IN ('B', 'D') THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS taxa_inadimplencia_pct
FROM loan l
INNER JOIN account a ON l.account_id = a.account_id
GROUP BY
    a.district_id,
    DATE_FORMAT(l.date, '%Y-%m-01'),
    l.status,
    CASE
        WHEN l.amount < 50000 THEN 'Pequeno'
        WHEN l.amount BETWEEN 50000 AND 150000 THEN 'Médio'
        ELSE 'Grande'
    END;
