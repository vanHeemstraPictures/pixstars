# LAMP_ARCHITECTURE_v3.md

## PIXSTARS — Animatronic Lamp: Architecture Migration

**Project:** PIXSTARS theatrical performance
**Performer:** W. van Heemstra / Team Rockstars Cloud B.V., Eersel NL
**Event:** Live team performance, October 2026
**Document purpose:** Migration guide from v2 (custom lazy Susan + NEMA 17 stepper) to v3 (ComXim programmable turntable as rotation engine). Intended for AugmentCode Intent to update dependent documentation, code, and configuration.

> **Previous versions:**
> `LAMP_ARCHITECTURE_v2.md` — v1 → v2 migration (distributed servos → Mechanical Turk cave architecture)
> `LAMP_ARCHITECTURE_v3.md` — v2 → v3 migration (custom stepper → ComXim turntable engine)

---

## 1. Summary of Change (v2 → v3)

In v2, base rotation was achieved by a custom-fabricated lazy Susan bearing ring (inner/outer rings), driven by a NEMA 17 stepper motor bolted to the inner ring, its rubber wheel pressing against the fixed outer ring rim. While mechanically sound, this required custom fabrication of the ring assembly, a stepper driver board, and bespoke firmware on the ESP32 to generate step pulses.

In v3, this entire custom rotation assembly is **replaced by a ComXim MTxRUWSLPro programmable motorized turntable**. The ComXim provides a precision stepper mechanism, silent operation, and a fully open CT command protocol accessible over WiFi — all in a tested, off-the-shelf unit. The ComXim becomes the rotation engine; the lamp's inner ring, servo rail, and all cave electronics are mounted above it.

The Mechanical Turk cave philosophy, all joint mechanisms, and all string/rod transmission paths remain unchanged from v2.

---

## 2. Base Rotation Platform Change (v2 → v3)

### v2 — Custom lazy Susan + NEMA 17

| Element | v2 |
|---|---|
| Bearing | Custom steel lazy Susan ring, Ø300–370mm |
| Outer ring | Fabricated, fixed to piano top |
| Inner ring | Fabricated, carries lamp + cave |
| Drive motor | NEMA 17 stepper, bolted to inner ring |
| Drive method | Rubber wheel on motor shaft pressing inner face of outer ring |
| Stepper driver | A4988 or TMC2209 on servo rail |
| Control | ESP32 generates step pulses to driver |
| Precision | Dependent on fabrication quality and belt/wheel slip |
| Noise | Variable — TMC2209 helps but not guaranteed |

### v3 — ComXim MTxRUWSLPro as rotation engine

| Element | v3 |
|---|---|
| Unit | ComXim MTxRUWSLPro programmable motorized turntable |
| Bearing | Internal — engineered flat thrust bearing |
| Drive motor | Internal precision stepper (brushless, high reduction) |
| Drive method | Internal — worm gear or toothed reduction, sealed |
| Stepper driver | Internal — no external driver board needed |
| Control | CT command protocol over WiFi — direct from Mac Mini |
| Precision | 0.1° minimum step angle (stepping mode) |
| Noise | Silent — engineered for <55dB operation |
| Load rating | 20kg in stepping/positioning mode |
| Origin memory | Yes — hardware origin position, returns on command |
| Position feedback | Yes — turntable confirms completion of commanded rotation |

**Key principle (unchanged from v2):** Everything above the ComXim's rotating top plate — the inner ring, servo rail, all cave electronics, lamp column — rotates as one rigid body. The ComXim's fixed base is bolted to the piano (via riser block). No slip ring is needed. The ComXim's WiFi receiver is internal and rotates with its top plate; it receives CT commands directly from the Mac Mini.

---

## 3. Riser Block — Cave Space

In v2, the cave space (approximately 120mm deep) was the gap between the inner ring underside and the piano top surface, created naturally by the ring bearing height.

In v3, the ComXim unit sits at piano level. Its top plate is approximately at piano surface height. To create the required cave depth for the hanging servo rail below the inner ring, a **riser block** is introduced.

