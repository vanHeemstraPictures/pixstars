# Pixstars Lamp Complete Build

This document is the canonical combined build guide for the Pixstars lamp system.

See `architecture_decision_records/LAMP_ARCHITECTURE_v2.md` for the design rationale.

## System Overview — Cave Architecture v2

All servos and electronics are hidden inside a "cave" under a Lazy Susan turntable.The lamp itself contains only a NeoPixel LED ring and a Dynamixel AX-12A for head nod.Cables route through a single central column. No USB cable connects to the lamp.

```
                    ┌─── Lamp Head ───┐
                    │  AX-12A (nod)   │
                    │  NeoPixel ring  │
                    │  Webcam (C920)  │
                    └────────┬────────┘
                             │ cables through column
                    ┌────────┴────────┐
                    │  Lazy Susan     │
                    │  turntable      │
                    └────────┬────────┘
                    ┌────────┴────────┐
                    │     CAVE        │
                    │  ESP32 DevKit   │
                    │  Maestro 18-ch  │
                    │  4x MG996R      │
                    │  1x MG90S       │
                    │  NEMA 17 + A4988│
                    │  PSU (5V + 12V) │
                    └─────────────────┘
                             │ WiFi
                    ┌────────┴────────┐
                    │  Mac Mini M4 Pro│
                    └─────────────────┘
```

## Bill of Materials

### Cave (under turntable)

| Component | Qty | Purpose |
| --- | --- | --- |
| ESP32 DevKit | 1 | WiFi bridge to Mac Mini, drives Maestro + AX-12A + NeoPixel |
| Pololu Mini Maestro 18-channel | 1 | Servo controller (serial from ESP32) |
| MG996R servo | 4 | Shoulder (Ch0), elbow (Ch1), forearm twist (Ch2), spare (Ch3) |
| MG90S servo | 1 | Neck pan (Ch4), push-pull rod to lamp head |
| NEMA 17 stepper motor | 1 | 360-degree base rotation |
| A4988 stepper driver | 1 | Drives NEMA 17 from ESP32 |
| Lazy Susan turntable bearing | 1 | Mechanical decoupling for base rotation |
| MEAN WELL LRS-50-5 | 1 | 5V power supply for servos and logic |
| 12V DC power supply | 1 | Power for NEMA 17 stepper |
| Carbon fibre push-pull rod | 1 | Neck pan mechanical linkage |

### Lamp Head

| Component | Qty | Purpose |
| --- | --- | --- |
| Dynamixel AX-12A | 1 | Head nod (TTL serial via ESP32, NOT on Maestro) |
| NeoPixel RGBW LED ring | 1 | Lamp "eye" light (driven by ESP32 directly) |
| Logitech C920 webcam | 1 | Gaze / projection source (role TBD) |

### Base Lamp

| Component | Qty | Purpose |
| --- | --- | --- |
| Anglepoise Original 1227 (Linen White) | 1 | Physical lamp body |

See `docs/LAMP_SPECIFICATIONS.md` for lamp product details.

### Host

| Component | Qty | Purpose |
| --- | --- | --- |
| Mac Mini M4 Pro | 1 | Show control host |

### Optional (HiveMind satellite — separate from lamp)

| Component | Qty | Purpose |
| --- | --- | --- |
| Raspberry Pi Zero 2 WH | 1 | HiveMind satellite client, voice/state monitoring |

## Servo Channel Map

| Channel | Servo | Motion | Location |
| --- | --- | --- | --- |
| Ch0 | MG996R | Shoulder | Cave |
| Ch1 | MG996R | Elbow | Cave |
| Ch2 | MG996R | Forearm twist | Cave |
| Ch3 | MG996R | Spare | Cave |
| Ch4 | MG90S | Neck pan (push-pull rod) | Cave |
| TTL | AX-12A | Head nod | Lamp head |
| Step/Dir | NEMA 17 | Base rotation (360-degree) | Cave |

## ESP32 Pin Assignments (TBD)

| Pin | Function |
| --- | --- |
| TX1 | Maestro serial TX |
| RX1 | Maestro serial RX |
| TX2 | AX-12A TTL serial |
| GPIO_STEP | NEMA 17 step (via A4988) |
| GPIO_DIR | NEMA 17 direction (via A4988) |
| GPIO_NEO | NeoPixel data out |

## Mac Mini (show control host)

- `hivemind-core`
- `hivemind-audio-binary-protocol`
- OVOS-side STT / TTS / wake word / synthetic voice
- Ardour 9 for deterministic cue playback
- Show Conductor (Python + OSC) — communicates with ESP32 via WiFi

## Wake Word

Target wake word: **Hey A.I.**

Using `hey_mycroft.tflite` until custom model is trained.See `mac/config/server.json.example`.

## LED State Language

| State | Meaning | Color | Motion |
| --- | --- | --- | --- |
| idle | resting but alive | warm amber | slow breathing |
| listening | hearing user input | blue | gentle pulse |
| thinking | processing | purple | tighter pulse |
| speaking | playing reply audio | warm orange/yellow | follows speech level |
| error | service problem | red | warning pulse |

## Assembly Order

1. Build the cave enclosure (box or 3D-printed housing)
2. Mount Lazy Susan bearing on top of cave
3. Install NEMA 17 + A4988 for base rotation
4. Mount Maestro 18-channel inside cave
5. Install 4x MG996R and 1x MG90S on mechanical linkages
6. Mount ESP32 DevKit inside cave
7. Wire all servos to Maestro, stepper to A4988, AX-12A TTL to ESP32
8. Route cables through central column to lamp head
9. Install AX-12A in lamp head for head nod
10. Install NeoPixel RGBW ring in lamp shade
11. Mount Anglepoise 1227 on Lazy Susan turntable
12. Connect PSUs (5V + 12V)
13. Flash ESP32 firmware
14. Test WiFi connectivity from Mac Mini
15. Calibrate servo ranges and home positions

## Recommended First Milestones

1. Prove ESP32 connects to Mac Mini WiFi and receives OSC
2. Prove Maestro serial control from ESP32 (one servo moves)
3. Prove AX-12A head nod from ESP32
4. Prove NEMA 17 base rotation
5. Prove NeoPixel LED ring from ESP32
6. Prove all 6 DOF move in coordination
7. Integrate with Show Conductor timeline
8. Add HiveMind satellite (optional, on separate Pi)

See `architecture_decision_records/LAMP_ARCHITECTURE_v2.md` for full design rationale.