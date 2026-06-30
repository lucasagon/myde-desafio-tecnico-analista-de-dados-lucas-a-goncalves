"""Build minimal Power BI report package from exported CSVs (Tabular model as PBIP)."""
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
PBIP = ROOT / "carteira_credito.pbip"
SEMANTIC = ROOT / "carteira_credito.SemanticModel"
REPORT = ROOT / "carteira_credito.Report"

TABLE_MAP = {
    "vw_dim_district": "dim_district",
    "vw_dim_client": "dim_client",
    "vw_dim_account": "dim_account",
    "vw_dim_disp": "dim_disp",
    "vw_dim_card": "dim_card",
    "vw_fact_loan": "fact_loan",
    "vw_fact_agg_carteira": "fact_agg_carteira",
    "vw_fact_card_account": "fact_card_account",
}

def main():
    if PBIP.exists():
        shutil.rmtree(PBIP.parent / "carteira_credito.SemanticModel", ignore_errors=True)
        shutil.rmtree(PBIP.parent / "carteira_credito.Report", ignore_errors=True)
        PBIP.unlink(missing_ok=True)

    SEMANTIC.mkdir(parents=True, exist_ok=True)
    (SEMANTIC / "definition").mkdir(exist_ok=True)
    REPORT.mkdir(parents=True, exist_ok=True)

  # PBIP manifest
    PBIP.write_text(json.dumps({
        "version": "1.0",
        "artifacts": [
            {"report": {"path": "carteira_credito.Report"}},
            {"dataset": {"path": "carteira_credito.SemanticModel"}},
        ],
        "settings": {"enableAutoRecovery": True},
    }, indent=2), encoding="utf-8")

    # Semantic model placeholder (open in Power BI Desktop to bind CSVs)
    (SEMANTIC / "definition.pbism").write_text(json.dumps({
        "version": "4.0",
        "settings": {},
    }), encoding="utf-8")

    readme = ROOT / "PBIX_BUILD.txt"
    readme.write_text("""
Para gerar carteira_credito.pbix:
1. Abra Power BI Desktop
2. Obter dados > Texto/CSV > selecione todos os arquivos em powerbi/data/
3. Renomeie tabelas conforme docs/POWERBI.md
4. Cole medidas de powerbi/medidas.dax
5. Crie relacionamentos FK e paginas de relatorio
6. Salvar como powerbi/carteira_credito.pbix

CSVs ja exportados por: python powerbi/export_views.py
""".strip(), encoding="utf-8")
    print("PBIP scaffold created. Follow PBIX_BUILD.txt for final .pbix in Desktop.")

if __name__ == "__main__":
    main()
