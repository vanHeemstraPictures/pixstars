#!/usr/bin/env python3
"""
Pixstars Projection — Display Controller

A pygame-based projection display that listens for OSC commands from the
Show Conductor and displays the correct visuals for each scene.

Listens on port 9002 for:
    /projection/scene <scene_name>  — Switch to named scene

Usage:
    source .venv/bin/activate
    python -m projection.display               # Windowed mode (mock)
    python -m projection.display --fullscreen   # Fullscreen on secondary display
    python -m projection.display --size 1280 720
"""

import argparse
import os
import signal
import sys
import threading
from pathlib import Path

import pygame
from pythonosc import dispatcher, osc_server

from projection.scenes import get_scene, list_scenes, Scene, ASSETS_DIR


class ProjectionDisplay:
    """Pygame-based projection display controlled by OSC."""

    def __init__(
        self,
        port: int = 9002,
        fullscreen: bool = False,
        width: int = 1280,
        height: int = 720,
        display_index: int = 0,
    ):
        self.port = port
        self.fullscreen = fullscreen
        self.width = width
        self.height = height
        self.display_index = display_index

        self.current_scene: Scene | None = None
        self.pending_scene: Scene | None = None
        self.running = True

        # Scene change lock
        self._lock = threading.Lock()

        # Set up OSC
        self._dispatcher = dispatcher.Dispatcher()
        self._dispatcher.map("/projection/scene", self._handle_scene)

    def _handle_scene(self, address: str, *args):
        """Handle /projection/scene OSC messages."""
        if not args:
            print("  [PROJ WARNING] /projection/scene with no arguments")
            return

        scene_name = str(args[0])
        try:
            scene = get_scene(scene_name)
        except KeyError as e:
            print(f"  [PROJ ERROR] {e}")
            return

        old = self.current_scene.name if self.current_scene else "NONE"
        print(f"  [PROJ] {old} → {scene.name}: {scene.description}")

        with self._lock:
            self.pending_scene = scene

    def _load_image(self, scene: Scene) -> pygame.Surface | None:
        """Load the image asset for a scene, or return None for BLACKOUT."""
        if not scene.image_file:
            return None

        path = ASSETS_DIR / scene.image_file
        if not path.exists():
            # Create a placeholder with the scene name
            return self._create_placeholder(scene)

        try:
            img = pygame.image.load(str(path)).convert()
            return pygame.transform.scale(img, (self.width, self.height))
        except pygame.error as e:
            print(f"  [PROJ WARNING] Could not load {path}: {e}")
            return self._create_placeholder(scene)

    def _create_placeholder(self, scene: Scene) -> pygame.Surface:
        """Create a placeholder surface with the scene name displayed."""
        surface = pygame.Surface((self.width, self.height))
        surface.fill(scene.background_color)

        # Render scene name as text
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)

        # Pick text color that contrasts with background
        bg = scene.background_color
        text_color = (255, 255, 255) if (bg[0] + bg[1] + bg[2]) < 384 else (0, 0, 0)

        # Title
        title = font_large.render(scene.name, True, text_color)
        title_rect = title.get_rect(center=(self.width // 2, self.height // 2 - 30))
        surface.blit(title, title_rect)

        # Description
        desc = font_small.render(scene.description, True, text_color)
        desc_rect = desc.get_rect(center=(self.width // 2, self.height // 2 + 30))
        surface.blit(desc, desc_rect)

        # Placeholder notice
        notice = font_small.render("[PLACEHOLDER]", True, (128, 128, 128))
        notice_rect = notice.get_rect(center=(self.width // 2, self.height - 40))
        surface.blit(notice, notice_rect)

        return surface

    def start(self):
        """Start the projection display and OSC listener."""
        # Start OSC server in background
        osc_srv = osc_server.ThreadingOSCUDPServer(
            ("0.0.0.0", self.port), self._dispatcher
        )
        osc_thread = threading.Thread(target=osc_srv.serve_forever, daemon=True)
        osc_thread.start()

        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Pixstars Projection")

        if self.fullscreen:
            if self.display_index > 0:
                os.environ["SDL_VIDEO_WINDOW_POS"] = f"{self.width * self.display_index},0"
            screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((self.width, self.height))

        clock = pygame.time.Clock()

        # Start with blackout
        self.current_scene = get_scene("BLACKOUT")
        current_surface = self._load_image(self.current_scene)

        print("=" * 50)
        print(f"  PIXSTARS PROJECTION DISPLAY")
        print(f"  Resolution: {self.width}x{self.height}")
        print(f"  Mode: {'Fullscreen' if self.fullscreen else 'Windowed'}")
        print(f"  OSC port: {self.port}")
        print(f"  Scenes: {', '.join(list_scenes())}")
        print("=" * 50)

        # Main display loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()

            # Check for pending scene change
            with self._lock:
                if self.pending_scene is not None:
                    self.current_scene = self.pending_scene
                    current_surface = self._load_image(self.current_scene)
                    self.pending_scene = None

            # Render
            if current_surface:
                screen.blit(current_surface, (0, 0))
            else:
                screen.fill(self.current_scene.background_color if self.current_scene else (0, 0, 0))

            pygame.display.flip()
            clock.tick(30)

        # Cleanup
        osc_srv.shutdown()
        pygame.quit()


def main():
    parser = argparse.ArgumentParser(description="Pixstars Projection Display")
    parser.add_argument("--port", type=int, default=9002, help="OSC listen port")
    parser.add_argument("--fullscreen", action="store_true", help="Fullscreen mode")
    parser.add_argument("--size", nargs=2, type=int, default=[1280, 720],
                        metavar=("W", "H"), help="Window size (default: 1280 720)")
    parser.add_argument("--display", type=int, default=0,
                        help="Display index for fullscreen (0=primary, 1=secondary)")
    args = parser.parse_args()

    display = ProjectionDisplay(
        port=args.port,
        fullscreen=args.fullscreen,
        width=args.size[0],
        height=args.size[1],
        display_index=args.display,
    )
    display.start()


if __name__ == "__main__":
    main()
