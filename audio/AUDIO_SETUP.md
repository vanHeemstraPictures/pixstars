# Pixstars — Audio Setup Documentation

> Documentation of decisions and instructions for using Pianoteq and MODO DRUM with Ardour to render piano and drum audio for the Pixstars project.

---

## Overview

The Pixstars project uses two virtual instrument plugins to render high-quality audio from a single MIDI file on an **Apple Mac Mini M4 Pro**:

- **Pianoteq** (by Modartt) — renders the piano part (Channel 1)
- **MODO DRUM** (by IK Multimedia) — renders the drum part (Channel 10)

Both plugins are hosted inside **Ardour** (open-source DAW), which imports the MIDI file and routes each channel to the correct instrument. This allows piano and drums to play simultaneously from the same session.

---

## Hardware

**Apple Mac Mini M4 Pro** running macOS. Both plugins run natively and efficiently on the M4 Pro chip.

---

## Plugin Format: VST3 vs AU — What is the difference?

Both Pianoteq and MODO DRUM are available in two formats on macOS: **VST3** and **AU (AudioUnit)**. Both have been loaded as VST3 in this project. Here is what the difference means in practice:

| | VST3 | AU (AudioUnit) |
|---|---|---|
| **Developer** | Steinberg (cross-platform standard) | Apple (macOS/iOS only) |
| **macOS support** | ✅ Yes | ✅ Yes |
| **Windows support** | ✅ Yes | ❌ No |
| **CPU efficiency** | Suspends processing when silent | Always processing |
| **Works in Ardour** | ✅ Yes | ✅ Yes |
| **Works in Logic Pro** | ✅ Yes | ✅ Yes (AU required by Logic) |
| **Works in GarageBand** | ✅ Yes | ✅ Yes (AU required) |
| **Sound quality difference** | None in practice | None in practice |

### Key points

- **AU is Apple's native format**, built into macOS at the system level. It was designed specifically for Apple DAWs — Logic Pro and GarageBand *require* AU and will not load VST plugins at all.
- **VST3 is the universal cross-platform standard**, developed by Steinberg (makers of Cubase). It is supported by virtually all non-Apple DAWs including Ardour, Ableton Live, Reaper, and Studio One.
- In terms of sound quality, there is **no audible difference** between the two formats for the same plugin.
- The one practical VST3 advantage is **CPU efficiency**: VST3 plugins suspend processing automatically when no audio signal is present, whereas AU plugins continue processing even during silence.

### Recommendation for Pixstars

**VST3 is the correct choice** for this project. Since Ardour is the host DAW (not Logic or GarageBand), VST3 is the more universally supported and future-proof format. Both Pianoteq and MODO DRUM have been loaded as VST3 — this is consistent and correct. If the project were ever moved to Logic Pro, switching to the AU versions would be necessary.

---

## MIDI Source File

The MIDI file used in this project is a professionally produced arrangement purchased from Hit Trax:

