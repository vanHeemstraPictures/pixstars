#!/usr/bin/env python3
"""
Pixstars Lamp — OSC Adapter for Jess+

Receives OSC messages from the Show Conductor and translates them into
Jess+ compatible motion parameters. In mock mode (no Jess+ connected),
logs the state transitions.

Listens on port 9001 for:
    /lamp/state <state_name>   — Set lamp to a named state (e.g. "CURIOUS")

Usage:
    source .venv/bin/activate
    python -m lamp.adapter                # Run with mock servo output (ESP32 WiFi in production)
    python -m lamp.adapter --verbose      # Verbose logging
"""

import argparse
import signal
import sys
import time
from threading import Event

from pythonosc import dispatcher, osc_server

from lamp.states import get_state, list_states, LampState


class LampAdapter:
    """Bridges OSC messages from Conductor to Jess+ lamp motion."""

    def __init__(self, port: int = 9001, verbose: bool = False):
        self.port = port
        self.verbose = verbose
        self.current_state: LampState | None = None
        self.running = Event()

        # Set up OSC dispatcher
        self.dispatcher = dispatcher.Dispatcher()
        self.dispatcher.map("/lamp/state", self._handle_state)
        self.dispatcher.set_default_handler(self._handle_unknown)

    def _handle_state(self, address: str, *args):
        """Handle /lamp/state OSC messages."""
        if not args:
            print("  [LAMP WARNING] /lamp/state received with no arguments")
            return

        state_name = str(args[0])
        try:
            state = get_state(state_name)
        except KeyError as e:
            print(f"  [LAMP ERROR] {e}")
            return

        old_name = self.current_state.name if self.current_state else "NONE"
        self.current_state = state

        print(f"  [LAMP] {old_name} → {state.name}: {state.description}")

        if self.verbose:
            print(f"         energy={state.energy:.1f} speed={state.speed:.1f} "
                  f"range={state.range:.1f} jitter={state.jitter:.2f} "
                  f"tilt_bias={state.tilt_bias:+.1f}")

        # TODO: When Jess+ is connected, feed these parameters into
        # the Jess+ hivemind/DataBorg to influence lamp motion:
        #   hivemind.master_stream = state.energy
        #   hivemind.rhythm_rate = state.speed
        #   etc.

        # TODO: When ESP32 WiFi bridge is connected, send servo commands
        # via ESP32 to Maestro. Base rotation uses ComXim CT protocol
        # directly from Mac Mini (not via ESP32).

    def _handle_unknown(self, address: str, *args):
        """Handle unrecognized OSC messages."""
        if self.verbose:
            print(f"  [LAMP WARNING] Unknown OSC: {address} {args}")

    def start(self):
        """Start the OSC server and listen for lamp commands."""
        server = osc_server.ThreadingOSCUDPServer(
            ("0.0.0.0", self.port), self.dispatcher
        )
        self.running.set()

        print("=" * 50)
        print(f"  PIXSTARS LAMP ADAPTER")
        print(f"  Listening on port {self.port}")
        print(f"  Valid states: {', '.join(list_states())}")
        print(f"  Servo: MOCKED (logging only — ESP32 WiFi bridge in production)")
        print("=" * 50)

        # Handle Ctrl+C gracefully
        def signal_handler(sig, frame):
            print("\n  [LAMP] Shutting down...")
            self.running.clear()
            server.shutdown()

        signal.signal(signal.SIGINT, signal_handler)

        server.serve_forever()

    def stop(self):
        """Stop the adapter."""
        self.running.clear()


def main():
    parser = argparse.ArgumentParser(description="Pixstars Lamp OSC Adapter")
    parser.add_argument("--port", type=int, default=9001, help="OSC listen port")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    adapter = LampAdapter(port=args.port, verbose=args.verbose)
    adapter.start()


if __name__ == "__main__":
    main()
