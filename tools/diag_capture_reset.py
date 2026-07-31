#!/usr/bin/env python3
"""Reset ESP32 via DTR/RTS, then read serial for N seconds with timestamps.

Wave-4 hardware capture helper: forces a fresh boot so the granular
UDP_READY -> SETUP_DONE markers are always captured from t=0.
"""
import sys, time, serial

port = sys.argv[1] if len(sys.argv) > 1 else "/dev/cu.usbmodem5C4C0912561"
secs = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0

ser = serial.Serial(port, 115200, timeout=0.2)
ser.setDTR(False)
ser.setRTS(True)
time.sleep(0.1)
ser.setRTS(False)
ser.reset_input_buffer()
t0 = time.monotonic()
buf = bytearray()
try:
    while time.monotonic() - t0 < secs:
        chunk = ser.read(512)
        if chunk:
            buf.extend(chunk)
            while b"\n" in buf:
                line, _, buf = buf.partition(b"\n")
                try:
                    text = line.decode("utf-8", errors="replace").rstrip("\r")
                except Exception:
                    text = repr(line)
                print(f"[{time.monotonic()-t0:6.2f}s] {text}", flush=True)
    if buf:
        print(f"[{time.monotonic()-t0:6.2f}s] <partial> {buf!r}", flush=True)
finally:
    ser.close()
