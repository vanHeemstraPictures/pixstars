#!/usr/bin/env python3
"""
Pixstars Laser Galvo Simulator

A pygame stand-in for the lamp head's RGB laser galvo scanner used during
software-only rehearsals. Listens on OSC port 9005 for laser cues and
renders them as bright vector lines on a black background, mimicking the
look of a real ILDA galvo laser projector tracing point-by-point.

Run:
    python -m simulator.laser_galvo
"""

from __future__ import annotations

import argparse
import math
import threading
import time
from dataclasses import dataclass

import pygame
from pythonosc import dispatcher, osc_server


DEFAULT_PORT = 9005
WINDOW_SIZE = (600, 400)
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (180, 180, 180)


def _format_timecode(elapsed: float) -> str:
    """Format elapsed seconds as MM:SS.s (e.g. '03:45.2')."""
    m = int(elapsed) // 60
    s = elapsed - m * 60
    return f"{m:02d}:{s:04.1f}"

# Per-pattern colors (BGR-bright, like real lasers)
COL_SWEEP = (60, 255, 90)
COL_STICK = (60, 255, 90)
COL_TEXT = (80, 160, 255)
COL_SIG = (255, 60, 60)

# Approximate "full draw" durations for the progressive patterns
DUR_STICK = 3.0
DUR_TEXT = 2.0
DUR_SIG = 3.0


# ── Pattern path builders ────────────────────────────────────────────────────
# Each builder returns a list of polylines (each a list of (x, y) points).
# The renderer interpolates progressively along the concatenated path.

def _stick_figure_segments(cx: int, cy: int) -> list[list[tuple[float, float]]]:
    """Child-like stick figure built from closed head circle + 4 limb strokes."""
    head_r = 22
    head_y = cy - 60
    head = [
        (cx + head_r * math.cos(2 * math.pi * i / 36),
         head_y + head_r * math.sin(2 * math.pi * i / 36))
        for i in range(37)
    ]
    body_top = (cx, head_y + head_r)
    body_bot = (cx, head_y + head_r + 55)
    return [
        head,
        [body_top, body_bot],
        [(cx - 28, head_y + head_r + 18), (cx + 28, head_y + head_r + 18)],
        [body_bot, (cx - 22, head_y + head_r + 90)],
        [body_bot, (cx + 22, head_y + head_r + 90)],
    ]


def _ai_text_segments(cx: int, cy: int) -> list[list[tuple[float, float]]]:
    """Blocky vector 'I AM' rendered as polyline strokes per letter."""
    h = 70  # glyph height
    w = 38  # glyph width
    gap = 18
    total_w = 3 * w + 2 * gap + w  # I + gap + A + gap + M (approx)
    x0 = cx - total_w / 2
    y0 = cy - h / 2
    yb = y0 + h  # baseline

    segs: list[list[tuple[float, float]]] = []

    # I -- top serif, vertical bar, bottom serif (three strokes)
    ix = x0
    segs.append([(ix, y0), (ix + w, y0)])
    segs.append([(ix + w / 2, y0), (ix + w / 2, yb)])
    segs.append([(ix, yb), (ix + w, yb)])

    # A -- left diag, right diag, crossbar (single polyline for outline)
    ax = ix + w + gap
    apex = (ax + w / 2, y0)
    segs.append([(ax, yb), apex, (ax + w, yb)])
    segs.append([(ax + w * 0.18, yb - h * 0.35),
                 (ax + w * 0.82, yb - h * 0.35)])

    # M -- four strokes as one polyline
    mx = ax + w + gap
    segs.append([
        (mx, yb),
        (mx, y0),
        (mx + w / 2, y0 + h * 0.55),
        (mx + w, y0),
        (mx + w, yb),
    ])

    return segs


