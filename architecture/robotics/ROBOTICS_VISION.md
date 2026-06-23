# ROBOTICS_VISION.md

Version: 1.0

Purpose

Vision allows PixStars to observe its environment.

The goal is not surveillance.

The goal is awareness.

⸻

Hardware

Current:

Lamp Head Camera

Future:

Stereo Cameras
Depth Cameras

⸻

Vision Pipeline
```
Camera
↓
Image Capture
↓
Detection
↓
Interpretation
↓
Character Decision
```
⸻

Phase 1

Face Detection

Capabilities:

* Audience awareness
* Performer awareness

Technology:

* OpenCV

⸻

Phase 2

Tracking

Capabilities:

* Follow Axel
* Follow audience members

Technology:

* OpenCV
* Object Tracking

⸻

Phase 3

Interaction

Capabilities:

* Detect waves
* Detect applause
* Detect movement

⸻

Vision States
```
Inactive
Scanning
Tracking
Focused
Lost Target
```
⸻

Character Integration

Example:
```
Audience waves.

↓

Vision detects motion.

↓

Emotion becomes curious.

↓

Behaviour becomes investigate.

↓

Motion performs head tilt.
```
⸻

MQTT Topics
```
pixstars/vision/events
pixstars/vision/targets
pixstars/vision/state
```
⸻

Future Opportunities

* Gesture recognition
* Audience engagement scoring
* Multi-character awareness
* Snowy Owl integration

⸻

References

ROBOTICS_CHARACTER_ARCHITECTURE.md

VISION_SERVICE.md

OpenCV

Learn Robotics Programming (3rd Edition)

https://github.com/PacktPublishing/Learn-Robotics-Programming-3rd-edition
