# PIXSTARS Architecture

> Master architecture documentation for the PIXSTARS AI-powered animatronic lamp performance platform.

---

## Status

We are going full-out on local AI.

The PIXSTARS lamp is no longer just a remotely controlled stage prop. It is designed as a distributed AI character with local perception, local voice, local inference, emotional state, and backstage show orchestration.

---

## Design Philosophy

> "The lamp is a character, not a prop."

The audience should experience a living stage partner with:

- attention
- emotion
- curiosity
- memory
- timing
- voice
- movement
- visual awareness

The technical architecture exists to support that illusion.

---

## Core Mental Model

| Component | Physical Location | Role |
|---|---|---|
| Apple Mac Mini M4 Pro | Backstage | Director |
| Seeed Studio reComputer RK3588-40 | Lamp base | AI Brain |
| PCIe AI Accelerator | Lamp base / expansion slot | Vision & inference coprocessor |
| Raspberry Pi Zero 2 WH | Lamp head | Nervous System |
| Camera | Lamp head | Eyes |
| Microphone | Lamp head | Ears |
| Speaker | Lamp head | Voice |
| WS2812 RGB LED ring | Lamp head / lampshade | Emotions |
| Servos | Neck / head / shoulder | Muscles |

---

## High-Level System Architecture

```text
                              AUDIENCE
                                  │
                                  ▼

                         ┌────────────────┐
                         │ PIXSTARS LAMP  │
                         │ AI CHARACTER   │
                         └───────┬────────┘
                                 │
                       WiFi / MQTT / HiveMind
                                 │
                                 ▼

┌────────────────────────────────────────────────────────────────┐
│                    APPLE MAC MINI M4 PRO                       │
│                          "DIRECTOR"                            │
│                                                                │
│  - Ardour timeline and music playback                          │
│  - HiveMind Server                                              │
│  - Home Assistant                                               │
│  - Projection control                                           │
│  - Lighting control                                             │
│  - Show control timeline                                        │
│  - Large AI / LLM services                                      │
│  - Logging and rehearsal tooling                                │
└────────────────────────────────────────────────────────────────┘
                                 │
                                 │ Ethernet / WiFi
                                 ▼

┌────────────────────────────────────────────────────────────────┐
│                 OPTIONAL BACKSTAGE AI VISION NODE              │
│                 RK3588 / AI Accelerator / Mac-side AI          │
│                                                                │
│  - Wide stage camera processing                                │
│  - Audience tracking                                            │
│  - Applause / attention analysis                                │
│  - Scene understanding                                          │
│  - Offloading heavy visual workloads                            │
└────────────────────────────────────────────────────────────────┘
```

---

## Internal Lamp Architecture

```text
                         LAMP HEAD
┌────────────────────────────────────────────────────────────────┐
│ Raspberry Pi Zero 2 WH                                         │
│ "NERVOUS SYSTEM"                                               │
│                                                                │
│ Connected locally to:                                          │
│  - USB microphone                                               │
│  - 40 mm speaker / audio output                                │
│  - WS2812 RGB LED ring                                          │
│  - camera                                                       │
│  - proximity / IR sensors                                       │
│  - ambient light sensor                                         │
│  - future servos                                                │
│  - physical buttons                                             │
└───────────────────────────────┬────────────────────────────────┘
                                │
                         USB / UART / MQTT
                                │
                       Through the lamp arm
                                │
                                ▼

                         LAMP BASE
┌────────────────────────────────────────────────────────────────┐
│ Seeed Studio reComputer RK3588-40                              │
│ "AI BRAIN"                                                     │
│                                                                │
│  - 16 GB RAM class system                                      │
│  - integrated NPU                                               │
│  - Linux / Docker                                               │
│  - OpenVoiceOS client services                                  │
│  - HiveMind client                                              │
│  - local speech processing                                      │
│  - local vision processing                                      │
│  - emotional state engine                                       │
│  - behaviour engine                                             │
│  - local memory / context store                                 │
└───────────────────────────────┬────────────────────────────────┘
                                │
                         PCIe expansion
                                │
                                ▼

┌────────────────────────────────────────────────────────────────┐
│ AI ACCELERATOR                                                  │
│ "VISION & INFERENCE COPROCESSOR"                               │
│                                                                │
│  - object detection                                             │
│  - face detection                                               │
│  - pose estimation                                              │
│  - gesture recognition                                          │
│  - visual attention                                             │
│  - multimodal perception                                        │
└────────────────────────────────────────────────────────────────┘
```

