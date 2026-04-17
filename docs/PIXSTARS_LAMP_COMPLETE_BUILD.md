# Pixstars Lamp Complete Build

This document is the canonical combined build guide for the Pixstars lamp system.

## System overview

### Lamp head

- Raspberry Pi Zero 2 WH (H means pre-soldered headers — no soldering required)
- USB microphone
- small speaker
- WS2812B / NeoPixel LED ring
- `hivemind-mic-satellite`

### Mac Mini M4 Pro

- `hivemind-core`
- `hivemind-audio-binary-protocol`
- OVOS-side STT / TTS / wake word / synthetic voice
- optional Ardour for deterministic cue playback

## Wake word

Target wake word: **Hey A.I.**

## LED state language

| State | Meaning | Color | Motion |
| --- | --- | --- | --- |
| idle | resting but alive | warm amber | slow breathing |
| listening | hearing user input | blue | gentle pulse |
| thinking | processing | purple | tighter pulse |
| speaking | playing reply audio | warm orange/yellow | follows speech level |
| error | service problem | red | warning pulse |

## Recommended first milestones

1. Prove Pi boots and is reachable by SSH
2. Prove microphone and speaker work
3. Prove HiveMind server and client can pair
4. Prove LED ring wiring and state script
5. Add wake-word flow
6. Add real STT / TTS
7. Add synthetic voice
8. Add Ardour timing-critical lines

See the other documents and scripts in this starter pack.