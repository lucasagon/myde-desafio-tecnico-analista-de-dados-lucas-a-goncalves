-- =============================================================================
-- MYDE — Desafio Técnico Analista de Dados
-- Parte 1: Consultas analíticas (9 questões)
-- Banco: financial @ relational.fel.cvut.cz
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1. Contas por região
-- Quantas contas existem por região? (JOIN account + district)
-- -----------------------------------------------------------------------------
WITH contas_por_regiao AS (
    SELECT
        d.district_id,
        d.A2 AS district_name,
        d.A3 AS region_name,
        COUNT(a.account_id) AS qtd_contas
    FROM account a
    INNER JOIN district d ON a.district_id = d.district_id
    GROUP BY d.district_id, d.A2, d.A3
)
SELECT *
FROM contas_por_regiao
ORDER BY qtd_contas DESC;


-- -----------------------------------------------------------------------------
-- 2. Carteira de crédito por status
-- Quantidade, valor total e valor médio por status de empréstimo
-- -----------------------------------------------------------------------------
WITH carteira_status AS (
    SELECT
        status,
        COUNT(*) AS qtd_emprestimos,
        SUM(amount) AS valor_total,
        ROUND(AVG(amount), 2) AS valor_medio
    FROM loan
    GROUP BY status
)
SELECT *
FROM carteira_status
ORDER BY status;


-- -----------------------------------------------------------------------------
-- 3. Taxa de inadimplência
-- Percentual de empréstimos "maus" (B ou D) sobre o total
-- -----------------------------------------------------------------------------
WITH classificacao AS (
    SELECT
        loan_id,
        CASE WHEN status IN ('B', 'D') THEN 1 ELSE 0 END AS flag_mau
    FROM loan
),
totais AS (
    SELECT
        COUNT(*) AS total_emprestimos,
        SUM(flag_mau) AS qtd_maus
    FROM classificacao
)
SELECT
    total_emprestimos,
    qtd_maus,
    ROUND(100.0 * qtd_maus / total_emprestimos, 2) AS taxa_inadimplencia_pct
FROM totais;


-- -----------------------------------------------------------------------------
-- 4. Saldo atual por conta (top 10)
-- Saldo da última transação por data para cada conta
-- -----------------------------------------------------------------------------
WITH ultima_transacao AS (
    SELECT
        t.account_id,
        t.balance,
        t.date,
        ROW_NUMBER() OVER (
            PARTITION BY t.account_id
            ORDER BY t.date DESC, t.trans_id DESC
        ) AS rn
    FROM trans t
),
saldo_atual AS (
    SELECT account_id, balance AS saldo_atual, date AS data_ultima_transacao
    FROM ultima_transacao
    WHERE rn = 1
)
SELECT
    account_id,
    saldo_atual,
    data_ultima_transacao
FROM saldo_atual
ORDER BY saldo_atual DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- 5. Faixas de empréstimo (CASE) — taxa de inadimplência por faixa
-- Pequeno < 50k | Médio 50k–150k | Grande > 150k
-- -----------------------------------------------------------------------------
WITH emprestimos_faixa AS (
    SELECT
        loan_id,
        amount,
        status,
        CASE
            WHEN amount < 50000 THEN 'Pequeno'
            WHEN amount BETWEEN 50000 AND 150000 THEN 'Médio'
            ELSE 'Grande'
        END AS faixa_valor,
        CASE WHEN status IN ('B', 'D') THEN 1 ELSE 0 END AS flag_mau
    FROM loan
)
SELECT
    faixa_valor,
    COUNT(*) AS qtd_emprestimos,
    SUM(flag_mau) AS qtd_maus,
    ROUND(100.0 * SUM(flag_mau) / COUNT(*), 2) AS taxa_inadimplencia_pct
FROM emprestimos_faixa
GROUP BY faixa_valor
ORDER BY FIELD(faixa_valor, 'Pequeno', 'Médio', 'Grande');


