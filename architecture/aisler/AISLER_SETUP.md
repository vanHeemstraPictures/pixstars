AISLER_SETUP.md

AISLER Integration for PixStars

Version: 1.0  
Status: Recommended  
Repository: pixstars/architecture/aisler  

⸻

1. Executive Summary

AISLER is a PCB manufacturing and electronics collaboration platform that integrates directly with Fritzing and other PCB design tools.

For PixStars, AISLER serves as the official manufacturing and hardware revision management platform.

AISLER is not part of the runtime architecture.

Instead, AISLER is used to:

* Manufacture custom PCBs
* Track hardware revisions
* Share PCB designs
* Order prototypes
* Produce installation-ready hardware
* Support long-term maintainability of the PixStars platform

Together, Fritzing and AISLER provide a complete workflow from concept to manufactured hardware.

⸻

2. References

AISLER

Website

https://aisler.net

Documentation

https://community.aisler.net

GitHub

https://github.com/aislerhq

⸻

Fritzing

Website

https://fritzing.org

Documentation

https://docs.fritzing.org

GitHub

https://github.com/fritzing/fritzing-app

⸻

3. Architectural Role

PixStars Architecture
```
PixStars
│
├── Performance Layer
│   ├── Ardour (audio / MIDI playback)
│   ├── Pianoteq 9 + MODO DRUM (VST instruments)
│   └── conductor/ (timeline.yaml, OSC cue dispatcher)
│
├── Show Control Layer (Mac Mini M4 Pro)
│   ├── projection/ (pygame, Epson EB-W05 rear projector)
│   ├── OSC to ESP32 cave (servos, LED ring, turntable)
│   └── OSC to ILDAWaveX16 V2 (laser galvo)
│
├── Hardware Layer
│   ├── ESP32-S3 N16R8 DevKit (cave controller)
│   ├── Pololu Mini Maestro 24-channel (servos)
│   ├── TMC2209 + NEMA 17 (DIY turntable)
│   ├── Dynamixel AX-12A (head nod, TTL serial)
│   ├── WS2812 LED ring (driven from cave via RMT GPIO)
│   ├── ILDAWaveX16 V2 + 40kpps galvo + Opt Lasers RGB
│   └── Raspberry Pi Zero 2 WH (lamp head: audio, sensors, camera)
│
├── Design Layer
│   └── Fritzing
│
└── Manufacturing Layer
    └── AISLER
```
AISLER is responsible for transforming hardware designs into physical hardware.

⸻

4. PixStars Hardware Philosophy

PixStars follows a modular hardware architecture.

Instead of one large custom board, PixStars is composed of independent modules.

Benefits:

* Easier maintenance
* Easier upgrades
* Faster prototyping
* Lower manufacturing costs
* Reduced technical risk

Each subsystem should be capable of evolving independently.

⸻

5. Recommended PCB Roadmap

The following PCB roadmap is recommended.

⸻

Phase 1

Documentation Only

Tools:

* Fritzing
* Markdown
* Draw.io

Deliverables (one .fzz per cave subsystem):

cave-controller.fzz
power-distribution.fzz
lamp-head.fzz
turntable.fzz
laser-chain.fzz

Goal:

Validate the cave architecture (CLAUDE.md, wiring/WIRING.md) before
manufacturing any PCB. Diagrams are the source of truth for the
hand-wired prototype.

⸻

Phase 2

Utility Boards

Small support PCBs that replace the most error-prone Dupont/breadboard
wiring in the cave.

Examples:

PIXSTARS_AX12A_BUFFER_V1
    74HCT245 level shifter + half-duplex voltage divider for the
    Dynamixel AX-12A TTL serial link from the ESP32-S3.

PIXSTARS_POWER_DISTRIBUTION_V1
    Three-rail cave power distribution board:
      - 5V  (MEAN WELL LRS-50-5)  -> servos, WS2812 LED ring
      - 12V (MEAN WELL LRS-50-12) -> LPLDD laser driver, TMC2209 VMOT
      - +/-24V (galvo scanner PSU) -> 40kpps galvo driver
    Common ground star point, fused per rail.

