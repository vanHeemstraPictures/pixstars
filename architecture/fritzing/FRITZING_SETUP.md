FRITZING_SETUP.md

Fritzing Integration for PixStars

Version: 2.0
Status: Recommended
Repository: pixstars/architecture/fritzing

⸻

1. Executive Summary

Fritzing is a visual electronics documentation and prototyping tool that allows hardware systems to be documented using:

* Breadboard diagrams
* Wiring diagrams
* Schematic diagrams
* PCB layouts

For PixStars, Fritzing is used as the authoritative source for documenting all electronic wiring and physical hardware connections in the Cave Architecture v3 build (ESP32-S3 controller, hidden cave under DIY turntable, lamp head with no motors).

Fritzing is not part of the runtime architecture.

Instead, it serves as:

* Hardware documentation
* Assembly documentation
* Troubleshooting documentation
* Wiring verification
* Future maintenance documentation

⸻

2. References

Fritzing

Website

https://fritzing.org

Documentation

https://docs.fritzing.org

GitHub

https://github.com/fritzing/fritzing-app

Reference design for the DIY turntable mechanical and stepper wiring:

https://github.com/MGX3D/Turntable

⸻

3. Why Fritzing Fits PixStars

PixStars combines numerous electronic subsystems hidden under one lamp:

* ESP32-S3 N16R8 DevKit (cave controller, WiFi bridge)
* Pololu Mini Maestro 24-channel servo controller
* MG996R / MG90S servos on the servo rail
* Dynamixel AX-12A head nod (TTL serial via 74HCT245 buffer)
* TMC2209 stepper driver + NEMA 17 (DIY turntable)
* WS2812 5050 RGB LED Ring 16 (in lamp head, driven by ESP32 RMT GPIO)
* ILDAWaveX16 V2 ILDA DAC + 40kpps galvo driver + LPLDD-1A-16V-3CH laser driver
* Opt Lasers 300mW Micro RGB laser galvo scanner (in lamp head)
* MEAN WELL LRS-50-5 and LRS-50-12 power supplies
* Hall effect origin sensor (SS49E / A3144)
* Raspberry Pi Zero 2 WH (lamp head I/O only -- audio, sensors, OV2640 camera)
* Seeed Studio reComputer RK3588-40 (local AI brain in lamp base)

These systems become difficult to understand from text alone.

Fritzing provides visual documentation showing:

* Which component is connected
* Where it is connected
* Which wire color is used
* Which GPIO pins are used
* Which power rails are used

This dramatically simplifies:

* Building
* Maintenance
* Troubleshooting
* Future upgrades

⸻

4. Architectural Role

PixStars Architecture Layers
```
Performance Layer
|
+-- Screenplay (11 scenes, v5.0)
+-- Ardour (audio/MIDI, Pianoteq 9, MODO DRUM)
+-- ROLAND keyboard (live or synced)
|
Show Control Layer
|
+-- Conductor (Python, timeline.yaml -> OSC cues)
+-- Projection subsystem (pygame, OSC port 9002, Epson EB-W05)
+-- Laser galvo simulator (rehearsal)
|
Transport Layer
|
+-- OSC over WiFi/Ethernet (Mac Mini <-> ESP32 cave, ILDAWaveX16 V2)
|
Hardware Layer
|
+-- ESP32-S3 cave controller (Maestro + AX-12A + LED ring + TMC2209)
+-- DIY turntable (NEMA 17 + TMC2209 + GT2 belt + lazy susan)
+-- Lamp head (WS2812 ring, AX-12A nod, laser galvo, Pi Zero 2 WH I/O)
+-- ILDAWaveX16 V2 + galvo driver + LPLDD laser driver chain
+-- Power distribution (LRS-50-5, LRS-50-12, galvo +/-24V PSU)
|
Documentation Layer
|
+-- Fritzing (.fzz files + PNG/SVG exports)
```
Fritzing documents the Hardware Layer.

