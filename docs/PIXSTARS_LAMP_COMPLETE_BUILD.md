# Pixstars Lamp Complete Build

This document is the canonical combined build guide for the Pixstars lamp system.

See `architecture_decision_records/LAMP_ARCHITECTURE_v3.md` for the v2->v3 migration rationale.

## System Overview — Cave Architecture v3

All servos and electronics are hidden inside a "cave" under a DIY rotating
platform on a 200mm Lazy Susan bearing, mounted on a riser block. Base
rotation is driven by a NEMA 17 stepper + TMC2209 driver in the cave, with a
GT2 belt friction-coupled to the bearing's outer race (inspired by the
MGX3D open-source turntable). The lamp head contains a WS2812 5050 RGB LED
Ring 16 (rear), a WS2812B 35-LED front ring around the laser galvo aperture,
an RGB Laser Galvo Scanner (vector laser galvo scanner that draws
shapes/patterns via a steered laser beam), an M5Stack Atom Echo wake-word
module, a Raspberry Pi Zero 2 WH (nervous system: audio I/O, sensors, I2C to
RK3588-40), and a Dynamixel AX-12A for head nod. Cables route through a
single central column. No USB cable connects to the lamp.

Base rotation is driven by the cave ESP32 (WiFi/OSC from Mac Mini, STEP/DIR
to TMC2209), unified with the servo/LED/laser control path on the same ESP32.

```
                    +--- Lamp Head ----------+
                    |  AX-12A (nod)          |
                    |  WS2812 rear ring (16) |
                    |  WS2812B front ring 35 |
                    |  Laser Galvo (RGB)     |
                    |  Pi Zero 2 WH          |
                    |  M5Stack Atom Echo     |
                    |  OV2640 cam (on Pi)    |
                    +-----------+------------+
                                | cables through column
                    +--------+--------+
                    |  Rotating top   |
                    |  plate (lamp)   |
                    +--------+--------+
                    |  Lazy Susan     |
                    |  bearing (200mm)|
                    |  GT2 belt around|
                    |  outer race     |
                    +--------+--------+
                    |                 |
                    |  RISER BLOCK    |
                    |  (cave walls)   |
                    |  120-150mm tall |
                    |                 |
                    +-----------------+
                       keyboard surface

    Inside cave (hanging from servo rail under rotating top plate):
      ESP32 DevKit, Maestro 24-ch, 4x MG996R, 1x MG90S,
      NEMA 17 + TMC2209 (base rotation drive),
      Hall sensor (origin detect), bilateral belt tensioner,
      MEAN WELL LRS-50-5 PSU (5V), MEAN WELL LRS-50-12 PSU (12V)
```

### Control Architecture

```
Mac Mini M4 Pro
  +-- WiFi/OSC --> ESP32 (cave)
                 +-- Serial --> Pololu Mini Maestro 24-ch
                 |     +-- PWM --> MG996R x 4 (arm joints)
                 |     +-- PWM --> MG90S x 1 (neck pan rod)
                 +-- TTL serial --> AX-12A #1 (head nod)
                 +-- STEP/DIR --> TMC2209 --> NEMA 17 (base rotation)
                 |     +-- GT2 belt friction-drive --> Lazy Susan bearing
                 |     +-- Hall sensor (origin detect)
                 +-- GPIO/RMT --> WS2812 5050 RGB LED Ring 16
                                  (single-wire data through cable column;
                                   5V from MEAN WELL LRS-50-5 in cave)
```

## Bill of Materials

### Base Rotation Platform (DIY)

