# November Rain — Drum Track Build Log

**Project:** Pixstars**Repository:** [https://github.com/vanHeemstraPictures/pixstars](https://github.com/vanHeemstraPictures/pixstars)**Goal:** Recreate the Matt Sorum drum track from "November Rain" by Guns N' Roses in Ardour + Hydrogen on a Mac Mini M4 Pro**Status:** 🟡 In Progress

## Table of Contents

1. [Hardware & Software Setup](#1-hardware--software-setup)
2. [Software Stack](#2-software-stack)
3. [JackPilot Configuration](#3-jackpilot-configuration)
4. [Hydrogen Configuration](#4-hydrogen-configuration)
5. [Ardour Configuration](#5-ardour-configuration)
6. [Connecting Everything via JackPilot Routing](#6-connecting-everything-via-jackpilot-routing)
7. [Recording the Drum Track in Ardour](#7-recording-the-drum-track-in-ardour)
8. [November Rain — Song Details](#8-november-rain--song-details)
9. [Hydrogen Pattern Library](#9-hydrogen-pattern-library)
10. [Song Editor Arrangement](#10-song-editor-arrangement)
11. [ForzeeStereo Drumkit Notes](#11-forzestereo-drumkit-notes)
12. [Troubleshooting](#12-troubleshooting)
13. [Startup Checklist](#13-startup-checklist)
14. [Open Items & Next Steps](#14-open-items--next-steps)

## 1. Hardware & Software Setup

| Item | Detail |
| --- | --- |
| Machine | Mac Mini M4 Pro |
| Memory | 24GB unified memory |
| OS | macOS |
| DAW | Ardour (installed locally) |
| Drum Machine | Hydrogen |
| Audio Bridge | JackPilot |
| Drumkit file | ForzeeStereo.h2drumkit |
| Reference video | https://www.youtube.com/watch?v=GsNfZ0TF-bk |

## 2. Software Stack

### Ardour

The DAW used for recording, mixing, and final output. Ardour connects to JACK as a client and acts as the **JACK Transport Master** — it drives the timeline and Hydrogen follows.

### Hydrogen

An open-source, dedicated drum machine application. Used to:

- Host the ForzeeStereo drumkit
- Program all drum patterns (verse, chorus, fills, etc.)
- Arrange patterns in the Song Editor
- Output audio via JACK to Ardour for recording

Install via Homebrew if not already installed:

```bash
brew install --cask hydrogen
```

### JackPilot

The JACK audio server control application for macOS. It acts as the audio routing backbone between Hydrogen and Ardour, allowing:

- Virtual audio cables between apps
- Synchronized playback via JACK Transport

### ForzeeStereo.h2drumkit

A Hydrogen drumkit file (`.h2drumkit` format) containing stereo drum samples. This is the kit used in the reference video tutorial. It must be imported into Hydrogen before use.

## 3. JackPilot Configuration

### Starting JackPilot

**Always start JackPilot before any other audio application.** This is the golden rule — if you start Hydrogen or Ardour first, they won't connect to JACK properly.

1. Open **JackPilot**
2. Click **Start** to launch the JACK server
3. Verify sample rate matches your Ardour session — either **44100 Hz** or **48000 Hz**
4. Leave JackPilot running in the background throughout your session

### JackPilot Routing Matrix

The routing matrix in JackPilot is where you draw the virtual cables between Hydrogen's outputs and Ardour's inputs. See [Section 6](#6-connecting-everything-via-jackpilot-routing) for the exact connections to make.

## 4. Hydrogen Configuration

### Step 1 — Set Audio Driver to JACK

1. Open **Hydrogen** (after JackPilot is running)
2. Go to **Options → Preferences → Audio System tab**
3. Set the audio driver to **JACK**
4. Click **OK** and **restart Hydrogen**

### Step 2 — Enable JACK Transport Slave

In Hydrogen's main toolbar, click the **JACK Transport** button (plug/sync icon). This makes Hydrogen a slave to Ardour's timeline — when you press play in Ardour, Hydrogen follows automatically.

### Step 3 — Install the ForzeeStereo Drumkit

1. Go to **Instruments → Import Library** (or **File → Import Drumkit**)
2. Browse to your `ForzeeStereo.h2drumkit` file
3. Click **Import**
4. In the Sound Library panel, right-click **ForzeeStereo** and choose **Load**
5. You will see the ForzeeStereo instruments populate the Pattern Editor's instrument list

### Step 4 — Configure the Pattern Editor

- Set BPM to **80**
- Set grid resolution to **16th notes** (gives finest control)
- Each row of 16 cells = one bar at 16th note resolution
- Beat positions: Beat 1 = cell 1, Beat 2 = cell 5, Beat 3 = cell 9, Beat 4 = cell 13

## 5. Ardour Configuration

### Step 1 — Open/Create a Session

- Create a new session or open your existing Pixstars session
- Set session sample rate to match JackPilot (44100 or 48000 Hz)
- Set session BPM to **80**

### Step 2 — Switch Ardour to JACK Transport

1. Look at the **top-left transport bar** in Ardour
2. Click the sync button labelled **"Int"** — it should switch to **"JACK"** and turn green
3. If it doesn't appear, go to **Edit → Preferences → Transport** and enable JACK Transport
4. Ardour is now the **JACK Transport Master** — it controls the timeline

### Step 3 — Create a Stereo Audio Track for Drums

1. Go to **Track → Add Track**
2. Choose **Stereo Audio Track**
3. Name it `Drums - November Rain`
4. This track will receive Hydrogen's audio output

## 6. Connecting Everything via JackPilot Routing

Once Hydrogen and Ardour are both running and connected to JACK:

1. In JackPilot, click **Routing** to open the connections matrix
2. Make the following connections:

| From (Output) | To (Input) |
| --- | --- |
| hydrogen:out_L | Ardour drum track — Left input |
| hydrogen:out_R | Ardour drum track — Right input |

1. You should now see signal on the Ardour drum track meter when Hydrogen plays

### Verifying the Connection

- Press play in Hydrogen's standalone pattern mode
- Watch the meter on your Ardour drum track
- If it moves — you are connected correctly
- If not — re-check the routing matrix and ensure Hydrogen is set to JACK audio driver

## 7. Recording the Drum Track in Ardour

1. **Record-arm** the drum track in Ardour (click the red button on the track header)
2. Press **Record** in Ardour's transport, then **Play**
3. Hydrogen will start playing automatically in sync (JACK Transport slave)
4. Ardour captures the audio from Hydrogen in real time
5. When done, press **Stop**
6. You now have a recorded drum region in Ardour — treat it like any other audio

### Tips

- Record the full arrangement in one pass, or record section by section and edit in Ardour
- After recording, you can add compression, EQ, and reverb as plugins on the drum track
- If you change a pattern in Hydrogen later, you will need to re-record that section

## 8. November Rain — Song Details

| Detail | Value |
| --- | --- |
| Artist | Guns N' Roses |
| Album | Use Your Illusion I (1991) |
| Drummer | Matt Sorum |
| BPM | 80 |
| Time Signature | 4/4 throughout |
| Song Length | ~8 min 56 sec |
| Key | B Major |
| Difficulty | Intermediate |

### Character of the Drumming

November Rain is a nine-minute epic that evolves dramatically. Matt Sorum plays with tremendous **restraint** in the early sections and builds to a **thunderous finish**. The hallmark of his performance is dynamic control — from near-silence in the intro verses to full rock power in the guitar solo and outro. This dynamic journey must be reflected in the velocity settings for each pattern in Hydrogen.

## 9. Hydrogen Pattern Library

Build these as **separate named patterns** in Hydrogen's Pattern Editor, then arrange them in the Song Editor.

In the grid notation below:

- Each row has 16 cells representing 16th notes in one bar
- Cells are numbered 1–16
- Beat positions: **Beat 1 = 1, Beat 2 = 5, Beat 3 = 9, Beat 4 = 13**

### Pattern 1 — INTRO (No Drums)

**Bars:** 1–8**Description:** The song opens with Axl Rose on solo piano. No drums at all.**Action:** Create an **empty pattern** in Hydrogen. Leave all cells blank.

### Pattern 2 — VERSE (Sparse, Restrained)

**Description:** The signature understated ballad groove. Matt Sorum plays very lightly here — this is the most delicate part of the song.

| Instrument | Active Cells (16th note grid) | Notes |
| --- | --- | --- |
| Hi-Hat (closed) | 1, 3, 5, 7, 9, 11, 13, 15 | 8th notes, very light |
| Kick | 1, 9 | Beats 1 and 3 only |
| Snare | 5, 13 | Classic backbeat, beats 2 and 4 |

**Velocity:** Keep all hits at **60–70 out of 127** to match the delicate feel.**Usage:** Main verse sections throughout the song.

### Pattern 3 — PRE-CHORUS / BUILD

**Description:** Tension builds. The hi-hat stays consistent but the kick gets busier, pushing the energy forward into the chorus.

| Instrument | Active Cells | Notes |
| --- | --- | --- |
| Hi-Hat (closed) | 1, 3, 5, 7, 9, 11, 13, 15 | 8th notes, slightly more energy |
| Kick | 1, 3, 9, 11 | Adds an extra kick hit before each main beat |
| Snare | 5, 13 | Backbeat stays solid |
| Crash | 1 | On the downbeat when first entering this section |

**Velocity:** Medium — around **80–90 out of 127**.

### Pattern 4 — CHORUS (Full Rock Groove)

**Description:** The song opens up fully. Switch from hi-hat to **ride cymbal** — this is a characteristic Matt Sorum sound. Higher velocities throughout.

| Instrument | Active Cells | Notes |
| --- | --- | --- |
| Ride Cymbal | 1, 3, 5, 7, 9, 11, 13, 15 | Replace hi-hat with ride in chorus |
| Kick | 1, 7, 9, 15 | Syncopated, driving pattern |
| Snare | 5, 13 | Solid backbeat, push velocity up |
| Crash | 1 | First bar of each chorus entry |
| Hi-Hat (foot) | 5, 13 | Foot hi-hat on the backbeat — classic Matt Sorum touch |

**Velocity:** High — snare at **100–110**, kick at **90–100**, ride at **80–90 out of 127**.

### Pattern 5 — FILL (Bar Transition)

**Description:** A classic descending tom fill used to transition between sections. This pattern is typically just one bar long.

| Instrument | Active Cells | Notes |
| --- | --- | --- |
| Kick | 1 | Anchors the bar |
| Snare | 5 | First half backbeat |
| Hi Tom | 9, 10 | Beginning of the descending fill |
| Mid Tom | 11, 12 | Middle of the fill |
| Floor Tom | 13, 14, 15 | Bottom of the fill, driving into the crash |
| Crash | 16 | Anticipates the downbeat of the next bar |

**Velocity:** Build across the toms — Hi Tom ~80, Mid Tom ~90, Floor Tom ~100, Crash ~120.

### Pattern 6 — GUITAR SOLO SECTION (Full Intensity)

**Description:** The electric guitar solo section. Drums are at full power. Ghost notes on the snare add a live, human feel.

| Instrument | Active Cells | Notes |
| --- | --- | --- |
| Hi-Hat | 1, 3, 5, 7, 9, 11, 13, 15 | 8th notes, strong |
| Kick | 1, 3, 7, 9, 13 | Busy, near 8th-note kick feel |
| Snare (main) | 5, 13 | Backbeat, full velocity |
| Snare (ghost) | 7, 11 | Ghost notes — set velocity very low (~35–45) |
| Crash | 1 | Every 2 bars |

**Velocity:** Maximum energy — snare backbeat at **115–120**, kick at **100–110 out of 127**.

### Pattern 7 — OUTRO / BIG ENDING

**Description:** The orchestral finale. Drums become massive and ceremonial. Simple but extremely powerful.

| Instrument | Active Cells | Notes |
| --- | --- | --- |
| Crash | 1, 9 | Every half bar — big, open crashes |
| Kick | 1, 5, 9, 13 | Four on the floor — every beat |
| Snare | 5, 13 | Heavy, maximum velocity |
| Floor Tom | 15 | Anticipation hit into the next bar |

**Velocity:** Maximum — snare at **120–127**, kick at **110–120 out of 127**.

## 10. Song Editor Arrangement

In Hydrogen's **Song Editor**, arrange the patterns in this sequence. Each unit is one bar at 80 BPM.

```
Bars   1–  8  →  Pattern 1  (empty — piano intro, no drums)
Bars   9– 16  →  Pattern 2  (verse — sparse groove)
Bars  17– 20  →  Pattern 3  (pre-chorus — build)
Bars  21– 28  →  Pattern 4  (chorus — full rock)
Bar   29       →  Pattern 5  (fill — descending toms)
Bars  30– 36  →  Pattern 2  (verse again — back to sparse)
Bars  37– 40  →  Pattern 3  (pre-chorus — build)
Bars  41– 48  →  Pattern 4  (chorus — full rock)
Bar   49       →  Pattern 5  (fill — descending toms)
Bars  50– 66  →  Pattern 6  (guitar solo — full intensity)
Bars  67– 72  →  Pattern 7  (outro — big ending)
```

> Note: These bar numbers are approximate based on the song structure. Listen to the original recording and adjust the arrangement to taste. The song is nearly 9 minutes long — some sections may be extended or repeated more than shown above.

## 11. ForzeeStereo Drumkit Notes

The **ForzeeStereo.h2drumkit** is a stereo drum sample kit. Key things to know:

- Verify it contains a **ride cymbal** instrument — this is essential for the chorus pattern (Pattern 4). If it only has hi-hat, you may need to re-map one of the cymbal instruments to act as the ride.
- Check the **tom layout** (Hi Tom, Mid Tom, Floor Tom) before programming Pattern 5 (the descending fill).
- The kit outputs a **stereo mix** — Hydrogen's `out_L` and `out_R` carry the full stereo signal.
- Use **velocity layers** if the kit supports them — this is what makes the dynamics feel realistic.

### Velocity Strategy Summary

| Section | Recommended Velocity Range |
| --- | --- |
| Intro | No drums |
| Verse | 60–70 |
| Pre-Chorus | 80–90 |
| Chorus | 90–110 |
| Fills | 80–120 (building) |
| Guitar Solo | 100–120 |
| Outro | 110–127 |

## 12. Troubleshooting

| Problem | Likely Cause | Fix |
| --- | --- | --- |
| Hydrogen has no sound | JACK not running when Hydrogen opened | Restart Hydrogen with JackPilot already running |
| Ardour says "Int", won't switch to "JACK" | Ardour opened before JACK | Restart Ardour with JACK already running |
| No signal on Ardour drum track | Routing not connected | Re-check Routing matrix in JackPilot |
| Playback is out of sync | Hydrogen JACK transport slave not active | Click the JACK transport button in Hydrogen's toolbar |
| Drumkit sounds are missing | ForzeeStereo not loaded | Right-click kit in Sound Library → Load |
| Xruns / audio glitches | Buffer size too small | Increase buffer size in JackPilot preferences |
| Hydrogen crashes on open | JACK driver conflict | Set Hydrogen audio driver to JACK in preferences before opening |

## 13. Startup Checklist

Follow this exact order every session — deviating from it causes connection problems.

- [ ] **1. Start JackPilot** — click Start, verify sample rate
- [ ] **2. Open Hydrogen** — confirm it connects to JACK (check Audio System tab)
- [ ] **3. Load ForzeeStereo kit** in Hydrogen
- [ ] **4. Enable JACK Transport slave** button in Hydrogen
- [ ] **5. Open Ardour** — confirm it connects to JACK
- [ ] **6. Switch Ardour transport from "Int" to "JACK"**
- [ ] **7. Open JackPilot Routing** — connect `hydrogen:out_L/R` to Ardour drum track inputs
- [ ] **8. Verify signal** — play a test hit in Hydrogen, check Ardour meter responds
- [ ] **9. Record-arm** the Ardour drum track
- [ ] **10. Press Record + Play in Ardour** — Hydrogen follows automatically

## 14. Open Items & Next Steps

- [ ] Verify ForzeeStereo kit has ride cymbal mapped correctly
- [ ] Check tom mapping (Hi/Mid/Floor) in ForzeeStereo for Pattern 5 fill
- [ ] Fine-tune bar counts in Song Editor against the original recording
- [ ] Set velocity levels per pattern and test against original
- [ ] Record full drum arrangement into Ardour
- [ ] Add EQ and compression on the Ardour drum track
- [ ] Layer drum track with other instruments (guitar, bass, piano, strings)
- [ ] Mix and export final session

*Document maintained alongside the Pixstars project. Update as the build progresses.*