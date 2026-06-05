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

    def __init__(self, dry_run: bool = False, rehearse: bool = False):
        self.dry_run = dry_run
        self.rehearse = rehearse
        self.clients = {}
        self._ardour_rolling = False  # Track Ardour transport state

        if not dry_run:
            cave_host = config.OSC_HOST if rehearse else config.ESP32_CAVE_HOST
            self.clients["ardour"] = udp_client.SimpleUDPClient(
                config.OSC_HOST, config.ARDOUR_OSC_PORT
            )
            self.clients["lamp"] = udp_client.SimpleUDPClient(
                config.OSC_HOST, config.LAMP_OSC_PORT
            )
            self.clients["cave"] = udp_client.SimpleUDPClient(
                cave_host, config.ESP32_CAVE_PORT
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
        """Send lamp state change to Jess+ adapter (legacy)."""
        self.send("lamp", "/lamp/state", state)

    # ── ESP32 Cave Controller ────────────────────────────────────────────
    # Channels: Ch1=lower arm, Ch2=elbow, Ch3=neck pan, Ch4-5=spare.
    # LED modes: "solid", "breathe", "pulse", "rainbow", "off".

    def cave_servo(self, channel: int, angle: int):
        """Maestro servo position (channel, angle in degrees)."""
        self.send("cave", "/servo/set", int(channel), int(angle))

    def cave_servo_speed(self, channel: int, speed: int):
        """Maestro servo speed (channel, speed in Maestro units)."""
        self.send("cave", "/servo/speed", int(channel), int(speed))

    def cave_head_nod(self, angle: float, speed: int | None = None):
        """AX-12A head nod position (0-300 deg), optional speed."""
        if speed is None:
            self.send("cave", "/head/nod", float(angle))
        else:
            self.send("cave", "/head/nod", float(angle), int(speed))

    def cave_led_rear(self, r: int, g: int, b: int, mode: str = "solid"):
        """Rear LED ring (16 LEDs): RGB 0-255 + mode."""
        self.send("cave", "/led/rear", int(r), int(g), int(b), str(mode))

    def cave_led_front(self, r: int, g: int, b: int, mode: str = "solid"):
        """Front LED ring (35 LEDs): RGB 0-255 + mode."""
        self.send("cave", "/led/front", int(r), int(g), int(b), str(mode))

    def cave_turntable_rotate(self, degrees: float, speed: int):
        """Turntable relative rotation in degrees at given step speed."""
        self.send("cave", "/turntable/rotate", float(degrees), int(speed))

    def cave_turntable_goto(self, degrees: float, speed: int):
        """Turntable absolute position in degrees at given step speed."""
        self.send("cave", "/turntable/goto", float(degrees), int(speed))

    def cave_turntable_origin(self):
        """Home the turntable to the hall sensor origin."""
        self.send("cave", "/turntable/origin")

    def cave_turntable_stop(self):
        """Emergency stop the turntable."""
        self.send("cave", "/turntable/stop")

    def cave_ping(self):
        """Health check ping to the ESP32 cave controller."""
        self.send("cave", "/ping")

    def projection_scene(self, scene: str):
        """Send projection scene change."""
        self.send("projection", "/projection/scene", scene)

    def lighting_state(self, state: str):
        """Send lighting state change."""
        self.send("lighting", "/lighting/state", state)
