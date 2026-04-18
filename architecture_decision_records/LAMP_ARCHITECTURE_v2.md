# LAMP_ARCHITECTURE_v2.md

## PIXSTARS — Animatronic Lamp: Architecture Migration

**Project:** PIXSTARS theatrical performance
**Performer:** W. van Heemstra / Team Rockstars Cloud B.V., Eersel NL
**Event:** Live team performance, October 2026
**Document purpose:** Migration guide from v1 (distributed servo architecture) to v2 (Mechanical Turk / cave architecture). Intended for AugmentCode Intent to update dependent documentation, code, and configuration.

---

## 1. Summary of Change

The v1 architecture placed servo motors at or near each joint on the lamp arm, with strings and PWM signals routed outward from a central Pololu Maestro controller. The v2 architecture inverts this entirely: **all servo motors are relocated to a hidden cavity ("the cave") underneath the rotating base platform**, inspired by the Mechanical Turk cabinet automaton (von Kempelen, 1770). The lamp arm and head contain no motors. Motion is transmitted upward from the cave via strings and a carbon fibre push-pull rod running through the hollow arm tubes.

The lamp must appear to the audience as an ordinary Anglepoise desk lamp. No motors, no wiring, and no mechanical components are visible anywhere on the lamp body.

---

## 2. Physical Platform Change

### v1 — Fixed base on piano surface

The lamp base sat directly on top of the Roland electronic piano, bolted in place. The base did not rotate.

### v2 — Lazy Susan turntable, embedded in piano top

| Element | v1 | v2 |
|---|---|---|
| Base mobility | Fixed | 360° continuous rotation |
| Bearing type | None | Lazy Susan ring bearing |
| Outer ring | N/A | Fixed to Roland piano top surface |
| Inner ring | N/A | Rotates freely, carries entire lamp world |
| Rotation drive | N/A | NEMA 17 stepper, fixed to inner ring, rubber wheel presses against fixed outer ring rim |
| Slip ring required | N/A | **No** — motor rotates with inner ring, no wire boundary crossed |

**Key principle:** The NEMA 17 stepper is bolted to the inner ring. Its output wheel presses against the fixed outer ring. Reaction force rotates the inner ring. Because the motor travels with the inner ring, all wiring stays in the rotating world — no slip ring is needed.

**Wireless boundary:** The only signal that crosses from the fixed world (Mac Mini) to the rotating world (all electronics) is WiFi. An ESP32 on the inner ring receives commands wirelessly and forwards them to the Pololu Maestro via serial. The power cable is the only physical wire that crosses; it enters through a loose central grommet with sufficient slack for performance rotation range.

---

## 3. The Cave — Hidden Servo Compartment

All servo motors are mounted on a **servo bracket rail** suspended from the underside of the inner ring. This creates a hidden cavity approximately 120mm deep between the inner ring underside and the piano top surface.

### Cave inventory (all items rotate with inner ring)

| Component | v1 location | v2 location |
|---|---|---|
| 4× MG996R servo | Distributed along arm | Cave servo rail |
| 2× MG90S servo | Near head joint | Cave servo rail |
| NEMA 17 stepper (base rotation) | N/A | Cave servo rail |
| Pololu Mini Maestro 24-ch | Lamp base exterior | Cave servo rail |
| MEAN WELL LRS-50-5 PSU | External | Cave servo rail |
| Arduino Nano (NeoPixel) | Near lamp head | Cave servo rail |
| ESP32 (WiFi bridge) | N/A (USB was used) | Cave servo rail |

**String exit:** Strings from servo drums exit upward through dedicated holes in the inner ring top plate, entering the lamp column from below. The lamp column is hollow and acts as a string conduit.

---

## 4. Joint-by-Joint Migration

### 4.1 Base Rotation (pan left/right)

| | v1 | v2 |
|---|---|---|
| Mechanism | Not implemented | NEMA 17 stepper on inner ring, wheel on outer ring rim |
| Range | N/A | 360° unlimited |
| Control | N/A | Stepper driver via Maestro or direct GPIO |
| Visibility | N/A | Fully hidden in cave |

---

### 4.2 Lower Arm Raise/Lower

| | v1 | v2 |
|---|---|---|
| Servo | MG996R at base joint | MG996R on cave servo rail |
| Transmission | Short string, direct | String routed up through lamp column, exits at base joint, runs along lower arm underside |
| Pulley | At joint | Guide pulley at base joint redirects string from vertical (column) to horizontal (arm) |
| Return | Manual / gravity | Extension spring at joint provides return force and keeps string taut |

---

### 4.3 Upper Arm Reach (elbow)

| | v1 | v2 |
|---|---|---|
| Servo | MG996R at elbow | MG996R on cave servo rail |
| Transmission | String along lower arm | String continues from cave, up column, along lower arm, over elbow pulley, along upper arm toward head |
| String routing | Exposed | Inside arm tube where possible; eyelets/guide rings on exterior where necessary |

