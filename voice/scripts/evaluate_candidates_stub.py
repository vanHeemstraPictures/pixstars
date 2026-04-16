#!/usr/bin/env python3
from pathlib import Path
import csv, json, random

QUEUE = Path("voice/orchestration/state/render_queue.json")
OUT = Path("voice/orchestration/state/evaluation.csv")

def main() -> None:
    if not QUEUE.exists():
        raise SystemExit(f"Missing {QUEUE}")
    jobs = json.loads(QUEUE.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "filename", "score", "status", "notes"])
        for job in jobs:
            score = round(random.uniform(0.55, 0.95), 2)
            status = "approved" if score >= 0.75 else "review"
            notes = "Stub score; replace with real evaluation"
            writer.writerow([job["id"], job["candidate_file"], score, status, notes])
    print(f"Wrote {OUT}")
    print("Replace this stub with your real evaluator or human-in-the-loop scoring.")

if __name__ == "__main__":
    main()
