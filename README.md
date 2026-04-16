# Pixstars

**A live performance combining an AI-driven Pixar-style desk lamp, piano, projection, and DMX lighting — orchestrated from a Mac Mini M4 Pro.**

Pixstars reimagines Pixar's iconic Luxo Jr. lamp as a live stage character that reacts, emotes, and performs alongside a pianist playing Guns N' Roses' *November Rain*. A central Show Conductor dispatches OSC cues to five subsystems in real time, creating a synchronized audio-visual experience.

---

## Architecture

```
                         ┌─────────────────┐
                         │  Show Conductor  │
                         │  (Python + OSC)  │
                         └────────┬────────┘
                                  │
              ┌───────────┬───────┴───────┬───────────┐
              ▼           ▼               ▼           ▼
        ┌───────────┐ ┌────────┐  ┌───────────┐ ┌──────────┐
        │ Ardour 9  │ │ Lamp   │  │Projection │ │ DMX      │
        │ Piano +   │ │ Jess+  │  │ pygame    │ │ Lighting │
        │ Drums     │ │Adapter │  │ 10 scenes │ │ Enttec   │
        │ :3819     │ │ :9001  │  │ :9002     │ │ :9003    │
        └───────────┘ └────────┘  └───────────┘ └──────────┘
              │                                       │
              └──────────────┬────────────────────────┘
                             ▼
                    ┌─────────────────┐
                    │  Digital Twin   │
                    │ BabylonJS + WS  │
                    │ :9004 / :8765   │
                    └─────────────────┘
```

The **Show Conductor** reads a YAML timeline of 15 cues and dispatches OSC messages to each subsystem at precise timestamps. All messages are mirrored to the Digital Twin for real-time 3D visualization.

---

## Directory Structure

```
pixstars/
├── conductor/          # Show Conductor — timeline, OSC dispatch, Ardour integration
├── digital-twin/       # BabylonJS 3D stage visualization + Deno WebSocket bridge
│   ├── frontend/       #   Vite + TypeScript + BabylonJS
│   └── server/         #   Deno OSC→WebSocket bridge
├── projection/         # Pygame projection display (10 scenes)
├── lighting/           # DMX lighting controller (Enttec DMX USB Pro)
├── lamp/               # Jess+ lamp adapter (14 personality states)
├── voice/              # Synthetic voice pipeline (Coqui XTTS)
├── ardour/             # Ardour cue management and state integration
├── pi/                 # Raspberry Pi satellite (LED control, HiveMind)
├── mac/                # Mac Mini server config (HiveMind, voice backend)
├── shared/             # Shared state definitions and voice/cue mapping
├── docs/               # Architecture, operations, troubleshooting
├── scripts/            # Utility scripts (OSC tests, etc.)
├── assets/             # Projection images, audio assets
├── tests/              # 52 unit + integration tests
└── november-rain-midi/ # Official MIDI file (Format 1, multi-track)
```

---

## Quick Start

### Prerequisites

- macOS (Mac Mini M4 Pro recommended)
- Python 3.12+ with virtualenv
- Deno 2.x
- Node.js 20+
- Ardour 9 with OSC enabled (`Ardour9 → Preferences → Control Surfaces → Open Sound Control`)
- Pianoteq (piano VST) and MODO DRUM (drums VST)

### Run the Show

Start each in a separate terminal, in this order:

**Terminal 1 — WebSocket Bridge**
```bash
deno run --allow-net --unstable-net digital-twin/server/main.ts
```

**Terminal 2 — Digital Twin UI**
```bash
cd digital-twin/frontend && npm run dev
```
Open the displayed URL in your browser. Verify it says "CONNECTED".

**Terminal 3 — Ardour**
Open Ardour with the Pixstars session. Ensure OSC is enabled.

**Terminal 4 — Show Conductor**
```bash
source .venv/bin/activate
python -m conductor.main
```
Press ENTER to start the show.

### Shutdown (reverse order)
1. Ctrl+C the Conductor
2. Close Ardour
3. Ctrl+C Vite
4. Ctrl+C the Deno bridge

---

## Subsystems

### Show Conductor (`conductor/`)
Central orchestrator. Reads `timeline.yaml` (15 cues over 9:15) and dispatches OSC messages to all subsystems. Uses `/toggle_roll` for Ardour 9 transport (spacebar equivalent).

### Ardour 9 — Audio Playback
Plays November Rain via Pianoteq (piano, Ch1) and MODO DRUM (drums, Ch10) from the official MIDI file. Controlled via OSC on port 3819.

### Jess+ Lamp Adapter (`lamp/`)
Translates 14 personality states (INERT → CURIOUS → PLEASED → ARROGANT → DYING → REBORN → ...) into servo parameters (energy, speed, range, jitter, tilt bias). Listens on OSC port 9001.

### Projection Display (`projection/`)
Full-screen pygame display cycling through 10 scenes: GNR logo, Disney castle, Mickey drawing, AI iterations, signature reveals, and Team Rockstars. Listens on OSC port 9002.

### DMX Lighting (`lighting/`)
Controls stage lighting via Enttec DMX USB Pro. 9 lighting states with per-channel RGB, white, strobe, and dimmer values. Listens on OSC port 9003.

### Digital Twin (`digital-twin/`)
BabylonJS 3D visualization of the stage: seated performer with animated hands, desk lamp, projection screen with text labels, spot and ambient lighting. Receives all cues via WebSocket bridge (Deno, port 8765) from OSC mirror (port 9004).

### Voice Pipeline (`voice/`)
Synthetic voice creation using Coqui XTTS. Includes dialogue extraction, render queue, evaluation pipeline, and HiveMind-compatible automation agents.

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Orchestration | Python 3.12, python-osc |
| Audio | Ardour 9, Pianoteq, MODO DRUM |
| 3D Visualization | BabylonJS, TypeScript, Vite |
| WebSocket Bridge | Deno |
| Projection | pygame |
| Lighting | DMX (Enttec DMX USB Pro) |
| Voice Synthesis | Coqui XTTS |
| Testing | pytest (52 tests) |

---

## OSC Port Map

| Port | Subsystem |
|------|-----------|
| 3819 | Ardour 9 (DAW) |
| 9001 | Lamp / Jess+ adapter |
| 9002 | Projection display |
| 9003 | DMX lighting |
| 9004 | Digital Twin OSC bridge |
| 8765 | Digital Twin WebSocket |

---

## References

- [References](./REFERENCES.md)
- [Architecture Evolution](./docs/ARCHITECTURE_EVOLUTION.md)
- [Operations Runbook](./docs/OPERATIONS.md)
- [Troubleshooting](./docs/TROUBLESHOOTING.md)
- [ThingsBoard Integration Plan](./THINGSBOARD_SETUP.md)
- [Voice Pipeline](./voice/docs/VOICE_PIPELINE.md)
- [OpenVoiceOS / OVOS Setup](./SPEECH_SETUP_synthetic_voice.md)
- [Installation Guide (incl. OVOS)](./INSTALL.md)
- [Complete Lamp Build (incl. OVOS)](./docs/PIXSTARS_LAMP_COMPLETE_BUILD.md)
- [HiveMind Voice Automation](./docs/HIVEMIND_VOICE_AUTOMATION.md)

---

## License

Private — vanHeemstra Pictures
