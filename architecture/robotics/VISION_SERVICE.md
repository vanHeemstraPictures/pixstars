# VISION_SERVICE.md

Version: 1.0

Purpose

The Vision Service gives PixStars situational awareness.

⸻

Responsibilities

* Face Detection
* Tracking
* Audience Awareness
* Performer Awareness

⸻

Hardware

Lamp Head Camera

⸻

Processing Pipeline
```
Camera
↓
Capture
↓
Detection
↓
Tracking
↓
Interpretation
↓
Character Event
```
⸻

Phase 1

Face Detection

Technology:

OpenCV

⸻

Phase 2

Tracking

Capabilities:

* Follow Axel
* Follow Audience

⸻

Phase 3

Interaction

Capabilities:

* Detect waves
* Detect applause
* Detect gestures

⸻

MQTT Topics
```
pixstars/vision/events
pixstars/vision/target
pixstars/vision/state
```
⸻

References

ROBOTICS_VISION.md

CHARACTER_SERVICE.md
