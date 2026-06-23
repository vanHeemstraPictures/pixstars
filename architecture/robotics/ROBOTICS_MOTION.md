# ROBOTICS_MOTION.md

Version: 1.0

Status: Core Architecture

⸻

Purpose

Motion is the primary mechanism through which PixStars communicates life.

A lamp has:

* No face
* No eyes
* No mouth

Therefore motion becomes the dominant storytelling tool.

The audience should understand the lamp’s thoughts and emotions from movement alone.

⸻

Motion Philosophy

PixStars motion should follow:
```
Intent
↓
Emotion
↓
Behavior
↓
Movement
```
Never:
```
Move
↓
Because We Can
```
Every movement must have purpose.

⸻

Motion Categories

Attention Motion

Examples:

* Look Left
* Look Right
* Look Up
* Look Down
* Focus On Object

Purpose:

Communicate attention.

⸻

Emotional Motion

Examples:

* Excited Bounce
* Curious Tilt
* Proud Pose
* Sad Droop

Purpose:

Communicate emotion.

⸻

Conversational Motion

Examples:

* Listening Tilt
* Speaking Nod
* Thinking Pause

Purpose:

Support dialogue.

⸻

Performance Motion

Examples:

* Scene Transitions
* Musical Synchronization
* Projection Alignment

Purpose:

Support storytelling.

⸻

Motion Parameters

Each motion includes:
```
{
  "speed": 0.5,
  "amplitude": 0.7,
  "duration": 2.0,
  "emotion": "curious"
}
```
⸻

Core Motion Library

Curious Tilt

Used frequently.

Characteristics:

* Small angle
* Slow approach
* Pause

⸻

Proud Rise

Characteristics:

* Upright posture
* Smooth movement

⸻

Investigate

Characteristics:

* Lean forward
* Small corrections

⸻

Apologize

Characteristics:

* Lower posture
* Reduced movement

⸻

Celebrate

Characteristics:

* Bounce
* Increased light output

⸻

Motion and Story

Motion should reinforce:
```
Curiosity
↓
Arrogance
↓
Conflict
↓
Remorse
↓
Co-Creation
```
⸻

References

CHARACTER_ANIMATION_PRINCIPLES.md

ROBOTICS_CHARACTER_ARCHITECTURE.md

MOTION_SERVICE.md
