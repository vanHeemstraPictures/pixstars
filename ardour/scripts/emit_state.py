#!/usr/bin/env python3
from pathlib import Path
import sys

STATE_FILE = Path("/tmp/pixstars_lamp_state.txt")
VALID = {"idle", "listening", "thinking", "speaking", "error"}

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: emit_state.py <state>")
    state = sys.argv[1].strip().lower()
    if state not in VALID:
        raise SystemExit(f"Invalid state: {state}")
    STATE_FILE.write_text(state, encoding="utf-8")
    print(f"State written: {state}")

if __name__ == "__main__":
    main()
