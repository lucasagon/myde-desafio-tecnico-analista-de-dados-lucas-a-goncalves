-- dim_card: cartões de crédito (PK: card_id, FK: disp_id)
SELECT
    card_id,
    disp_id,
    type AS card_type,
    issued AS card_issued_date
FROM card;
