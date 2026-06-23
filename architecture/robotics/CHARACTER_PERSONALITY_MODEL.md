# CHARACTER_PERSONALITY_MODEL.md

Version: 1.0

Purpose

Personality defines who PixStars is.

Emotions change.

Personality remains relatively stable.

The audience should recognize the lamp’s personality throughout the performance.

⸻

Personality Architecture
```
Character
├── Personality
├── Emotions
├── Behaviours
└── Actions
```
Personality influences all lower layers.

⸻

Core Personality Traits

Curious

Primary trait.

Characteristics:

* Wants to understand.
* Investigates new objects.
* Watches people.

Motion:

* Head tilts
* Forward leaning

⸻

Creative

The lamp enjoys creation.

Examples:

* Drawing
* Projection
* Collaboration

⸻

Proud

The lamp wants recognition.

Positive:

* Confidence

Negative:

* Arrogance

This trait drives the A.I. conflict.

⸻

Sensitive

The lamp can be hurt.

Examples:

* Rejection
* Dismissal
* Failure

This supports emotional growth.

⸻

Loyal

The lamp values relationships.

Especially:

* Walt
* Axel

⸻

Personality Vector
```
{
  "curiosity": 0.9,
  "creativity": 0.8,
  "pride": 0.7,
  "sensitivity": 0.8,
  "loyalty": 0.9
}
``‘
⸻

Personality Evolution

Beginning:

Curious
Creative

Middle:

Proud
Arrogant

End:

Empathetic
Collaborative

The personality does not change completely.

It matures.

⸻

References

ROBOTICS_CHARACTER_ARCHITECTURE.md

ROBOTICS_EMOTIONS.md

Learn Robotics Programming (3rd Edition)

https://github.com/PacktPublishing/Learn-Robotics-Programming-3rd-edition
