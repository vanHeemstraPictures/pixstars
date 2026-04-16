import time
import math
import threading
from collections import deque

import numpy as np
import sounddevice as sd
import board
import neopixel

NUM_PIXELS = 12
PIXEL_PIN = board.D18
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, auto_write=False)

state = "idle"
last_state_change = time.time()
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

def set_state(new_state):
    global state, last_state_change
    if state != new_state:
        state = new_state
        last_state_change = time.time()

def audio_callback(indata, frames, time_info, status):
    global smoothed_level, last_audio_time
    volume = np.linalg.norm(indata) * GAIN
    audio_queue.append(volume)
    avg = np.mean(audio_queue) if audio_queue else volume
    smoothed_level = (SMOOTHING * avg) + ((1 - SMOOTHING) * smoothed_level)
    if smoothed_level > 0.01:
        last_audio_time = time.time()

def render_loop():
    global state
    while True:
        now = time.time()
        if state == "idle":
            b = breathing_wave(now)
            fill_color(scale_color(COLOR_IDLE, b))
        elif state == "listening":
            b = pulse_wave(now, period=1.5, minimum=0.08, maximum=0.35)
            fill_color(scale_color(COLOR_LISTENING, b))
        elif state == "thinking":
            b = pulse_wave(now, period=0.9, minimum=0.08, maximum=0.45)
            fill_color(scale_color(COLOR_THINKING, b))
        elif state == "speaking":
            b = clamp(smoothed_level, 0.03, 1.0)
            fill_color(scale_color((255, 140, 30), b))
            if (now - last_audio_time) > SPEECH_TIMEOUT:
                set_state("idle")
        elif state == "error":
            b = pulse_wave(now, period=0.35, minimum=0.0, maximum=0.7)
            fill_color(scale_color(COLOR_ERROR, b))
        time.sleep(0.02)

def keyboard_demo():
    print("i=idle l=listening t=thinking s=speaking e=error q=quit")
    while True:
        cmd = input("> ").strip().lower()
        if cmd == "i":
            set_state("idle")
        elif cmd == "l":
            set_state("listening")
        elif cmd == "t":
            set_state("thinking")
        elif cmd == "s":
            set_state("speaking")
        elif cmd == "e":
            set_state("error")
        elif cmd == "q":
            break

def main():
    thread = threading.Thread(target=render_loop, daemon=True)
    thread.start()
    with sd.InputStream(callback=audio_callback):
        keyboard_demo()

if __name__ == "__main__":
    main()
