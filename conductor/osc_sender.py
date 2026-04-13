"""
Pixstars Show Conductor — OSC Sender

Sends OSC messages to all subsystems (Ardour, Jess+, Projection, Lighting)
and mirrors them to the Digital Twin WebSocket bridge.

Note: Ardour 9 uses /toggle_roll (equivalent to spacebar) for transport
control, as /transport_play does not produce audio output.
"""

from pythonosc import udp_client
from conductor import config


class OSCSender:
    """Manages OSC clients for all Pixstars subsystems."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.clients = {}
        self._ardour_rolling = False  # Track Ardour transport state

        if not dry_run:
            self.clients["ardour"] = udp_client.SimpleUDPClient(
                config.OSC_HOST, config.ARDOUR_OSC_PORT
            )
            self.clients["lamp"] = udp_client.SimpleUDPClient(
                config.OSC_HOST, config.LAMP_OSC_PORT
            )
            self.clients["projection"] = udp_client.SimpleUDPClient(
                config.OSC_HOST, config.PROJECTION_OSC_PORT
            )
            self.clients["lighting"] = udp_client.SimpleUDPClient(
                config.OSC_HOST, config.LIGHTING_OSC_PORT
            )
            self.clients["twin"] = udp_client.SimpleUDPClient(
                config.OSC_HOST, config.DIGITAL_TWIN_OSC_PORT
            )

    def send(self, target: str, address: str, *args):
        """Send an OSC message to a target subsystem.

        Also mirrors the message to the digital twin (unless the target
        is already 'twin').
        """
        if self.dry_run:
            args_str = " ".join(str(a) for a in args) if args else ""
            print(f"  [OSC → {target:12s}] {address} {args_str}")
            return

        if target not in self.clients:
            print(f"  [OSC WARNING] Unknown target: {target}")
            return

        self.clients[target].send_message(address, list(args) if args else [])

        # Mirror to digital twin
        if target != "twin" and "twin" in self.clients:
            self.clients["twin"].send_message(address, list(args) if args else [])

    # ── Ardour Transport (using /toggle_roll) ────────────────────────────

    def ardour_play(self):
        """Start Ardour playback. Uses /toggle_roll if not already rolling."""
        if not self._ardour_rolling:
            self.send("ardour", "/toggle_roll")
            self._ardour_rolling = True
            # Explicitly notify digital twin of transport state
            self.send("twin", "/transport/state", "PLAYING")

    def ardour_stop(self):
        """Stop Ardour playback. Uses /toggle_roll if currently rolling."""
        if self._ardour_rolling:
            self.send("ardour", "/toggle_roll")
            self._ardour_rolling = False
            # Explicitly notify digital twin of transport state
            self.send("twin", "/transport/state", "STOPPED")

    def ardour_locate(self, samples: int, roll: int = 1):
        """Locate Ardour playhead to a sample position."""
        self.send("ardour", "/locate", samples, roll)

    def ardour_goto_start(self):
        self.send("ardour", "/goto_start")

    # ── Subsystem Convenience Methods ────────────────────────────────────

    def lamp_state(self, state: str):
        """Send lamp state change to Jess+ adapter."""
        self.send("lamp", "/lamp/state", state)

    def projection_scene(self, scene: str):
        """Send projection scene change."""
        self.send("projection", "/projection/scene", scene)

    def lighting_state(self, state: str):
        """Send lighting state change."""
        self.send("lighting", "/lighting/state", state)
