#!/usr/bin/env python3
"""
Pixstars Cave Simulator -- LED Rings

A pygame-based stand-in for the ESP32 cave controller used during
software-only rehearsals. Listens on the same OSC port (8000) and handles
the same endpoints as the real firmware, rendering the rear (16 LED) and
front (35 LED) rings as concentric circles and logging non-LED commands
as a text overlay.

Run:
    python -m simulator.led_rings
"""

from __future__ import annotations

import argparse
import colorsys
import math
import threading
import time
from dataclasses import dataclass

import pygame
from pythonosc import dispatcher, osc_server


REAR_COUNT = 16
FRONT_COUNT = 35
DEFAULT_PORT = 8000
WINDOW_SIZE = (600, 600)
REAR_RADIUS = 150
FRONT_RADIUS = 250
LED_DOT_RADIUS = 12
BG_COLOR = (0, 0, 0)
TEXT_COLOR = (200, 200, 200)
DIM_COLOR = (20, 20, 20)


def _format_timecode(elapsed: float) -> str:
    """Format elapsed seconds as MM:SS.s (e.g. '03:45.2')."""
    m = int(elapsed) // 60
    s = elapsed - m * 60
    return f"{m:02d}:{s:04.1f}"


@dataclass
class RingState:
    r: int = 0
    g: int = 0
    b: int = 0
    mode: str = "off"
    set_at: float = 0.0


