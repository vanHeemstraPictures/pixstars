"""
Pixstars Show Conductor — Configuration

Central configuration for all OSC targets, ports, and system settings.
"""

# ── OSC Targets ──────────────────────────────────────────────────────────────
OSC_HOST = "127.0.0.1"

# Ardour DAW (built-in OSC control surface, default port)
ARDOUR_OSC_PORT = 3819

# Jess+ Lamp Adapter (legacy — superseded by ESP32 cave controller)
LAMP_OSC_PORT = 9001

# ESP32 Cave Controller (A.I. lamp servos, head, LED rings, turntable)
# Hostname resolves on the local network via mDNS; override for static IPs.
ESP32_CAVE_HOST = "pixstars-cave.local"
ESP32_CAVE_PORT = 8000

# Projection Controller
PROJECTION_OSC_PORT = 9002

# DMX Lighting Controller
LIGHTING_OSC_PORT = 9003

# Digital Twin WebSocket Bridge (Deno server)
DIGITAL_TWIN_OSC_PORT = 9004

# Laser Galvo Simulator (lamp head ILDA galvo stand-in)
LASER_OSC_PORT = 9005

# ── Timeline ─────────────────────────────────────────────────────────────────
TIMELINE_FILE = "conductor/timeline.yaml"

# ── Display ──────────────────────────────────────────────────────────────────
# Refresh rate for conductor UI (Hz)
UI_REFRESH_RATE = 10
