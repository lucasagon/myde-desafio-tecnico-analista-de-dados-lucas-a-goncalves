-- dim_disp: relacionamento cliente-conta (PK: disp_id)
SELECT
    disp_id,
    client_id,
    account_id,
    type AS disp_type
FROM disp;