---

## Lamp Head

### Raspberry Pi Zero 2 WH

The Raspberry Pi Zero 2 WH is mounted inside the lamp head.

It sits close to the physical devices that make the lamp feel alive:

- microphone
- speaker
- LED ring
- camera
- sensors
- future servos

This keeps head wiring short and avoids running many delicate signal cables through the lamp arm.

### Purpose

The Raspberry Pi acts as the lamp's nervous system.

It is responsible for direct hardware interaction:

- microphone interface
- speaker interface
- LED ring control
- sensor collection
- servo control
- physical button handling
- diagnostics
- health monitoring
- heartbeat reporting

It should not be responsible for heavy AI workloads.

### Why the Pi stays in the head

The Pi is useful because the head is where most expressive hardware lives. It can react quickly to local events and keep low-level hardware behaviour stable even when the AI brain is busy.

Examples:

- keep LED breathing animation alive
- report microphone status
- detect button presses
- monitor sensor state
- drive future head/neck servos
- expose a simple hardware API to the RK3588 brain

---

## Lamp Base

### Seeed Studio reComputer RK3588-40

The reComputer RK3588-40 is mounted inside the lamp base.

The base provides:

- more physical room
- better cooling
- safer power distribution
- easier maintenance access
- space for PCIe expansion
- cable routing to the head

### Purpose

The RK3588-40 is the lamp's AI brain.

It is responsible for:

- OpenVoiceOS
- HiveMind client
- speech-to-text
- text-to-speech
- wake-word logic
- local LLM experiments
- local memory
- emotional state engine
- behaviour selection
- face tracking
- gesture recognition
- object detection
- attention management
- autonomous reactions

The RK3588-40 allows the lamp to remain intelligent even when temporarily disconnected from the backstage Mac Mini.

---

## AI Accelerator

### Purpose

The AI accelerator is reserved for high-throughput perception and inference.

It should be treated as the lamp's visual and multimodal coprocessor.

Responsibilities:

- object detection
- person detection
- face detection
- pose estimation
- gesture recognition
- visual attention
- scene understanding
- multi-model inference
- future multimodal AI experiments

### Why include it now

PIXSTARS is intended to grow from a talking lamp into an audience-aware AI character.

The PCIe accelerator path keeps the architecture future-proof. Instead of redesigning the lamp later, the base already reserves space, cooling, and power for an AI expansion module.

### Suggested workload split

| Workload | Preferred Device |
|---|---|
| LED animations | Raspberry Pi Zero 2 WH |
| Sensor polling | Raspberry Pi Zero 2 WH |
| Servo control | Raspberry Pi Zero 2 WH |
| Speech-to-text | RK3588-40 |
| Text-to-speech | RK3588-40 |
| Wake-word logic | RK3588-40 / Pi depending on latency |
| Emotional state | RK3588-40 |
| Behaviour selection | RK3588-40 |
| Face detection | AI accelerator |
| Pose estimation | AI accelerator |
| Gesture recognition | AI accelerator |
| Object detection | AI accelerator |
| Large show-level AI | Mac Mini M4 Pro |

---

## Backstage Director

### Apple Mac Mini M4 Pro

The Mac Mini is the director of the show.

It is responsible for:

- Ardour session playback
- November Rain timeline
- dialogue and sound effects
- projection cues
- lighting cues
- show timeline
- Home Assistant automations
- HiveMind Server
- OpenVoiceOS server-side services
- larger AI models
- rehearsal tooling
- logging
- fallback control

The Mac Mini owns the show.  
The lamp owns its character.

---

## Software Components

### OpenVoiceOS

Used for:

- wake words
- voice assistant behaviour
- skills
- voice interaction framework

### HiveMind

Used for:

- distributed intelligence
- communication between Mac Mini and lamp
- multi-agent orchestration
- remote skill execution

### Home Assistant

Used for:

- automations
- lighting state
- device state
- event triggers
- integration glue