-- -----------------------------------------------------------------------------
-- 6. Risco x perfil da região
-- Taxa de inadimplência por distrito vs salário médio e desemprego
-- -----------------------------------------------------------------------------
WITH emprestimos_regiao AS (
    SELECT
        a.district_id,
        l.loan_id,
        CASE WHEN l.status IN ('B', 'D') THEN 1 ELSE 0 END AS flag_mau
    FROM loan l
    INNER JOIN account a ON l.account_id = a.account_id
),
agg_regiao AS (
    SELECT
        district_id,
        COUNT(*) AS qtd_emprestimos,
        ROUND(100.0 * SUM(flag_mau) / COUNT(*), 2) AS taxa_inadimplencia_pct
    FROM emprestimos_regiao
    GROUP BY district_id
)
SELECT
    d.district_id,
    d.A2 AS district_name,
    d.A11 AS avg_salary,
    d.A12 AS unemployment_1995,
    d.A13 AS unemployment_1996,
    r.qtd_emprestimos,
    r.taxa_inadimplencia_pct
FROM agg_regiao r
INNER JOIN district d ON r.district_id = d.district_id
ORDER BY r.taxa_inadimplencia_pct DESC;


-- -----------------------------------------------------------------------------
-- 7. Window function — ranking do valor do empréstimo dentro da região
-- -----------------------------------------------------------------------------
WITH emprestimos_regiao AS (
    SELECT
        l.loan_id,
        l.amount,
        a.district_id,
        d.A2 AS district_name
    FROM loan l
    INNER JOIN account a ON l.account_id = a.account_id
    INNER JOIN district d ON a.district_id = d.district_id
)
SELECT
    loan_id,
    district_id,
    district_name,
    amount,
    RANK() OVER (
        PARTITION BY district_id
        ORDER BY amount DESC
    ) AS ranking_regiao
FROM emprestimos_regiao
ORDER BY district_id, ranking_regiao;


-- -----------------------------------------------------------------------------
-- 8. Subquery/CTE — contas com saldo médio acima da média do distrito
-- -----------------------------------------------------------------------------
WITH saldo_por_conta AS (
    SELECT
        t.account_id,
        a.district_id,
        AVG(t.balance) AS saldo_medio_conta
    FROM trans t
    INNER JOIN account a ON t.account_id = a.account_id
    GROUP BY t.account_id, a.district_id
),
media_distrito AS (
    SELECT
        district_id,
        AVG(saldo_medio_conta) AS saldo_medio_distrito
    FROM saldo_por_conta
    GROUP BY district_id
)
SELECT
    sc.account_id,
    sc.district_id,
    ROUND(sc.saldo_medio_conta, 2) AS saldo_medio_conta,
    ROUND(md.saldo_medio_distrito, 2) AS saldo_medio_distrito
FROM saldo_por_conta sc
INNER JOIN media_distrito md ON sc.district_id = md.district_id
WHERE sc.saldo_medio_conta > md.saldo_medio_distrito
ORDER BY sc.district_id, sc.saldo_medio_conta DESC;


-- -----------------------------------------------------------------------------
-- 9. Cartões e risco — inadimplência com vs sem cartão de crédito
-- card → disp → account → loan
-- -----------------------------------------------------------------------------
WITH contas_cartao AS (
    SELECT DISTINCT
        d.account_id,
        1 AS possui_cartao
    FROM card c
    INNER JOIN disp d ON c.disp_id = d.disp_id
),
emprestimos_conta AS (
    SELECT
        l.loan_id,
        l.account_id,
        CASE WHEN l.status IN ('B', 'D') THEN 1 ELSE 0 END AS flag_mau,
        COALESCE(cc.possui_cartao, 0) AS possui_cartao
    FROM loan l
    LEFT JOIN contas_cartao cc ON l.account_id = cc.account_id
)
SELECT
    CASE possui_cartao WHEN 1 THEN 'Com cartão' ELSE 'Sem cartão' END AS grupo_cartao,
    COUNT(*) AS qtd_emprestimos,
    SUM(flag_mau) AS qtd_maus,
    ROUND(100.0 * SUM(flag_mau) / COUNT(*), 2) AS taxa_inadimplencia_pct
FROM emprestimos_conta
GROUP BY possui_cartao
ORDER BY possui_cartao DESC;
