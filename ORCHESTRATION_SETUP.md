Here is your ORCHESTRATION_SETUP.md. You can paste this directly into your Pixstars repository.

⸻

ORCHESTRATION_SETUP.md

Pixstars — Unified AI-Driven Performance Orchestration

⸻

1. Introduction

Pixstars is a live theatrical performance that blends:
	•	Music (November Rain piano + drums)
	•	Acting (Axel Rose → Walt Disney → Axel)
	•	Projection (logos, drawings, AI iterations)
	•	Stage lighting
	•	Animatronic desk lamp (AI character)
	•	Dialogue (A.I., Walt, Axel)
	•	Special effects (overheating, flicker, death, rebirth)

To guarantee perfect timing, while still allowing AI-driven behavior, we use a hybrid orchestration architecture built on:
	•	DigiScore (show timeline / conductor)
	•	Ardour (audio engine & MIDI playback)
	•	Jess+ (AI-driven animatronic lamp behavior)

This document defines the vision, architecture, and implementation guidelines.

⸻

2. Vision

Pixstars is not a scripted show with props.

Pixstars is a live collaboration between human and AI.

Therefore:
	•	The show timeline is deterministic
	•	The lamp behavior is AI-driven
	•	Events are triggered centrally
	•	AI reacts inside constrained windows

This results in:
	•	Reliable performance
	•	Artistic freedom
	•	AI as real character
	•	Non-identical shows
	•	Controlled unpredictability

The lamp is not:
	•	a prop
	•	a puppet
	•	a fixed animation

The lamp is:

a bounded AI performer

⸻

3. System Overview

The orchestration is built around three components:

DigiScore — Show Conductor

Responsibilities:
	•	Master timeline
	•	Cue triggering
	•	Scene transitions
	•	Projection control
	•	Lighting control
	•	Lamp state transitions
	•	Development storyboard playback

DigiScore is the brain of the show.

⸻

Ardour — Audio Engine

Responsibilities:
	•	Piano intro playback
	•	Continuous drum track
	•	Voice playback (A.I., Walt, Axel)
	•	SFX (ticks, smoke cues)
	•	Final piano chords
	•	Master audio export

Ardour is the heartbeat of the show.

⸻

Jess+ — AI Lamp Engine

Repository:
https://github.com/DigiScore/jess_plus

Responsibilities:
	•	Lamp motion AI
	•	Emotional state interpretation
	•	Micro movements
	•	Variations between performances
	•	Expressive behavior
	•	Servo control
	•	Lamp light control

Jess+ is the soul of the lamp.

⸻

4. High Level Architecture

                 ┌───────────────┐
                 │   DigiScore   │
                 │  Show Timeline│
                 └───────┬───────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌────────┐     ┌────────────┐     ┌──────────┐
   │ Ardour │     │ Projection │     │ Lighting │
   └────────┘     └────────────┘     └──────────┘
        │
        ▼
   ┌──────────┐
   │  Jess+   │
   │  AI Lamp │
   └──────────┘
        │
        ▼
   Animatronic Lamp


⸻

5. Event Driven Orchestration

DigiScore sends events.

Jess+ interprets lamp behavior.

Ardour plays audio cues.

Example:

EVENT: SCENE_TRANSFORM_WALT
→ Ardour continues drums
→ Projection shows Disney castle
→ Jess+ lamp enters CURIOUS state
→ Lighting changes to soft blue


⸻

6. Lamp AI State Model

Jess+ receives state commands:

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

Jess+ decides:
	•	movement
	•	tilt
	•	speed
	•	micro motion
	•	attention direction
	•	timing variation

This gives the lamp AI personality.

⸻

7. Timeline Example

00:00 dark stage
00:05 Guns N' Roses logo
00:12 lamp ON reveal
01:00 drums begin
01:10 lamp curious
02:00 Disney castle projection
02:30 Mickey drawing
03:10 lamp dismisses
03:40 lamp drawing
04:30 AI iteration projections
05:40 overheating ticks
06:00 smoke
06:20 lamp death
07:30 rebirth flicker
07:40 "A.I."
07:50 "W.A.L.T."
08:00 "A.X.E.L."
08:10 Team Rockstars logo
08:20 final piano chords
09:15 lamp OFF
09:17 blackout


⸻

8. Ardour Responsibilities

Ardour session contains:

Tracks:
	•	Piano intro
	•	Drum track (continuous)
	•	Lamp voice
	•	Overheat ticking
	•	Smoke cue
	•	Final piano chords
	•	Click track (optional)
	•	Master bus

Export:

PIXSTARS_MASTER.wav

Optional:

Separate cue output for performer monitor.

⸻

9. Projection Control

DigiScore triggers projections:

Opening:
	•	Guns N’ Roses logo

Transformation:
	•	Disney castle

Development:
	•	Storyboard frames

Drawing:
	•	Mickey Mouse
	•	Lamp sketch

AI phase:
	•	Iterative drawings
	•	faster / better

Dialogue:
	•	A.I. signature
	•	W.A.L.T. signature
	•	A.X.E.L. signature

Finale:
	•	Team Rockstars logo

⸻

10. Lighting Control

Lighting states:

BLACKOUT
LAMP_ONLY
ROCKSTAR
DISNEY_SOFT
AI_COLD
OVERHEAT_FLICKER
DEATH_DIM
REBIRTH_WARM
FINALE_ROCK
BLACKOUT_FINAL

DigiScore triggers these.

⸻

11. Lamp Behavior Design

Jess+ must implement:

Neutral idle micro motion
Curious head tilt
Dismissive turn away
Pleased lean forward
Arrogant show-off motion
Overheat jitter + flicker
Death collapse
Weak rebirth tremble
Learning slow movement
Celebrate rhythmic swing
Final OFF freeze

The lamp must never move randomly.

All motion must derive from emotional state.

⸻

12. AI Artistic Principle

The lamp must appear:

Alive
Curious
Imperfect
Learning
Emotional

NOT:

Robotic
Mechanical
Predictable
Looping

Jess+ introduces bounded variation:
	•	timing ±10%
	•	angle ±5°
	•	micro jitter
	•	idle breathing

This preserves realism.

⸻

13. Development Mode

During rehearsal:

DigiScore shows:

Storyboard sketches
Scene labels
Timing markers

This allows choreography tuning.

Production mode:

Storyboard disabled.

⸻

14. Hardware Recommendations

Mac Mini M4 Pro
Ardour
DigiScore
Jess+
USB MIDI interface
DMX interface
Lamp servo controller (Arduino / ESP32)
Mini speaker inside lamp
Projection beamer

⸻

15. Communication Protocol

Recommended:

OSC between systems

DigiScore → Jess+
DigiScore → Lighting
DigiScore → Projection
DigiScore → Ardour (optional)

⸻

16. Safety Requirements

Lamp death must always occur
Lamp rebirth must always occur
Final lamp OFF must always occur

These are non-AI controlled anchors.

⸻

17. Performance Philosophy

The show must feel:

Scripted
Yet alive

Deterministic
Yet emotional

Controlled
Yet intelligent

This is achieved through:

Timeline + AI interpretation

⸻

18. References

Jess+
https://github.com/DigiScore/jess_plus

Ardour
https://ardour.org

DigiScore
(Show orchestration framework)

Pixstars concept
Human + AI performance collaboration

⸻

19. Summary

DigiScore controls time
Ardour controls sound
Jess+ controls AI lamp

Together they create:

Pixstars — a live collaboration between human and artificial intelligence.
