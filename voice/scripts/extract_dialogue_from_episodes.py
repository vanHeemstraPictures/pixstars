#!/usr/bin/env python3
from pathlib import Path
import csv
import re

ROOT = Path(".")
SOURCES = ROOT / "voice/orchestration/state/episode_sources.txt"
OUT = ROOT / "voice/data/dialogue.csv"

def guess_emotion(text: str) -> str:
    t = text.lower()
    if "?" in text:
        return "curious"
    if "please" in t or "stay" in t:
        return "fragile"
    if "remember" in t or "light" in t:
        return "warm"
    return "curious"

def filename_hint(idx: int, text: str, emotion: str) -> str:
    slug = "".join(c.lower() if c.isalnum() else "_" for c in text)[:40].strip("_")
    slug = re.sub(r"_+", "_", slug)
    return f"lamp_{idx:03d}_{slug}_{emotion}"

def extract_candidate_lines(markdown: str):
    lines = []
    for raw in markdown.splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        # heuristic: quoted dialogue or dialogue-ish short line
        if '"' in s:
            for m in re.findall(r'"([^"]+)"', s):
                if 0 < len(m) <= 140:
                    lines.append(m.strip())
        elif len(s) <= 100 and any(ch.isalpha() for ch in s) and s.endswith((".", "!", "?", "…")):
            lines.append(s)
    # de-dup preserve order
    seen = set()
    out = []
    for l in lines:
        if l not in seen:
            seen.add(l)
            out.append(l)
    return out

def main() -> None:
    if not SOURCES.exists():
        raise SystemExit(f"Missing {SOURCES}")
    source_paths = []
    for line in SOURCES.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        source_paths.append(ROOT / line)

    rows = []
    idx = 1
    for src in source_paths:
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8", errors="ignore")
        for line in extract_candidate_lines(text):
            emotion = guess_emotion(line)
            rows.append({
                "id": str(idx),
                "episode": src.stem,
                "scene": "",
                "text": line,
                "emotion": emotion,
                "delivery_notes": "Generated from episode source; review manually",
                "filename_hint": filename_hint(idx, line, emotion),
            })
            idx += 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "episode", "scene", "text", "emotion", "delivery_notes", "filename_hint"],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {OUT} with {len(rows)} rows")

if __name__ == "__main__":
    main()