class CaveSimulator:
    """Pygame OSC listener that mimics the ESP32 cave controller."""

    def __init__(self, port: int = DEFAULT_PORT):
        self.port = port
        self.running = True

        self.rear = RingState()
        self.front = RingState()
        self.last_command = "(waiting for OSC commands on port %d)" % port
        self.timecode = 0.0
        self._lock = threading.Lock()

        self._dispatcher = dispatcher.Dispatcher()
        self._dispatcher.map("/led/rear", self._handle_led_rear)
        self._dispatcher.map("/led/front", self._handle_led_front)
        self._dispatcher.map("/servo/set", self._handle_servo_set)
        self._dispatcher.map("/servo/speed", self._handle_servo_speed)
        self._dispatcher.map("/head/nod", self._handle_head_nod)
        self._dispatcher.map("/turntable/rotate", self._handle_turntable_rotate)
        self._dispatcher.map("/turntable/goto", self._handle_turntable_goto)
        self._dispatcher.map("/turntable/origin", self._handle_turntable_origin)
        self._dispatcher.map("/turntable/stop", self._handle_turntable_stop)
        self._dispatcher.map("/ping", self._handle_ping)
        self._dispatcher.map("/timecode", self._handle_timecode)

    # -- OSC handlers -----------------------------------------------------

    def _set_ring(self, ring: RingState, args):
        if len(args) < 3:
            print("  [SIM WARNING] LED command needs at least r,g,b")
            return
        r, g, b = int(args[0]), int(args[1]), int(args[2])
        mode = str(args[3]) if len(args) >= 4 else "solid"
        with self._lock:
            ring.r, ring.g, ring.b = r, g, b
            ring.mode = mode
            ring.set_at = time.monotonic()

    def _handle_led_rear(self, address, *args):
        self._set_ring(self.rear, args)
        print(f"  [SIM] /led/rear {args}")

    def _handle_led_front(self, address, *args):
        self._set_ring(self.front, args)
        print(f"  [SIM] /led/front {args}")

    def _log_cmd(self, text: str):
        with self._lock:
            self.last_command = text
        print(f"  [SIM] {text}")

    def _handle_servo_set(self, address, *args):
        self._log_cmd(f"/servo/set ch={args[0]} angle={args[1]}" if len(args) >= 2 else "/servo/set ?")

    def _handle_servo_speed(self, address, *args):
        self._log_cmd(f"/servo/speed ch={args[0]} speed={args[1]}" if len(args) >= 2 else "/servo/speed ?")

    def _handle_head_nod(self, address, *args):
        if len(args) >= 2:
            self._log_cmd(f"/head/nod angle={args[0]} speed={args[1]}")
        elif args:
            self._log_cmd(f"/head/nod angle={args[0]}")
        else:
            self._log_cmd("/head/nod ?")

    def _handle_turntable_rotate(self, address, *args):
        self._log_cmd(f"/turntable/rotate deg={args[0]} speed={args[1]}" if len(args) >= 2 else "/turntable/rotate ?")

    def _handle_turntable_goto(self, address, *args):
        self._log_cmd(f"/turntable/goto deg={args[0]} speed={args[1]}" if len(args) >= 2 else "/turntable/goto ?")

    def _handle_turntable_origin(self, address, *args):
        self._log_cmd("/turntable/origin")

    def _handle_turntable_stop(self, address, *args):
        self._log_cmd("/turntable/stop")

    def _handle_ping(self, address, *args):
        self._log_cmd("/ping")

    def _handle_timecode(self, address, *args):
        if not args:
            return
        try:
            with self._lock:
                self.timecode = float(args[0])
        except (TypeError, ValueError):
            pass

    # -- LED rendering ----------------------------------------------------

    def _led_color(self, ring: RingState, index: int, count: int, now: float):
        if ring.mode == "off":
            return DIM_COLOR
        base = (ring.r, ring.g, ring.b)
        elapsed = now - ring.set_at
        if ring.mode == "solid":
            return base
        if ring.mode == "breathe":
            # ~2s period sine fade between 10% and 100%
            phase = 0.5 - 0.5 * math.cos(2 * math.pi * elapsed / 2.0)
            k = 0.1 + 0.9 * phase
            return (int(base[0] * k), int(base[1] * k), int(base[2] * k))
        if ring.mode == "pulse":
            # quick flash (200ms) then fade over ~1s, then idle dim
            if elapsed < 0.2:
                k = 1.0
            elif elapsed < 1.2:
                k = max(0.0, 1.0 - (elapsed - 0.2))
            else:
                return DIM_COLOR
            return (int(base[0] * k), int(base[1] * k), int(base[2] * k))
        if ring.mode == "rainbow":
            # rotating hue around the ring, 4s/rev
            offset = (elapsed / 4.0) % 1.0
            hue = (index / count + offset) % 1.0
            v = max(base) / 255.0 if max(base) > 0 else 1.0
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, v)
            return (int(r * 255), int(g * 255), int(b * 255))
        return base

    def _draw_ring(self, screen, ring: RingState, count: int, radius: int, now: float):
        cx, cy = WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2
        for i in range(count):
            theta = -math.pi / 2 + 2 * math.pi * i / count
            x = int(cx + radius * math.cos(theta))
            y = int(cy + radius * math.sin(theta))
            color = self._led_color(ring, i, count, now)
            # outline + filled disc for visibility against black background
            pygame.draw.circle(screen, (40, 40, 40), (x, y), LED_DOT_RADIUS + 1)
            pygame.draw.circle(screen, color, (x, y), LED_DOT_RADIUS)

    # -- Main loop --------------------------------------------------------

    def start(self):
        osc_srv = osc_server.ThreadingOSCUDPServer(("0.0.0.0", self.port), self._dispatcher)
        osc_thread = threading.Thread(target=osc_srv.serve_forever, daemon=True)
        osc_thread.start()

        pygame.init()
        pygame.display.set_caption("Pixstars Cave Simulator")
        screen = pygame.display.set_mode(WINDOW_SIZE)
        font = pygame.font.Font(None, 22)
        small = pygame.font.Font(None, 18)
        tc_font = pygame.font.SysFont("monospace", 20, bold=True)
        clock = pygame.time.Clock()

        print("=" * 50)
        print("  PIXSTARS CAVE SIMULATOR")
        print(f"  OSC port: {self.port}")
        print(f"  Rear ring: {REAR_COUNT} LEDs   Front ring: {FRONT_COUNT} LEDs")
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
                rear_snapshot = RingState(self.rear.r, self.rear.g, self.rear.b, self.rear.mode, self.rear.set_at)
                front_snapshot = RingState(self.front.r, self.front.g, self.front.b, self.front.mode, self.front.set_at)
                last_cmd = self.last_command
                tc = self.timecode

            self._draw_ring(screen, front_snapshot, FRONT_COUNT, FRONT_RADIUS, now)
            self._draw_ring(screen, rear_snapshot, REAR_COUNT, REAR_RADIUS, now)

            # Header labels
            header = small.render(
                f"front: rgb({front_snapshot.r},{front_snapshot.g},{front_snapshot.b}) {front_snapshot.mode}   "
                f"rear: rgb({rear_snapshot.r},{rear_snapshot.g},{rear_snapshot.b}) {rear_snapshot.mode}",
                True, TEXT_COLOR,
            )
            screen.blit(header, (12, 10))

            # Bottom overlay: last non-LED command
            overlay = font.render(last_cmd, True, TEXT_COLOR)
            screen.blit(overlay, (12, WINDOW_SIZE[1] - 28))

            # Top-right timecode overlay
            tc_surf = tc_font.render(_format_timecode(tc), True, (255, 255, 255))
            screen.blit(tc_surf, (WINDOW_SIZE[0] - tc_surf.get_width() - 10, 8))

            pygame.display.flip()
            clock.tick(30)

        osc_srv.shutdown()
        pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="Pixstars Cave Simulator (LED rings)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="OSC listen port")
    args = parser.parse_args()
    CaveSimulator(port=args.port).start()


if __name__ == "__main__":
    main()
