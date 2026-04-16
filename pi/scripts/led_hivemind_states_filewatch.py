import os
import time
import math
import threading
from collections import deque

import numpy as np
import sounddevice as sd
import board
import neopixel

NUM_PIXELS = 12
pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS, auto_write=False)

STATE_FILE = "/tmp/pixstars_lamp_state.txt"
audio_queue = deque(maxlen=3)
smoothed_level = 0.0
last_audio_time = 0

GAIN = 10.0
SMOOTHING = 0.18
SPEECH_TIMEOUT = 0.4

COLOR_IDLE = (255, 100, 0)
COLOR_LISTENING = (0, 80, 255)
COLOR_THINKING = (140, 0, 255)
COLOR_ERROR = (255, 0, 0)

def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

def scale_color(color, brightness):
    brightness = clamp(brightness)
    return tuple(int(c * brightness) for c in color)

def fill_color(color):
    pixels.fill(color)
    pixels.show()

def breathing_wave(t, period=2.8, minimum=0.03, maximum=0.16):
    x = (math.sin((2 * math.pi * t) / period) + 1) / 2
    return minimum + (maximum - minimum) * x

def pulse_wave(t, period=1.2, minimum=0.08, maximum=0.40):
    x = (math.sin((2 * math.pi * t) / period) + 1) / 2
    return minimum + (maximum - minimum) * x

def read_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                value = f.read().strip()
                return value or "idle"
        except Exception:
            return "error"
    return "idle"

def audio_callback(indata, frames, time_info, status):
    global smoothed_level, last_audio_time
    volume = np.linalg.norm(indata) * GAIN
    audio_queue.append(volume)
    avg = np.mean(audio_queue) if audio_queue else volume
    smoothed_level = (SMOOTHING * avg) + ((1 - SMOOTHING) * smoothed_level)
    if smoothed_level > 0.01:
        last_audio_time = time.time()

def render_loop():
    while True:
        state = read_state()
        now = time.time()

        if state == "idle":
            fill_color(scale_color(COLOR_IDLE, breathing_wave(now)))
        elif state == "listening":
            fill_color(scale_color(COLOR_LISTENING, pulse_wave(now, period=1.5, minimum=0.08, maximum=0.35)))
        elif state == "thinking":
            fill_color(scale_color(COLOR_THINKING, pulse_wave(now, period=0.9, minimum=0.08, maximum=0.45)))
        elif state == "speaking":
            fill_color(scale_color((255, 140, 30), clamp(smoothed_level, 0.03, 1.0)))
            if (now - last_audio_time) > SPEECH_TIMEOUT:
                fill_color(scale_color(COLOR_IDLE, breathing_wave(now)))
        elif state == "error":
            fill_color(scale_color(COLOR_ERROR, pulse_wave(now, period=0.35, minimum=0.0, maximum=0.7)))
        else:
            fill_color((0, 0, 0))

        time.sleep(0.02)

def main():
    thread = threading.Thread(target=render_loop, daemon=True)
    thread.start()
    with sd.InputStream(callback=audio_callback):
        while True:
            time.sleep(1)

if __name__ == "__main__":
    main()