### Ardour

Used for:

- November Rain playback
- piano and drum rendering
- dialogue playback
- sound effects
- timing backbone

Detailed audio setup lives in:

```text
docs/audio/AUDIO_SETUP.md
```

### Docker

Used where possible for:

- repeatable deployment
- isolated services
- easy recovery
- reproducible development

---

## Communication Architecture

### Director to Brain

Between Mac Mini and RK3588-40:

- HiveMind
- MQTT
- WebSocket
- REST
- OSC where useful for show control

### Brain to Nervous System

Between RK3588-40 and Raspberry Pi Zero 2 WH:

- USB
- UART
- MQTT
- lightweight local REST API

The final transport can be selected during hardware integration.

### Nervous System to Hardware

Between Raspberry Pi and physical hardware:

- GPIO
- PWM
- I2C
- UART
- USB
- audio output

---

## Power Architecture

Power should be distributed from the lamp base.

```text
AC power
   │
   ▼
Power supply in lamp base
   │
   ├── RK3588-40
   ├── AI accelerator
   ├── Raspberry Pi Zero 2 WH
   ├── LED ring
   ├── audio amplifier / speaker
   ├── sensors
   └── future servos
```

The base should include room for:

- 5V rail
- 12V rail if servos or lighting require it
- fuse protection
- cable strain relief
- service disconnects
- cooling airflow

---

## AI Behaviour Layers

The lamp behaviour should be layered.

```text
Physical Layer
  LEDs, speaker, microphone, camera, servos

Reflex Layer
  fast local responses, heartbeat, sensor reactions

Perception Layer
  speech, vision, gesture, face, pose

Emotion Layer
  mood, confidence, fear, curiosity, pride

Character Layer
  personality, memory, timing, intent

Show Layer
  scene cues, music sync, projection sync, scripted beats
```

This layered model prevents the lamp from becoming a fragile one-piece script.

---

## Example Interaction Flow

```text
Performer says: "Hey A.I."
        │
        ▼
Microphone in lamp head captures audio
        │
        ▼
Raspberry Pi forwards audio stream/state
        │
        ▼
RK3588-40 performs wake-word and speech handling
        │
        ▼
AI accelerator checks visual context
        │
        ▼
RK3588-40 selects emotional response
        │
        ▼
Pi drives LED ring and speaker output
        │
        ▼
Mac Mini receives state update for show timeline
```

---

## Failure Modes and Fallbacks

### If Mac Mini connection drops

The lamp should still be able to:

- breathe with LEDs
- respond with local idle behaviour
- show status
- keep basic personality alive

### If RK3588-40 fails

The Pi should still be able to:

- show emergency LED state
- stop servos safely
- report heartbeat failure if possible

### If Pi fails

The RK3588-40 should:

- detect missing heartbeat
- notify Mac Mini
- disable dependent behaviours

### If AI accelerator is unavailable

The RK3588-40 should fall back to:

- simpler vision models
- reduced frame rate
- scripted behaviour
- Mac Mini assistance

---

## Future AI Capabilities

Planned or possible future expansions:

- OpenHuman-based personality memory
- persistent character history
- performer recognition
- audience attention tracking
- gesture-driven interaction
- emotional growth
- local visual question answering
- scene understanding
- autonomous improvisation
- rehearsal learning
- show analytics

---

## Repository Structure

Recommended documentation structure:

```text
docs/
├── architecture/
│   └── ARCHITECTURE.md
├── audio/
│   └── AUDIO_SETUP.md
├── hardware/
│   ├── LAMP_HEAD.md
│   ├── LAMP_BASE.md
│   └── POWER.md
├── software/
│   ├── OPENVOICEOS.md
│   ├── HIVEMIND.md
│   ├── HOME_ASSISTANT.md
│   └── DOCKER.md
└── show-control/
    ├── ARDOUR.md
    ├── TIMELINE.md
    └── CUES.md
```

---

## Final Principle

The architecture should never be optimized only for technical elegance.

It should be optimized for theatrical illusion.

When the audience looks at the stage, they should not see:

- a computer
- an AI model
- a GPIO pin
- a camera
- a speaker

They should see:

> A living lamp with a soul.
