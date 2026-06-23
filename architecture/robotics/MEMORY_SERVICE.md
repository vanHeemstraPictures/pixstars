# MEMORY_SERVICE.md

Version: 1.0

Purpose

The Memory Service provides continuity.

Without memory, PixStars reacts.

With memory, PixStars remembers.

⸻

Responsibilities

* Store events
* Retrieve memories
* Summarize experiences
* Maintain character continuity

⸻

Memory Layers
```
Memory Service
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

* Last audience interaction
* Last spoken phrase
* Current focus target

⸻

Performance Memory

Duration:

* Current show

Examples:

* Walt drew Mickey
* Lamp became arrogant
* Walt removed bulb

⸻

Long-Term Memory

Duration:

* Across performances

Examples:

* Character biography
* Learned behaviours
* Persistent relationships

⸻

MQTT Topics
```
pixstars/memory/store
pixstars/memory/recall
pixstars/memory/event
pixstars/memory/history
```
⸻

Storage

Phase 1

SQLite

Phase 2

PostgreSQL

Phase 3

Vector Database

⸻

References

ROBOTICS_MEMORY.md

CHARACTER_SERVICE.md
