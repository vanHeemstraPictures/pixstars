# ROBOTICS_STATE_MACHINE.md

Version: 1.0 

⸻

Purpose

The Robotics State Machine defines the high-level operational states of the PixStars character.

The state machine governs:

* Motion
* Voice
* Vision
* Projection
* Emotions
* Behaviours

Every subsystem derives its current behaviour from the active state.

⸻

Core Philosophy

Traditional robotics uses:
```
Idle
Running
Error
```
PixStars uses:
```
Sleeping
Observing
Thinking
Feeling
Speaking
Performing
Remembering
```
because PixStars is a character rather than a machine.

⸻

Primary States

OFF

No power.

Outputs:

* Lamp Dark
* Audio Silent
* Projection Off

⸻

BOOTING

Character awakening.

Outputs:

* Soft LED pulse
* Self checks
* MQTT registration

⸻

IDLE

Waiting state.

Behaviours:

* Breathing motion
* Small head movements
* Ambient observation

⸻

OBSERVING

Perceiving environment.

Inputs:

* Camera
* Microphone
* Timeline events

Outputs:

* Tracking
* Attention shifts

⸻

THINKING

Internal processing.

Outputs:

* Slight pause
* Reduced movement
* Focused light

⸻

SPEAKING

Character communication.

Outputs:

* Voice
* Light synchronization
* Mouth-equivalent motion

⸻

PERFORMING

Timeline-driven show mode.

Inputs:

* Ardour
* Jess+
* Mission Control

Outputs:

* Scripted actions
* Scripted emotions

⸻

REMEMBERING

Memory retrieval state.

Outputs:

* Context reconstruction
* Character continuity

⸻

Emotional Overlay

Any state may be modified by:

* Curious
* Happy
* Proud
* Confused
* Sad
* Excited
* Ashamed

These overlays affect motion and voice.

⸻

References

ROBOTICS_CHARACTER_ARCHITECTURE.md

Learn Robotics Programming (3rd Edition)

https://github.com/PacktPublishing/Learn-Robotics-Programming-3rd-edition
