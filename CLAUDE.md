# PIXSTARS

A 20-minute silent theatrical performance commissioned by Ruurd Dam (Managing Director, Team Rockstars) for a live event in **October 2026**. The piece is production-bound, not exploratory — the screenplay is in ten acts and ready to drive build decisions.

## Core concept

A single performer on stage with an animatronic desk lamp ("A.I."), live piano, and a deconstructed audio/MIDI rendering of Guns N' Roses' "November Rain." The performer holds three simultaneous character identities — **Rockstar**, **Creator**, and **Witness** — shifting between them without dialogue. Silence is the medium; movement, light, and sound carry the narrative.

Tonal reference: Kim Ki-duk's filmmaking. Sparse, patient, physical, emotionally loaded.

## Screenplay

- Ten acts, production-ready draft
- Lamp movement vocabulary defined (not ad-lib — choreographed gestures with named primitives)
- Spatial sound design notes per act
- Director's Appendix included (staging intent, transitions, cue logic)
- Three-identity throughline (Rockstar / Creator / Witness) is load-bearing — treat as structural, not decorative

When editing the screenplay, preserve the identity shifts and the lamp vocabulary. Don't collapse them.

## Hardware stack (A.I. lamp) — Cave Architecture v3

All servos and electronics are hidden inside a "cave" under a DIY ESP32-driven
turntable (NEMA 17 + TMC2209 + GT2 belt friction-drive on a 200mm lazy Susan bearing),
mounted on a riser block. The lamp itself contains no motors
— only a WS2812 5050 RGB LED Ring 16 and a Dynamixel AX-12A for head nod. Cables route through
a single central column.

See `architecture_decision_records/LAMP_ARCHITECTURE_v3.md` for the original cave rationale
(note: the v3 ComXim turntable has been superseded by the DIY ESP32-driven turntable below).

### Base rotation
- **DIY ESP32-driven turntable** — NEMA 17 stepper (1.8°, 200 steps/rev) driven by **TMC2209**
  (StealthChop for silent operation, 1/16 microstepping) via the cave ESP32 (STEP/DIR pins).
  **GT2 belt friction-drive** wrapped directly around a **200mm lazy Susan bearing** outer race
  (no ring gear/pulley needed) — ~15.7:1 ratio (628mm bearing circumference / 40mm 20T pulley),
  yielding **~0.00717° per microstep** (~50,240 steps/rev). **Hall effect sensor** (SS49E/A3144)
  + neodymium magnet for origin detection. Bilateral belt tensioner maintains friction grip.
  Controlled via **OSC** from Mac Mini through the same cave ESP32
  (endpoints: `/turntable/rotate`, `/turntable/origin`, `/turntable/stop`).
  Firmware uses FastAccelStepper (hardware pulse generation).
  Reference design: github.com/MGX3D/Turntable.
- **Riser block** (120–150mm AL or plywood) — creates cave depth, turntable platform mounts on top

### Cave (under turntable, on servo rail)
- **ESP32-S3 N16R8 DevKit** — WiFi bridge to Mac Mini, drives Maestro + AX-12A + WS2812 LED ring (RMT peripheral) + TMC2209/NEMA 17 turntable stepper (STEP/DIR/ENABLE + Hall sensor input)
- **TMC2209 stepper driver** — silent (StealthChop) microstepping driver for the NEMA 17 turntable motor, 12V from shared 12V rail, STEP/DIR/EN from ESP32
- **Pololu Mini Maestro 24-channel** servo controller (serial from ESP32)
- **4x MG996R** servos — lower arm (Ch1), elbow (Ch2), spare (Ch3-4)
- **1x MG90S** servo — neck pan (Ch3), carbon fibre push-pull rod to lamp head
- **ILDAWaveX16 V2** (ESP32-S3 + RP2354, 16-bit DAC) — ILDA DAC with WiFi/Ethernet/USB, receives laser cues from Mac Mini via Ether Dream or IDN protocol, outputs standard ILDA DB25 (+/-5V X/Y galvo signals, 0-5V RGB laser modulation)
- **40kpps galvo driver board** (110 x 68 x 35 mm, Teclulu GH40 or equivalent) — drives the X/Y galvo motors in the lamp head, +/-5V input from ILDAWaveX16 V2 DB25
- **LPLDD-1A-16V-3CH laser driver** — drives the Opt Lasers 300mW Micro RGB module; 0-5V analog modulation per channel from the ILDAWaveX16 V2 DB25 RGB lines
- **MEAN WELL LRS-50-5** power supply (5V rail for servos and LED ring, separated from logic)
- **+/-24V galvo PSU** — dedicated dual-rail supply for the 40kpps galvo driver board (included in galvo scanner set)
- **MEAN WELL LRS-35-12** (or equivalent) — 12V PSU for the LPLDD-1A-16V-3CH laser driver (which powers the Opt Lasers 300mW Micro RGB module; DC 12V input)

