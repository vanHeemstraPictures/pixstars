#!/usr/bin/env python3
"""
Pixstars — End-to-End Integration Test

Starts all subsystem listeners (lamp, projection, lighting) in mock mode,
then runs the conductor dry-run and verifies all OSC messages are received
correctly by every subsystem.

Usage:
    source .venv/bin/activate
    python scripts/integration_test.py
"""

import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from pythonosc import dispatcher, osc_server, udp_client

from conductor.main import load_timeline, format_time
from conductor.osc_sender import OSCSender
from conductor.ardour_osc import ArdourOSC
from lamp.states import get_state
from projection.scenes import get_scene
from lighting.states import get_lighting_state


class SubsystemLogger:
    """Collects OSC messages received by a mock subsystem."""

    def __init__(self, name: str, port: int, address_pattern: str):
        self.name = name
        self.port = port
        self.messages: list[tuple[str, list]] = []

        self._dispatcher = dispatcher.Dispatcher()
        self._dispatcher.map(address_pattern, self._handle)
        self._dispatcher.set_default_handler(self._handle_default)

    def _handle(self, address: str, *args):
        self.messages.append((address, list(args)))

    def _handle_default(self, address: str, *args):
        self.messages.append((address, list(args)))

    def start(self) -> osc_server.ThreadingOSCUDPServer:
        server = osc_server.ThreadingOSCUDPServer(
            ("127.0.0.1", self.port), self._dispatcher
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server


def run_integration_test():
    print("=" * 70)
    print("  PIXSTARS END-TO-END INTEGRATION TEST")
    print("=" * 70)
    print()

    # ── Start mock subsystem listeners ───────────────────────────────────
    print("Starting mock subsystems...")

    lamp_log = SubsystemLogger("Lamp", 9001, "/lamp/*")
    projection_log = SubsystemLogger("Projection", 9002, "/projection/*")
    lighting_log = SubsystemLogger("Lighting", 9003, "/lighting/*")

    servers = []
    for sub in [lamp_log, projection_log, lighting_log]:
        srv = sub.start()
        servers.append(srv)
        print(f"  ✓ {sub.name} listener on port {sub.port}")

    # Give servers time to start
    time.sleep(0.3)

    # ── Load timeline ────────────────────────────────────────────────────
    print("\nLoading timeline...")
    cues = load_timeline("conductor/timeline.yaml")
    print(f"  ✓ {len(cues)} cues loaded")

    # ── Create live OSC sender (sends real OSC to localhost) ─────────────
    sender = OSCSender(dry_run=False)
    ardour_osc = ArdourOSC(sender)

    # ── Dispatch all cues ────────────────────────────────────────────────
    print("\nDispatching all cues (fast mode — no wait)...\n")

    for i, cue in enumerate(cues):
        t = cue["time"]
        name = cue["name"]
        print(f"  [{format_time(t)}] CUE {i+1}/{len(cues)}: {name}")

        if "lamp" in cue and cue["lamp"]:
            sender.lamp_state(cue["lamp"])
        if "projection" in cue and cue["projection"]:
            sender.projection_scene(cue["projection"])
        if "lighting" in cue and cue["lighting"]:
            sender.lighting_state(cue["lighting"])

        # Small delay for OSC delivery
        time.sleep(0.05)

    # Wait for all messages to arrive
    time.sleep(0.5)

    # ── Verify results ───────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  VERIFICATION")
    print("=" * 70)

    errors = 0

    # Count expected messages per subsystem
    expected_lamp = sum(1 for c in cues if c.get("lamp"))
    expected_proj = sum(1 for c in cues if c.get("projection"))
    expected_light = sum(1 for c in cues if c.get("lighting"))

    # Lamp
    print(f"\n  Lamp:       {len(lamp_log.messages)} received, {expected_lamp} expected")
    if len(lamp_log.messages) == expected_lamp:
        print("  ✓ Lamp messages PASS")
    else:
        print(f"  ✗ Lamp messages FAIL (got {len(lamp_log.messages)}, expected {expected_lamp})")
        errors += 1

    # Validate lamp states
    for addr, args in lamp_log.messages:
        if args:
            try:
                get_state(str(args[0]))
            except KeyError:
                print(f"  ✗ Invalid lamp state: {args[0]}")
                errors += 1

    # Projection
    print(f"\n  Projection: {len(projection_log.messages)} received, {expected_proj} expected")
    if len(projection_log.messages) == expected_proj:
        print("  ✓ Projection messages PASS")
    else:
        print(f"  ✗ Projection messages FAIL (got {len(projection_log.messages)}, expected {expected_proj})")
        errors += 1

    # Validate projection scenes
    for addr, args in projection_log.messages:
        if args:
            try:
                get_scene(str(args[0]))
            except KeyError:
                print(f"  ✗ Invalid projection scene: {args[0]}")
                errors += 1

    # Lighting
    print(f"\n  Lighting:   {len(lighting_log.messages)} received, {expected_light} expected")
    if len(lighting_log.messages) == expected_light:
        print("  ✓ Lighting messages PASS")
    else:
        print(f"  ✗ Lighting messages FAIL (got {len(lighting_log.messages)}, expected {expected_light})")
        errors += 1

    # Validate lighting states
    for addr, args in lighting_log.messages:
        if args:
            try:
                get_lighting_state(str(args[0]))
            except KeyError:
                print(f"  ✗ Invalid lighting state: {args[0]}")
                errors += 1

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    total_msgs = len(lamp_log.messages) + len(projection_log.messages) + len(lighting_log.messages)
    if errors == 0:
        print(f"  ✅ ALL TESTS PASSED — {total_msgs} OSC messages verified")
    else:
        print(f"  ❌ {errors} ERROR(S) FOUND")
    print("=" * 70)

    # Cleanup
    for srv in servers:
        srv.shutdown()

    return errors == 0


if __name__ == "__main__":
    success = run_integration_test()
    sys.exit(0 if success else 1)
