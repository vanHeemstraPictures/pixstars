# Pixstars Lamp Complete Build

This document is the canonical combined build guide for the Pixstars lamp system.

See `architecture_decision_records/LAMP_ARCHITECTURE_v3.md` for the v2->v3 migration rationale.

## System Overview — Cave Architecture v3

All servos and electronics are hidden inside a "cave" under a ComXim MTxRUWSLPro
programmable turntable, mounted on a riser block. The lamp itself contains only a
NeoPixel LED ring and a Dynamixel AX-12A for head nod. Cables route through a single
central column. No USB cable connects to the lamp.

Base rotation is handled by the ComXim turntable (WiFi CT commands from Mac Mini),
completely decoupled from the ESP32/Maestro servo chain.

```
                    +--- Lamp Head ---+
                    |  AX-12A (nod)   |
                    |  NeoPixel ring  |
                    |  Webcam (C920)  |
                    +--------+--------+
                             | cables through column
                    +--------+--------+
                    |  ComXim top     |
                    |  plate (rotates)|
                    +--------+--------+
                    |  ComXim internal|
                    |  stepper + drive|
                    |  ComXim base    |
                    +--------+--------+
                    |                 |
                    |  RISER BLOCK    |
                    |  (cave walls)   |
                    |  120-150mm tall |
                    |                 |
                    +-----------------+
                         piano top

    Inside cave (hanging from servo rail under ComXim top plate):
      ESP32 DevKit, Maestro 24-ch, 4x MG996R, 1x MG90S,
      Arduino Nano, MEAN WELL LRS-50-5 PSU
```

### Control Architecture

```
Mac Mini M4 Pro
  +-- WiFi --> ComXim MTxRUWSLPro (base rotation, CT commands)
  |              +-- Internal stepper executes rotation
  |              +-- Confirms completion back to Mac Mini
  +-- WiFi --> ESP32 (on servo rail, rotating with cave)
                 +-- Serial --> Pololu Mini Maestro 24-ch
                 |     +-- PWM --> MG996R x 4 (arm joints)
                 |     +-- PWM --> MG90S x 1 (neck pan rod)
                 |     +-- Serial bridge --> Arduino Nano --> NeoPixel ring
                 +-- TTL serial --> AX-12A #1 (head nod)
```

## Bill of Materials

### Base Rotation Platform

| Component | Qty | Purpose |
|-----------|-----|---------|
| ComXim MTxRUWSLPro | 1 | Programmable turntable (20cm, USB+WiFi, 0.1 deg precision) |
| Riser block (AL tube or 18mm plywood) | 1 | Creates cave depth (120-150mm), ComXim mounts on top |
| Riser-to-piano fixings | 1 set | M6 bolts or clamp system (non-destructive) |
| Inner ring adapter plate | 1 | AL plate, couples inner ring to ComXim top bolt pattern |
| Decorative skirt | 1 | Fabric or formed AL, conceals riser + ComXim base |

### Cave (under turntable, on servo rail)

| Component | Qty | Purpose |
|-----------|-----|---------|
| ESP32 DevKit (ESP32-WROOM-32) | 1 | WiFi bridge to Mac Mini, drives Maestro + AX-12A |
| Pololu Mini Maestro 24-channel | 1 | Servo controller (serial from ESP32) |
| MG996R servo | 4 | Lower arm (Ch1), elbow (Ch2), spare (Ch3-4) |
| MG90S servo | 1 | Neck pan (Ch3), push-pull rod to lamp head |
| Arduino Nano | 1 | NeoPixel serial bridge (Maestro Ch5) |
| MEAN WELL LRS-50-5 | 1 | 5V power supply for servos and logic |
| Servo bracket rail | 1 | Aluminium plate, ~280x100mm |
| Hanger rods (x4) | 4 | M4 threaded, 100mm |
| Carbon fibre push-pull rod | 1 | Neck pan mechanical linkage (3mm CF tube, 400mm) |

### Lamp Head

| Component | Qty | Purpose |
|-----------|-----|---------|
| Dynamixel AX-12A | 1 | Head nod (TTL serial via ESP32, NOT on Maestro) |
| NeoPixel RGBW LED ring | 1 | Lamp "eye" light (via Arduino Nano serial bridge) |
| Logitech C920 webcam | 1 | Gaze / projection source (role TBD) |
| 3D-printed AX-12A shade cradle | 1 | PLA or PETG |
| Steel rod (10mm, 200mm) | 1 | Head nod axle |

### Mechanical Transmission

| Component | Qty | Purpose |
|-----------|-----|---------|
| Capstan wheel (64mm AL or 3D print) | 1 | Neck pan drive |
| Crank pin M4 (4mm, offset 20mm) | 1 | Neck pan crank |
| Flanged guide pulleys (44mm, ball bearing) | 3 | String routing |
| Extension springs (2 N/mm) | 2 | String tension |
| Dyneema string (1.2mm braid) | 1 | Joint transmission |
| TTL half-duplex adapter | 1 | USB-to-TTL for AX-12A |
| Central cable grommet (rubber, 8mm) | 1 | Cable routing through column |