⸻

5. Recommended Repository Structure
```
pixstars/
|
+-- architecture/
|   +-- fritzing/
|       +-- FRITZING_SETUP.md
|
+-- electronics/
|   +-- fritzing/
|   |
|   +-- cave-controller.fzz
|   +-- power-distribution.fzz
|   +-- lamp-head.fzz
|   +-- turntable.fzz
|   +-- laser-chain.fzz
|   |
|   +-- exports/
|       +-- cave-controller.png
|       +-- power-distribution.png
|       +-- lamp-head.png
|       +-- turntable.png
|       +-- laser-chain.png
```
⸻

6. Required PixStars Diagrams

The following diagrams should be maintained. Each .fzz file corresponds to one of the five cave subsystems.

Cave Controller

Contains:

* ESP32-S3 N16R8 DevKit
* Pololu Mini Maestro 24-channel (serial from ESP32 UART)
* 74HCT245 octal bus transceiver (half-duplex buffer for AX-12A)
* Dynamixel AX-12A TTL serial link (via 74HCT245, DIR pin on ESP32 GPIO 8)
* TMC2209 STEP / DIR / EN lines from ESP32
* Hall effect sensor (SS49E or A3144) input to ESP32 GPIO 27
* Common ground rail

Document:

* ESP32 GPIO assignments (STEP, DIR, EN, RMT data, UART, 74HCT245 DIR)
* Logic ground tie-points
* WiFi role (OSC bridge to Mac Mini)

Filename:

cave-controller.fzz

⸻

Power Distribution

Contains:

* MEAN WELL LRS-50-5 (5V rail -- servos, WS2812 ring via cable column)
* MEAN WELL LRS-50-12 (12V rail -- TMC2209 VMOT, LPLDD-1A-16V-3CH)
* +/-24V galvo PSU (dedicated dual-rail for 40kpps galvo driver board)
* Common ground bus (ESP32 logic GND tied to 5V and 12V returns)
* Capacitor placement (1000uF near WS2812 ring, 100uF across TMC2209 VMOT)

Filename:

power-distribution.fzz

⸻

Lamp Head

Contains:

* WS2812 5050 RGB LED Ring 16 (rear-facing, 5V/GND/DATA via cable column)
* WS2812B 35-LED front ring (front-facing halo, separate JST-SM 3-pin)
* Dynamixel AX-12A (head nod, TTL serial via cable column)
* Opt Lasers 300mW Micro RGB module + 40kpps X/Y galvo mirrors
* JST-SM 3-pin connector at the lamp head junction
* 1000uF electrolytic capacitor at the LED ring
* Raspberry Pi Zero 2 WH (lamp head I/O only -- OV2640 CSI, USB mic, speaker)

Filename:

lamp-head.fzz

⸻

Turntable

Contains:

* NEMA 17 stepper motor (1.8 deg, 200 steps/rev)
* TMC2209 stepper driver (StealthChop, 1/16 microstepping)
* GT2 belt friction-drive (20T pulley to 200mm lazy susan bearing race)
* Bilateral belt tensioner
* Hall effect sensor (SS49E or A3144) + neodymium magnet
* ESP32 STEP / DIR / EN wiring
* 12V VMOT supply from LRS-50-12

Filename:

turntable.fzz

⸻

Laser Chain

Contains:

* ILDAWaveX16 V2 (ESP32-S3 + RP2354, 16-bit DAC, WiFi/Ethernet/USB)
* DB25 fan-out to galvo driver and LPLDD laser driver
* 40kpps galvo driver board (Teclulu GH40 or equivalent)
* LPLDD-1A-16V-3CH laser driver (0-5V analog modulation, 3 channels)
* Opt Lasers 300mW Micro RGB module (638 / 520 / 450 nm)
* Cable column routing (X/Y +/-5V, RGB 0-5V, galvo motor +/-24V)

Filename:

laser-chain.fzz

⸻

