# INTENT_MVP_1.md

PixStars Intent Engine MVP 1

Version: 1.0

Status: Proposed

Repository: pixstars/intent

⸻

1. Executive Summary

PixStars is more than a stage performance.

It combines:

* Storytelling
* Live acting
* Music
* Robotics
* Artificial Intelligence
* Projection Mapping
* Lighting
* Audience Experience

To coordinate these disciplines, PixStars requires a shared understanding of:

* What is happening
* Why it is happening
* What the audience should experience
* How success is measured

This document introduces the first Minimal Viable Product (MVP) of the PixStars Intent Engine.

The Intent Engine acts as a bridge between:
```
Story
   ↓
Intent
   ↓
Timeline
   ↓
Technical Systems
```
The purpose is to capture:

* Scenes
* Actions
* Cues
* States
* Audience intent
* Performance scores

in a single timeline-driven model.

⸻

2. Vision

A future PixStars performance should be executable from a single source of truth.

The same timeline should drive:

* Screenplay
* Storyboards
* Lamp behaviour
* Projections
* Audio cues
* Lighting cues
* Home Assistant
* Jess+
* DigiScore

while simultaneously documenting:

* Emotional intent
* Narrative intent
* Audience understanding
* Technical readiness

⸻

3. MVP Scope

Included:

* Storyboard-based timeline
* Scene model
* Cue model
* State model
* Intent model
* Scoring model
* Export to Home Assistant dashboard

Excluded:

* Real-time automation
* AI scene evaluation
* Automatic cue generation
* Live audience analytics
* Machine learning

⸻

4. Architecture
```
Storyboarder
      │
      ▼
Intent Timeline
      │
      ▼
Mission Control
      │
      ├── Ardour
      ├── Jess+
      ├── DigiScore
      ├── Home Assistant
      ├── Lamp
      └── Projection System
```
[Storyboarder](https://tinythings.net/storyboarder/) becomes the authoring tool.

Mission Control becomes the operational tool.

⸻

5. Timeline Model

Each storyboard frame represents a timeline event.

Example:
```
frame: 42
timecode: 00:04:12
title: Lamp Discovers Its Portrait
scene: Drawing Duel
description:
  Lamp notices Walt's lamp sketch.
duration: 8s
```
⸻

6. Intent Model

Every frame contains intent.

Example:
```
intent:
  audience_emotion:
    - curiosity
    - delight
  narrative_goal:
    lamp_feels_seen
  message:
    intelligence_requires_recognition
  importance:
    high
```
⸻

7. State Model

Each frame contains active states.

Example:
```
states:
  performer:
    identity: Walt
  lamp:
    mood: curious
    power: on
  projection:
    active: true
    asset: lamp_sketch
  audio:
    cue: piano_theme
  lighting:
    cue: warm_white
```
⸻

8. Cue Model

Technical systems receive cues.

Example:
```
cues:
  lamp:
    look_at_drawing
  projection:
    display_lamp_sketch
  audio:
    play_cue_17
  lighting:
    warm_fade
```
⸻

9. Scoring Model

Every frame can be evaluated.

Example:
```
score:
  clarity: 90
  emotional_impact: 85
  technical_complexity: 45
  audience_confusion_risk: 10
  narrative_importance: 95
```
Scores use a 0–100 scale.

⸻

10. Scene Score Aggregation

Scene scores are calculated from frame scores.

Example:
```
scene:
  name: Drawing Duel
  average_clarity: 88
  emotional_impact: 92
  confusion_risk: 15
```
This allows weak scenes to be identified before rehearsals.

⸻

11. Mission Control View

Mission Control should display:

Current Scene

Current Frame

Current Timecode

Current Intent

Current Active States

Current Cues

Current Scores

Example:

Scene:
Drawing Duel
Frame:
42
Intent:
Lamp Feels Seen
Emotion:
Wonder
Projection:
Lamp Sketch
Lamp:
Curious
Audio:
Cue 17
Score:
92

⸻

12. Storyboarder Integration

Storyboarder becomes the primary design interface.

Designers create:

* Frames
* Notes
* Timing
* Camera ideas
* Stage notes

Additional PixStars metadata is attached.

Example:
```
pixstars:
  intent:
    wonder
  emotion:
    delight
  score:
    92
```
⸻

13. Home Assistant Integration

Mission Control receives exported timeline data.

Example export:
```
timeline:
  - frame: 42
    title:
      Lamp Discovers Portrait
    timecode:
      00:04:12
    intent:
      lamp_feels_seen
    score:
      92
```
Home Assistant displays:

* Current frame
* Next frame
* Current cue
* Current score

⸻

14. Future Evolution

MVP 2

* Automatic cue generation
* Timeline validation
* Cue conflict detection

MVP 3

* Real-time performance execution

MVP 4

* AI rehearsal assistant

MVP 5

* Audience reaction scoring

MVP 6

* Full Intent-Driven Performance Engine

⸻

15. Success Criteria

The MVP is successful when:

1. PixStars scenes can be represented in Storyboarder.
2. Every frame has intent metadata.
3. Every frame has score metadata.
4. Timeline data can be exported.
5. Home Assistant Mission Control can visualize the timeline.
6. Designers can review story, intent, cues and scores from a single source of truth.

⸻

16. Conclusion

The Intent Engine introduces a new layer within PixStars.

Instead of only describing what happens, PixStars also captures why it happens and how well it communicates its message.

This creates a foundation for future AI-assisted performance design, rehearsal analysis, show control and audience experience optimisation.

The long-term goal is a fully intent-driven stage performance where story, technology and emotion remain synchronized from design through execution.