---

### 4.4 Neck Pan (head turns left/right)

This joint is entirely new in v2. It did not exist in v1.

| | v1 | v2 |
|---|---|---|
| Mechanism | Not implemented | Push-pull carbon fibre rod |
| Servo | N/A | MG90S on cave servo rail |
| Rod material | N/A | Ø3mm carbon fibre tube |
| Rod routing | N/A | Through 7mm internal bore of upper arm tube |
| Joint at top | N/A | Capstan wheel (Ø64mm) fixed to yoke shaft; crank pin offset 20mm from centre; rod top pivot-pins to crank pin |
| Operation | N/A | Rod PUSH ↑ = head turns LEFT; rod PULL ↓ = head turns RIGHT |
| Range | N/A | ±90° |

**Why not a servo in the arm:** The upper arm tube is 10mm OD / 7mm ID. No servo exists that fits this bore. All actuation must originate in the cave.

**Wire routing:** The 7mm bore carries the Ø3mm carbon rod plus two thin wires (TTL signal + 12V power) for the AX-12A head servo above. Total bore occupancy is within tolerance.

---

### 4.5 Head Nod (shade tilts up/down)

| | v1 | v2 |
|---|---|---|
| Servo type | MG90S (PWM) | Dynamixel AX-12A (TTL smart servo) |
| Servo location | Near head bracket | Inside lamp shade |
| Mounting principle | Servo body fixed, spindle drives shade | **Inverted:** fixed axle through both yoke arms; AX-12A body rotates on axle; shade bolted to servo body |
| Axle | Single spindle, one bearing point | Ø10mm steel rod through both yoke arms — two bearing points, no side-load |
| Control protocol | PWM via Maestro | TTL serial, daisy-chained with neck servo if applicable |
| Position feedback | None | Yes — AX-12A reports position, temperature, load |
| Compliance mode | None | Yes — software-adjustable stiffness for organic movement feel |
| Range | ~90° | 300° (software-limited to ±150° for safety) |
| NeoPixel ring | Wired externally | Wired through upper arm tube; rotates with shade, always centred in reflector |

**Assembly order (v2):**
1. Left yoke arm (A)
2. Ø10mm steel axle through left yoke arm (B) — fixed, does not rotate
3. Left AX-12A horn / ball bearing (C) onto axle
4. AX-12A body slides onto axle (D) — body will rotate on axle
5. Right horn / bearing (E)
6. Right yoke arm (F) — axle end pins into it
7. Shade collar bolted to AX-12A body with 4× M3 screws (G)
8. Shade drops over collar

---

## 5. Control Stack Changes

### v1 control chain

```
Mac Mini M4 Pro
  └── USB cable
        └── Pololu Mini Maestro 24-ch
              └── PWM signals to servos (MG996R × 4, MG90S × 2)
              └── Serial to Arduino Nano → NeoPixel ring
```

### v2 control chain

```
Mac Mini M4 Pro
  └── WiFi (802.11)
        └── ESP32 (on inner ring, rotating)
              └── Serial → Pololu Mini Maestro 24-ch
                    └── PWM → MG996R × 4 (arm joints, in cave)
                    └── PWM → MG90S × 1 (neck pan rod, in cave)
                    └── PWM → NEMA 17 driver (base rotation)
                    └── Serial bridge → Arduino Nano → NeoPixel ring
              └── TTL serial (daisy-chain) → AX-12A #1 (head nod, in shade)
```

**Removed:** USB cable from Mac Mini to Maestro.
**Added:** ESP32 WiFi bridge on inner ring. TTL serial bus for AX-12A.
**Unchanged:** Arduino Nano / NeoPixel ring relationship.

---

## 6. Servo Channel Map (v2)

Update Maestro configuration and all Python servo control files to reflect this map.

| Maestro Channel | Joint | Servo | v1 Channel |
|---|---|---|---|
| 0 | Base rotation (NEMA 17 step) | Stepper driver | — |
| 1 | Lower arm raise/lower | MG996R | 1 |
| 2 | Upper arm reach (elbow) | MG996R | 2 |
| 3 | Neck pan (push-pull rod) | MG90S | — |
| 4 | (spare) | — | — |
| 5 | NeoPixel (via Nano serial) | Arduino Nano bridge | 5 |
| — | Head nod | AX-12A (TTL, ID=1) | 3 |

**Note:** Head nod (AX-12A) is no longer on a Maestro PWM channel. It is addressed directly via TTL serial using the Dynamixel Protocol 1.0 SDK. Update any code that previously called `set_target(3, angle)` for head nod — this must be replaced with a Dynamixel SDK write instruction to ID=1.

---

## 7. Python Code Migration Notes

### 7.1 Remove

```python
# REMOVE — v1 head nod via Maestro PWM
set_target(3, angle)  # was head nod
```

### 7.2 Add — AX-12A TTL control

