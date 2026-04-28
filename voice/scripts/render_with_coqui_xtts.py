#!/usr/bin/env python3
from pathlib import Path
import argparse
import json
import subprocess
import sys

CFG = Path("voice/config/coqui_xtts_backend.json")

def load_cfg():
    if not CFG.exists():
        raise SystemExit(
            f"Missing {CFG}. Copy voice/config/coqui_xtts_backend.json.example to "
            f"voice/config/coqui_xtts_backend.json first."
        )
    return json.loads(CFG.read_text(encoding="utf-8"))

def parse_json_arg(raw: str) -> str:
    try:
        return json.loads(raw)
    except Exception:
        return raw

def list_reference_wavs(ref_dir: Path):
    return sorted(ref_dir.glob("*.wav"))

def synthesize(text: str, emotion: str, output: Path, cfg: dict):
    output.parent.mkdir(parents=True, exist_ok=True)

    model_name = cfg["model_name"]
    language_idx = cfg.get("language_idx", "en")
    speaker_id = cfg.get("speaker_id", "lamp_et_inspired")
    reference_dir = Path(cfg.get("reference_wavs_dir", "voice/reference_audio"))
    voice_dir = Path(cfg.get("voice_dir", "voice/models/coqui_cached_voices"))
    voice_dir.mkdir(parents=True, exist_ok=True)

    refs = list_reference_wavs(reference_dir)

    # emotional text shaping
    shaped_text = text
    if emotion == "fragile" and not text.startswith("..."):
        shaped_text = "... " + text
    elif emotion == "warm" and not text.endswith("..."):
        shaped_text = text + " ..."
    elif emotion == "curious" and "?" not in text and not text.endswith("..."):
        shaped_text = text + "..."

    base_cmd = [
        "tts",
        "--model_name", model_name,
        "--text", shaped_text,
        "--language_idx", language_idx,
        "--out_path", str(output),
    ]

    # first run: clone/cache if refs exist
    if refs:
        cmd = base_cmd + ["--speaker_wav"] + [str(p) for p in refs]
    else:
        # reuse cached speaker if already present, else fall back to speaker id only
        cmd = base_cmd + ["--speaker_idx", speaker_id]

    env = dict(**dict())
    subprocess.run(cmd, check=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="JSON-encoded or plain text")
    parser.add_argument("--emotion", required=True, help="JSON-encoded or plain emotion label")
    parser.add_argument("--output", required=True, help="JSON-encoded or plain output wav path")
    args = parser.parse_args()

    text = parse_json_arg(args.text)
    emotion = parse_json_arg(args.emotion)
    output = Path(parse_json_arg(args.output))

    cfg = load_cfg()
    synthesize(text, emotion, output, cfg)
    print(f"Rendered {output}")

if __name__ == "__main__":
    main()
