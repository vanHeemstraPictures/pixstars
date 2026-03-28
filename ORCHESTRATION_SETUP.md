# Orchestration Setup
## Pixstars — Unified AI-Driven Performance Orchestration

---

# 1. Introduction

**Pixstars** is a live theatrical performance that blends:

- Music (November Rain piano + drums)
- Acting (Axel Rose → Walt Disney → Axel)
- Projection (logos, drawings, AI iterations)
- Stage lighting
- Animatronic desk lamp (AI character)
- Dialogue (A.I., Walt, Axel)
- Special effects (overheating, flicker, death, rebirth)

To guarantee **perfect timing**, while still allowing **AI-driven behavior**, we use a hybrid orchestration architecture built on:

- DigiScore (show timeline / conductor)
- Ardour (audio engine & MIDI playback)
- Jess+ (AI-driven animatronic lamp behavior)

---

# 2. Vision

Pixstars is a **live collaboration between human and AI**.

Therefore:

- The show timeline is deterministic
- The lamp behavior is AI-driven
- Events are triggered centrally
- AI reacts inside constrained windows

The lamp is a **bounded AI performer**.

---

# 3. System Overview

## DigiScore — Show Conductor
- Master timeline
- Cue triggering
- Scene transitions
- Projection control
- Lighting control
- Lamp state transitions

## Ardour — Audio Engine
- Piano intro playback
- Continuous drum track
- Voice playback
- SFX
- Final piano chords

## Jess+ — AI Lamp Engine
https://github.com/DigiScore/jess_plus

- Lamp motion AI
- Emotional state interpretation
- Micro movements
- Servo control

---

# 4. High Level Architecture

DigiScore → Ardour → Jess+ → Lamp  
DigiScore → Lighting  
DigiScore → Projection

---

# 5. Event Driven Orchestration

Example:

EVENT: SCENE_TRANSFORM_WALT  
→ Ardour continues drums  
→ Projection shows Disney castle  
→ Jess+ lamp enters CURIOUS state  
→ Lighting changes  

---

# 6. Lamp AI State Model

INERT  
FUNCTIONAL  
CURIOUS  
DISMISSIVE  
PLEASED  
ARROGANT  
OVERHEATING  
DYING  
DEAD  
WEAK  
REBORN  
LEARNING  
CELEBRATE  
OFF  

Jess+ decides motion within these states.

---

# 7. Timeline Example

00:00 dark stage  
00:05 Guns N' Roses logo  
00:12 lamp ON  
01:00 drums begin  
02:00 Disney castle  
03:10 Mickey drawing  
04:30 AI iteration  
05:40 overheating  
06:20 death  
07:40 "A.I."  
08:00 "W.A.L.T."  
08:10 "A.X.E.L."  
08:20 Team Rockstars logo  
09:15 lamp OFF  

---

# 8. Ardour Responsibilities

Tracks:

- Piano intro
- Drum track
- Lamp voice
- SFX
- Final piano
- Master bus

Export:

PIXSTARS_MASTER.wav

---

# 9. Projection Control

Opening:
- Guns N' Roses

Transformation:
- Disney castle

Drawing:
- Mickey
- Lamp

AI:
- Iterations
- signatures

Finale:
- Team Rockstars

---

# 10. Lighting States

BLACKOUT  
LAMP_ONLY  
ROCKSTAR  
DISNEY_SOFT  
AI_COLD  
OVERHEAT  
DEATH  
REBIRTH  
FINALE  

---

# 11. Lamp Behavior Design

Jess+ implements:

Neutral idle  
Curious tilt  
Dismissive turn  
Pleased lean  
Arrogant show-off  
Overheat jitter  
Death collapse  
Weak rebirth  
Learning motion  
Celebrate swing  
Final OFF  

---

# 12. AI Artistic Principle

The lamp must appear:

Alive  
Curious  
Imperfect  
Learning  
Emotional  

---

# 13. Communication

Recommended:

OSC between components.

---

# 14. Hardware

Mac Mini M4 Pro  
Ardour  
DigiScore  
Jess+  
DMX interface  
Lamp controller  
Projector  

---

# 15. Summary

DigiScore controls time  
Ardour controls sound  
Jess+ controls AI lamp  

Pixstars becomes a collaboration between human and artificial intelligence.

