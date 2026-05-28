# docs/architecture/ARCHITECTURE.md

# PIXSTARS Architecture

> Master architecture documentation for the PIXSTARS AI-powered animatronic lamp performance platform.

---

# Design Philosophy

PIXSTARS follows a simple principle:

> "The lamp is a character, not a prop."

The audience should perceive:

* intelligence
* emotion
* curiosity
* personality

rather than seeing individual technical components.

---

# System Architecture

PIXSTARS is built using a distributed architecture.

```text
                    AUDIENCE
                         │
                         ▼

                ┌────────────────┐
                │ PIXSTARS LAMP  │
                │   Character    │
                └───────┬────────┘
                        │
             HiveMind / MQTT / WiFi
                        │
                        ▼

┌───────────────────────────────────────────────┐
│          APPLE MAC MINI M4 PRO                │
│                "DIRECTOR"                     │
│                                               │
│ Ardour                                        │
│ HiveMind Server                               │
│ Home Assistant                                │
│ Projection Control                            │
│ Lighting Control                              │
│ Show Timeline Engine                          │
│ Voice Services                                │
└───────────────────────────────────────────────┘
                        │
                        │
                        ▼

┌───────────────────────────────────────────────┐
│        OPTIONAL RK3576 VISION NODE            │
│                                               │
│ Audience Tracking                             │
│ YOLO Recognition                              │
│ Scene Understanding                           │
│ Visual Analytics                              │
└───────────────────────────────────────────────┘
```

---

# Internal Lamp Architecture

The lamp itself contains two independent computing systems.

```text
                 Mac Mini M4 Pro
                     Director
                         │
                HiveMind / MQTT
                         │
                         ▼

           ┌───────────────────────┐
           │ RK3576 AI COMPUTER    │
           │       (BASE)          │
           │       BRAIN           │
           └───────────┬───────────┘
                       │
             USB / UART / MQTT
                       │
                       ▼

           ┌───────────────────────┐
           │ Raspberry Pi Zero 2 WH│
           │       (HEAD)          │
           │   NERVOUS SYSTEM      │
           └──────┬─────┬─────┬────┘
                  │     │     │
                  ▼     ▼     ▼

            Microphone LEDs Speaker

                  │
                  ▼

                Camera
```

---

# Lamp Head

## Raspberry Pi Zero 2 WH

### Physical Location

Mounted inside the lamp head.

Located near:

* microphone
* speaker
* LED ring
* camera
* sensors
* future servos

This minimizes cable runs through the lamp arm.

---

## Purpose

The Raspberry Pi Zero 2 WH acts as the hardware controller.

Responsibilities:

* microphone management
* speaker management
* LED ring control
* sensor collection
* servo control
* diagnostics
* heartbeat monitoring

The Pi handles physical devices but not heavy AI workloads.

---

## Connected Hardware

### Microphone

Used for:

* performer interaction
* audience interaction
* wake-word detection

### Speaker

Used for:

* character voice
* dialogue
* sound effects

### WS2812 RGB LED Ring

Mounted inside the lampshade.

Used for:

* emotional state display
* speech visualization
* AI activity indication
* diagnostics

### Camera

Used for:

* face detection
* performer tracking
* gesture recognition

### Future Servos

Potential locations:

* neck
* shoulder
* head assembly

Used for expressive movement.

---

# Lamp Base

## Seeed Studio reComputer RK3576

### Physical Location

Mounted inside the lamp base.

The base provides:

* cooling capacity
* power distribution
* maintenance access
* expansion space

---

## Purpose

The RK3576 acts as the lamp's AI brain.

Responsibilities:

* OpenVoiceOS
* HiveMind Client
* speech recognition
* speech synthesis
* computer vision
* face tracking
* gesture recognition
* emotional state engine
* autonomous behaviour
* local AI inference

The lamp can continue functioning even if temporarily disconnected from the backstage network.

---

# Backstage Director

## Apple Mac Mini M4 Pro

The Mac Mini acts as the master controller.

Responsibilities:

* Ardour
* Home Assistant
* HiveMind Server
* Projection Control
* Lighting Control
* Camera Routing
* Show Timeline
* Audio Playback
* AI Orchestration

The Mac Mini is effectively the director of the performance.

---

# Software Components

## OpenVoiceOS

Provides:

* wake words
* speech recognition
* speech synthesis integration
* skills framework

---

## HiveMind

Provides:

* distributed intelligence
* inter-device communication
* agent orchestration

---

## Home Assistant

Provides:

* automation
* event handling
* lighting integration
* state management

---

## Ardour

Provides:

* November Rain playback
* dialogue playback
* sound effects
* synchronized show timing

See:

`docs/audio/AUDIO_SETUP.md`

---

# Communication Architecture

## Director ↔ Brain

Protocols:

* HiveMind
* MQTT
* WebSocket
* REST

---

## Brain ↔ Nervous System

Protocols:

* USB
* UART
* MQTT

Final implementation to be selected during hardware integration.

---

# Future Expansion

## OpenHuman

Potential capabilities:

* persistent memory
* emotional growth
* long-term learning
* character development

---

## Advanced Vision

Potential capabilities:

* audience engagement scoring
* applause detection
* audience sentiment analysis
* performer recognition

---

# Mental Model

| Component              | Role           |
| ---------------------- | -------------- |
| Mac Mini M4 Pro        | Director       |
| RK3576                 | Brain          |
| Raspberry Pi Zero 2 WH | Nervous System |
| Camera                 | Eyes           |
| Microphone             | Ears           |
| Speaker                | Voice          |
| LED Ring               | Emotions       |
| Servos                 | Muscles        |

This model should guide future hardware and software decisions.


LAMP HEAD
│
├─ Camera
├─ USB Microphone
├─ 40mm Speaker
├─ WS2812 LED Ring
├─ Future Servos
│
└─ Raspberry Pi Zero 2 WH
      (Nervous System)

           │
           │ Through Lamp Arm
           │

LAMP BASE
│
├─ RK3576
│    (Brain)
│
├─ Power Distribution
├─ USB Audio Interfaces
├─ Future Expansion
└─ HiveMind Client

           │ WiFi / MQTT

BACKSTAGE
│
├─ Mac Mini M4 Pro
│    (Director)
│
├─ Ardour
├─ Home Assistant
├─ HiveMind Server
├─ Projection Control
├─ Lighting Control
└─ Show Timeline

           │

OPTIONAL
│
└─ RK3576 Vision Node
     Audience Tracking
     YOLO Recognition
     Analytics
