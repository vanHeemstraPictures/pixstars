#!/usr/bin/env python3
from pathlib import Path
import csv, json, wave, math

QUEUE = Path("voice/orchestration/state/render_queue.json")
OUT = Path("voice/orchestration/state/evaluation.csv")
POLICY = Path("voice/config/review_policy.json")

def duration_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as wf:
        return wf.getnframes() / float(wf.getframerate())

def score_candidate(path: Path, emotion: str) -> tuple[float, list[str]]:
    notes = []
    score = 0.5

    try:
        dur = duration_seconds(path)
    except Exception:
        return 0.0, ["unreadable_wav"]

    if 0.4 <= dur <= 6.0:
        score += 0.2
        notes.append("duration_ok")
    else:
        notes.append("duration_suspicious")

    # very lightweight heuristics for a first operational review layer
    if emotion in {"curious", "warm", "fragile", "hopeful"}:
        score += 0.1
        notes.append("emotion_known")
    else:
        notes.append("emotion_unknown")

    size = path.stat().st_size
    if size > 1000:
        score += 0.15
        notes.append("nontrivial_file")
    else:
        notes.append("file_too_small")

    # keep within [0, 1]
    score = max(0.0, min(1.0, score))
    return round(score, 2), notes

def main() -> None:
    if not QUEUE.exists():
        raise SystemExit(f"Missing {QUEUE}")
    policy = json.loads(POLICY.read_text(encoding="utf-8")) if POLICY.exists() else {
        "auto_approve_min_score": 0.9,
        "human_review_min_score": 0.75
    }

    jobs = json.loads(QUEUE.read_text(encoding="utf-8"))
    rows = []
    for job in jobs:
        path = Path(job["candidate_file"])
        if not path.exists():
            rows.append([job["id"], str(path), 0.0, "missing", "missing_file"])
            continue

        score, notes = score_candidate(path, job["emotion"])
        if score >= policy.get("auto_approve_min_score", 0.9):
            status = "approved"
        elif score >= policy.get("human_review_min_score", 0.75):
            status = "review"
        else:
            status = "rejected"

        rows.append([job["id"], str(path), score, status, ";".join(notes)])

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "filename", "score", "status", "notes"])
        writer.writerows(rows)
    print(f"Wrote {OUT}")
