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

## Hardware stack (Pinokio lamp)

- **Pololu Mini Maestro 24-channel USB servo controller** — primary motion brain
- **4× MG996R** servos (large articulation: base, shoulder, elbow, head tilt)
- **2× MG90S** servos (fine motion)
- **MEAN WELL LRS-50-5** power supply (5V rail for servos, separated from logic)
- **Logitech C920** webcam — mounted on/near the lamp, role TBD in script (gaze / projection source / both)
- **NeoPixel RGBW LED ring** driven by an **Arduino Nano** acting as a serial bridge (the Maestro doesn't speak NeoPixel, hence the Nano)
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
- Maestro Control Center or scripted serial control for servos
- Arduino serial bridge for the NeoPixel ring
- Piano (Pianoteq) either synced to Ardour transport or played live — screenplay specifies per act

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
