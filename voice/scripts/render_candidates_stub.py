#!/usr/bin/env python3
from pathlib import Path
import json, wave, struct

QUEUE = Path("voice/orchestration/state/render_queue.json")
OUTDIR = Path("voice/output/candidates")

def write_silent_wav(path: Path, seconds: float = 1.0, rate: int = 48000):
    frames = int(seconds * rate)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(rate)
        silence = struct.pack("<h", 0)
        wf.writeframes(silence * frames)

def main() -> None:
    if not QUEUE.exists():
        raise SystemExit(f"Missing {QUEUE}")
    jobs = json.loads(QUEUE.read_text(encoding="utf-8"))
    OUTDIR.mkdir(parents=True, exist_ok=True)
    created = 0
    for job in jobs:
        path = Path(job["candidate_file"])
        if not path.exists():
            write_silent_wav(path)
            created += 1
    print(f"Created {created} placeholder candidate wav files in {OUTDIR}")
    print("Replace this stub with your real synthetic voice renderer on the Mac Mini.")

if __name__ == "__main__":
    main()
