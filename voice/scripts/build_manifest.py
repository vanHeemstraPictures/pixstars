#!/usr/bin/env python3
from pathlib import Path
import csv
import json

SRC = Path("voice/data/dialogue.csv")
OUT = Path("voice/output/dialogue_manifest.json")

def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing {SRC}")
    rows = []
    with SRC.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
