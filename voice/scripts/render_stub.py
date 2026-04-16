#!/usr/bin/env python3
from pathlib import Path
import csv

SRC = Path("voice/data/dialogue.csv")
OUT_DIR = Path("voice/output/final_wav")

def slugify(text: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in text).strip("_")

def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Missing {SRC}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    with SRC.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stem = row.get("filename_hint") or f"{row.get('id','x')}_{slugify(row.get('text','line'))}"
            placeholder = OUT_DIR / f"{stem}.txt"
            placeholder.write_text(
                "\n".join([
                    "PLACEHOLDER FOR RENDERED WAV",
                    f"text={row.get('text','')}",
                    f"emotion={row.get('emotion','')}",
                    f"delivery_notes={row.get('delivery_notes','')}",
                ]),
                encoding="utf-8",
            )
    print(f"Created render placeholders in {OUT_DIR}")

if __name__ == "__main__":
    main()
