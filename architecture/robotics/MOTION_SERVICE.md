# MOTION_SERVICE.md

Version: 1.0

Status: Runtime Service

⸻

Purpose

The Motion Service translates character intent into physical movement.

⸻

Responsibilities

* Execute movements
* Control actuators
* Manage movement queues
* Apply emotional modifiers

⸻

Inputs

MQTT Topics:
```
pixstars/character/behavior
pixstars/emotion/current
pixstars/timeline/event
pixstars/motion/command
```
⸻

Outputs
```
pixstars/motion/state
pixstars/motion/current
pixstars/motion/completed
```
⸻

Architecture
```
Character Service
↓
Motion Service
↓
Motion Controller
↓
Actuator Drivers
↓
Physical Lamp
```
⸻

Motion Queue

Example:
```
Observe
↓
Investigate
↓
Pause
↓
Return Idle
```
⸻

Emotional Modifiers

Curious:
```
speed: medium
amplitude: small
````
Excited:
```
speed: high
amplitude: large
```
Sad:
```
speed: low
amplitude: small
```
⸻

Safety

Motion Service must enforce:

* Range limits
* Speed limits
* Collision prevention

⸻

Future Hardware

Phase 1

Timeline-only

Phase 2

Motorized joints

Phase 3

Autonomous movement

⸻

References

ROBOTICS_MOTION.md

EMOTION_SERVICE.md

CHARACTER_SERVICE.md
