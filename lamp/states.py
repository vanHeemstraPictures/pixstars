"""
Pixstars Lamp — State Definitions

Maps the 14 Pixstars lamp states to motion parameters for Jess+.
Each state defines behavioral bounds that Jess+ AI interprets
within its gesture manager.

Motion parameters:
    energy:     0.0–1.0  Overall movement intensity
    speed:      0.0–1.0  Movement speed (maps to Jess+ arm_speed)
    range:      0.0–1.0  Movement amplitude / range of motion
    jitter:     0.0–1.0  Randomness / irregularity of movement
    tilt_bias:  -1.0–1.0 Vertical bias (-1 = down/collapsed, +1 = up/proud)
    description: Human-readable description of the behavior
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LampState:
    name: str
    energy: float
    speed: float
    range: float
    jitter: float
    tilt_bias: float
    description: str


# ── All 14 Pixstars Lamp States ──────────────────────────────────────────────

LAMP_STATES: dict[str, LampState] = {
    "INERT": LampState(
        name="INERT",
        energy=0.0, speed=0.0, range=0.0, jitter=0.0, tilt_bias=0.0,
        description="Completely still, powered off, no movement"
    ),
    "FUNCTIONAL": LampState(
        name="FUNCTIONAL",
        energy=0.1, speed=0.2, range=0.1, jitter=0.0, tilt_bias=0.0,
        description="Basic operational state, minimal neutral idle movement"
    ),
    "CURIOUS": LampState(
        name="CURIOUS",
        energy=0.4, speed=0.3, range=0.4, jitter=0.1, tilt_bias=0.3,
        description="Interested tilting, looking around, exploring"
    ),
    "DISMISSIVE": LampState(
        name="DISMISSIVE",
        energy=0.3, speed=0.4, range=0.3, jitter=0.05, tilt_bias=-0.2,
        description="Turning away, disinterested, slight avoidance"
    ),
    "PLEASED": LampState(
        name="PLEASED",
        energy=0.5, speed=0.3, range=0.3, jitter=0.05, tilt_bias=0.4,
        description="Happy leaning forward, gentle rhythmic nods"
    ),
    "ARROGANT": LampState(
        name="ARROGANT",
        energy=0.7, speed=0.5, range=0.5, jitter=0.1, tilt_bias=0.6,
        description="Show-off movements, exaggerated proud poses"
    ),
    "OVERHEATING": LampState(
        name="OVERHEATING",
        energy=0.9, speed=0.8, range=0.3, jitter=0.8, tilt_bias=0.1,
        description="Erratic jittering, shaking, unstable rapid movements"
    ),
    "DYING": LampState(
        name="DYING",
        energy=0.4, speed=0.2, range=0.2, jitter=0.6, tilt_bias=-0.5,
        description="Slowing down, drooping, intermittent spasms"
    ),
    "DEAD": LampState(
        name="DEAD",
        energy=0.0, speed=0.0, range=0.0, jitter=0.0, tilt_bias=-1.0,
        description="Collapsed, no movement, fully dropped"
    ),
    "WEAK": LampState(
        name="WEAK",
        energy=0.1, speed=0.1, range=0.1, jitter=0.2, tilt_bias=-0.6,
        description="Faint twitches, barely alive, struggling to rise"
    ),
    "REBORN": LampState(
        name="REBORN",
        energy=0.5, speed=0.3, range=0.4, jitter=0.1, tilt_bias=0.2,
        description="Rising up, rediscovering movement, growing strength"
    ),
    "LEARNING": LampState(
        name="LEARNING",
        energy=0.4, speed=0.3, range=0.3, jitter=0.15, tilt_bias=0.1,
        description="Tentative exploration, testing movements, careful"
    ),
    "CELEBRATE": LampState(
        name="CELEBRATE",
        energy=0.8, speed=0.6, range=0.6, jitter=0.1, tilt_bias=0.5,
        description="Joyful swinging, rhythmic celebration"
    ),
    "OFF": LampState(
        name="OFF",
        energy=0.0, speed=0.0, range=0.0, jitter=0.0, tilt_bias=0.0,
        description="Power off, no movement, show complete"
    ),
}


def get_state(name: str) -> LampState:
    """Get a lamp state by name.

    Args:
        name: State name (case-insensitive)

    Returns:
        LampState dataclass

    Raises:
        KeyError: If state name is unknown
    """
    key = name.upper().strip()
    if key not in LAMP_STATES:
        raise KeyError(f"Unknown lamp state: '{name}'. Valid states: {list(LAMP_STATES.keys())}")
    return LAMP_STATES[key]


def list_states() -> list[str]:
    """Return list of all valid state names."""
    return list(LAMP_STATES.keys())