| Component | Qty | Purpose |
|-----------|-----|---------|
| NEMA 17 stepper motor (1.8 deg, 200 steps/rev) | 1 | Base rotation drive (in cave) |
| TMC2209 stepper driver | 1 | StealthChop silent drive, 1/16 microstepping; STEP/DIR from ESP32 |
| GT2 timing belt (closed loop or open-ended, 6mm width) | 1 | Friction-drive belt wrapping the lazy susan bearing outer race |
| GT2 20T pulley (5mm bore) | 1 | Mounted on NEMA 17 shaft, drives the GT2 belt |
| Lazy Susan bearing (200mm aluminum swivel plate) | 1 | Rotates the lamp platform; outer race is the belt friction surface |
| Bilateral belt tensioner (idler pulleys or sprung blocks) | 1 set | Maintains friction grip on bearing race (MGX3D-style) |
| Hall effect sensor (SS49E or A3144) + neodymium magnet | 1 set | Origin detect for homing |
| Riser block (AL tube or 18mm plywood) | 1 | Creates cave depth (120-150mm); bearing + drive mount on top |
| Riser-to-keyboard fixings | 1 set | M6 bolts or clamp system (non-destructive) |
| Inner ring adapter plate | 1 | AL plate, couples inner ring to lazy susan bearing top |
| Decorative skirt | 1 | Fabric or formed AL, conceals riser + cave |

Reference design: github.com/MGX3D/Turntable (100kg+ load, zero backlash, proven).

### Cave (under turntable, on servo rail)

| Component | Qty | Purpose |
|-----------|-----|---------|
| ESP32 DevKit (ESP32-WROOM-32) | 1 | WiFi bridge to Mac Mini, drives Maestro + AX-12A |
| Pololu Mini Maestro 24-channel | 1 | Servo controller (serial from ESP32) |
| MG996R servo | 4 | Lower arm (Ch1), elbow (Ch2), spare (Ch3-4) |
| MG90S servo | 1 | Neck pan (Ch3), push-pull rod to lamp head |
| MEAN WELL LRS-50-5 | 1 | 5V power supply for servos and logic |
| +/-24V PSU for galvo motors | 1 | Powers the 40kpps galvo driver board (galvo motor power into the head) |
| ILDAWaveX16 V2 (ESP32-S3 + RP2354, 16-bit ILDA DAC) | 1 | 16-bit ILDA DAC, receives laser cues from Mac Mini via Ether Dream or IDN protocol over WiFi/Ethernet/USB; outputs standard ILDA DB25 (+/-5V X/Y galvo signals, 0-5V RGB laser modulation) |
| 40kpps galvo driver board (Teclulu GH40) | 1 | Drives X/Y galvo motors from +/-5V analog signals on the ILDAWaveX16 V2 DB25 output; powered from the +/-24V cave PSU |
| MEAN WELL LRS-35-12 | 1 | 12V PSU for LPLDD-1A-16V-3CH laser driver, which powers the Opt Lasers 300mW Micro RGB module (DC 12V input; cave-internal, separate from the 5V servo/LED rail) |
| Servo bracket rail | 1 | Aluminium plate, ~280x100mm |
| Hanger rods (x4) | 4 | M4 threaded, 100mm |
| Carbon fibre push-pull rod | 1 | Neck pan mechanical linkage (3mm CF tube, 400mm) |

### Lamp Head

| Component | Qty | Purpose |
|-----------|-----|---------|
| Dynamixel AX-12A | 1 | Head nod (TTL serial via ESP32, NOT on Maestro) |
| WS2812 5050 RGB LED Ring 16 | 1 | Rear "eye" light (GPIO/RMT drive from ESP32 in the cave via cable column; 5V from MEAN WELL PSU) |
| WS2812B 35-LED ring | 1 | Front cone beam halo around laser galvo aperture (separate JST-SM 3-pin from rear ring; 5V from MEAN WELL PSU) |
| RGB laser diode module | 1 | Opt Lasers 300mW Micro RGB (44 x 39 x 27 mm, ~55g, 638/520/450 nm) + 40kpps galvo mirrors (7 x 12 mm), 0-5V analog modulation from ILDAWaveX16 V2 DB25 in the cave via LPLDD-1A-16V-3CH driver, 12V DC power through cable column |
| Galvo motor + mirror pair (X/Y) | 1 set | 2x galvo motors with mirrors (~60-80 g), steer the laser beam to draw vector shapes/patterns; analog +/-5V differential X/Y signals and motor power via cable column |
| Galvo + laser mounting bracket | 1 | ~20 g bracket securing galvo pair, laser diode, and aperture alignment in the lamp head |
| M5Stack Atom Echo | 1 | Wake word capture in lamp head |
| Raspberry Pi Zero 2 WH | 1 | Lamp head nervous system (audio I/O, sensors, I2C to RK3588-40) |
| Microphone | 1 | Head mic input |
| 40mm 4 Ohm 3W speaker | 1 | Head speaker (PAM8403 amp in base) |
| OV2640 camera module | 1 | Camera input on Pi Zero 2 WH (CSI/SPI, ~3g) -- role TBD |
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