```
        lamp column
             │
    ═════════╪═════════   ← inner ring (bolted to ComXim top plate)
    ░░░ servo rail ░░░░   ← MG996R × 4, MG90S × 1, Maestro, ESP32, PSU, Nano
    ─────────────────────
    │  ComXim top plate  │  ← inner ring bolts here
    │  ComXim internals  │  ← stepper, precision drive, WiFi receiver
    │  ComXim base       │  ← bolts to top of riser block
    ─────────────────────
    │                   │
    │   RISER BLOCK     │  ← 120–150mm tall cylinder, AL or plywood
    │   (cave walls)    │  ← hides servo rail inside
    │                   │
    ─────────────────────
          piano top
```

### Riser block specification

| Property | Value |
|---|---|
| Height | 120–150mm (sufficient for servo rail + clearance) |
| Outer diameter | Match ComXim base footprint |
| Material | Aluminium tube section or 18mm plywood cylinder |
| Finish | Black or white to match piano/stage aesthetic |
| Fixed to | Piano top surface (non-destructively via clamp or bolt-through) |
| ComXim mounts to | Top face of riser block |
| Exterior appearance | Decorative skirt covers riser + ComXim base — invisible to audience |

---

## 4. Cave Electronics (v3 — unchanged from v2 except stepper removal)

### Cave inventory

| Component | v2 location | v3 location | Change |
|---|---|---|---|
| 4× MG996R servo | Cave servo rail | Cave servo rail | Unchanged |
| 1× MG90S servo | Cave servo rail | Cave servo rail | Unchanged |
| ~~NEMA 17 stepper~~ | ~~Cave servo rail~~ | **Removed** | Replaced by ComXim internal stepper |
| ~~Stepper driver (A4988/TMC2209)~~ | ~~Cave servo rail~~ | **Removed** | Internal to ComXim |
| Pololu Mini Maestro 24-ch | Cave servo rail | Cave servo rail | Unchanged |
| MEAN WELL LRS-50-5 PSU | Cave servo rail | Cave servo rail | Unchanged |
| Arduino Nano (NeoPixel) | Cave servo rail | Cave servo rail | Unchanged |
| ESP32 (WiFi bridge) | Cave servo rail | Cave servo rail | Unchanged — still handles servo commands |

**Net result:** Two components removed from the cave (NEMA 17 + driver board), creating additional space and reducing heat load.

---

## 5. Control Stack Changes (v2 → v3)

### v2 control chain

```
Mac Mini M4 Pro
  └── WiFi (802.11)
        └── ESP32 (on inner ring, rotating)
              └── Serial → Pololu Mini Maestro 24-ch
                    └── PWM → MG996R × 4 (arm joints)
                    └── PWM → MG90S × 1 (neck pan rod)
                    └── PWM → NEMA 17 stepper driver (base rotation)
                    └── Serial bridge → Arduino Nano → NeoPixel ring
              └── TTL serial → AX-12A #1 (head nod)
```

### v3 control chain

```
Mac Mini M4 Pro
  ├── WiFi → ComXim MTxRUWSLPro (base rotation, CT commands)
  │             └── Internal stepper executes rotation
  │             └── Confirms completion back to Mac Mini
  └── WiFi → ESP32 (on inner ring, rotating)
               └── Serial → Pololu Mini Maestro 24-ch
                     └── PWM → MG996R × 4 (arm joints)
                     └── PWM → MG90S × 1 (neck pan rod)
                     └── Serial bridge → Arduino Nano → NeoPixel ring
               └── TTL serial → AX-12A #1 (head nod)
```

**Removed from v2:** ESP32 generating step pulses to NEMA 17 driver.
**Added in v3:** Direct WiFi CT command channel from Mac Mini to ComXim.
**Result:** Base rotation is now a first-class, independently addressable device with its own WiFi connection — decoupled from the ESP32/Maestro chain entirely.

---

## 6. Servo Channel Map (v3)

The NEMA 17 stepper has been removed from Maestro channel 0. That channel is now spare.

