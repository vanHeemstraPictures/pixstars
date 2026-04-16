#!/usr/bin/env python3
from pathlib import Path
import csv

EVAL = Path("voice/orchestration/state/evaluation.csv")

def main() -> None:
    if not EVAL.exists():
        raise SystemExit(f"Missing {EVAL}")

    totals = {"approved": 0, "review": 0, "rejected": 0, "missing": 0}
    with EVAL.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            totals[row["status"]] = totals.get(row["status"], 0) + 1

    print("Review summary:")
    for k, v in totals.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