```python
# ADD — v2 head nod via Dynamixel SDK
from dynamixel_sdk import PortHandler, PacketHandler

DEVICENAME      = '/dev/cu.usbserial-XXXX'  # TTL adapter port
BAUDRATE        = 1000000
PROTOCOL_VER    = 1.0
DXL_ID_HEAD_NOD = 1
ADDR_GOAL_POS   = 30

port    = PortHandler(DEVICENAME)
packet  = PacketHandler(PROTOCOL_VER)
port.openPort()
port.setBaudRate(BAUDRATE)

def set_head_nod(angle_deg):
    # AX-12A: 0–300° mapped to 0–1023
    value = int((angle_deg / 300.0) * 1023)
    value = max(0, min(1023, value))
    packet.write2ByteTxRx(port, DXL_ID_HEAD_NOD, ADDR_GOAL_POS, value)
```

### 7.3 Add — ESP32 WiFi command dispatch

```python
# ADD — v2 command dispatch over WiFi instead of USB serial
import socket

ESP32_IP   = '192.168.1.XXX'  # set static IP on ESP32
ESP32_PORT = 5005

def send_command(channel, angle):
    msg = f'CH:{channel}:{angle}\n'.encode()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(msg, (ESP32_IP, ESP32_PORT))
```

### 7.4 Add — Neck pan (push-pull rod)

```python
# ADD — v2 neck pan via MG90S push-pull rod
# Maestro channel 3
# Neutral = 90°, LEFT = 50°, RIGHT = 130°
def set_neck_pan(angle_deg):
    """angle_deg: 50=full left, 90=centre, 130=full right"""
    send_command(3, angle_deg)
```

---

## 8. Hardware Procurement Delta (v1 → v2)

### Remove from BOM

| Item | Reason |
|---|---|
| Servo mounting brackets at joints | Servos no longer at joints |
| External wiring along arm exterior | All wiring internal or in cave |

### Add to BOM

| Item | Specification | Purpose |
|---|---|---|
| Lazy Susan bearing ring | Ø300–370mm, steel | Base rotation platform |
| NEMA 17 stepper motor | 12V, ≥40 N·cm | Base pan drive |
| Stepper driver board | A4988 or TMC2209 | NEMA 17 control |
| Servo bracket rail | Aluminium plate, ~280×100mm | Cave servo mounting |
| Hanger rods (×4) | M4 threaded, 100mm | Suspend rail from inner ring |
| ESP32 dev board | ESP32-WROOM-32 | WiFi bridge, replaces USB |
| Dynamixel AX-12A | ROBOTIS, TTL version | Head nod servo |
| TTL half-duplex adapter | USB-to-TTL, direction pin | AX-12A communication |
| Ø10mm steel rod, 200mm | Mild steel | Head nod axle through yoke |
| Ø3mm carbon fibre tube, 400mm | CF, rigid | Neck pan push-pull rod |
| Capstan wheel, Ø64mm | AL or 3D print | Neck joint crank disc |
| Crank pin M4, Ø4mm | Steel | Offset 20mm on capstan |
| Flanged guide pulleys (×3) | Ø44mm, ball bearing | String redirection at joints |
| Extension springs (×2) | 2 N/mm | Return force at arm joints |
| Dyneema string | Ø1.2mm braid | Arm joint strings |
| 3D-printed AX-12A shade cradle | PLA or PETG | Mounts AX-12A inside shade |
| Central cable grommet | Rubber, Ø8mm | Power cable entry to cave |

---

## 9. Files to Update

The following files in the repository should be reviewed and updated to reflect this architecture:

| File | Change required |
|---|---|
| `CLAUDE.md` | Update hardware stack section — servo locations, AX-12A, ESP32, turntable |
| `src/servo_control.py` (or equivalent) | Channel map, AX-12A SDK calls, WiFi dispatch |
| `src/maestro_config.uscp` | Remove head nod channel, add neck pan channel 3 |
| `docs/hardware.md` (if exists) | Full BOM update per section 8 |
| `docs/wiring.md` (if exists) | Cave wiring diagram, TTL bus topology |
| `README.md` | Architecture overview paragraph |

---

## 10. What Has NOT Changed

The following remain identical between v1 and v2:

- Mac Mini M4 Pro as show control host
- Ardour + Pianoteq 9 + MODO DRUM audio stack
- NeoPixel RGBW ring inside shade, driven by Arduino Nano
- Logitech C920 webcam role (gaze / projection source)
- Ten-act screenplay structure and lamp movement vocabulary
- Pololu Mini Maestro 24-channel as PWM servo hub
- MEAN WELL LRS-50-5 power supply (5V rail)
- MG996R servos for large articulation joints (now in cave rather than at joints)
- Performance date: October 2026

---

*Document generated from design session, April 2026.*
*Drawings reference: PX-001-A (base turntable), PX-002-A (elbow joint), PX-003-A (head joint), PX-004-A (neck push-pull).*