def _signature_segments(cx: int, cy: int) -> list[list[tuple[float, float]]]:
    """Signature tracing 'A.I.' as letter strokes followed by a cursive flourish."""
    h = 70
    w = 40
    gap = 18
    dot_r = 4
    flourish_w = 70
    total_w = w + gap + 2 * dot_r + gap + w + gap + 2 * dot_r + gap + flourish_w
    x0 = cx - total_w / 2
    y0 = cy - h / 2
    yb = y0 + h

    segs: list[list[tuple[float, float]]] = []

    # A -- left diag, apex, right diag (one polyline) + crossbar
    ax = x0
    apex = (ax + w / 2, y0)
    segs.append([(ax, yb), apex, (ax + w, yb)])
    segs.append([(ax + w * 0.18, yb - h * 0.35),
                 (ax + w * 0.82, yb - h * 0.35)])

    # Dot after A (small filled-look circle traced as polyline)
    cx1 = ax + w + gap + dot_r
    segs.append([
        (cx1 + dot_r * math.cos(2 * math.pi * i / 16),
         yb + dot_r * math.sin(2 * math.pi * i / 16))
        for i in range(17)
    ])

    # I -- top serif, vertical bar, bottom serif
    ix = cx1 + dot_r + gap
    segs.append([(ix, y0), (ix + w, y0)])
    segs.append([(ix + w / 2, y0), (ix + w / 2, yb)])
    segs.append([(ix, yb), (ix + w, yb)])

    # Dot after I
    cx2 = ix + w + gap + dot_r
    segs.append([
        (cx2 + dot_r * math.cos(2 * math.pi * i / 16),
         yb + dot_r * math.sin(2 * math.pi * i / 16))
        for i in range(17)
    ])

    # Trailing cursive flourish
    fx0 = cx2 + dot_r + gap
    flourish: list[tuple[float, float]] = []
    n = 80
    for i in range(n + 1):
        t = i / n
        x = fx0 + t * flourish_w
        y = yb - 8 + 14 * math.sin(t * math.pi * 3.0)
        flourish.append((x, y))
    segs.append(flourish)

    return segs


# ── Simulator ────────────────────────────────────────────────────────────────

@dataclass
class LaserState:
    scene: str = "BLACKOUT"
    set_at: float = 0.0


