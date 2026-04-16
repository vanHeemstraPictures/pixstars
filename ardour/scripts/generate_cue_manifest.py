#!/usr/bin/env python3
from pathlib import Path
import csv

VOICE_DIR = Path("voice/output/final_wav")
OUT = Path("ardour/cues/cue_manifest.csv")

def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wavs = sorted(VOICE_DIR.glob("*.wav"))
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["cue_id", "cue_label", "audio_file", "pre_state", "during_state", "post_state", "notes"])
        for idx, wav in enumerate(wavs, start=1):
            cue_id = f"cue_{idx:03d}"
            label = wav.stem
            writer.writerow([cue_id, label, str(wav), "thinking", "speaking", "idle", "auto-generated"])
    print(f"Wrote {OUT}")

if __name__ == "__main__":
    main()
