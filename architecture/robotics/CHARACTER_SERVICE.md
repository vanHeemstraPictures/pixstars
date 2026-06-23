# CHARACTER_SERVICE.md

Version: 1.0

Purpose

The Character Service is the brain of PixStars.

It coordinates:

* Personality
* Emotions
* Memory
* Behaviour Selection

⸻

Responsibilities

The Character Service decides:

What should the character do next?

It does not directly move hardware.

⸻

Inputs

MQTT:
```
pixstars/vision/events
pixstars/voice/input
pixstars/memory/events
pixstars/timeline/events
```
⸻

Outputs
```
pixstars/character/behavior
pixstars/character/state
pixstars/character/intent
```
⸻

Example

Input:

Audience waves.

Decision:

Curious

Behaviour:

Investigate

Output:

Head Tilt

⸻

Internal Components
```
Character Service
├── Personality Engine
├── Emotion Engine
├── Memory Interface
├── Behaviour Selector
└── Story Context Engine
```
⸻

Story Awareness

The Character Service knows:

* Current Scene
* Current Act
* Current Character Arc

This prevents inappropriate behaviour.

⸻

References

CHARACTER_PERSONALITY_MODEL.md

CHARACTER_STORY_INTEGRATION.md

ROBOTICS_BEHAVIORS.md
