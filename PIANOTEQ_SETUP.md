# Pixstars — Pianoteq Piano Playback Setup

> Documentation of decisions and instructions for using Pianoteq to render piano audio for the Pixstars project.

---

## Overview

The Pixstars project uses **Pianoteq** by Modartt to render high-quality piano audio from MIDI files on an **Apple Mac Mini M4 Pro**. Rather than using pre-recorded audio samples, Pianoteq uses physical modelling technology to synthesise piano sound in real time — producing expressive, lifelike results from any MIDI source.

---

## Software: Pianoteq

- **Product:** [Pianoteq 9](https://www.modartt.com/pianoteq_overview) by Modartt
- **Technology:** Physical modelling (not sample-based) — notes are generated in real time
- **Platform:** macOS (Windows, Linux and iOS also supported)
- **Download size:** ~50 MB
- **Website:** https://www.modartt.com/pianoteq

### Edition in use: Free Trial (Demo)

We are using the **free trial version** of Pianoteq. This is a deliberate decision:

> The demo version disables a few keys on an external MIDI keyboard. Since Pixstars does **not** use an external keyboard — only pre-recorded MIDI files — the key restriction has no effect. MIDI file playback works fully in the demo version.

There is no need to purchase a licence for the current workflow. Should the project later require external keyboard input or commercial export, upgrading to **Pianoteq Stage** (entry paid edition) would be the appropriate next step.

---

## Hardware: Apple Mac Mini M4 Pro

Pianoteq runs natively on macOS and is well-suited to the M4 Pro chip. Its low CPU footprint and small file size make it an efficient fit for the Mac Mini's architecture.

---

## MIDI Source File

The MIDI file used in this project is a professionally produced arrangement of:

| Field        | Value                                      |
|--------------|--------------------------------------------|
| Song         | November Rain                              |
| Artist       | Guns N' Roses                              |
| Source       | [midi.com.au](https://www.midi.com.au) (Hit Trax) |
| File (Format 0) | `ds1056.mid`                            |
| File (Format 1) | `ds1056-format1.mid` *(recommended)*    |
| Duration     | 8:59 / 182 bars                            |
| Tempo        | Part 1: 78 bpm / Part 2: 92 bpm, rall to end |
| Key          | B major (Part 1), B minor (Part 2)         |

### MIDI Channels

| Channel | Instrument         |
|---------|--------------------|
| Ch 1    | **Piano 1** ← primary channel for Pianoteq |
| Ch 2    | Fingered Bass      |
| Ch 3    | Steel-String Guitar |
| Ch 4    | Clean Guitar       |
| Ch 5    | Distortion Guitar  |
| Ch 6    | Overdrive Guitar   |
| Ch 7    | Sweep Pad          |
| Ch 8    | Flute              |
| Ch 9    | Choir Aahs         |
| Ch 10   | Drums (Standard Kit) |
| Ch 11   | Strings            |
| Ch 12   | Tremolo Strings    |
| Ch 13   | Pizzicato Strings  |

> **Use `ds1056-format1.mid`** (Format 1). This file keeps all channels on separate tracks, giving Pianoteq the cleanest input for isolating the piano part.

---

## Step-by-Step: Loading and Playing the MIDI File

1. Open **Pianoteq** on the Mac Mini.
2. Go to **File → Load MIDI File**.
3. Select **`ds1056-format1.mid`**.
4. The piano roll will appear at the top of the screen.
5. Go to **Options → MIDI** and set Pianoteq to receive on **Channel 1 only** — this isolates the piano and silences guitars, drums, strings, etc.
6. Choose your preferred piano model (see recommendation below).
7. Press **Play**.

---

## Recommended Piano Model

For *November Rain*, a **Steinway grand** is the closest match to the original recording. In Pianoteq, select:

- **Steinway Model D** (concert grand, bright and powerful)
- or **Steinway Model B** (slightly warmer — also suitable)

These are available in the free trial in demo mode for evaluation.

---

## Volume Setting — Important

> ⚠️ **Do not set the master volume above `-8.0 dB`.**

A volume higher than **-8.0 dB** causes the audio output to exceed peak levels, resulting in **distortion** (clipping). 

**Recommended setting: `-8.0 dB`** on the Pianoteq master volume control.

This ensures clean, undistorted audio for both live playback and exported files.

---

## Exporting Audio

To save the piano performance as a permanent audio file:

1. Load the MIDI file as described above.
2. Configure channel, piano model and volume (`-8.0 dB`).
3. Go to **File → Export to Audio File**.
4. Choose format:
   - **FLAC** — lossless, best quality, recommended for archiving
   - **WAV** — uncompressed, also lossless
   - **MP3** — compressed, smaller file size, suitable for sharing
5. The export renders faster than real-time playback.

The resulting audio file can be played back in any media player without needing Pianoteq.

---

## Saving for Repeated Playback in Pianoteq

If you prefer to replay via Pianoteq rather than a fixed audio file:

- Store `ds1056-format1.mid` in a stable folder on the Mac.
- Add it to Pianoteq's built-in playlist via **File → Manage MIDI Playlist** for one-click access.
- Pianoteq also auto-saves recent performances — go to **File → Recently played on the keyboard** to recover a session.

---

## Copyright Note

*November Rain* is a copyrighted work. The MIDI file was obtained from [midi.com.au](https://www.midi.com.au) (Hit Trax), a licensed MIDI retailer that pays royalties to songwriters and publishers. Use of this file is for private, personal purposes within the Pixstars project only. Publishing or distributing any resulting audio recording commercially would require separate licensing.

---

## Summary of Key Decisions

| Decision | Choice | Reason |
|---|---|---|
| Software | Pianoteq (free trial) | MIDI playback unaffected by demo key restrictions |
| Hardware | Mac Mini M4 Pro | Native macOS support, low CPU usage |
| MIDI file | `ds1056-format1.mid` | Format 1 keeps tracks separate for cleaner channel isolation |
| Active channel | Ch 1 (Piano 1) | All other channels muted in Pianoteq MIDI settings |
| Piano model | Steinway grand | Closest match to original November Rain recording |
| Master volume | `-8.0 dB` | Higher levels cause peak distortion (clipping) |
| Export format | FLAC (recommended) | Lossless quality for archiving |

---

*Last updated: March 2026*