| Maestro Channel | Joint | Servo | v2 Channel | Change |
|---|---|---|---|---|
| 0 | (spare) | — | Base rotation (NEMA 17) | **Freed — stepper removed** |
| 1 | Lower arm raise/lower | MG996R | 1 | Unchanged |
| 2 | Upper arm reach (elbow) | MG996R | 2 | Unchanged |
| 3 | Neck pan (push-pull rod) | MG90S | 3 | Unchanged |
| 4 | (spare) | — | 4 | Unchanged |
| 5 | NeoPixel (via Nano serial) | Arduino Nano bridge | 5 | Unchanged |
| — | Head nod | AX-12A TTL ID=1 | — | Unchanged |
| — | Base rotation | ComXim (WiFi CT) | — | **New — separate device** |

---

## 7. Python Code Migration Notes (v2 → v3)

### 7.1 Remove — NEMA 17 stepper control via ESP32

```python
# REMOVE — v2 base rotation via stepper driver on Maestro channel 0
send_command(0, steps)   # no longer valid — channel 0 is freed
```

### 7.2 Remove — stepper step pulse logic

Any code that calculated step counts, acceleration ramps, or TMC2209
microstepping configuration should be removed. The ComXim handles
all of this internally.

### 7.3 Add — ComXim CT command dispatch

```python
# ADD — v3 base rotation via ComXim CT command protocol over WiFi
import socket

COMXIM_IP   = '192.168.1.YYY'   # set static IP on ComXim
COMXIM_PORT = 8080               # confirm port from ComXim docs

def rotate_base(degrees, direction='CW', speed=3):
    """
    Rotate the lamp base by a precise angle.
    direction: 'CW' (clockwise) or 'CCW' (counter-clockwise)
    speed: 1 (slow) to 5 (fast) — ComXim internal scale
    degrees: 0.1° resolution in stepping mode
    """
    dir_code = 1 if direction == 'CW' else 0
    cmd = f'CT+START({dir_code},2,1,{degrees},{speed},1);\n'.encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((COMXIM_IP, COMXIM_PORT))
        s.sendall(cmd)

def rotate_base_to_origin():
    """Return to hardware origin position via shortest path."""
    cmd = b'CT+ORIGIN();\n'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((COMXIM_IP, COMXIM_PORT))
        s.sendall(cmd)

def rotate_base_continuous(direction='CW', speed=2):
    """Continuous rotation — use for slow atmospheric spin."""
    dir_code = 1 if direction == 'CW' else 0
    cmd = f'CT+START({dir_code},1,0,0,{speed},0);\n'.encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((COMXIM_IP, COMXIM_PORT))
        s.sendall(cmd)

def stop_base():
    """Stop all rotation immediately."""
    cmd = b'CT+STOP();\n'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((COMXIM_IP, COMXIM_PORT))
        s.sendall(cmd)
```

> **Note:** CT command syntax should be verified against the ComXim
> SDK documentation supplied with the MTxRUWSLPro unit. The commands
> above follow the published CT protocol pattern but exact parameter
> ordering must be confirmed before use in performance.

### 7.4 Unchanged — all other control functions

All v2 Python functions for arm joints, neck pan, head nod, and
NeoPixel remain valid and require no changes in v3.

---

## 8. Hardware Procurement Delta (v2 → v3)

### Remove from BOM

| Item | Reason |
|---|---|
| Lazy Susan bearing ring (Ø300–370mm) | Replaced by ComXim internal bearing |
| NEMA 17 stepper motor | Replaced by ComXim internal stepper |
| Stepper driver board (A4988 or TMC2209) | Replaced by ComXim internal driver |
| Rubber drive wheel | No longer needed |

### Add to BOM

| Item | Specification | Purpose |
|---|---|---|
| ComXim MTxRUWSLPro | 20cm platform, USB+WiFi model | Precision rotation engine |
| Riser block | AL tube or 18mm ply, 120–150mm tall | Creates cave depth below ComXim |
| Riser-to-piano fixings | M6 bolts or clamp system | Non-destructive piano attachment |
| Inner ring adapter plate | AL plate, matches ComXim top bolt pattern | Couples inner ring to ComXim top plate |
| Decorative skirt | Fabric or formed AL, black/white | Conceals riser + ComXim base from audience |