### Stage Projection

| Component | Qty | Purpose |
|-----------|-----|---------|
| Epson EB-W05 3LCD projector | 1 | Rear projector (behind screen); theater-scale imagery (Disney castle, GNR logo, AI iterations, signatures); HDMI from Mac Mini, driven by projection/ subsystem (pygame, OSC port 9002) |
| Rear-projection screen | 1 | Translucent stage screen between performer/lamp and audience backdrop; size TBD by venue; receives Epson imagery from behind and lamp laser vector drawings from the front |
| HDMI cable (Mac Mini -> Epson) | 1 | Video link from Mac Mini to Epson EB-W05 |

Staging note: the Epson EB-W05 sits backstage behind the rear-projection screen and lights it from behind; the lamp laser galvo (Opt Lasers 300mW Micro RGB) sits in the lamp head on stage and projects vector drawings onto the front of the same screen. The two systems share one screen from opposite sides.

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
| 0 | (spare) | -- | Available |
| 1 | Lower arm raise/lower | MG996R | Cable routed through column |
| 2 | Upper arm reach (elbow) | MG996R | Cable routed through column |
| 3 | Neck pan (push-pull rod) | MG90S | Carbon fibre rod to lamp head |
| 4 | (spare) | -- | Available |
| 5 | (spare) | -- | LED ring driven from ESP32 GPIO/RMT, not from Maestro |
| TTL | Head nod | AX-12A (ID=1) | TTL serial via ESP32 |
| ESP32 STEP/DIR | Base rotation | NEMA 17 via TMC2209 | DIY turntable in cave, OSC from Mac Mini |

## ESP32 Pin Assignments

| Pin | Function |
|-----|----------|
| TX1 | Maestro serial TX |
| RX1 | Maestro serial RX |
| TX2 | AX-12A TTL serial |
| GPIO (RMT) | WS2812 LED ring data line (single wire via cable column to lamp head; 330 ohm series resistor at the ESP32 end, 1000 uF cap near the ring) |
| GPIO 25 | Base rotation STEP -> TMC2209 |
| GPIO 26 | Base rotation DIR -> TMC2209 |
| GPIO 27 | Hall effect sensor input (origin detect) |
| GPIO 14 | TMC2209 ENABLE (optional; pulls motor out of idle hold) |

Stepper pulse generation uses the FastAccelStepper library (hardware RMT/MCPWM
pulse generation on the ESP32), keeping CPU free for OSC and other I/O.

## OSC Turntable Commands

The Mac Mini drives base rotation by sending OSC messages to the cave ESP32
over WiFi. The ESP32 translates OSC into STEP/DIR pulses for the TMC2209.

| OSC Endpoint | Args | Behaviour |
|--------------|------|-----------|
| `/turntable/rotate` | `float degrees`, `float speed_dps` | Move by `degrees` (signed: + = CW, - = CCW) at `speed_dps` deg/sec. Acknowledged when target reached. |
| `/turntable/origin` | (none) | Home to the Hall-sensor origin magnet, then zero the internal step counter. |
| `/turntable/stop` | (none) | Decelerate to a stop and hold position. |

| Parameter | Value |
|-----------|-------|
| Motor | NEMA 17, 1.8 deg / 200 steps/rev |
| Driver | TMC2209, 1/16 microstepping (StealthChop) |
| Transmission | GT2 belt friction-drive around 200mm lazy susan bearing outer race |
| Ratio | ~15.7:1 (200mm bearing circumference ~628mm / 20T GT2 pulley ~40mm) |
| Resolution | 200 x 16 x 15.7 = ~50,240 microsteps/rev = ~0.00717 deg/microstep |
| Origin detection | Hall effect sensor (SS49E/A3144) + neodymium magnet |
| Protocol | OSC over WiFi (shared cave ESP32) |
| Library (ESP32) | FastAccelStepper (hardware pulse generation) |
| Noise | StealthChop near-silent during slow moves |