### Base Lamp

| Component | Qty | Purpose |
|-----------|-----|---------|
| Anglepoise Original 1227 (Linen White) | 1 | Physical lamp body |

See `docs/LAMP_SPECIFICATIONS.md` for lamp product details.

### Host

| Component | Qty | Purpose |
|-----------|-----|---------|
| Mac Mini M4 Pro | 1 | Show control host |

### Optional (HiveMind satellite — separate from lamp)

| Component | Qty | Purpose |
|-----------|-----|---------|
| Raspberry Pi Zero 2 WH | 1 | HiveMind satellite client, voice/state monitoring |

## Servo Channel Map (v3)

| Maestro Channel | Joint | Servo | Notes |
|-----------------|-------|-------|-------|
| 0 | (spare) | -- | Freed in v3 (was NEMA 17 in v2) |
| 1 | Lower arm raise/lower | MG996R | Cable routed through column |
| 2 | Upper arm reach (elbow) | MG996R | Cable routed through column |
| 3 | Neck pan (push-pull rod) | MG90S | Carbon fibre rod to lamp head |
| 4 | (spare) | -- | Available |
| 5 | NeoPixel | Arduino Nano bridge | Serial from Maestro |
| TTL | Head nod | AX-12A (ID=1) | TTL serial via ESP32 |
| WiFi CT | Base rotation | ComXim MTxRUWSLPro | Separate device, Mac Mini direct |

## ESP32 Pin Assignments (TBD)

| Pin | Function |
|-----|----------|
| TX1 | Maestro serial TX |
| RX1 | Maestro serial RX |
| TX2 | AX-12A TTL serial |
| GPIO_NEO | NeoPixel data (if driving directly, else via Nano) |

> Note: ESP32 no longer drives a stepper. NEMA 17 step/dir pins are removed in v3.

## ComXim CT Command Reference

> Verify against ComXim SDK documentation before use in performance.

```python
# Precise rotation (stepping mode)
CT+START(direction, 2, 1, degrees, speed, 1);
# direction: 1=CW, 0=CCW | speed: 1-5 | degrees: 0.1 deg resolution

# Return to origin
CT+ORIGIN();

# Continuous rotation (atmospheric spin)
CT+START(direction, 1, 0, 0, speed, 0);

# Stop all rotation
CT+STOP();
```

| Parameter | Value |
|-----------|-------|
| ComXim IP | 192.168.1.YYY (set static) |
| ComXim Port | 8080 (confirm from docs) |
| Protocol | TCP socket, CT command strings |
| Precision | 0.1 deg minimum step |
| Load rating | 20kg (stepping mode) |
| Noise | <55dB |

## Assembly Order

1. Build riser block (AL tube or plywood cylinder, 120-150mm tall)
2. Mount ComXim MTxRUWSLPro on top of riser block
3. Attach inner ring adapter plate to ComXim top plate
4. Build servo bracket rail with hanger rods
5. Mount 4x MG996R and 1x MG90S on servo rail
6. Mount Maestro 24-channel, ESP32, Arduino Nano, PSU on servo rail
7. Attach servo rail under inner ring (hanging into cave)
8. Route string/rod linkages through central column to lamp joints
9. Install AX-12A in lamp head for head nod
10. Install NeoPixel RGBW ring in lamp shade
11. Mount Anglepoise 1227 on inner ring
12. Connect PSU (5V) and ComXim power
13. Flash ESP32 firmware
14. Configure ComXim WiFi (static IP, confirm CT commands)
15. Attach decorative skirt around riser + ComXim base
16. Fix riser to piano top (non-destructive)
17. Calibrate servo ranges and home positions
18. Test ComXim origin return

## Recommended First Milestones

1. Prove ComXim WiFi receives CT commands from Mac Mini (rotation works)
2. Prove ESP32 connects to Mac Mini WiFi and receives OSC
3. Prove Maestro serial control from ESP32 (one servo moves)
4. Prove AX-12A head nod from ESP32
5. Prove NeoPixel LED ring via Arduino Nano bridge
6. Prove all 6 DOF move in coordination
7. Integrate with Show Conductor timeline
8. Add HiveMind satellite (optional, on separate Pi)

## Open Questions (v3)

| Question | Impact |
|----------|--------|
| Does ComXim top plate have accessible bolt holes for inner ring? | Determines adapter plate design |
| Exact height of ComXim unit? | Determines riser block height |
| Does ComXim WiFi receiver rotate with top plate? | Confirms no slip ring needed |
| Exact CT command syntax for MTxRUWSLPro WiFi mode? | Required before Python control code |
| Max load in stepping mode with full cave hanging below? | Must not exceed 20kg |
| Can riser attach to piano non-destructively? | Stage requirement |

See `architecture_decision_records/LAMP_ARCHITECTURE_v3.md` for full design rationale.
