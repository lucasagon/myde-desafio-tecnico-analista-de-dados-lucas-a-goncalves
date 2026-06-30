-- dim_district: atributos demográficos por região (PK: district_id)
SELECT
    district_id,
    A2 AS district_name,
    A3 AS region_name,
    A4 AS inhabitants,
    A5 AS municipalities_lt_499,
    A6 AS municipalities_500_1999,
    A7 AS municipalities_2000_9999,
    A8 AS municipalities_gt_10000,
    A9 AS cities,
    A10 AS urban_ratio,
    A11 AS avg_salary,
    A12 AS unemployment_1995,
    A13 AS unemployment_1996,
    A14 AS entrepreneurs_per_1000,
    A15 AS crimes_1995,
    A16 AS crimes_1996
FROM district;
