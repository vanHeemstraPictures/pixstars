# led-adapter

WS2812 5050 RGB LED Ring 16 adapter board (Cave Architecture v3).

## Purpose

Clean interface between the cave **ESP32-S3** (RMT peripheral GPIO) and the
**WS2812 5050 RGB LED Ring 16** that physically lives in the lamp head.
Replaces the earlier Raspberry Pi GPIO assumption -- in v3 the ring is driven
from the cave ESP32 over the central cable column, not from a Pi.

## Features

- **5V / GND / DATA** terminals from the cave power-distribution board
  (5V rail from MEAN WELL LRS-50-5)
- **330 ohm series resistor** on the data line at the ESP32 end
- **1000 uF capacitor** near the LED ring side (decoupling / inrush)
- **JST-SM 3-pin connector** at the lamp head junction so the ring can be
  swapped without rewiring the cable column
- Optional **level shifter** footprint (e.g. 74AHCT125) for cases where the
  3.3V ESP32 data line proves marginal at the ring; usually not needed with
  the 330 ohm + short JST-SM tail

## Routing

ESP32-S3 GPIO (RMT) -> 330 ohm -> cable column -> JST-SM at lamp head ->
1000 uF || WS2812 Ring 16 DIN.

## Status

Phase 1 -- documentation only. No .fzz yet (added in a separate task).