| Field           | Value                                               |
|-----------------|-----------------------------------------------------|
| Song            | November Rain                                       |
| Artist          | Guns N' Roses                                       |
| Source          | [midi.com.au](https://www.midi.com.au) (Hit Trax)   |
| File (Format 0) | `ds1056.mid`                                        |
| File (Format 1) | `ds1056-format1.mid` *(recommended — use this one)* |
| Duration        | 8:59 / 182 bars                                     |
| Tempo           | Part 1: 78 bpm / Part 2: 92 bpm, rall to end       |
| Key             | B major (Part 1), B minor (Part 2)                  |

> **Always use `ds1056-format1.mid`** (MIDI Format 1). This keeps all channels on separate tracks, which is essential for routing each instrument to the correct plugin in Ardour.

### MIDI Channels

| Channel | Instrument          | Plugin assigned      |
|---------|---------------------|----------------------|
| Ch 1    | Piano 1             | **Pianoteq (VST3)**  |
| Ch 2    | Fingered Bass       | —                    |
| Ch 3    | Steel-String Guitar | —                    |
| Ch 4    | Clean Guitar        | —                    |
| Ch 5    | Distortion Guitar   | —                    |
| Ch 6    | Overdrive Guitar    | —                    |
| Ch 7    | Sweep Pad           | —                    |
| Ch 8    | Flute               | —                    |
| Ch 9    | Choir Aahs          | —                    |
| Ch 10   | Drums               | **MODO DRUM (VST3)** |
| Ch 11   | Strings             | —                    |
| Ch 12   | Tremolo Strings     | —                    |
| Ch 13   | Pizzicato Strings   | —                    |

The remaining 11 channels (bass, guitars, strings, pad, choir) are present in Ardour as silent MIDI tracks, available for future instrument assignment.

---

## Software 1: Pianoteq (Piano — Channel 1)

- **Product:** [Pianoteq 9](https://www.modartt.com/pianoteq_overview) by Modartt
- **Technology:** Physical modelling — notes are synthesised in real time, no samples
- **Edition:** Free trial (demo)
- **Plugin format:** VST3
- **Download size:** ~50 MB
- **Website:** https://www.modartt.com/pianoteq

### Why the free trial is sufficient

The demo version disables a few keys on an **external MIDI keyboard**. Since Pixstars does not use an external keyboard — only pre-recorded MIDI files — this restriction has no effect. MIDI file playback works fully in the demo version.

### Recommended piano model

For *November Rain*, a **Steinway grand** is the closest match to the original recording:

- **Steinway Model D** — concert grand, bright and powerful
- **Steinway Model B** — slightly warmer, also suitable

Both are available in demo mode in the free trial.

### Volume setting — important

> ⚠️ **Do not set the master volume above `-8.0 dB`.**

A volume higher than **-8.0 dB** causes the audio output to exceed peak levels, resulting in **distortion** (clipping).

**Recommended setting: `-8.0 dB`** on the Pianoteq master volume control.

---

## Software 2: MODO DRUM (Drums — Channel 10)

- **Product:** [MODO DRUM 1.5](https://www.ikmultimedia.com/products/mododrum/) by IK Multimedia
- **Technology:** Physical modelling via modal synthesis — drum sounds generated in real time
- **Edition:** Licensed (purchased)
- **Plugin format:** VST3
- **Drum kit:** **Rock Custom Sounds** (licensed and purchased)

### Installing MODO DRUM

MODO DRUM installs through IK Multimedia's package manager:

1. Download **IK Product Manager** for macOS:
   `https://g1.ikmultimedia.com/plugins/ProductManager/ik_product_manager_1.1.11.dmg`
2. Install and open IK Product Manager
3. Create a free IK Multimedia account at https://www.ikmultimedia.com/userarea/
4. Log in, locate **MODO DRUM** and the **Rock Custom Sounds** kit
5. Click **Install** — the plugin installs as both AU and VST3 automatically

---

## Software 3: Ardour (DAW)

- **Product:** [Ardour](https://ardour.org) — open-source DAW
- **Role:** Hosts both Pianoteq and MODO DRUM, imports the MIDI file, and routes each channel to the correct plugin
- **Why needed:** MODO DRUM cannot load external MIDI files in standalone mode — a DAW is required. Running both plugins inside Ardour also allows piano and drums to play simultaneously in one session.

### Step-by-step: Setting up the full session in Ardour

#### Step 1 — Import the MIDI file

1. Open Ardour and create a new session (**File → New Session**)
2. Go to **Session → Import** (or press **Ctrl+I**)
3. Select **`ds1056-format1.mid`**
4. Set **"Import as"** to **MIDI tracks** and select **"One track per channel"**
5. Click **OK** — Ardour creates 13 separate MIDI tracks, one per channel

#### Step 2 — Open the Mixer

Press **Alt+M** (or **Window → Mixer**). You will see all 13 tracks as vertical strips.

#### Step 3 — Add Pianoteq to the Channel 1 track (Piano)

1. Locate the **Channel 1** strip in the Mixer
2. **Double-click** in the Processor Box (the upper area of the strip containing the blue Fader block)
3. On first use, Ardour will scan your computer for VST/AU plugins — allow this scan to complete
4. When the **Plugin Selector** opens, type **Pianoteq** in the search box
5. Select the **VST3** version and click **Add**, then **Insert Plugin / Close**
6. Double-click the Pianoteq block to open its interface and select your Steinway model

#### Step 4 — Add MODO DRUM to the Channel 10 track (Drums)

1. Locate the **Channel 10** strip in the Mixer
2. **Double-click** in the Processor Box
3. In the **Plugin Selector**, type **MODO DRUM**
4. Select the **VST3** version and click **Add**, then **Insert Plugin / Close**
5. Double-click the MODO DRUM block to open its interface and confirm the **Rock Custom Sounds** kit is loaded

#### Step 5 — Play and save

- Press **Spacebar** to play — both piano and drums will sound simultaneously
- Use the fader on each mixer strip to balance the volume of piano vs drums to taste
- Save the session with **Ctrl+S** — Ardour remembers both plugin assignments and all settings for next time

---

## Exporting Audio from Ardour

To render the session as a permanent audio file:

1. Go to **Session → Export → Export to Audio File**
2. Select the range (full session or a specific section)
3. Choose format: **FLAC** (lossless, recommended), **WAV**, or **MP3**
4. Click **Export**

The resulting file contains both piano and drums mixed together and plays in any media player without needing Ardour.

---

## Copyright Note

*November Rain* is a copyrighted work. The MIDI file was obtained from [midi.com.au](https://www.midi.com.au) (Hit Trax), a licensed MIDI retailer that pays royalties to songwriters and publishers. The MODO DRUM Rock Custom Sounds kit is a purchased, licensed product. Use of these files is for private, personal purposes within the Pixstars project only. Publishing or distributing any resulting audio recording commercially would require separate licensing.

---

## Summary of Key Decisions

| Decision | Choice | Reason |
|---|---|---|
| Piano software | Pianoteq 9 (free trial) | MIDI playback unaffected by demo key restrictions |
| Drum software | MODO DRUM (licensed) | Physical modelling, realistic rock drum sounds |
| Drum kit | Rock Custom Sounds | Suited to November Rain; purchased licence |
| Plugin format | VST3 (both plugins) | Works in Ardour; cross-platform; CPU-efficient |
| DAW | Ardour | Hosts both plugins; open-source; routes MIDI channels |
| Hardware | Mac Mini M4 Pro | Native macOS support, low CPU usage |
| MIDI file | `ds1056-format1.mid` | Format 1 keeps tracks separate for clean channel routing |
| Piano channel | Ch 1 → Pianoteq | Assigned in Ardour Mixer |
| Drums channel | Ch 10 → MODO DRUM | Assigned in Ardour Mixer |
| Master volume (Pianoteq) | `-8.0 dB` | Higher levels cause peak distortion (clipping) |
| Export format | FLAC (recommended) | Lossless quality for archiving |

---

*Last updated: March 2026*
