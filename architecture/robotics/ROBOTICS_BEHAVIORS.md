# ROBOTICS_BEHAVIORS.md

Version: 1.0 

⸻

Purpose

Behaviours convert emotion into visible actions.

Relationship:
```
Story
↓
Emotion
↓
Behaviour
↓
Motion
```
⸻

Core Behaviours

Observe

Purpose:

Gather information.

Motion:

* Slow scan
* Pause

⸻

Investigate

Purpose:

Examine an object.

Motion:

* Forward movement
* Head tilt

⸻

Celebrate

Purpose:

Express success.

Motion:

* Bounce
* Light increase

⸻

Retreat

Purpose:

Express uncertainty.

Motion:

* Pull back
* Dim light

⸻

ShowOff

Purpose:

Express pride.

Motion:

* Exaggerated movement
* Projection emphasis

Useful during the A.I. superiority sequence.

⸻

Apologize

Purpose:

Express remorse.

Motion:

* Reduced motion
* Lower posture

Useful after lamp shutdown sequence.

⸻

Behaviour Selection

Inputs:

* Emotion
* Story state
* Timeline state
* Audience state

Outputs:

* Motion
* Projection
* Voice

⸻

Example

Scene:

Walt draws lamp.

Emotion:

Curiosity

Behaviour:

Investigate

Motion:

Head tilt
Forward lean
Light brighten

⸻

References

ROBOTICS_CHARACTER_ARCHITECTURE.md

ROBOTICS_EMOTIONS.md

ROBOTICS_MOTION.md

Learn Robotics Programming (3rd Edition)

https://github.com/PacktPublishing/Learn-Robotics-Programming-3rd-edition
