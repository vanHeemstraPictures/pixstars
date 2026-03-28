"""
Pixstars Projection — Scene Definitions

Maps scene names to display assets and configuration.
"""

from dataclasses import dataclass
from pathlib import Path

ASSETS_DIR = Path(__file__).parent.parent / "assets" / "projection"


@dataclass(frozen=True)
class Scene:
    name: str
    image_file: str
    background_color: tuple[int, int, int]
    description: str


# ── All Pixstars Projection Scenes ──────────────────────────────────────────

SCENES: dict[str, Scene] = {
    "BLACKOUT": Scene(
        name="BLACKOUT",
        image_file="",
        background_color=(0, 0, 0),
        description="Black screen — no projection",
    ),
    "GNR_LOGO": Scene(
        name="GNR_LOGO",
        image_file="gnr_logo.png",
        background_color=(0, 0, 0),
        description="Guns N' Roses logo",
    ),
    "DISNEY_CASTLE": Scene(
        name="DISNEY_CASTLE",
        image_file="disney_castle.png",
        background_color=(10, 10, 30),
        description="Disney castle — Walt transformation",
    ),
    "MICKEY_DRAWING": Scene(
        name="MICKEY_DRAWING",
        image_file="mickey_drawing.png",
        background_color=(255, 255, 255),
        description="Mickey Mouse drawing",
    ),
    "LAMP_DRAWING": Scene(
        name="LAMP_DRAWING",
        image_file="lamp_drawing.png",
        background_color=(255, 255, 255),
        description="Lamp character drawing",
    ),
    "AI_ITERATIONS": Scene(
        name="AI_ITERATIONS",
        image_file="ai_iterations.png",
        background_color=(20, 20, 40),
        description="AI iteration visuals",
    ),
    "AI_SIGNATURE": Scene(
        name="AI_SIGNATURE",
        image_file="ai_signature.png",
        background_color=(0, 0, 0),
        description="A.I. signature reveal",
    ),
    "WALT_SIGNATURE": Scene(
        name="WALT_SIGNATURE",
        image_file="walt_signature.png",
        background_color=(0, 0, 0),
        description="W.A.L.T. signature reveal",
    ),
    "AXEL_SIGNATURE": Scene(
        name="AXEL_SIGNATURE",
        image_file="axel_signature.png",
        background_color=(0, 0, 0),
        description="A.X.E.L. signature reveal",
    ),
    "TEAM_ROCKSTARS": Scene(
        name="TEAM_ROCKSTARS",
        image_file="team_rockstars.png",
        background_color=(0, 0, 0),
        description="Team Rockstars logo — finale",
    ),
}


def get_scene(name: str) -> Scene:
    """Get a scene by name (case-insensitive).

    Raises KeyError if unknown.
    """
    key = name.upper().strip()
    if key not in SCENES:
        raise KeyError(f"Unknown scene: '{name}'. Valid: {list(SCENES.keys())}")
    return SCENES[key]


def list_scenes() -> list[str]:
    """Return all valid scene names."""
    return list(SCENES.keys())
