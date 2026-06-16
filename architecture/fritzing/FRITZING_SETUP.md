FRITZING_SETUP.md

Fritzing Integration for PixStars

Version: 1.0  
Status: Recommended  
Repository: pixstars/architecture/fritzing  

⸻

1. Executive Summary

Fritzing is a visual electronics documentation and prototyping tool that allows hardware systems to be documented using:

* Breadboard diagrams
* Wiring diagrams
* Schematic diagrams
* PCB layouts

For PixStars, Fritzing should be used as the authoritative source for documenting all electronic wiring and physical hardware connections.

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

⸻

3. Why Fritzing Fits PixStars

PixStars combines numerous electronic subsystems:

* Raspberry Pi Zero 2 WH
* USB microphone
* USB audio devices
* LED ring
* Camera
* Speakers
* Amplifiers
* Power distribution
* ESP32 devices
* Sensors
* Smart lighting

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

Performance Layer
│
├── Ardour
├── DigiScore
├── Jess+
│
Automation Layer
│
├── Home Assistant
├── OpenVoiceOS
├── HiveMind
│
Hardware Layer
│
├── Raspberry Pi
├── ESP32
├── LED Ring
├── Camera
├── Audio
│
Documentation Layer
│
└── Fritzing

Fritzing documents the Hardware Layer.

⸻

5. Recommended Repository Structure

pixstars/
│
├── architecture/
│   └── fritzing/
│       ├── FRITZING_SETUP.md
│
├── electronics/
│   ├── fritzing/
│   │
│   ├── lamp-head.fzz
│   ├── lamp-base.fzz
│   ├── audio-system.fzz
│   ├── power-system.fzz
│   ├── led-ring.fzz
│   ├── home-assistant-network.fzz
│   │
│   └── exports/
│       ├── lamp-head.png
│       ├── lamp-base.png
│       ├── audio-system.png
│       ├── power-system.png
│       └── led-ring.png

⸻

6. Required PixStars Diagrams

The following diagrams should be maintained.

Lamp Head

Contains:

* Raspberry Pi Zero 2 WH
* Camera
* USB microphone
* Speaker
* WS2812 LED ring

Document:

* GPIO usage
* USB usage
* Audio routing
* Power routing

Filename:

lamp-head.fzz

⸻

Lamp Base

Contains:

* USB hub
* Amplifier
* Power supplies
* Cable routing

Filename:

lamp-base.fzz

⸻

Audio System

Contains:

* Ardour output
* USB audio adapter
* Amplifier
* Speaker connections

Filename:

audio-system.fzz

⸻

LED Ring

Contains:

* GPIO18
* 330Ω resistor
* WS2812 ring
* Power supply
* Capacitor

Filename:

led-ring.fzz

⸻

Power Distribution

Contains:

* Pi power
* USB peripherals
* Amplifier power
* Future ESP32 devices

Filename:

power-system.fzz

⸻

7. Lamp Head Reference Design

Initial reference wiring

Raspberry Pi Zero 2 WH
GPIO18
   │
   └── 330Ω Resistor
           │
           └── WS2812 DIN
5V
   │
   ├── WS2812 Ring
   └── Camera
USB OTG
   │
   ├── USB Microphone
   └── USB Audio Adapter
Audio Adapter
   │
   └── Speaker Amplifier
           │
           └── Speaker

This design should become the first Fritzing project.

⸻

8. Documentation Standards

Every Fritzing project must include:

Component Names

Example:

Raspberry Pi Zero 2 WH
WS2812 Ring
MAX98357A
USB Audio Adapter
SunFounder USB Microphone

⸻

Wire Colours

Use consistent colours.

Red     = +5V
Black   = Ground
Yellow  = GPIO
Green   = Audio
Blue    = USB

⸻

Labels

All GPIO pins must be labelled.

Example:

GPIO18
GPIO17
GPIO4

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

WIRING.md
LAMP_AUDIO_SETUP.md
HOME_ASSISTANT_SETUP.md
OVOS_SETUP.md
HIVEMIND_SETUP.md

Example:

See:
electronics/fritzing/exports/lamp-head.png

for complete wiring details.

⸻

11. Future Expansion

Future PixStars hardware can be documented using the same approach.

Examples:

* Additional cameras
* ESP32 satellites
* Servo motors
* Laser projector
* Smoke generator
* DMX interfaces
* MIDI interfaces
* Projection hardware

Each subsystem should receive:

Subsystem Name
│
├── .fzz
├── PNG Export
└── SVG Export

⸻

12. Recommendation

Recommendation: Adopt Fritzing as the official electronics documentation platform for PixStars.

Use:

* Markdown for architecture
* Draw.io for system diagrams
* Home Assistant for operational dashboards
* Ardour for show control
* Fritzing for all hardware wiring documentation

This provides a complete documentation chain from high-level architecture down to individual wires.
