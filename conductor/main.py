#!/usr/bin/env python3
"""
Pixstars Show Conductor — Main Entry Point

The show conductor is the master timeline for the Pixstars performance.
It reads a timeline of cues and dispatches OSC messages to all subsystems
at the correct times.

Usage:
    source .venv/bin/activate
    python -m conductor.main              # Run the show (live)
    python -m conductor.main --dry-run    # Print all cues without sending OSC
"""

import argparse
import sys
import time
from pathlib import Path

import yaml

from conductor.osc_sender import OSCSender
from conductor.ardour_osc import ArdourOSC
from conductor import config


def load_timeline(path: str) -> list[dict]:
    """Load and validate the timeline YAML file.

    Returns a sorted list of cue dicts.
    """
    timeline_path = Path(path)
    if not timeline_path.exists():
        print(f"ERROR: Timeline file not found: {path}")
        sys.exit(1)

    with open(timeline_path) as f:
        data = yaml.safe_load(f)

    cues = data.get("cues", [])
    if not cues:
        print("ERROR: No cues found in timeline")
        sys.exit(1)

    # Sort by time
    cues.sort(key=lambda c: c["time"])
    return cues


def format_time(seconds: float) -> str:
    """Format seconds as MM:SS.s"""
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{s:05.2f}"


def run_show(cues: list[dict], sender: OSCSender, ardour: ArdourOSC, dry_run: bool = False):
    """Run through the show timeline, dispatching cues at the correct times.

    In dry-run mode, prints all cues immediately without waiting.
    """
    total_cues = len(cues)
    show_duration = cues[-1]["time"] if cues else 0

    print("=" * 70)
    print(f"  PIXSTARS SHOW CONDUCTOR")
    print(f"  Cues: {total_cues}  |  Duration: {format_time(show_duration)}")
    print(f"  Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 70)
    print()

    if dry_run:
        # In dry-run mode, print all cues immediately
        for i, cue in enumerate(cues):
            _dispatch_cue(cue, i, total_cues, sender, ardour)
            print()
        print("=" * 70)
        print("  DRY RUN COMPLETE")
        print("=" * 70)
        return

    # Live mode — wait for real time
    print("Press ENTER to start the show (Ctrl+C to abort)...")
    try:
        input()
    except KeyboardInterrupt:
        print("\nAborted.")
        return

    show_start = time.time()
    cue_index = 0

    print(f"  SHOW STARTED at {time.strftime('%H:%M:%S')}")
    print("-" * 70)

    try:
        while cue_index < total_cues:
            elapsed = time.time() - show_start
            cue = cues[cue_index]

            if elapsed >= cue["time"]:
                _dispatch_cue(cue, cue_index, total_cues, sender, ardour)
                print()
                cue_index += 1
            else:
                # Show status line
                next_in = cue["time"] - elapsed
                status = (
                    f"\r  [{format_time(elapsed)}] "
                    f"Next: {cue['name']} in {next_in:.1f}s"
                )
                print(status, end="", flush=True)
                time.sleep(0.05)

    except KeyboardInterrupt:
        elapsed = time.time() - show_start
        print(f"\n\n  SHOW STOPPED at {format_time(elapsed)}")
        sender.ardour_stop()
        return

    elapsed = time.time() - show_start
    print("=" * 70)
    print(f"  SHOW COMPLETE — Total time: {format_time(elapsed)}")
    print("=" * 70)


def _dispatch_cue(cue: dict, index: int, total: int, sender: OSCSender, ardour: ArdourOSC):
    """Dispatch a single cue to all relevant subsystems."""
    t = cue["time"]
    name = cue["name"]

    print(f"  [{format_time(t)}] CUE {index + 1}/{total}: {name}")

    # Ardour commands
    if "ardour" in cue and cue["ardour"]:
        ardour.process_cue(cue["ardour"])

    # Lamp state
    if "lamp" in cue and cue["lamp"]:
        sender.lamp_state(cue["lamp"])

    # Projection scene
    if "projection" in cue and cue["projection"]:
        sender.projection_scene(cue["projection"])

    # Lighting state
    if "lighting" in cue and cue["lighting"]:
        sender.lighting_state(cue["lighting"])


def main():
    parser = argparse.ArgumentParser(description="Pixstars Show Conductor")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print all cues without sending OSC or waiting",
    )
    parser.add_argument(
        "--timeline",
        default=config.TIMELINE_FILE,
        help=f"Path to timeline YAML (default: {config.TIMELINE_FILE})",
    )
    args = parser.parse_args()

    # Load timeline
    cues = load_timeline(args.timeline)

    # Create OSC sender
    sender = OSCSender(dry_run=args.dry_run)
    ardour = ArdourOSC(sender)

    # Run the show
    run_show(cues, sender, ardour, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
