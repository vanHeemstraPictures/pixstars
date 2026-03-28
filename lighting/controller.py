#!/usr/bin/env python3
"""
Pixstars Lighting — DMX Controller

Receives OSC messages from the Show Conductor and outputs DMX values
via the Enttec DMX USB Pro using the DMXEnttecPro library.
In mock mode (no hardware), logs DMX values.

Listens on port 9003 for:
    /lighting/state <state_name>  — Switch to named lighting state

Usage:
    source .venv/bin/activate
    python -m lighting.controller               # Mock mode (logging only)
    python -m lighting.controller --device auto  # Auto-detect Enttec DMX USB Pro
    python -m lighting.controller --device /dev/tty.usbserial-EN055555A
    python -m lighting.controller --verbose
"""

import argparse
import signal
import sys
import threading

from pythonosc import dispatcher, osc_server

from lighting.states import get_lighting_state, list_lighting_states, LightingState


class DMXOutput:
    """DMX output via Enttec DMX USB Pro, or mock for testing."""

    def __init__(self, device: str = "mock", verbose: bool = False):
        self.device = device
        self.verbose = verbose
        self._controller = None  # DMXEnttecPro.Controller when connected

        if device != "mock":
            self._init_hardware(device)

    def _init_hardware(self, device: str):
        """Initialize the Enttec DMX USB Pro via DMXEnttecPro library.

        Args:
            device: 'auto' to auto-detect, or a serial port path
        """
        try:
            from DMXEnttecPro import Controller
            from DMXEnttecPro.utils import get_port_by_product_id

            if device == "auto":
                # Enttec DMX USB Pro has FTDI PID 24577 (0x6001)
                port = get_port_by_product_id(24577)
                if port is None:
                    print("  [DMX WARNING] No Enttec DMX USB Pro found, using mock")
                    self.device = "mock"
                    return
            else:
                port = device

            self._controller = Controller(port, auto_submit=True)
            print(f"  [DMX] Connected to Enttec DMX USB Pro on {port}")

        except ImportError:
            print("  [DMX WARNING] DMXEnttecPro not installed, using mock")
            print("  [DMX]         Install with: pip install DMXEnttecPro")
            self.device = "mock"
        except Exception as e:
            print(f"  [DMX WARNING] Could not open hardware: {e}, using mock")
            self.device = "mock"

    def set_channels(self, channels: dict[int, int]):
        """Set DMX channel values.

        Args:
            channels: Dict of channel_number → value (1-based, 0–255)
        """
        if self.device == "mock":
            self._log_channels(channels)
            return

        if self._controller is None:
            return

        try:
            for ch, val in channels.items():
                clamped = max(0, min(255, val))
                self._controller.set_channel(ch, clamped)
            # auto_submit=True handles submit() automatically
        except Exception as e:
            print(f"  [DMX ERROR] Send failed: {e}")

    def _log_channels(self, channels: dict[int, int]):
        """Log DMX channel values (mock mode)."""
        ch_str = " ".join(f"Ch{ch}={val}" for ch, val in sorted(channels.items()))
        print(f"  [DMX MOCK] {ch_str}")

    def blackout(self):
        """Set all channels to zero."""
        if self.device == "mock":
            print("  [DMX MOCK] BLACKOUT — all channels 0")
            return

        if self._controller is None:
            return

        try:
            # Set all used channels to 0
            for ch in range(1, 513):
                self._controller.set_channel(ch, 0, submit_after=False)
            self._controller.submit()
        except Exception as e:
            print(f"  [DMX ERROR] Blackout failed: {e}")

    def close(self):
        """Close hardware connection."""
        if self._controller is not None:
            self.blackout()
            self._controller.close()
            self._controller = None


class LightingController:
    """Receives OSC lighting commands and outputs DMX."""

    def __init__(self, port: int = 9003, device: str = "mock", verbose: bool = False):
        self.port = port
        self.verbose = verbose
        self.dmx = DMXOutput(device=device, verbose=verbose)
        self.current_state: LightingState | None = None
        self.running = True

        # OSC dispatcher
        self._dispatcher = dispatcher.Dispatcher()
        self._dispatcher.map("/lighting/state", self._handle_state)

    def _handle_state(self, address: str, *args):
        """Handle /lighting/state OSC messages."""
        if not args:
            print("  [LIGHT WARNING] /lighting/state with no arguments")
            return

        state_name = str(args[0])
        try:
            state = get_lighting_state(state_name)
        except KeyError as e:
            print(f"  [LIGHT ERROR] {e}")
            return

        old = self.current_state.name if self.current_state else "NONE"
        self.current_state = state
        print(f"  [LIGHT] {old} → {state.name}: {state.description}")

        # Apply DMX values
        self.dmx.set_channels(state.channels)

    def start(self):
        """Start the OSC server and DMX output."""
        server = osc_server.ThreadingOSCUDPServer(
            ("0.0.0.0", self.port), self._dispatcher
        )

        print("=" * 50)
        print(f"  PIXSTARS LIGHTING CONTROLLER")
        print(f"  OSC port: {self.port}")
        print(f"  DMX device: {self.dmx.device}")
        print(f"  DMX library: DMXEnttecPro")
        print(f"  States: {', '.join(list_lighting_states())}")
        print("=" * 50)

        def signal_handler(sig, frame):
            print("\n  [LIGHT] Shutting down...")
            self.dmx.blackout()
            self.dmx.close()
            self.running = False
            server.shutdown()

        signal.signal(signal.SIGINT, signal_handler)
        server.serve_forever()

    def stop(self):
        """Stop the controller."""
        self.dmx.blackout()
        self.dmx.close()
        self.running = False


def main():
    parser = argparse.ArgumentParser(description="Pixstars Lighting Controller")
    parser.add_argument("--port", type=int, default=9003, help="OSC listen port")
    parser.add_argument("--device", default="mock",
                        help="DMX device: 'mock', 'auto', or serial port path")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    ctrl = LightingController(port=args.port, device=args.device, verbose=args.verbose)
    ctrl.start()


if __name__ == "__main__":
    main()
