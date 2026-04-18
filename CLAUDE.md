# PIXSTARS

A 20-minute silent theatrical performance commissioned by Ruurd Dam (Managing Director, Team Rockstars) for a live event in **October 2026**. The piece is production-bound, not exploratory — the screenplay is in ten acts and ready to drive build decisions.

## Core concept

A single performer on stage with an animatronic desk lamp ("Pinokio"), live piano, and a deconstructed audio/MIDI rendering of Guns N' Roses' "November Rain." The performer holds three simultaneous character identities — **Rockstar**, **Creator**, and **Witness** — shifting between them without dialogue. Silence is the medium; movement, light, and sound carry the narrative.

Tonal reference: Kim Ki-duk's filmmaking. Sparse, patient, physical, emotionally loaded.

## Screenplay

- Ten acts, production-ready draft
- Lamp movement vocabulary defined (not ad-lib — choreographed gestures with named primitives)
- Spatial sound design notes per act
- Director's Appendix included (staging intent, transitions, cue logic)
- Three-identity throughline (Rockstar / Creator / Witness) is load-bearing — treat as structural, not decorative

When editing the screenplay, preserve the identity shifts and the lamp vocabulary. Don't collapse them.

## Hardware stack (Pinokio lamp) — Cave Architecture v3

All servos and electronics are hidden inside a "cave" under a ComXim MTxRUWSLPro
programmable turntable, mounted on a riser block. The lamp itself contains no motors
— only a NeoPixel LED ring and a Dynamixel AX-12A for head nod. Cables route through
a single central column.

See `architecture_decision_records/LAMP_ARCHITECTURE_v3.md` for the full rationale.

### Base rotation
- **ComXim MTxRUWSLPro** programmable turntable — precision base rotation (0.1°),
  WiFi CT command protocol, controlled directly from Mac Mini (not via ESP32)
- **Riser block** (120–150mm AL or plywood) — creates cave depth, ComXim mounts on top

### Cave (under turntable, on servo rail)
- **ESP32 DevKit** — WiFi bridge to Mac Mini, drives Maestro + AX-12A
- **Pololu Mini Maestro 24-channel** servo controller (serial from ESP32)
- **4x MG996R** servos — lower arm (Ch1), elbow (Ch2), spare (Ch3-4)
- **1x MG90S** servo — neck pan (Ch3), carbon fibre push-pull rod to lamp head
- **Arduino Nano** — NeoPixel serial bridge (Ch5 on Maestro)
- **MEAN WELL LRS-50-5** power supply (5V rail for servos, separated from logic)

### Lamp head
- **Dynamixel AX-12A** — head nod (TTL serial via ESP32, NOT on Maestro)
- **NeoPixel RGBW LED ring** — driven by Arduino Nano (serial bridge from Maestro Ch5)
- **Logitech C920** webcam — mounted on/near the lamp, role TBD in script

### Host
- **Mac Mini M4 Pro** — show control host, runs everything

Servo channel map and sequence scripts live in this repo. Update both together when channels shift.

## Audio stack ("November Rain")

Hosted in **Ardour** from a purchased Hit Trax MIDI file (licensed, don't redistribute the source MIDI).

- **Pianoteq 9** (Steinway model, VST3) — piano
- **MODO DRUM** with **Rock Custom Sounds** kit — drums
- Deconstructed arrangement: this is not a cover, it's a reduction. Respect the editorial decisions already made in the Ardour session — stems have been pulled out deliberately.

## Show control

Mac Mini M4 Pro runs:
- Ardour (audio/MIDI playback and routing)
- ESP32 WiFi communication (OSC commands to lamp cave servos)
- ComXim WiFi communication (CT commands for base rotation)
- Piano (Pianoteq) either synced to Ardour transport or played live — screenplay specifies per act

ESP32 in the lamp cave handles:
- Maestro serial control for MG996R/MG90S servos
- AX-12A TTL serial for head nod
- Arduino Nano serial bridge for NeoPixel RGBW ring

ComXim MTxRUWSLPro handles:
- Base rotation (precision stepping, 0.1° resolution)
- Origin return on command
- Controlled directly from Mac Mini via WiFi CT protocol

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
