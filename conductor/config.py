"""
Pixstars Show Conductor — Configuration

Central configuration for all OSC targets, ports, and system settings.
"""

# ── OSC Targets ──────────────────────────────────────────────────────────────
OSC_HOST = "127.0.0.1"

# Ardour DAW (built-in OSC control surface, default port)
ARDOUR_OSC_PORT = 3819

# Jess+ Lamp Adapter
LAMP_OSC_PORT = 9001

# Projection Controller
PROJECTION_OSC_PORT = 9002

# DMX Lighting Controller
LIGHTING_OSC_PORT = 9003

# Digital Twin WebSocket Bridge (Deno server)
DIGITAL_TWIN_OSC_PORT = 9004

# ── Timeline ─────────────────────────────────────────────────────────────────
TIMELINE_FILE = "conductor/timeline.yaml"

# ── Display ──────────────────────────────────────────────────────────────────
# Refresh rate for conductor UI (Hz)
UI_REFRESH_RATE = 10
