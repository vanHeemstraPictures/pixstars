"""
Pixstars Show Conductor — Ardour OSC Integration

Provides high-level Ardour control via OSC, based on the Ardour OSC API.
Uses /toggle_roll for transport (Ardour 9 — equivalent to spacebar).

Ardour must have OSC control surface enabled:
  Ardour9 → Preferences → Control Surfaces → Open Sound Control (OSC)
"""

from conductor.osc_sender import OSCSender


class ArdourOSC:
    """High-level interface for controlling Ardour via OSC."""

    # Ardour default sample rate (can be overridden)
    SAMPLE_RATE = 48000

    def __init__(self, sender: OSCSender):
        self.sender = sender

    # ── Transport ────────────────────────────────────────────────────────

    def play(self):
        """Start Ardour playback (uses /toggle_roll)."""
        self.sender.ardour_play()

    def stop(self):
        """Stop Ardour playback (uses /toggle_roll)."""
        self.sender.ardour_stop()

    def goto_start(self):
        """Move playhead to beginning of session."""
        self.sender.ardour_goto_start()

    def locate_seconds(self, seconds: float, roll: bool = True):
        """Locate playhead to a time position in seconds.

        Args:
            seconds: Target position in seconds from session start
            roll: If True, keep transport rolling after locate
        """
        samples = int(seconds * self.SAMPLE_RATE)
        self.sender.ardour_locate(samples, 1 if roll else 0)

    def toggle_roll(self):
        """Toggle between play and stop (raw, no state tracking)."""
        self.sender.send("ardour", "/toggle_roll")

    # ── Markers ──────────────────────────────────────────────────────────

    def goto_marker(self, marker_name: str):
        """Jump to a named marker in Ardour."""
        self.sender.send("ardour", "/marker", marker_name)

    def next_marker(self):
        """Jump to next marker."""
        self.sender.send("ardour", "/next_marker")

    def prev_marker(self):
        """Jump to previous marker."""
        self.sender.send("ardour", "/prev_marker")

    def add_marker(self):
        """Add a marker at current playhead position."""
        self.sender.send("ardour", "/add_marker")

    # ── Mixing ───────────────────────────────────────────────────────────

    def master_gain(self, db: float):
        """Set master gain in dB (-193 to +6)."""
        self.sender.send("ardour", "/master/gain", db)

    def master_mute(self, muted: bool = True):
        """Mute/unmute master bus."""
        self.sender.send("ardour", "/master/mute", 1 if muted else 0)

    def strip_mute(self, strip_id: int, muted: bool = True):
        """Mute/unmute a specific strip."""
        self.sender.send("ardour", "/strip/mute", strip_id, 1 if muted else 0)

    def strip_gain(self, strip_id: int, db: float):
        """Set strip gain in dB."""
        self.sender.send("ardour", "/strip/gain", strip_id, db)

    # ── Session ──────────────────────────────────────────────────────────

    def save(self):
        """Save current Ardour session."""
        self.sender.send("ardour", "/save_state")

    # ── Cue Processing ───────────────────────────────────────────────────

    def process_cue(self, ardour_data: dict):
        """Process an Ardour cue from the timeline.

        Args:
            ardour_data: Dict with 'command' key and optional parameters.
                         e.g. {"command": "transport_play"}
                         e.g. {"command": "locate", "seconds": 120.0}
        """
        command = ardour_data.get("command", "")

        match command:
            case "transport_play":
                self.play()
            case "transport_stop":
                self.stop()
            case "goto_start":
                self.goto_start()
            case "locate":
                seconds = ardour_data.get("seconds", 0.0)
                roll = ardour_data.get("roll", True)
                self.locate_seconds(seconds, roll)
            case "marker":
                name = ardour_data.get("name", "")
                self.goto_marker(name)
            case _:
                print(f"  [Ardour WARNING] Unknown command: {command}")
