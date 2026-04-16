#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, shlex, os, wave, struct

QUEUE = Path("voice/orchestration/state/render_queue.json")
CFG = Path("voice/config/render_backend.json")
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
    if not CFG.exists():
        raise SystemExit(f"Missing {CFG}. Copy voice/config/render_backend.json.example to voice/config/render_backend.json first.")

    cfg = json.loads(CFG.read_text(encoding="utf-8"))
    backend = cfg.get("backend", "command")
    template = cfg.get("command_template", "")

    jobs = json.loads(QUEUE.read_text(encoding="utf-8"))
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rendered = 0
    skipped = 0

    for job in jobs:
        out_path = Path(job["candidate_file"])
        if out_path.exists():
            skipped += 1
            continue
        out_path.parent.mkdir(parents=True, exist_ok=True)

        text_json = json.dumps(job["text"], ensure_ascii=False)
        emotion_json = json.dumps(job["emotion"], ensure_ascii=False)
        output_json = json.dumps(str(out_path))

        if backend == "command" and template:
            cmd = template.format(
                text_json=text_json,
                emotion_json=emotion_json,
                output_json=output_json
            )
            try:
                subprocess.run(cmd, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                raise SystemExit(f"Render command failed for {out_path}: {e}")
            if not out_path.exists():
                raise SystemExit(f"Renderer completed but did not create {out_path}")
            rendered += 1
        else:
            # Safe fallback for first bootstrapping
            write_silent_wav(out_path)
            rendered += 1

    print(f"Rendered {rendered} candidate files, skipped {skipped}.")