7. Lamp Head Reference Design

Initial reference wiring for the WS2812 rear ring (driven from the cave):
```
ESP32-S3 N16R8 (in cave)
   |
   +-- RMT GPIO (data line)
           |
           +-- 330 ohm resistor (cave end)
                   |
                   +-- DATA wire (cable column)
                           |
                           +-- JST-SM 3-pin (lamp head junction)
                                   |
                                   +-- WS2812 D0 (in head)

MEAN WELL LRS-50-5 (cave)
   |
   +-- 5V wire (cable column) ---- JST-SM ---- WS2812 PWR 5V
   +-- GND wire (cable column) --- JST-SM ---- WS2812 GND
                                                  |
                                                  +-- 1000uF capacitor (near ring)

ESP32 logic GND must be tied to MEAN WELL GND (common ground).
```
This design should be the first Fritzing project.

The full lamp head .fzz also documents the AX-12A TTL serial link, the laser galvo cabling, and the Pi Zero 2 WH I/O (audio, OV2640 CSI).

⸻

8. Documentation Standards

Every Fritzing project must include:

Component Names

Example:

ESP32-S3 N16R8 DevKit
Pololu Mini Maestro 24-channel
Dynamixel AX-12A
74HCT245 (DIP-20)
TMC2209 Stepper Driver
NEMA 17 Stepper Motor
WS2812 5050 RGB LED Ring 16
Opt Lasers 300mW Micro RGB
ILDAWaveX16 V2
LPLDD-1A-16V-3CH
MEAN WELL LRS-50-5
MEAN WELL LRS-50-12

⸻

Wire Colours

Use consistent colours, matching wiring/WIRING.md conventions.
```
Red              = +5V
Black            = Ground (GND)
Green / Yellow   = Data (WS2812 DIN, AX-12A TTL, stepper STEP/DIR)
Orange / Yellow  = Servo PWM signal
Red (speaker+)   = Audio +
Black (speaker-) = Audio return
```
⸻

Labels

All ESP32 GPIO pins must be labelled.

Example:

ESP32 RMT GPIO (WS2812 data)
ESP32 GPIO 25 (TMC2209 STEP)
ESP32 GPIO 26 (TMC2209 DIR)
ESP32 GPIO 14 (TMC2209 EN, active low)
ESP32 GPIO 27 (Hall sensor input)
ESP32 GPIO 8 (74HCT245 DIR)
ESP32 UART (to Maestro)

Never leave signal lines unnamed.

⸻

9. Export Standards

Every project should be exported as:

PNG
SVG

Store exports in:

electronics/fritzing/exports/

Recommended resolution:

3000px wide

This allows inclusion in:

* Documentation
* Build manuals
* Presentations
* Maintenance guides

⸻

10. Integration With Existing Documentation

Fritzing diagrams should be referenced from:

wiring/WIRING.md
architecture_decision_records/LAMP_ARCHITECTURE_v3.md
HARDWARE_INVENTORY.md
docs/architecture/ARCHITECTURE.md
SHOW_CONTROL.md (if present)

Example:

See:
electronics/fritzing/exports/cave-controller.png

for complete wiring details.

⸻

11. Future Expansion

Future PixStars hardware can be documented using the same approach.

Examples:

* Additional cameras
* Extra ESP32 satellites
* Additional servos beyond the current rail
* Smoke generator
* DMX interfaces
* MIDI interfaces
* Additional projection hardware

Each subsystem should receive:
```
Subsystem Name
|
+-- .fzz
+-- PNG Export
+-- SVG Export
```
⸻

12. Recommendation

Recommendation: Fritzing is the official electronics documentation platform for PixStars Cave Architecture v3.

Use:

* Markdown for architecture
* Draw.io for system diagrams
* Conductor (timeline.yaml) for show control
* Ardour for audio/MIDI playback
* Fritzing for all hardware wiring documentation

This provides a complete documentation chain from high-level architecture down to individual wires.
