"""Validate PBIT/PBIX data model tables and relationships."""
import json
import sys
import zipfile
from pathlib import Path

EXPECTED_TABLES = {
    "dim_district",
    "dim_client",
    "dim_account",
    "dim_disp",
    "dim_card",
    "fact_loan",
    "fact_trans",
    "fact_card_account",
    "fact_agg_carteira",
}

CALENDAR_TABLE_NAMES = {"Calendario", "CalendarAuto", "DateTable", "dim_calendar"}

EXPECTED_RELATIONSHIPS = [
    ("fact_loan", "district_id", "dim_district", "district_id"),
    ("fact_loan", "account_id", "dim_account", "account_id"),
    ("fact_loan", "loan_date", "Calendario", "Date"),
    ("fact_trans", "account_id", "dim_account", "account_id"),
    ("fact_trans", "trans_date", "Calendario", "Date"),
    ("fact_card_account", "account_id", "dim_account", "account_id"),
    ("fact_card_account", "card_id", "dim_card", "card_id"),
    ("fact_agg_carteira", "district_id", "dim_district", "district_id"),
    ("dim_client", "district_id", "dim_district", "district_id"),
    ("dim_disp", "client_id", "dim_client", "client_id"),
    ("dim_disp", "account_id", "dim_account", "account_id"),
    ("dim_card", "disp_id", "dim_disp", "disp_id"),
]

EXPECTED_ROW_COUNTS = {
    "dim_district": 77,
    "dim_client": 5369,
    "dim_account": 4500,
    "dim_disp": 5369,
    "dim_card": 892,
    "fact_loan": 682,
    "fact_trans": 1056320,
    "fact_card_account": 4500,
    "fact_agg_carteira": 648,
}


def load_schema(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        if "DataModelSchema" in z.namelist():
            return json.loads(z.read("DataModelSchema").decode("utf-16-le"))
        raise SystemExit(
            f"{path.name} usa formato DataModel compactado (.pbix recente). "
            "Exporte um .pbit (Arquivo > Exportar > Modelo do Power BI) para validar com este script."
        )


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "desafio-analista-de-dados-myde-lucas-a-goncalves.pbit"
    schema = load_schema(path)
    model = schema["model"]
    tables = model.get("tables", [])
    rels = model.get("relationships", [])

    print(f"Arquivo: {path.name}\n")
    print("=== TABELAS ===")
    actual_names = []
    for t in tables:
        name = t["name"]
        if name.startswith("LocalDateTable"):
            continue
        actual_names.append(name)
        cols = [c["name"] for c in t.get("columns", [])]
        part = t.get("partitions", [{}])[0]
        mode = part.get("mode", "?")
        rows = part.get("rows", "?")
        print(f"  {name}: mode={mode}, colunas={len(cols)}, linhas={rows}")

    print("\n=== PRESENCA DAS TABELAS ===")
    calendar_found = [n for n in actual_names if n in CALENDAR_TABLE_NAMES]
    for name in sorted(EXPECTED_TABLES):
        found = name in actual_names or any(
            name.replace("dim_", "vw_dim_").replace("fact_", "vw_fact_") == a for a in actual_names
        )
        print(f"  {'OK' if found else 'FALTANDO'}: {name}")
    if calendar_found:
        print(f"  OK (calendario): {', '.join(calendar_found)}")
    else:
        print("  FALTANDO: CalendarAuto / Calendario")
    extras = [n for n in actual_names if n not in EXPECTED_TABLES]
    if extras:
        print(f"  EXTRAS: {', '.join(extras)}")

    print("\n=== RELACIONAMENTOS ===")
    actual_rels = []
    for r in rels:
        ft, fc = r.get("fromTable"), r.get("fromColumn")
        tt, tc = r.get("toTable"), r.get("toColumn")
        active = r.get("isActive", True)
        cross = r.get("crossFilteringBehavior", "?")
        print(f"  {ft}[{fc}] -> {tt}[{tc}] | active={active} | cross={cross}")
        actual_rels.append((ft, fc, tt, tc))
        actual_rels.append((tt, tc, ft, fc))

    print("\n=== VALIDACAO RELACIONAMENTOS ESPERADOS ===")
    for rel in EXPECTED_RELATIONSHIPS:
        ok = rel in actual_rels
        print(f"  {'OK' if ok else 'FALTANDO/INVERTIDO'}: {rel[0]}[{rel[1]}] <-> {rel[2]}[{rel[3]}]")

    print("\n=== CONTAGEM DE LINHAS (se disponivel) ===")
    for t in tables:
        name = t["name"]
        if name.startswith("LocalDateTable") or name == "Calendario":
            continue
        part = t.get("partitions", [{}])[0]
        rows = part.get("rows")
        if rows is not None and name in EXPECTED_ROW_COUNTS:
            exp = EXPECTED_ROW_COUNTS[name]
            status = "OK" if rows == exp else f"DIVERGE (esperado {exp})"
            print(f"  {name}: {rows} -> {status}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
