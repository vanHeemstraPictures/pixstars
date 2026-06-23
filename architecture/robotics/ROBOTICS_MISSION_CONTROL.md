# ROBOTICS_MISSION_CONTROL.md

Version: 1.0

Status: Operations Architecture

⸻

Purpose

Mission Control is the operational cockpit of PixStars.

It provides complete visibility into the character.

⸻

Design Principle

Operators should see:
```
What the character sees
What the character feels
What the character remembers
What the character is doing
```
⸻

Dashboard Layout

Character Panel

Displays:

* Current State
* Current Behaviour
* Personality Profile

⸻

Emotion Panel

Displays:
```
Curiosity
Joy
Pride
Confusion
Sadness
```
Real-time values.

⸻

Voice Panel

Displays:

* Listening
* Thinking
* Speaking

Current transcript.

⸻

Vision Panel

Displays:

* Camera Feed
* Tracked Targets
* Face Detection

⸻

Motion Panel

Displays:

* Current Motion
* Queue
* Completion Status

⸻

Projection Panel

Displays:

* Current Projection
* Next Projection

⸻

Timeline Panel

Displays:

* Current Scene
* Current Cue
* Upcoming Cue

Integration:

* Ardour
* Jess+

⸻

MQTT Panel

Displays:

* Broker Status
* Service Status
* Message Rate

⸻

Deployment

Recommended:
```
Home Assistant
+
Custom Dashboard
+
MQTT Integration
```
Running on:

Mac Mini M4 Pro

⸻

Future Extensions

Character Health

Displays:

* CPU
* Memory
* Temperature

⸻

Multi-Character Control

Future:
```
PixStars Lamp
Snowy Owl
Detective Mouse
```
Single Mission Control.

⸻

Success Criteria

An operator should be able to answer:
```
What is PixStars thinking?
What is PixStars feeling?
What is PixStars doing?
Why is PixStars doing it?
```
within five seconds.

⸻

References

PIXSTARS_MISSION_CONTROL.md

MQTT_ROBOTICS_ARCHITECTURE.md

ROBOTICS_CHARACTER_ARCHITECTURE.md

Home Assistant Documentation

Learn Robotics Programming (3rd Edition)

https://github.com/PacktPublishing/Learn-Robotics-Programming-3rd-edition
