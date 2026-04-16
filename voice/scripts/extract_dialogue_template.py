#!/usr/bin/env python3
from pathlib import Path
import csv

INPUT_HINT = Path("voice/config/dialogue.csv.example")
OUTPUT_PATH = Path("voice/data/dialogue.csv")

def main() -> None:
    if OUTPUT_PATH.exists():
        print(f"{OUTPUT_PATH} already exists")
        return
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(INPUT_HINT.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Created starter dialogue file at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
