"""Detailed PBIT/PBIX model analysis for MYDE challenge."""
import json
import sys
import zipfile
from pathlib import Path

CALENDAR_NAMES = {"dim_calendar", "Calendario", "CalendarAuto", "DateTable"}


def load_schema(path: Path) -> dict:
    with zipfile.ZipFile(path) as z:
        if "DataModelSchema" not in z.namelist():
            raise SystemExit(f"{path.name}: exporte um .pbit para analisar.")
        return json.loads(z.read("DataModelSchema").decode("utf-16-le"))


def analyze(path: Path) -> dict:
    model = load_schema(path)["model"]
    tables = model.get("tables", [])
    rels = model.get("relationships", [])

    result = {
        "tables": [],
        "measures": [],
        "rels_core": [],
        "rels_calendar": [],
        "rels_local_date": [],
        "issues": [],
        "ok": [],
    }

    for t in tables:
        name = t["name"]
        if name.startswith("LocalDateTable"):
            continue
        measures = [{"table": name, "name": m["name"]} for m in t.get("measures", [])]
        result["measures"].extend(measures)
        part = t.get("partitions", [{}])[0]
        result["tables"].append(
            {
                "name": name,
                "mode": part.get("mode"),
                "cols": len(t.get("columns", [])),
                "hidden": t.get("isHidden", False),
            }
        )

    for r in rels:
        ft, fc, tt, tc = r["fromTable"], r["fromColumn"], r["toTable"], r["toColumn"]
        entry = {
            "from": f"{ft}[{fc}]",
            "to": f"{tt}[{tc}]",
            "active": r.get("isActive", True),
            "cross": r.get("crossFilteringBehavior", "oneDirection"),
        }
        if ft.startswith("LocalDateTable") or tt.startswith("LocalDateTable"):
            result["rels_local_date"].append(entry)
        elif ft in CALENDAR_NAMES or tt in CALENDAR_NAMES:
            result["rels_calendar"].append(entry)
        else:
            result["rels_core"].append(entry)

    names = {t["name"] for t in result["tables"]}
    expected = {
        "dim_district", "dim_client", "dim_account", "dim_disp", "dim_card",
        "fact_loan", "fact_trans", "fact_card_account", "fact_agg_carteira",
    }
    if expected <= names:
        result["ok"].append("9 tabelas dim/fact presentes")
    else:
        result["issues"].append(f"Faltam tabelas: {sorted(expected - names)}")

    if names & CALENDAR_NAMES:
        result["ok"].append(f"Calendario: {', '.join(sorted(names & CALENDAR_NAMES))}")
    else:
        result["issues"].append("Sem tabela de calendario")

    loan_cal = [r for r in result["rels_calendar"] if "fact_loan" in r["from"] or "fact_loan" in r["to"]]
    trans_cal = [r for r in result["rels_calendar"] if "fact_trans" in r["from"] or "fact_trans" in r["to"]]
    if loan_cal and loan_cal[0]["active"]:
        result["ok"].append("fact_loan -> dim_calendar ativo")
    else:
        result["issues"].append("Relacao fact_loan -> calendario ausente ou inativa")
    if trans_cal and not trans_cal[0]["active"]:
        result["ok"].append("fact_trans -> dim_calendar inativo (evita ambiguidade)")
    elif trans_cal and trans_cal[0]["active"]:
        result["issues"].append("fact_trans -> calendario ATIVO (risco de ambiguidade)")

    for r in result["rels_core"]:
        if r["cross"] == "bothDirections":
            result["issues"].append(f"Bidirecional: {r['from']} -> {r['to']}")
        if not r["active"]:
            result["issues"].append(f"Inativo: {r['from']} -> {r['to']}")

    if result["measures"]:
        result["ok"].append(f"{len(result['measures'])} medida(s) DAX")
    else:
        result["issues"].append("Nenhuma medida DAX criada")

    return result


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "desafio-analista-de-dados-myde-lucas-a-goncalves.pbit"
    r = analyze(path)
    print(f"=== {path.name} ===\n")
    print("TABELAS:")
    for t in r["tables"]:
        print(f"  {t['name']}: {t['mode']}, {t['cols']} cols")
    print("\nMEDIDAS:")
    if r["measures"]:
        for m in r["measures"]:
            print(f"  [{m['table']}] {m['name']}")
    else:
        print("  (nenhuma)")
    print("\nREL. CALENDARIO:")
    for x in r["rels_calendar"]:
        print(f"  {'ATIVO' if x['active'] else 'INATIVO':8} {x['from']} -> {x['to']}")
    print("\nREL. CORE:")
    for x in r["rels_core"]:
        print(f"  {'ATIVO' if x['active'] else 'INATIVO':8} {x['cross']:14} {x['from']} -> {x['to']}")
    print(f"\nLocalDateTable: {len(r['rels_local_date'])} relacoes (ocultar se possivel)")
    print("\nOK:")
    for x in r["ok"]:
        print(f"  + {x}")
    print("\nATENCAO:")
    for x in r["issues"]:
        print(f"  ! {x}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
