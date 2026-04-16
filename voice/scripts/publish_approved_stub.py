#!/usr/bin/env python3
from pathlib import Path
import csv, shutil
from datetime import datetime

EVAL = Path("voice/orchestration/state/evaluation.csv")
PUB = Path("voice/orchestration/state/published.csv")
FINAL = Path("voice/output/final_wav")

def main() -> None:
    if not EVAL.exists():
        raise SystemExit(f"Missing {EVAL}")
    FINAL.mkdir(parents=True, exist_ok=True)
    published_rows = []
    with EVAL.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"] != "approved":
                continue
            src = Path(row["filename"])
            if not src.exists():
                continue
            target = FINAL / src.name
            shutil.copy2(src, target)
            published_rows.append({
                "id": row["id"],
                "source_file": str(src),
                "target_file": str(target),
                "published_at": datetime.utcnow().isoformat() + "Z",
                "notes": "Published by stub publisher"
            })

    with PUB.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "source_file", "target_file", "published_at", "notes"])
        writer.writeheader()
        writer.writerows(published_rows)
    print(f"Published {len(published_rows)} approved files to {FINAL}")

if __name__ == "__main__":
    main()