Reference design: github.com/MGX3D/Turntable.

## Assembly Order

1. Build riser block (AL tube or plywood cylinder, 120-150mm tall)
2. Mount ComXim MTxRUWSLPro on top of riser block
3. Attach inner ring adapter plate to ComXim top plate
4. Build servo bracket rail with hanger rods
5. Mount 4x MG996R and 1x MG90S on servo rail
6. Mount Maestro 24-channel, ESP32, PSU on servo rail
7. Attach servo rail under inner ring (hanging into cave)
8. Route string/rod linkages through central column to lamp joints
9. Install AX-12A in lamp head for head nod
10. Install WS2812 5050 RGB LED Ring 16 (rear) in lamp shade
11. Mount the RGB Laser Galvo Scanner in the lamp head: secure the
    galvo motor + mirror pair (X/Y) and the Opt Lasers 300mW Micro RGB
    module (44 x 39 x 27 mm) on the
    mounting bracket, aperture facing forward along the lamp's
    eye-line (the "E.T. luminous finger"); confirm the beam exits
    the shade opening cleanly and that the shade physically blocks
    the beam when the head nods above horizontal
15. Install WS2812B 35-LED front ring as a halo around the laser
    galvo aperture (separate JST-SM 3-pin from the rear ring)
16. Mount M5Stack Atom Echo and Pi Zero 2 WH inside the lamp head
    (the Pi handles audio I/O, sensors, and I2C to the RK3588-40 only)
17. Route the laser galvo wiring through the cable column to the
    cave: galvo X/Y analog signals (4 wires, +/-5V differential) to
    the ILDAWaveX16 V2 DB25 RGB lines, laser RGB analog 0-5V
    modulation (3 wires) to the ILDAWaveX16 V2 DB25 RGB lines (Opt
    Lasers 300mW Micro RGB module powered cave-internally by the
    MEAN WELL LRS-35-12 12V PSU via the LPLDD-1A-16V-3CH driver),
    and galvo motor power (2 wires, +/-24V) from the cave galvo PSU
    to the 40kpps galvo driver board
15. Mount Anglepoise 1227 on inner ring
16. Connect PSU (5V) and ComXim power
17. Flash ESP32 firmware
18. Configure ComXim WiFi (static IP, confirm CT commands)
19. Attach decorative skirt around riser + ComXim base
20. Fix riser to keyboard stand (non-destructive)
21. Calibrate servo ranges and home positions
22. Test ComXim origin return

## Recommended First Milestones

1. Prove ESP32 stepper rotation via OSC (`/turntable/rotate` and
   `/turntable/origin` move the platform and home to the Hall magnet)
2. Prove ESP32 connects to Mac Mini WiFi and receives OSC
3. Prove Maestro serial control from ESP32 (one servo moves)
4. Prove AX-12A head nod from ESP32
5. Prove WS2812 5050 RGB LED Ring 16 via ESP32 GPIO/RMT direct drive (data through cable column, 5V from MEAN WELL PSU)
6. Prove all 6 DOF move in coordination
7. Integrate with Show Conductor timeline
8. Add HiveMind satellite (optional, on separate Pi)

## Open Questions (v3)

| Question | Impact |
|----------|--------|
| Belt friction-drive backlash on the bearing outer race under full lamp load? | Determines if a positive-engagement ring gear is needed |
| TMC2209 StealthChop motor noise at performance speeds vs. SpreadCycle audibility? | Stage silence requirement; may dictate driver mode and microstep choice |
| Lazy susan bearing alignment / wobble with cave load hanging below? | Affects laser/camera pointing stability from the lamp head |
| Hall sensor / magnet mounting repeatability (origin drift between shows)? | Determines whether a secondary index or re-home cadence is needed |
| Riser block height vs. cave component stack (NEMA 17 + bracket + tensioner)? | Final riser dimension |
| Can riser attach to keyboard stand non-destructively? | Stage requirement |

See `architecture_decision_records/LAMP_ARCHITECTURE_v3.md` for full design rationale.
