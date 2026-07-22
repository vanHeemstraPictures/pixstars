FRITZING_SETUP.md

Fritzing Integration for PixStars

Version: 3.0
Status: Narrow scope -- PSU verification bench-test only
Repository: pixstars/architecture/fritzing

⸻

1. Executive Summary

PixStars uses custom SVG drawings as the preferred format for hardware visual
documentation. Custom SVG is used wherever the shape and identity of real parts
must be represented truthfully (cave layout, cable column, lamp head, turntable,
laser chain).

Fritzing is retained only for the PSU verification bench-test
(`electronics/fritzing/psu-verification_v1.fzz`). It is not the repo-wide
hardware documentation platform, and its stand-in part shapes are not treated
as accurate representations of the physical build.

Fritzing is not part of the runtime architecture. In its retained bench-test
role it serves as:

* Schematic capture for the isolated PSU verification circuit
* A reproducible test setup that another builder can follow
* A wiring cross-check for the 5V and 12V rails before they are integrated

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

3. Why SVG-first, and where Fritzing still fits

Fritzing part libraries rely on generic, stand-in symbols and breadboard
graphics that do not match the physical shape, footprint, or identity of the
actual PixStars parts (Opt Lasers Micro RGB module, ILDAWaveX16 V2, MEAN WELL
LRS-50 series, 200mm lazy susan bearing, GT2 belt drive, JST-SM connectors,
cable column geometry, and the cave enclosure itself). Presenting those as
"the hardware" in Fritzing breadboard views is misleading and makes assembly
and maintenance harder, not easier.

Custom SVG (drawn in Inkscape or equivalent) is therefore preferred for any
visual that must be true to the real hardware -- cave layout, cable column,
lamp head, turntable, and laser chain. Custom SVG lets us draw parts at their
actual dimensions and orientations, label real connectors, and keep the visual
consistent with build photos.

Fritzing is kept only where its schematic-capture view is genuinely useful and
where stand-in parts are acceptable: the isolated PSU verification bench-test.
That circuit is small, uses generic power-supply and load symbols, and does
not need to depict the real physical layout of the cave.

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
+-- Custom SVG (true-to-hardware visuals -- preferred)
+-- Fritzing (.fzz) -- PSU verification bench-test only
+-- Markdown build guides + wiring/WIRING.md
```
Custom SVG is the primary format for the Hardware Layer visuals. Fritzing is
scoped to the PSU verification bench-test and is not used to represent the
integrated cave.

⸻

5. Repository Structure
```
pixstars/
|
+-- architecture/
|   +-- fritzing/
|       +-- FRITZING_SETUP.md   (this file -- SVG-first policy + Fritzing scope)
|
+-- electronics/
    +-- fritzing/
        +-- README.md
        +-- psu-verification_v1.fzz          (PSU bench-test -- retained)
        +-- ax-12a-bench-test.svg            (SVG bench-test drawing)
        +-- ax12a-buffer-v1-build-guide.md   (build guide, references the SVG)
