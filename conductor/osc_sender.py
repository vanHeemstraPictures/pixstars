"""
Pixstars Show Conductor — OSC Sender

Sends OSC messages to all subsystems (Ardour, Jess+, Projection, Lighting).
"""

from pythonosc import udp_client
from conductor import config


class OSCSender:
    """Manages OSC clients for all Pixstars subsystems."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.clients = {}

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

    def send(self, target: str, address: str, *args):
        """Send an OSC message to a target subsystem.

        Args:
            target: One of 'ardour', 'lamp', 'projection', 'lighting'
            address: OSC address path (e.g. '/transport_play')
            *args: OSC message arguments
        """
        if self.dry_run:
            args_str = " ".join(str(a) for a in args) if args else ""
            print(f"  [OSC → {target:12s}] {address} {args_str}")
            return

        if target not in self.clients:
            print(f"  [OSC WARNING] Unknown target: {target}")
            return

        self.clients[target].send_message(address, list(args) if args else [])

    # ── Convenience methods ──────────────────────────────────────────────

    def ardour_transport_play(self):
        self.send("ardour", "/transport_play")

    def ardour_transport_stop(self):
        self.send("ardour", "/transport_stop")

    def ardour_locate(self, samples: int, roll: int = 1):
        """Locate Ardour playhead to a sample position."""
        self.send("ardour", "/locate", samples, roll)

    def ardour_goto_start(self):
        self.send("ardour", "/goto_start")

    def lamp_state(self, state: str):
        """Send lamp state change to Jess+ adapter."""
        self.send("lamp", "/lamp/state", state)

    def projection_scene(self, scene: str):
        """Send projection scene change."""
        self.send("projection", "/projection/scene", scene)

    def lighting_state(self, state: str):
        """Send lighting state change."""
        self.send("lighting", "/lighting/state", state)
