#!/usr/bin/env python3
from pathlib import Path
import csv, shutil
from datetime import datetime

APPROVED = Path("voice/review/approved")
FINAL = Path("voice/output/final_wav")
PUB = Path("voice/orchestration/state/published.csv")

def main() -> None:
    APPROVED.mkdir(parents=True, exist_ok=True)
    FINAL.mkdir(parents=True, exist_ok=True)

    rows = []
    count = 0
    for src in sorted(APPROVED.glob("*.wav")):
        dst = FINAL / src.name
        shutil.copy2(src, dst)
        count += 1
        rows.append({
            "id": src.stem,
            "source_file": str(src),
            "target_file": str(dst),
            "published_at": datetime.utcnow().isoformat() + "Z",
            "notes": "Published from review-approved bucket"
        })

    with PUB.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "source_file", "target_file", "published_at", "notes"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Published {count} approved files to {FINAL}")
