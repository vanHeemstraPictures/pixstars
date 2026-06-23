# MQTT_ROBOTICS_ARCHITECTURE.md

Version: 1.0

Purpose

MQTT serves as the nervous system of PixStars.

All services communicate through MQTT.

No service should directly depend upon another service.

This enables:

* Loose Coupling
* Independent Deployment
* Fault Isolation
* Scalability

⸻

Architecture
```
                     MQTT Broker
                            │
 ┌──────────────┬────────────┼────────────┬─────────────┐
 │              │            │            │             │
Character    Emotion      Vision      Voice      Mission Control
 Service     Service      Service     Service
 │              │            │            │
Memory      Motion      Projection    Timeline
Service     Service      Service      Service
```
⸻

Broker

Recommended:

Mosquitto

Running on:

Mac Mini M4 Pro

⸻

Naming Convention

pixstars/<service>/<topic>

Examples:
```
pixstars/voice/state
pixstars/emotion/current
pixstars/motion/command
pixstars/vision/target
pixstars/timeline/event
```
⸻

Event-Driven Character

Example:
```
Vision detects Axel
↓
pixstars/vision/target
↓
Emotion Service
↓
Curiosity increases
↓
pixstars/emotion/current
↓
Motion Service
↓
Head Tilt
```
⸻

Reliability

QoS Levels:
```
QoS 0
Telemetry
QoS 1
Character Events
QoS 2
Critical Show Events
```
⸻

References

Learn Robotics Programming (3rd Edition)

https://github.com/PacktPublishing/Learn-Robotics-Programming-3rd-edition

ROBOTICS_CHARACTER_ARCHITECTURE.md