PIXSTARS_LED_RING_ADAPTER_V1
    Carrier for the WS2812 5050 RGB LED Ring 16 cable column tail:
    330 ohm series resistor on the ESP32 GPIO data line, 1000 uF
    bulk capacitor across the 5V rail, JST-SM 3-pin header.

Goal:

Reduce hand-wiring in the cave and on the lamp-head tail without
committing to a fully integrated board.

⸻

Phase 3

Integrated Cave Controller

Example:

PIXSTARS_CAVE_CONTROLLER_V1
    Single PCB combining:
      - ESP32-S3 N16R8 DevKit footprint
      - Pololu Mini Maestro 24-channel header (serial from ESP32)
      - TMC2209 stepper driver socket (STEP/DIR/EN, Hall sensor input)
      - 74HCT245 AX-12A buffer (rolls in the Phase 2 buffer board)
      - WS2812 LED ring driver output (RMT GPIO + resistor + cap)
      - Connectors for the three cave power rails

Goal:

Consolidate the cave electronics onto one serviceable board.
The lamp head and turntable subsystems still connect via cable
column and motor harness respectively.

⸻

Phase 4

Production Hardware

Examples:

PIXSTARS_CAVE_CONTROLLER_V2
    Production revision of the cave controller (silkscreen, mounting
    holes for the cave rail, test points).

PIXSTARS_LAMP_HEAD_V1
    Optional integrated head board: cable column terminator, LED
    ring carrier, galvo + laser connector breakout.

Goal:

Create reusable, reproducible PixStars hardware revisions for
long-term maintenance after the October 2026 show.

⸻

6. First Recommended Board

The first board should be:

PIXSTARS_AX12A_BUFFER_V1

Purpose:

Provide a reliable half-duplex level-shifted interface between the
ESP32-S3 cave controller (3.3V UART) and the Dynamixel AX-12A
(5V TTL half-duplex) head-nod servo. This is the most fragile
breadboard link in the current cave wiring and the easiest to retire
with a small PCB.

Features:

74HCT245 octal bus transceiver (3.3V to 5V level shifter)
Direction-control logic for half-duplex AX-12A protocol
Voltage divider on the AX-12A return line
3-pin TTL header to AX-12A
ESP32 UART header (TX, RX, DIR, GND)
5V from cave MEAN WELL LRS-50-5
Common ground star tie

Benefits:

* Eliminates the most error-prone breadboard wiring in the cave
* Protects the ESP32 UART input from 5V swings
* Creates first AISLER manufacturing experience
* Drops directly into the Phase 3 cave controller as a sub-circuit

⸻

7. Power Distribution Board

Second recommended board:

PIXSTARS_POWER_DISTRIBUTION_V1

Purpose:

Centralised cave power distribution across three independent rails,
with a common ground star and per-rail fusing.

Inputs:

5V    from MEAN WELL LRS-50-5
12V   from MEAN WELL LRS-50-12
+/-24V from the galvo scanner dual-rail PSU (included in the
       40kpps galvo scanner set)

Outputs:

5V rail
  - Pololu Mini Maestro logic and servo rail (MG996R, MG90S)
  - WS2812 LED ring (via cable column to lamp head)
  - ESP32-S3 DevKit VIN (optional, or USB-powered)

12V rail
  - LPLDD-1A-16V-3CH laser driver (Opt Lasers 300mW Micro RGB)
  - TMC2209 VMOT for the NEMA 17 turntable stepper

+/-24V rail
  - 40kpps galvo driver board (Teclulu GH40 or equivalent)

Ground:
  - Single star ground point common to all three rails, ESP32
    logic ground, Maestro ground, TMC2209 ground, and the
    ILDAWaveX16 V2 ground.

Benefits:

* Cleaner internal wiring across three rails
* Per-rail fusing and indicator LEDs simplify diagnostics
* Removes ground-loop risk between laser, stepper and servo power

⸻

8. LED Ring Adapter Board

Third recommended board:

PIXSTARS_LED_RING_ADAPTER_V1

Purpose:

Carrier for the cable column tail that feeds the WS2812 5050 RGB
LED Ring 16 in the lamp head from the ESP32-S3 in the cave.

Features:

ESP32 GPIO data input (RMT peripheral)
330 ohm series resistor on the data line at the cave end
1000 uF electrolytic capacitor across the 5V rail
JST-SM 3-pin output header (5V / DATA / GND) to the cable column
5V input from the cave MEAN WELL LRS-50-5

Benefits:

* Standardises the WS2812 cable column termination
* Replaces the breadboard resistor / capacitor with a soldered board
* Easier to swap the ring without disturbing cave wiring

⸻

9. Future PixStars Cave Controller

Long-term objective:

PIXSTARS_CAVE_CONTROLLER_V1

Potential Features:

ESP32-S3 N16R8 DevKit footprint (WiFi to Mac Mini)
Pololu Mini Maestro 24-channel header (serial from ESP32)
TMC2209 stepper driver socket (STEP / DIR / EN, Hall sensor input)
74HCT245 AX-12A buffer (rolled in from Phase 2)
WS2812 LED ring driver output (RMT GPIO + resistor + cap)
Three-rail power input connectors (5V / 12V / +/-24V)
Test points on every signal line

This board becomes the hardware kernel of the PixStars cave.
The lamp head and the laser chain (ILDAWaveX16 V2, 40kpps galvo
driver, LPLDD laser driver) remain on their own boards and connect
via the cable column and the cave 12V / +/-24V rails.

⸻

10. Repository Structure

Recommended structure (matches the current electronics/ scaffold):
```
pixstars/
│
├── architecture/
│   ├── fritzing/
│   │   └── FRITZING_SETUP.md
│   └── aisler/
│       └── AISLER_SETUP.md
│
├── electronics/
│   │
│   ├── fritzing/
│   │   ├── cave-controller.fzz
│   │   ├── power-distribution.fzz
│   │   ├── lamp-head.fzz
│   │   ├── turntable.fzz
│   │   └── laser-chain.fzz
│   │
│   ├── pcbs/
│   │   ├── led-adapter/
│   │   ├── power-board/
│   │   ├── audio-board/
│   │   └── pixstars-controller/
│   │
│   ├── exports/
│   │
│   └── manufacturing/
│       └── aisler/
│
└── docs/
```
⸻

11. Revision Management

Every board should be versioned.

Example:

PIXSTARS_AX12A_BUFFER_V1
PIXSTARS_AX12A_BUFFER_V2
PIXSTARS_POWER_DISTRIBUTION_V1
PIXSTARS_POWER_DISTRIBUTION_V2
PIXSTARS_LED_RING_ADAPTER_V1
PIXSTARS_CAVE_CONTROLLER_V1
PIXSTARS_CAVE_CONTROLLER_V2

Never overwrite earlier hardware revisions.

Manufactured boards should remain reproducible.

⸻

12. Manufacturing Workflow

Recommended workflow:
```
Architecture
    ↓
Fritzing Design
    ↓
Review
    ↓
Prototype
    ↓
AISLER Order
    ↓
Assembly
    ↓
Testing
    ↓
Documentation
    ↓
Production Revision
```
Every hardware change should follow this process.

⸻

13. Integration with Existing Documentation

AISLER documentation should be referenced from:

architecture/fritzing/FRITZING_SETUP.md
wiring/WIRING.md
architecture_decision_records/LAMP_ARCHITECTURE_v3.md
CLAUDE.md (hardware stack section)

This ensures complete traceability from architecture to manufactured hardware.

⸻

14. Recommendation

Recommendation: Adopt AISLER as the official PCB manufacturing and hardware revision platform for PixStars.

Use:

* Markdown for architecture
* Draw.io for system diagrams
* Fritzing for electronics design
* AISLER for PCB manufacturing
* Ardour + conductor/ for show orchestration

This creates a complete engineering workflow from concept, through design and manufacturing, to live stage performance.
