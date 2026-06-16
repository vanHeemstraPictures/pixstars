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
│   ├── Ardour
│   ├── DigiScore
│   └── Jess+
│
├── Automation Layer
│   ├── Home Assistant
│   ├── OpenVoiceOS
│   └── HiveMind
│
├── Hardware Layer
│   ├── Raspberry Pi
│   ├── ESP32
│   ├── Sensors
│   ├── Audio
│   └── Lighting
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

Deliverables:

lamp-head.fzz
lamp-base.fzz
led-ring.fzz
audio-system.fzz
power-system.fzz

Goal:

Validate the architecture before manufacturing.

⸻

Phase 2

Utility Boards

Create small support boards.

Examples:

PIXSTARS_LED_RING_ADAPTER_V1
PIXSTARS_AUDIO_BREAKOUT_V1
PIXSTARS_POWER_DISTRIBUTION_V1

Goal:

Reduce wiring complexity.

⸻

Phase 3

Integrated Boards

Examples:

PIXSTARS_HEAD_CONTROLLER_V1
PIXSTARS_BASE_CONTROLLER_V1

Goal:

Consolidate electronics.

⸻

Phase 4

Production Hardware

Examples:

PIXSTARS_CONTROLLER_V1
PIXSTARS_CONTROLLER_V2

Goal:

Create reusable PixStars hardware platforms.

⸻

6. First Recommended Board

The first board should be:

PIXSTARS_LED_RING_ADAPTER_V1

Purpose:

Provide a clean interface between:

* Raspberry Pi Zero 2 WH
* WS2812 LED Ring

Features:

GPIO18 Input
5V Input
Ground
330Ω Data Resistor
1000µF Capacitor
LED Connector

Benefits:

* Simplifies wiring
* Improves reliability
* Reduces solder joints
* Creates first AISLER manufacturing experience

⸻

7. Power Distribution Board

Second recommended board:

PIXSTARS_POWER_DISTRIBUTION_V1

Purpose:

Centralized power management.

Inputs:

5V Power

Outputs:

Pi Zero
LED Ring
Audio Amplifier
ESP32 Expansion
Future Hardware

Benefits:

* Cleaner internal wiring
* Easier diagnostics
* Better power management

⸻

8. Audio Breakout Board

Third recommended board:

PIXSTARS_AUDIO_BREAKOUT_V1

Purpose:

Audio routing.

Connect:

USB Audio Adapter
Amplifier
Speaker

Benefits:

* Easier replacement
* Easier troubleshooting
* Cleaner installation

⸻

9. Future PixStars Controller

Long-term objective:

PIXSTARS_CONTROLLER_V1

Potential Features:

Pi Zero Integration
LED Ring Connector
Speaker Connector
Camera Connector
Servo Connector
I2C Expansion
UART Expansion
ESP32 Expansion
MIDI Expansion
DMX Expansion

This board would become the hardware kernel of the PixStars lamp.

⸻

10. Repository Structure

Recommended structure:
```
pixstars/
│
├── architecture/
│   ├── fritzing/
│   └── aisler/
│
├── electronics/
│
│   ├── fritzing/
│   │   ├── lamp-head.fzz
│   │   ├── lamp-base.fzz
│   │   ├── led-ring.fzz
│   │   └── power-system.fzz
│
│   ├── pcbs/
│   │
│   ├── led-ring-adapter/
│   │
│   ├── power-distribution/
│   │
│   ├── audio-breakout/
│   │
│   └── pixstars-controller/
│
│   └── manufacturing/
│       └── aisler/
│
└── docs/
```
⸻

11. Revision Management

Every board should be versioned.

Example:

PIXSTARS_LED_RING_ADAPTER_V1
PIXSTARS_LED_RING_ADAPTER_V2
PIXSTARS_POWER_DISTRIBUTION_V1
PIXSTARS_POWER_DISTRIBUTION_V2
PIXSTARS_CONTROLLER_V1
PIXSTARS_CONTROLLER_V2

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

FRITZING_SETUP.md
WIRING.md
LAMP_AUDIO_SETUP.md
HOME_ASSISTANT_SETUP.md
OVOS_SETUP.md
HIVEMIND_SETUP.md

This ensures complete traceability from architecture to manufactured hardware.

⸻

14. Recommendation

Recommendation: Adopt AISLER as the official PCB manufacturing and hardware revision platform for PixStars.

Use:

* Markdown for architecture
* Draw.io for system diagrams
* Fritzing for electronics design
* AISLER for PCB manufacturing
* Home Assistant for operational monitoring
* Ardour for show orchestration

This creates a complete engineering workflow from concept, through design and manufacturing, to live stage performance.
