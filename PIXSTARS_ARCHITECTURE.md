# PIXSTARS_ARCHITECTURE.md

# PIXSTARS Architecture

> Master architecture documentation for the PIXSTARS performance platform.

---

# Vision

PIXSTARS is an AI-powered theatrical performance platform that combines:

* Animatronics
* Artificial Intelligence
* Voice Interaction
* Computer Vision
* Show Control
* Lighting
* Projection Mapping
* Music Playback
* Character Performance

The goal is to create the illusion that the lamp is a living character rather than a piece of stage equipment.

---

# Design Philosophy

> "The lamp is a character, not a prop."

Every architectural decision should support:

* personality
* emotion
* responsiveness
* audience engagement
* autonomy

---

# System Overview

PIXSTARS consists of four major layers:

1. Backstage Director
2. Lamp Intelligence
3. Vision & Audience Systems
4. Show Infrastructure

```text
Audience
    │
    ▼

┌──────────────────────────────┐
│      PIXSTARS LAMP           │
│     AI Character Layer       │
└──────────────┬───────────────┘
               │
      HiveMind / MQTT / WiFi
               │
               ▼

┌──────────────────────────────┐
│    APPLE MAC MINI M4 PRO     │
│      Backstage Director      │
└──────────────┬───────────────┘
               │
       Ethernet / WiFi
               │
               ▼

┌──────────────────────────────┐
│ RK3576 AI EDGE NODE OPTIONAL │
│     Vision Processing        │
└──────────────────────────────┘
```

---

# Backstage Director

## Apple Mac Mini M4 Pro

The Mac Mini is the central control point of the entire show.

Responsibilities:

* Ardour
* HiveMind Server
* Home Assistant
* Projection Control
* Lighting Control
* Show Timeline
* Voice Services
* AI Orchestration
* Camera Management

The Mac Mini acts as the "director" of the performance.

---

# Lamp Intelligence

## Seeed Studio reComputer RK3576

Installed inside the lamp base.

Responsibilities:

* Wake Word Detection
* Speech Recognition
* Speech Synthesis
* Vision Processing
* Face Tracking
* Gesture Recognition
* Emotional State Engine
* Autonomous Behaviour

The RK3576 allows the lamp to remain intelligent even when disconnected from the backstage network.

---

# Optional Edge AI Node

## Secondary RK3576

A second RK3576 may be installed backstage.

Responsibilities:

* Audience Tracking
* Multi-Camera Processing
* Emotion Detection
* YOLO Object Recognition
* Scene Understanding
* Visual Analytics

Benefits:

* Keeps heavy AI workloads away from the lamp.
* Improves responsiveness.
* Allows future expansion.

---

# Lamp Hardware

## Inputs

### Microphone

Used for:

* audience interaction
* performer interaction
* wake words

### Camera

Used for:

* face tracking
* gesture recognition
* performer recognition

### Proximity Sensors

Used for:

* awareness
* reactions
* interaction triggers

### Ambient Light Sensor

Used for adaptive brightness.

### Maintenance Buttons

Used for:

* diagnostics
* emergency override

---

## Outputs

### Speaker

Provides:

* voice
* sound effects
* AI responses

### Main Lamp Bulb

Used for:

* storytelling
* mood indication

### RGB LED Ring

Located inside the lampshade.

Used as:

* AI brain visualization
* emotional state indicator
* speech visualization
* system status feedback

### Servo Motors

Future capability:

* head tilt
* head rotation
* expressive movement

---

# Cameras

## Lamp Camera

Mounted inside the lamp.

Used for:

* local awareness
* face tracking
* performer recognition

## Stage Cameras

Used for:

* audience viewing
* projection screens
* monitoring

## Audience Camera

Used for:

* audience analysis
* applause detection
* engagement metrics

---

# Software Components

## OpenVoiceOS

Provides:

* wake words
* speech recognition
* skills
* speech synthesis integration

---

## HiveMind

Provides:

* distributed intelligence
* inter-device communication
* multi-agent orchestration

---

## Home Assistant

Provides:

* automation
* state management
* lighting coordination
* event orchestration

---

## Ardour

Provides:

* music playback
* synchronized audio
* dialogue playback
* sound effects

Detailed setup:

See:

docs/audio/AUDIO_SETUP.md

---

# Communication Architecture

## Network Protocols

Used between systems:

* MQTT
* HiveMind
* WebSocket
* REST API

---

## Local Lamp Connections

Interfaces:

* GPIO
* I2C
* UART
* USB
* PWM

Connected devices:

* LEDs
* Sensors
* Servos
* Audio hardware

---

# Audio Architecture

The November Rain soundtrack and supporting audio are rendered using:

* Pianoteq
* MODO DRUM
* Ardour

Detailed documentation:

docs/audio/AUDIO_SETUP.md

---

# Future Integrations

## OpenHuman

Potential capabilities:

* persistent memory
* long-term character development
* emotional growth
* contextual learning

---

## MIA Desktop Assistant Components

Potential capabilities:

* multimodal interaction
* gesture control
* vision-driven behaviour
* conversational enhancement

---

# Future Lamp Capabilities

Planned enhancements:

* head movement
* performer tracking
* audience awareness
* emotional animation
* autonomous conversation
* scene understanding

---

# Guiding Principle

The audience should never experience:

* a Raspberry Pi
* an AI model
* a microphone
* a camera

The audience should experience:

"A living lamp with personality."
