# ROBOTICS_MEMORY.md

Version: 1.0

Purpose

Memory transforms a reactive robot into a persistent character.

Without memory, PixStars only responds.

With memory, PixStars develops relationships, continuity, and growth.

⸻

Memory Architecture
```
Character Memory
├── Short-Term Memory
├── Performance Memory
├── Long-Term Memory
└── Knowledge Memory
```
⸻

Short-Term Memory

Duration:

* Seconds
* Minutes

Examples:

* Last spoken sentence
* Current audience member
* Current emotional state

Storage:

* In-memory cache

⸻

Performance Memory

Duration:

* Entire performance

Examples:

* Walt drew Mickey
* Lamp signed A.I.
* Walt removed bulb
* Reconciliation occurred

Purpose:

Maintain narrative continuity.

⸻

Long-Term Memory

Duration:

* Across performances

Examples:

* Character biography
* Learned preferences
* Frequently used responses

Storage:

* SQLite
* PostgreSQL
* Vector Database

⸻

Knowledge Memory

Sources:

* Robotics documentation
* Character documentation
* PixStars screenplay
* Mission notes

Purpose:

Provide context for AI reasoning.

⸻

Memory Service API
```
memory/store
memory/recall
memory/search
memory/delete
memory/summarize
```
MQTT Topics:
```
pixstars/memory/events
pixstars/memory/store
pixstars/memory/recall
```
⸻

Story Integration

Memory supports:

* Character growth
* Character relationships
* Character accountability

Example:

The lamp remembers Walt restoring the bulb.

This influences future behaviour.

⸻

References

ROBOTICS_CHARACTER_ARCHITECTURE.md

MEMORY_SERVICE.md

Learn Robotics Programming (3rd Edition)

https://github.com/PacktPublishing/Learn-Robotics-Programming-3rd-edition