class LaserSimulator:
    """Pygame OSC listener that mimics the lamp's ILDA galvo laser."""

    def __init__(self, port: int = DEFAULT_PORT):
        self.port = port
        self.running = True
        self.state = LaserState(set_at=time.monotonic())
        self.last_command = "(waiting for OSC commands on port %d)" % port
        self.timecode = 0.0
        self._lock = threading.Lock()

        cx, cy = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2
        # Pre-compute static pattern geometries
        self._stick = _stick_figure_segments(cx, cy)
        self._text = _ai_text_segments(cx, cy)
        self._sig = _signature_segments(cx, cy)

        self._dispatcher = dispatcher.Dispatcher()
        self._dispatcher.map("/laser/scene", self._handle_scene)
        self._dispatcher.map("/laser/clear", self._handle_clear)
        self._dispatcher.map("/timecode", self._handle_timecode)

    # -- OSC handlers ----------------------------------------------------

    def _handle_scene(self, address, *args):
        if not args:
            print("  [LASER SIM WARNING] /laser/scene needs a cmd string")
            return
        cmd = str(args[0])
        with self._lock:
            self.state = LaserState(scene=cmd, set_at=time.monotonic())
            self.last_command = f"/laser/scene {cmd}"
        print(f"  [LASER SIM] /laser/scene {cmd}")

    def _handle_clear(self, address, *args):
        with self._lock:
            self.state = LaserState(scene="BLACKOUT", set_at=time.monotonic())
            self.last_command = "/laser/clear"
        print("  [LASER SIM] /laser/clear")

    def _handle_timecode(self, address, *args):
        if not args:
            return
        try:
            with self._lock:
                self.timecode = float(args[0])
        except (TypeError, ValueError):
            pass

    # -- Drawing helpers -------------------------------------------------

    @staticmethod
    def _draw_glow_line(screen, color, p0, p1):
        """Draw a bright vector line with a soft glow halo behind it."""
        # Outer glow (dim, wide)
        glow = (color[0] // 4, color[1] // 4, color[2] // 4)
        pygame.draw.line(screen, glow, p0, p1, 6)
        # Mid glow
        mid = (color[0] // 2, color[1] // 2, color[2] // 2)
        pygame.draw.line(screen, mid, p0, p1, 3)
        # Bright core
        pygame.draw.aaline(screen, color, p0, p1)

    def _draw_polyline_progress(self, screen, color, pts, progress: float):
        """Draw a polyline up to fractional progress (0..1) along its length."""
        if progress <= 0 or len(pts) < 2:
            return
        # Compute cumulative length
        seg_len = []
        total = 0.0
        for i in range(len(pts) - 1):
            dx = pts[i + 1][0] - pts[i][0]
            dy = pts[i + 1][1] - pts[i][1]
            d = math.hypot(dx, dy)
            seg_len.append(d)
            total += d
        if total <= 0:
            return
        target = total * min(1.0, progress)
        acc = 0.0
        for i, d in enumerate(seg_len):
            p0 = pts[i]
            p1 = pts[i + 1]
            if acc + d <= target:
                self._draw_glow_line(screen, color, p0, p1)
                acc += d
            else:
                # partial segment
                remain = target - acc
                if remain > 0 and d > 0:
                    f = remain / d
                    px = p0[0] + (p1[0] - p0[0]) * f
                    py = p0[1] + (p1[1] - p0[1]) * f
                    self._draw_glow_line(screen, color, p0, (px, py))
                break

    def _draw_segments_progressive(self, screen, color, segments, duration, elapsed):
        """Sequentially draw a list of polylines over `duration` seconds."""
        total_len = 0.0
        seg_lengths = []
        for seg in segments:
            L = 0.0
            for i in range(len(seg) - 1):
                L += math.hypot(seg[i + 1][0] - seg[i][0],
                                seg[i + 1][1] - seg[i][1])
            seg_lengths.append(L)
            total_len += L
        if total_len <= 0:
            return
        target = total_len * min(1.0, elapsed / duration)
        acc = 0.0
        for seg, L in zip(segments, seg_lengths):
            if acc + L <= target:
                self._draw_polyline_progress(screen, color, seg, 1.0)
                acc += L
            else:
                remain = target - acc
                if remain > 0 and L > 0:
                    self._draw_polyline_progress(screen, color, seg, remain / L)
                break

    # -- Scene renderers -------------------------------------------------

    def _render_sweep(self, screen, elapsed: float):
        """Bright green beam sweeping left-to-right-to-left, lighthouse style."""
        margin = 40
        x_min = margin
        x_max = WINDOW_SIZE[0] - margin
        period = 2.4  # seconds for a full back-and-forth
        phase = 0.5 - 0.5 * math.cos(2 * math.pi * (elapsed % period) / period)
        x = x_min + (x_max - x_min) * phase
        # Sweep beam goes from a virtual source at the top center down to (x, bottom)
        src = (WINDOW_SIZE[0] // 2, 30)
        tip = (x, WINDOW_SIZE[1] - 30)
        self._draw_glow_line(screen, COL_SWEEP, src, tip)
        # Small bright dot at the source
        pygame.draw.circle(screen, COL_SWEEP, src, 4)

    def _render(self, screen, scene: str, elapsed: float):
        if scene == "LASER_SWEEP":
            self._render_sweep(screen, elapsed)
        elif scene == "LASER_STICK_FIGURE":
            self._draw_segments_progressive(
                screen, COL_STICK, self._stick, DUR_STICK, elapsed
            )
        elif scene == "LASER_AI_TEXT":
            self._draw_segments_progressive(
                screen, COL_TEXT, self._text, DUR_TEXT, elapsed
            )
        elif scene == "LASER_SIGNATURE":
            self._draw_segments_progressive(
                screen, COL_SIG, self._sig, DUR_SIG, elapsed
            )
        # BLACKOUT or unknown: draw nothing

    # -- Main loop -------------------------------------------------------

    def start(self):
        osc_srv = osc_server.ThreadingOSCUDPServer(
            ("0.0.0.0", self.port), self._dispatcher
        )
        osc_thread = threading.Thread(target=osc_srv.serve_forever, daemon=True)
        osc_thread.start()

        pygame.init()
        pygame.display.set_caption("Pixstars Laser Galvo Simulator")
        screen = pygame.display.set_mode(WINDOW_SIZE)
        font = pygame.font.Font(None, 20)
        small = pygame.font.Font(None, 16)
        tc_font = pygame.font.SysFont("monospace", 20, bold=True)
        clock = pygame.time.Clock()

        print("=" * 50)
        print("  PIXSTARS LASER GALVO SIMULATOR")
        print(f"  OSC port: {self.port}")
        print("  Scenes: LASER_SWEEP, LASER_STICK_FIGURE,")
        print("          LASER_AI_TEXT, LASER_SIGNATURE, BLACKOUT")
        print("  ESC or window close to quit")
        print("=" * 50)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            now = time.monotonic()
            screen.fill(BG_COLOR)

            with self._lock:
                scene = self.state.scene
                set_at = self.state.set_at
                last_cmd = self.last_command
                tc = self.timecode

            elapsed = now - set_at
            self._render(screen, scene, elapsed)

            header = small.render(f"scene: {scene}   t+{elapsed:5.2f}s",
                                  True, TEXT_COLOR)
            screen.blit(header, (10, 8))
            overlay = font.render(last_cmd, True, TEXT_COLOR)
            screen.blit(overlay, (10, WINDOW_SIZE[1] - 22))

            # Top-right timecode overlay
            tc_surf = tc_font.render(_format_timecode(tc), True, (255, 255, 255))
            screen.blit(tc_surf, (WINDOW_SIZE[0] - tc_surf.get_width() - 10, 8))

            pygame.display.flip()
            clock.tick(60)

        osc_srv.shutdown()
        pygame.quit()


def main():
    parser = argparse.ArgumentParser(
        description="Pixstars Laser Galvo Simulator"
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT,
                        help="OSC listen port")
    args = parser.parse_args()
    LaserSimulator(port=args.port).start()


if __name__ == "__main__":
    main()
