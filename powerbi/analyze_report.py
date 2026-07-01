"""Parse PBIT report layout for pages and visual types."""
import json
import re
import sys
import zipfile
from pathlib import Path


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent / "desafio-analista-de-dados-myde-lucas-a-goncalves.pbit"
    with zipfile.ZipFile(path) as z:
        layout = json.loads(z.read("Report/Layout").decode("utf-16-le"))

    sections = layout.get("sections", [])
    print(f"Paginas: {len(sections)}")
    for i, sec in enumerate(sections):
        name = sec.get("displayName") or sec.get("name") or f"Page{i+1}"
        visuals = sec.get("visualContainers", [])
        print(f"\n--- {name} ({len(visuals)} visuais) ---")
        for v in visuals:
            cfg = v.get("config", "")
            if isinstance(cfg, dict):
                cfg = json.dumps(cfg)
            m = re.search(r'"visualType"\s*:\s*"([^"]+)"', cfg)
            vt = m.group(1) if m else "unknown"
            # try to find fields in singleVisual projections
            fields = re.findall(r'"Property"\s*:\s*"([^"]+)"', cfg)
            fields += re.findall(r'"queryRef"\s*:\s*"([^"]+)"', cfg)
            uniq = list(dict.fromkeys(fields))[:8]
            print(f"  {vt}: {', '.join(uniq) if uniq else '(sem campos parseados)'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