### Lamp head
- **Dynamixel AX-12A** — head nod (TTL serial via ESP32, NOT on Maestro)
- **WS2812 5050 RGB LED Ring 16** — physically in the lamp head, driven by ESP32 DevKit GPIO (RMT peripheral) in the cave, powered from the cave MEAN WELL LRS-50-5; 5V/GND/DATA route through the central cable column with a JST-SM 3-pin connector at the lamp head junction, 330Ω series resistor on the data line at the ESP32 end, 1000µF capacitor near the ring
- **RGB Laser Galvo Scanner** — Opt Lasers 300mW Micro RGB (44 x 39 x 27 mm, 638/520/450nm) + 40kpps X/Y galvo mirrors (7 x 12 mm), projects along the lamp eye-line (vector laser drawing); 0-5V RGB modulation + galvo motor signal cables route through cable column to ILDAWaveX16 V2 and galvo driver in the cave; 12V DC power through cable column
- **OV2640 camera module** (~3g) — on Pi Zero 2 WH (CSI/SPI), role TBD in script

### Host
- **Mac Mini M4 Pro** — show control host, runs everything

### Lamp base AI
- **Seeed Studio reComputer RK3588-40** — local AI brain (6 TOPS NPU, 16GB LPDDR5, expandable to 26 TOPS via PCIe)
- Runs: wake word, STT, TTS, local LLM, computer vision, emotional state engine, HiveMind client

Servo channel map and sequence scripts live in this repo. Update both together when channels shift.

## Audio stack ("November Rain")

Hosted in **Ardour** from a purchased Hit Trax MIDI file (licensed, don't redistribute the source MIDI).

- **Pianoteq 9** (Steinway model, VST3) — piano
- **MODO DRUM** with **Rock Custom Sounds** kit — drums
- Deconstructed arrangement: this is not a cover, it's a reduction. Respect the editorial decisions already made in the Ardour session — stems have been pulled out deliberately.

## Show control

Mac Mini M4 Pro runs:
- Ardour (audio/MIDI playback and routing)
- ESP32 WiFi communication (OSC commands to lamp cave servos, LED ring, and DIY turntable stepper)
- Piano (Pianoteq) either synced to Ardour transport or played live — screenplay specifies per act
- projection/ subsystem (pygame, OSC port 9002) -- drives the Epson EB-W05 rear projector over HDMI for theater-scale imagery (Disney castle, GNR logo, AI iterations, signatures)

### Dual projection system

The performance uses two projection systems sharing one rear-projection screen:
- **Rear projector (Epson EB-W05)** -- HDMI from Mac Mini, projects large theater-readable imagery onto the back of the screen from backstage
- **Lamp laser (Opt Lasers 300mW Micro RGB + 40kpps galvo)** -- projects small vector drawings (lamp's "thoughts": stick figures, text) onto the front of the same screen from the lamp head

Both systems target the same rear-projection screen from opposite sides.

ESP32 in the lamp cave handles:
- Maestro serial control for MG996R/MG90S servos
- AX-12A TTL serial for head nod
- WS2812 LED ring drive via GPIO (RMT peripheral); the Mac Mini orchestrates LED cues over the same WiFi/OSC channel used for servo commands
- ILDAWaveX16 V2 (16-bit ILDA DAC) receives cues from Mac Mini via Ether Dream or IDN protocol over WiFi/Ethernet; outputs ILDA DB25 signals (+/-5V X/Y to galvo driver, 0-5V RGB to Opt Lasers laser module) through the cable column to the lamp head

Base rotation (DIY turntable) handles:
- Precision stepping (~0.00717° per microstep) via the cave ESP32 -> TMC2209 -> NEMA 17, with GT2 belt friction-drive on a 200mm lazy Susan bearing
- Origin return on command via Hall effect sensor (SS49E/A3144) + magnet
- Controlled from Mac Mini via OSC through the same cave ESP32 (no separate device or protocol)

Timecode strategy and cue routing should live in `docs/` or a top-level `SHOW_CONTROL.md` — check what's there before assuming.

## Project conventions

- **Quotes**: straight ASCII `"` only, never smart quotes. If editing files programmatically, verify before handing back.
- **File delivery**: prefer writing files to disk over pasting content into chat (smart-quote corruption risk in clipboards).
- **Repo layout**: follow the numbered `100–1900` directory convention used across the `stallone` GitHub org if this repo adopts it; otherwise respect whatever structure is already here.
- **Language**: screenplay and director notes are in English. Internal comments may be Dutch where that's already the pattern — don't translate existing Dutch unless asked.

## What this project is NOT

- Not a tech demo. The hardware serves the performance; don't propose features that don't earn their stage time.
- Not a speaking piece. No dialogue, no voiceover. If a problem seems to want words, the answer is almost always lamp motion, light, or silence.
- Not improvised. The screenplay is the contract.

## Collaborators

- **Willem van Heemstra** — performer, creator, technical lead (Cloud Engineer at Team Rockstars Cloud, 30+ years IT, card magician, five languages)
- **Ruurd Dam** — commissioning party, Managing Director, Team Rockstars
- Performance target: **October 2026**, live event

## Working with this repo

Before making changes:
1. Read the current screenplay draft end-to-end — acts reference each other
2. Check the servo channel map against any motion script you're editing
3. If touching the Ardour session, note which plugins are involved (Pianoteq 9 VST3, MODO DRUM) — don't assume availability

When in doubt, ask. This is a live performance with a fixed date; ambiguity compounds badly.