### Unchanged in BOM (carried from v2)

| Item | Specification |
|---|---|
| Servo bracket rail | Aluminium plate, ~280×100mm |
| Hanger rods (×4) | M4 threaded, 100mm |
| ESP32 dev board | ESP32-WROOM-32 |
| Dynamixel AX-12A | ROBOTIS, TTL version |
| TTL half-duplex adapter | USB-to-TTL, direction pin |
| Ø10mm steel rod, 200mm | Head nod axle |
| Ø3mm carbon fibre tube, 400mm | Neck pan push-pull rod |
| Capstan wheel, Ø64mm | AL or 3D print |
| Crank pin M4, Ø4mm | Steel, offset 20mm |
| Flanged guide pulleys (×3) | Ø44mm, ball bearing |
| Extension springs (×2) | 2 N/mm |
| Dyneema string | Ø1.2mm braid |
| 3D-printed AX-12A shade cradle | PLA or PETG |
| Central cable grommet | Rubber, Ø8mm |
| 4× MG996R servo | Metal gear |
| 1× MG90S servo | Metal gear |
| Pololu Mini Maestro 24-ch | USB servo controller |
| MEAN WELL LRS-50-5 PSU | 5V / 10A |
| Arduino Nano | NeoPixel bridge |
| NeoPixel RGBW ring | Inside shade |

---

## 9. Files to Update

| File | Change required |
|---|---|
| `CLAUDE.md` | Update hardware stack — remove NEMA 17/driver, add ComXim + riser |
| `src/servo_control.py` | Remove stepper logic, add ComXim CT command functions |
| `src/maestro_config.uscp` | Free channel 0 (was NEMA 17), document as spare |
| `config/network.py` (or equivalent) | Add COMXIM_IP and COMXIM_PORT constants |
| `docs/hardware.md` | BOM delta per section 8 |
| `docs/wiring.md` | Remove stepper wiring, add ComXim WiFi network diagram |
| `README.md` | Update architecture overview — ComXim as rotation engine |

---

## 10. What Has NOT Changed (v2 → v3)

The following are identical between v2 and v3:

- Mechanical Turk cave philosophy — all actuation hidden below lamp
- All joint mechanisms — lower arm, elbow, neck pan, head nod
- String routing — Dyneema through lamp column and arms
- Carbon fibre push-pull rod — neck pan mechanism
- AX-12A through-axle head nod — inverted servo principle
- Capstan/crank neck pan — push = left, pull = right
- ESP32 WiFi bridge for servo commands
- Pololu Mini Maestro 24-ch as PWM servo hub
- MEAN WELL LRS-50-5 power supply
- Arduino Nano / NeoPixel ring
- TTL daisy-chain to AX-12A
- Mac Mini M4 Pro as show control host
- Ardour + Pianoteq 9 + MODO DRUM audio stack
- Logitech C920 webcam
- Ten-act screenplay structure and lamp movement vocabulary
- Performance date: October 2026

---

## 11. Open Questions for Build Phase

The following should be resolved before fabrication begins:

| Question | Impact |
|---|---|
| Does ComXim top plate have accessible bolt holes for inner ring attachment? | Determines inner ring adapter plate design |
| What is the exact height of the ComXim unit? | Determines riser block height |
| Does ComXim WiFi receiver rotate with top plate or stay fixed to base? | Confirms no slip ring needed for ComXim control |
| What is the exact CT command syntax for the MTxRUWSLPro WiFi mode? | Required before writing Python control code |
| What is the ComXim's maximum load in stepping mode with the full cave hanging below? | Must not exceed 20kg rated limit |
| Can the riser block attach to the piano non-destructively? | Stage requirement — no permanent piano modification |

---

*Document generated from design session, April 2026.*
*Supersedes: LAMP_ARCHITECTURE_v2.md*
*Drawings reference: PX-001-A (base turntable), PX-002-A (elbow joint), PX-003-A (head joint), PX-004-A (neck push-pull).*
*ComXim product: MTxRUWSLPro — comxim.com*
