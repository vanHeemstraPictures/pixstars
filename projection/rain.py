#!/usr/bin/env python3
"""
Pixstars Projection -- Digital Rain Renderer

A Matrix-style green digital rain that can be composited over projection
scenes. Implements a state machine covering all ten rain states defined in
the screenplay.

Restricted word list: the rain may only ever contain the words WALT, AXEL,
A.I. or WE. Individual random characters are unrestricted, but no other
recognizable words are allowed to lock into the columns.

Usage as a module:
    from projection.rain import DigitalRainRenderer
    renderer = DigitalRainRenderer(1280, 720)
    renderer.set_state("RAIN_TRACES")
    surface = renderer.render()
    screen.blit(surface, (0, 0))

Standalone demo:
    .venv/bin/python -m projection.rain
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import pygame


# --- Matrix green palette -----------------------------------------------------

HEAD_COLOR: Tuple[int, int, int] = (220, 255, 220)
BRIGHT: Tuple[int, int, int] = (0, 255, 65)      # #00FF41
TRAIL: Tuple[int, int, int] = (0, 143, 17)       # #008F11
DARK: Tuple[int, int, int] = (0, 60, 0)


# --- State identifiers --------------------------------------------------------

RAIN_OFF = "RAIN_OFF"
RAIN_TRACES = "RAIN_TRACES"
RAIN_BUILDING = "RAIN_BUILDING"
RAIN_STORM = "RAIN_STORM"
RAIN_SHATTER = "RAIN_SHATTER"
RAIN_STOP = "RAIN_STOP"
RAIN_GENTLE = "RAIN_GENTLE"
RAIN_NAMES = "RAIN_NAMES"
RAIN_THREE = "RAIN_THREE"
RAIN_WE = "RAIN_WE"

ALL_STATES: Tuple[str, ...] = (
    RAIN_OFF, RAIN_TRACES, RAIN_BUILDING, RAIN_STORM, RAIN_SHATTER,
    RAIN_STOP, RAIN_GENTLE, RAIN_NAMES, RAIN_THREE, RAIN_WE,
)


# --- Character pools ----------------------------------------------------------

DIGITS = "0123456789"
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SYMBOLS = "!@#$%^&*+=<>/\\|~?"
DEFAULT_CHARS = DIGITS + LETTERS + SYMBOLS

# The ONLY words ever allowed to appear vertically in the rain. Any change
# here must also be made in the spec rain state table and CLAUDE.md.
ALLOWED_WORDS: Tuple[str, ...] = ("WALT", "AXEL", "A.I.", "WE")


# --- Per-state configuration --------------------------------------------------

@dataclass(frozen=True)
class StateConfig:
    density: float                 # fraction of columns active
    speed_range: Tuple[float, float]  # rows-per-second min/max
    char_pool: str
    word_freq: float               # probability a new column locks a word
    allowed_words: Tuple[str, ...]
    trail_len: int = 18


STATE_CONFIG = {
    RAIN_OFF:      StateConfig(0.00, (4, 8),   DEFAULT_CHARS,        0.00, ()),
    RAIN_TRACES:   StateConfig(0.15, (3, 7),   DEFAULT_CHARS,        0.00, (),                       trail_len=14),
    RAIN_BUILDING: StateConfig(0.45, (8, 16),  DEFAULT_CHARS,        0.03, ("WALT", "A.I.")),
    RAIN_STORM:    StateConfig(0.85, (14, 28), DEFAULT_CHARS,        0.05, ("WALT", "A.I.", "AXEL")),
    RAIN_SHATTER:  StateConfig(0.85, (14, 28), DEFAULT_CHARS,        0.00, ()),
    RAIN_STOP:     StateConfig(0.00, (0, 0),   DEFAULT_CHARS,        0.00, ()),
    RAIN_GENTLE:   StateConfig(0.08, (2, 4),   DEFAULT_CHARS,        0.00, (),                       trail_len=10),
    RAIN_NAMES:    StateConfig(0.40, (5, 10),  "AILWT" + SYMBOLS,    0.06, ("WALT", "A.I.")),
    RAIN_THREE:    StateConfig(0.40, (5, 10),  DEFAULT_CHARS,        0.08, ("AXEL", "WALT", "A.I.")),
    RAIN_WE:       StateConfig(0.10, (1, 3),   "WE",                 0.00, (),                       trail_len=8),
}


# --- Column and particle primitives -------------------------------------------

class Column:
    __slots__ = ("x", "head_row", "speed", "chars", "trail_len",
                 "active", "word", "word_pos", "head_partial")

    def __init__(self, x: int) -> None:
        self.x = x
        self.head_row = 0.0
        self.speed = 8.0
        self.chars: List[str] = []
        self.trail_len = 18
        self.active = False
        self.word: Optional[str] = None
        self.word_pos = 0
        self.head_partial = 0.0


@dataclass
class Particle:
    x: float
    y: float
    char: str
    vx: float
    vy: float
    age: float = 0.0
    ttl: float = 1.2


# --- Renderer -----------------------------------------------------------------

class DigitalRainRenderer:
    """Animated digital rain overlay surface."""

    GRAVITY = 400.0           # px/s^2 for SHATTER particles
    STOP_FADE_PER_SEC = 220   # alpha units per second when dissolving
    WE_DECAY_SECONDS = 10.0   # time for RAIN_WE to slow to a stop

    def __init__(self, width: int, height: int, font_size: int = 18) -> None:
        if not pygame.font.get_init():
            pygame.font.init()
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("monospace", font_size, bold=True)
        self.cell_w, self.cell_h = self.font.size("M")
        self.n_cols = max(1, width // self.cell_w)
        self.n_rows = max(1, height // self.cell_h)
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.columns: List[Column] = [
            Column(i * self.cell_w) for i in range(self.n_cols)
        ]
        self.particles: List[Particle] = []
        self.state = RAIN_OFF
        self._config = STATE_CONFIG[RAIN_OFF]
        self.fade_alpha = 255.0
        self._we_elapsed = 0.0
        self.rng = random.Random()
        self._glyph_cache: dict = {}

    # -- state machine --------------------------------------------------------

    def set_state(self, state: str) -> None:
        if state not in STATE_CONFIG:
            raise ValueError(f"unknown rain state: {state!r}")
        if state == self.state:
            return
        self.state = state
        self._config = STATE_CONFIG[state]
        if state == RAIN_SHATTER:
            self._explode_columns()
        elif state == RAIN_STOP:
            self.fade_alpha = 255.0
        elif state == RAIN_OFF:
            self._clear_all()
        elif state == RAIN_WE:
            self._we_elapsed = 0.0
            self.fade_alpha = 255.0
        else:
            self.fade_alpha = 255.0

    def _clear_all(self) -> None:
        for c in self.columns:
            c.active = False
            c.chars.clear()
            c.word = None
            c.word_pos = 0
        self.particles = []
        self.fade_alpha = 255.0

    def _explode_columns(self) -> None:
        self.particles = []
        for c in self.columns:
            if not c.chars:
                continue
            n = len(c.chars)
            for i, ch in enumerate(c.chars):
                row = int(c.head_row) - (n - 1 - i)
                if 0 <= row < self.n_rows:
                    self.particles.append(Particle(
                        x=float(c.x),
                        y=float(row * self.cell_h),
                        char=ch,
                        vx=self.rng.uniform(-220, 220),
                        vy=self.rng.uniform(-60, 220),
                        ttl=self.rng.uniform(0.8, 1.8),
                    ))
            c.active = False
            c.chars.clear()
            c.word = None
            c.word_pos = 0

    # -- per-frame update -----------------------------------------------------

    def update(self, dt: float) -> None:
        if self.state == RAIN_OFF:
            return
        if self.state == RAIN_SHATTER:
            self._update_shatter(dt)
            return
        if self.state == RAIN_STOP:
            self.fade_alpha = max(0.0, self.fade_alpha - self.STOP_FADE_PER_SEC * dt)
            return
        if self.state == RAIN_WE:
            self._we_elapsed += dt

        self._update_columns(dt)

    def _update_shatter(self, dt: float) -> None:
        survivors: List[Particle] = []
        for p in self.particles:
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.vy += self.GRAVITY * dt
            p.age += dt
            if (p.age < p.ttl and -40 <= p.x <= self.width + 40
                    and p.y <= self.height + 40):
                survivors.append(p)
        self.particles = survivors

    def _density_scale(self) -> float:
        if self.state == RAIN_WE:
            return max(0.0, 1.0 - self._we_elapsed / self.WE_DECAY_SECONDS)
        return 1.0

    def _speed_scale(self) -> float:
        if self.state == RAIN_WE:
            return max(0.05, 1.0 - self._we_elapsed / (self.WE_DECAY_SECONDS + 2))
        return 1.0

    def _update_columns(self, dt: float) -> None:
        cfg = self._config
        target_active = int(self.n_cols * cfg.density * self._density_scale())
        active = [c for c in self.columns if c.active]
        if len(active) < target_active:
            inactive = [c for c in self.columns if not c.active]
            self.rng.shuffle(inactive)
            for c in inactive[: target_active - len(active)]:
                self._spawn(c, cfg)

        speed_mul = self._speed_scale()
        for c in self.columns:
            if not c.active and not c.chars:
                continue
            if c.active:
                c.head_partial += c.speed * speed_mul * dt
                while c.head_partial >= 1.0:
                    c.head_partial -= 1.0
                    c.head_row += 1
                    c.chars.append(self._next_char(c, cfg))
                    if len(c.chars) > c.trail_len:
                        c.chars.pop(0)
                if c.head_row - c.trail_len > self.n_rows:
                    c.active = False
                    c.chars.clear()
                    c.word = None
                    c.word_pos = 0

    def _spawn(self, c: Column, cfg: StateConfig) -> None:
        c.active = True
        c.head_row = float(-self.rng.randint(0, max(1, self.n_rows // 3)))
        c.head_partial = 0.0
        lo, hi = cfg.speed_range
        c.speed = self.rng.uniform(lo, hi) if hi > lo else lo
        c.trail_len = cfg.trail_len
        c.chars = []
        if cfg.allowed_words and self.rng.random() < cfg.word_freq:
            c.word = self.rng.choice(cfg.allowed_words)
            c.word_pos = 0
        else:
            c.word = None
            c.word_pos = 0

    def _next_char(self, c: Column, cfg: StateConfig) -> str:
        if c.word is not None:
            if c.word_pos < len(c.word):
                ch = c.word[c.word_pos]
                c.word_pos += 1
                return ch
            c.word = None
            c.word_pos = 0
        return self.rng.choice(cfg.char_pool)

    # -- rendering ------------------------------------------------------------

    def render(self) -> pygame.Surface:
        self.surface.fill((0, 0, 0, 0))
        if self.state == RAIN_OFF:
            return self.surface
        if self.state == RAIN_SHATTER:
            for p in self.particles:
                a = max(0, int(255 * (1.0 - p.age / p.ttl)))
                self._blit_char(p.x, p.y, p.char, BRIGHT, a)
            return self.surface

        global_alpha = int(self.fade_alpha)
        for c in self.columns:
            if not c.chars:
                continue
            n = len(c.chars)
            for i, ch in enumerate(c.chars):
                row = int(c.head_row) - (n - 1 - i)
                if row < 0 or row >= self.n_rows:
                    continue
                color, alpha = self._trail_color(n - 1 - i, c.trail_len)
                alpha = min(alpha, global_alpha)
                if alpha > 0:
                    self._blit_char(c.x, row * self.cell_h, ch, color, alpha)
        return self.surface

    def _trail_color(self, depth: int, trail_len: int) -> Tuple[Tuple[int, int, int], int]:
        if depth == 0:
            return HEAD_COLOR, 255
        third = max(1, trail_len // 3)
        if depth < third:
            return BRIGHT, max(60, 255 - depth * 18)
        if depth < 2 * third:
            return TRAIL, max(30, 200 - depth * 10)
        return DARK, max(0, 100 - depth * 6)

    def _blit_char(self, x: float, y: float, ch: str,
                   color: Tuple[int, int, int], alpha: int) -> None:
        if alpha <= 0:
            return
        bucket = max(1, min(8, (alpha + 31) // 32))
        key = (ch, color, bucket)
        surf = self._glyph_cache.get(key)
        if surf is None:
            base = self.font.render(ch, True, color)
            surf = pygame.Surface(base.get_size(), pygame.SRCALPHA)
            surf.blit(base, (0, 0))
            a = min(255, bucket * 32 - 1)
            surf.fill((255, 255, 255, a), special_flags=pygame.BLEND_RGBA_MULT)
            self._glyph_cache[key] = surf
        self.surface.blit(surf, (int(x), int(y)))


# --- Standalone demo ----------------------------------------------------------

def _demo() -> None:
    pygame.init()
    width, height = 960, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pixstars digital rain demo")
    clock = pygame.time.Clock()
    label_font = pygame.font.SysFont("monospace", 20, bold=True)

    renderer = DigitalRainRenderer(width, height)
    cycle = [
        (RAIN_OFF, 1.5), (RAIN_TRACES, 4.0), (RAIN_BUILDING, 4.0),
        (RAIN_STORM, 4.0), (RAIN_SHATTER, 2.0), (RAIN_STOP, 2.0),
        (RAIN_GENTLE, 4.0), (RAIN_NAMES, 4.0), (RAIN_THREE, 4.0),
        (RAIN_WE, 12.0),
    ]
    idx = 0
    state_time = 0.0
    renderer.set_state(cycle[0][0])

    running = True
    while running:
        dt = clock.tick(30) / 1000.0
        state_time += dt
        if state_time >= cycle[idx][1]:
            idx = (idx + 1) % len(cycle)
            renderer.set_state(cycle[idx][0])
            state_time = 0.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (
                    pygame.K_ESCAPE, pygame.K_q):
                running = False

        renderer.update(dt)
        screen.fill((0, 0, 0))
        screen.blit(renderer.render(), (0, 0))
        label = label_font.render(
            f"{cycle[idx][0]}   ({state_time:0.1f}s)", True, (0, 255, 65))
        screen.blit(label, (12, 12))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    _demo()
