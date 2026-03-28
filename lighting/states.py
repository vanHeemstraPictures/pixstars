"""
Pixstars Lighting — State Definitions

Maps the 9 Pixstars lighting states to DMX channel values.

DMX Channel Layout (configurable):
    Channel 1: Master dimmer (0–255)
    Channel 2: Red (0–255)
    Channel 3: Green (0–255)
    Channel 4: Blue (0–255)
    Channel 5: White (0–255)
    Channel 6: Strobe (0=off, 1–255=speed)
    Channel 7: Effect (0=none, 1–127=fade, 128–255=pulse)

These are placeholder mappings — adjust channel values to match
your actual DMX fixtures.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LightingState:
    name: str
    channels: dict[int, int]  # DMX channel → value (0–255)
    description: str


# ── All 9 Pixstars Lighting States ──────────────────────────────────────────

LIGHTING_STATES: dict[str, LightingState] = {
    "BLACKOUT": LightingState(
        name="BLACKOUT",
        channels={1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0},
        description="All lights off",
    ),
    "LAMP_ONLY": LightingState(
        name="LAMP_ONLY",
        channels={1: 80, 2: 255, 3: 200, 4: 100, 5: 60, 6: 0, 7: 0},
        description="Warm spot on desk lamp only",
    ),
    "ROCKSTAR": LightingState(
        name="ROCKSTAR",
        channels={1: 255, 2: 255, 3: 50, 4: 0, 5: 0, 6: 0, 7: 0},
        description="Bold red/amber rock concert lighting",
    ),
    "DISNEY_SOFT": LightingState(
        name="DISNEY_SOFT",
        channels={1: 180, 2: 100, 3: 120, 4: 255, 5: 80, 6: 0, 7: 64},
        description="Soft blue/purple fairy-tale ambiance",
    ),
    "AI_COLD": LightingState(
        name="AI_COLD",
        channels={1: 200, 2: 40, 3: 180, 4: 255, 5: 120, 6: 0, 7: 0},
        description="Cold blue/cyan technical/AI atmosphere",
    ),
    "OVERHEAT": LightingState(
        name="OVERHEAT",
        channels={1: 255, 2: 255, 3: 80, 4: 0, 5: 0, 6: 180, 7: 200},
        description="Intense red with strobe — overheating crisis",
    ),
    "DEATH": LightingState(
        name="DEATH",
        channels={1: 40, 2: 80, 3: 0, 4: 20, 5: 0, 6: 0, 7: 128},
        description="Dim fading red/purple — death scene",
    ),
    "REBIRTH": LightingState(
        name="REBIRTH",
        channels={1: 160, 2: 200, 3: 180, 4: 220, 5: 255, 6: 0, 7: 64},
        description="Warm white growing glow — rebirth",
    ),
    "FINALE": LightingState(
        name="FINALE",
        channels={1: 255, 2: 255, 3: 220, 4: 180, 5: 255, 6: 0, 7: 0},
        description="Full bright warm celebration — finale",
    ),
}


def get_lighting_state(name: str) -> LightingState:
    """Get a lighting state by name (case-insensitive).

    Raises KeyError if unknown.
    """
    key = name.upper().strip()
    if key not in LIGHTING_STATES:
        raise KeyError(f"Unknown lighting state: '{name}'. Valid: {list(LIGHTING_STATES.keys())}")
    return LIGHTING_STATES[key]


def list_lighting_states() -> list[str]:
    """Return all valid lighting state names."""
    return list(LIGHTING_STATES.keys())