```
True-to-hardware visuals (cave layout, cable column, lamp head, turntable,
laser chain) are drawn as custom SVG and live alongside the build guide or
architecture doc that references them, not under `electronics/fritzing/`.

⸻

6. Retained Fritzing Scope

Only one Fritzing project is maintained:

PSU Verification Bench-Test

Contains:

* MEAN WELL LRS-50-5 (5V rail) and MEAN WELL LRS-50-12 (12V rail) as
  schematic-symbol sources
* Representative resistive / servo dummy loads on each rail
* Common ground bus tie-point
* Bulk capacitor placement notes (1000uF near WS2812 ring load, 100uF near
  the 12V driver load)
* Probe points and expected voltage / current at each measurement

Purpose:

* Verify the 5V and 12V rails behave correctly under representative load
  before they are wired into the integrated cave
* Provide a schematic another builder can follow to reproduce the bench-test

Filename:

`electronics/fritzing/psu-verification_v1.fzz`

Stand-in part shapes in this file are acceptable because the bench-test is
schematic-oriented and does not attempt to represent the physical cave.

⸻

7. Custom SVG for true-to-hardware visuals

For anything where physical shape, footprint, cable path, or connector
identity matters -- cave layout, cable column routing, lamp head assembly,
turntable mechanics, and the laser chain -- draw a custom SVG (Inkscape or
equivalent) instead of a Fritzing breadboard view.

Guidelines:

* Draw parts at their real proportions where possible; do not substitute
  visually different stand-ins
* Label real connectors and pinouts (JST-SM 3-pin, DB25, TTL headers)
* Keep the wire-colour convention below consistent with Fritzing so the two
  formats remain readable side by side
* Store each SVG next to the build guide or architecture doc that references
  it, using a descriptive filename

Existing example: `electronics/fritzing/ax-12a-bench-test.svg`, referenced
from `ax12a-buffer-v1-build-guide.md`.

⸻

8. Documentation Standards

Applies to the retained Fritzing schematic and to custom SVG drawings:

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
Orange           = +12V (motor / laser driver rail)
Red              = +5V (logic / servo / LED rail)
Black            = Ground (GND)
Green / Yellow   = Data (WS2812 DIN, AX-12A TTL, stepper STEP/DIR)
Yellow           = Servo PWM signal (kept distinct from the Orange +12V rail)
Red (speaker+)   = Audio +
Black (speaker-) = Audio return

Rail rule: on any DC rail wire, `Orange = +12V` and `Red = +5V`. Never
use red for +12V. This matches `wiring/WIRING.md` and
`electronics/fritzing/ax12a-buffer-v1-build-guide.md`.
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

For the retained PSU verification Fritzing project, export a PNG and an SVG
at 3000px wide alongside the `.fzz` file, so the schematic can be viewed
without running Fritzing.

Custom SVG drawings are already in a portable format and do not need a
separate export step; commit the working `.svg` file directly.

Both formats are appropriate for inclusion in build manuals and maintenance
guides.

⸻

10. Integration With Existing Documentation

The PSU verification Fritzing file can be referenced from any build guide or
architecture doc that discusses the 5V / 12V rails, for example
`wiring/WIRING.md`, `HARDWARE_INVENTORY.md`, or PSU-specific build guides.

Custom SVG drawings for the integrated cave, cable column, lamp head,
turntable, and laser chain should be referenced from:

wiring/WIRING.md
architecture_decision_records/LAMP_ARCHITECTURE_v3.md
HARDWARE_INVENTORY.md
docs/architecture/ARCHITECTURE.md
SHOW_CONTROL.md (if present)

Example:

See:
electronics/fritzing/ax-12a-bench-test.svg

as an example of a custom SVG referenced from a Markdown build guide.

⸻

11. Future Expansion

Future PixStars hardware documentation defaults to custom SVG:

* Additional cameras
* Extra ESP32 satellites
* Additional servos beyond the current rail
* Smoke generator
* DMX interfaces
* MIDI interfaces
* Additional projection hardware

Fritzing may be added again only for a new isolated bench-test where
schematic capture with generic parts is genuinely useful (for example, a
future PSU or driver bring-up). It should not be introduced for the
integrated cave.

⸻

12. Recommendation

Recommendation: custom SVG is the preferred format for hardware visual
documentation in PixStars. Fritzing is kept only for the PSU verification
bench-test.

Use:

* Markdown for architecture, build guides, and wiring notes
* Draw.io for system diagrams
* Custom SVG (Inkscape) for true-to-hardware visuals of the integrated build
* Fritzing schematic for the PSU verification bench-test only
* Conductor (timeline.yaml) for show control
* Ardour for audio/MIDI playback

This keeps the documentation chain honest: schematic where a schematic is
appropriate, true-to-hardware SVG where the physical build is what needs to
be understood.
