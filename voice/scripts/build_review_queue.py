#!/usr/bin/env python3
from pathlib import Path
import csv, shutil

EVAL = Path("voice/orchestration/state/evaluation.csv")
APPROVED = Path("voice/review/approved")
REVIEW = Path("voice/review/needs_human_review")
REJECTED = Path("voice/review/rejected")

def clear_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)
    for p in path.iterdir():
        if p.is_file():
            p.unlink()

def main() -> None:
    if not EVAL.exists():
        raise SystemExit(f"Missing {EVAL}")

    for d in [APPROVED, REVIEW, REJECTED]:
        clear_dir(d)

    counts = {"approved": 0, "review": 0, "rejected": 0}
    with EVAL.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src = Path(row["filename"])
            if not src.exists():
                continue

            if row["status"] == "approved":
                dst = APPROVED / src.name
                counts["approved"] += 1
            elif row["status"] == "review":
                dst = REVIEW / src.name
                counts["review"] += 1
            else:
                dst = REJECTED / src.name
                counts["rejected"] += 1

            shutil.copy2(src, dst)

    print(f"Review queue built: {counts}")
