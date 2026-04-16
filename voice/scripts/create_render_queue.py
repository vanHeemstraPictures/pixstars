#!/usr/bin/env python3
from pathlib import Path
import csv, json

DIALOGUE = Path("voice/data/dialogue.csv")
OUT = Path("voice/orchestration/state/render_queue.json")
CANDIDATES = Path("voice/output/candidates")

def main() -> None:
    if not DIALOGUE.exists():
        raise SystemExit(f"Missing {DIALOGUE}")
    jobs = []
    with DIALOGUE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stem = row["filename_hint"]
            target = CANDIDATES / f"{stem}.wav"
            status = "done" if target.exists() else "pending"
            jobs.append({
                "id": row["id"],
                "text": row["text"],
                "emotion": row["emotion"],
                "filename_hint": stem,
                "candidate_file": str(target),
                "status": status
            })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(jobs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT} with {len(jobs)} jobs")

if __name__ == "__main__":
    main()
