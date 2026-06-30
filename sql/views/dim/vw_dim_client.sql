-- dim_client: clientes com idade calculada (PK: client_id, FK: district_id)
SELECT
    client_id,
    district_id,
    gender,
    birth_date,
    TIMESTAMPDIFF(YEAR, birth_date, CURDATE()) AS idade_cliente
FROM client;
