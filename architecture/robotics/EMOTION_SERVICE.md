# EMOTION_SERVICE.md

Version: 1.0

Purpose

Maintain the emotional state of PixStars.

The Emotion Service converts events into feelings.

⸻

Inputs
```
Vision Events
Voice Events
Memory Events
Timeline Events
Character Events
```
⸻

Emotion Model
```
{
  "curiosity": 0.8,
  "joy": 0.4,
  "pride": 0.3,
  "sadness": 0.0
}
```
⸻

Emotion Decay

Emotions naturally fade.

Example:
```
Curiosity 0.9
↓
Curiosity 0.7
↓
Curiosity 0.4
↓
Curiosity 0.2
```
⸻

Emotional Triggers

Example:
```
Lamp sees new drawing.
↓
Curiosity +0.4
```
⸻

MQTT Topics
```
pixstars/emotion/current
pixstars/emotion/history
pixstars/emotion/changes
```
⸻

Consumers

* Voice Service
* Motion Service
* Projection Service
* Mission Control

⸻

References

ROBOTICS_EMOTIONS.md

CHARACTER_SERVICE.md
