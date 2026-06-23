# LEARN_ROBOTICS_PROGRAMMING_SETUP.md

Version: 1.0
Status: Implementation Guide
Project: PixStars

---

# 1. Purpose

This document maps the concepts from:

Learn Robotics Programming
(Danny Staple)

to the PixStars implementation.

The goal is not to reproduce the robot from the book.

The goal is to apply relevant robotics concepts to create a believable AI-powered animatronic lamp character.

---

# 2. PixStars Robotics Architecture

```text
                      PixStars Kernel

                              MQTT

 ┌─────────────────────────────────────────────┐
 │                                             │
 │ Voice Service                               │
 │ Vision Service                              │
 │ Motion Service                              │
 │ Projection Service                          │
 │ Timeline Service                            │
 │ Home Assistant Service                      │
 │ HiveMind Service                            │
 │ Mission Control Service                     │
 │ Ardour Service                              │
 │                                             │
 └─────────────────────────────────────────────┘
```

---

# 3. Chapter-to-PixStars Mapping

## Raspberry Pi Setup

Book Topic

- Raspberry Pi Installation

PixStars Usage

- Pi Zero 2 WH
- Lamp Head Controller

Deliverables

- Raspberry Pi OS
- SSH
- WiFi
- Remote Updates

Priority

HIGH

---

## Python Robotics

Book Topic

- Python Robot Control

PixStars Usage

- Character Logic
- Motion Control
- Device Integration

Deliverables

```python
LampStateMachine
VoiceController
MotionController
ProjectionController
```

Priority

HIGH

---

## MQTT

Book Topic

- Messaging Architecture

PixStars Usage

Primary communication layer.

Deliverables

Topics:

```text
pixstars/voice
pixstars/vision
pixstars/motion
pixstars/projection
pixstars/emotion
pixstars/timeline
pixstars/mission-control
```

Priority

VERY HIGH

---

## Vision

Book Topic

- OpenCV

PixStars Usage

Camera in lamp head.

Deliverables

Phase 1

- Face detection

Phase 2

- Performer tracking

Phase 3

- Audience awareness

Priority

MEDIUM

---

## Speech Recognition

Book Topic

- Vosk

PixStars Usage

Wake Word

```text
Hey A.I.
```

Deliverables

- Voice Commands
- Rehearsal Commands

Priority

HIGH

---

## Speech Synthesis

Book Topic

- Piper

PixStars Usage

E.T.-style lamp voice.

Deliverables

- Voice Generation
- Character Personality

Priority

HIGH

---

## Artificial Intelligence

Book Topic

- Local AI

PixStars Usage

Character intelligence.

Deliverables

- Conversation
- Reactions
- Improvisation

Priority

MEDIUM

---

# 4. Robotics State Machine

Recommended implementation:

```text
OFF

 ↓

BOOTING

 ↓

IDLE

 ↓

LISTENING

 ↓

THINKING

 ↓

SPEAKING

 ↓

IDLE
```

Additional states:

```text
CURIOUS
EXCITED
ANGRY
SAD
CONFUSED
```

These states drive:

- LEDs
- Voice
- Projection
- Motion

---

# 5. Motion System

Current Stage

Timeline-driven.

Future Stage

Hybrid.

```text
Timeline

+

Autonomous Reactions
```

Examples:

Audience laughs

↓

Lamp looks audience direction

↓

Returns to performance

---

# 6. Vision System

Hardware

- Camera inside lamp head

Phase 1

Face Detection

Phase 2

Performer Detection

Phase 3

Audience Interaction

Suggested Technology

- OpenCV

---

# 7. Voice System

Hardware

- USB Microphone
- Head Speaker
- Base Speaker

Software

- OpenVoiceOS
- HiveMind
- Piper

Workflow

```text
Wake Word

↓

Speech Recognition

↓

AI Processing

↓

Speech Synthesis

↓

Audio Output
```

---

# 8. Mission Control Integration

Mission Control should display:

- Current Scene
- Current Emotion
- Voice State
- Vision State
- MQTT Status
- Camera Feed
- Projection Status

This creates a robotics-style control center.

---

# 9. Future Extensions

## Snowy Owl

Future project.

Can reuse:

- MQTT
- Vision
- Voice
- Motion
- Mission Control

---

## Detective Mouse

Future project.

Can reuse:

- Character AI
- Voice System
- Vision System

---

## Multi-Character World

Future possibility:

```text
PixStars Lamp

+

Snowy Owl

+

Detective Mouse

+

Other Characters
```

all connected through:

- HiveMind
- MQTT
- Mission Control

---

# 10. Implementation Roadmap

Phase 1

Foundation

- Raspberry Pi
- MQTT
- Voice
- LEDs

Phase 2

Character

- Speech
- Emotions
- Projection

Phase 3

Awareness

- Camera
- Face Detection
- Tracking

Phase 4

Autonomy

- AI Behaviors
- Reactions
- Improvisation

Phase 5

Character Ecosystem

- Multiple Characters
- Shared Intelligence
- Shared Mission Control

---

# 11. Success Criteria

PixStars should behave as:

- A believable character
- A robotics system
- A theatrical performer
- An AI companion

without appearing to be a traditional robot.

The audience should perceive:

> A living lamp.

Not:

> A collection of technologies.

---

# References

Learn Robotics Programming
Danny Staple

https://www.packtpub.com/en-us/product/learn-robotics-programming-9781803236575

---

# Related Documents

LEARN_ROBOTICS_PROGRAMMING.md

../home_assistant/HOME_ASSISTANT_SETUP.md

../mission-control/PIXSTARS_MISSION_CONTROL.md

../timeline/TIMELINE_ARCHITECTURE.md

../voice/VOICE_ARCHITECTURE.md
