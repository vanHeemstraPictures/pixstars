APPLE_CONTAINER_SETUP.md

Apple Container Integration for Pixstars

Version: 1.0  
Status: Recommended  
Repository: pixstars/architecture/container  

⸻

1. Executive Summary

Apple Container is Apple’s modern container runtime for Apple Silicon Macs.

Repository:

https://github.com/apple/container

For Pixstars, Apple Container should be used as a:

* Development Environment Platform
* Integration Testing Platform
* Local AI Services Platform
* Mission Control Services Platform
* Reproducible Contributor Environment

Apple Container should not be used for:

* Live stage-critical cue execution
* Real-time lamp control
* Servo movement control
* Audio playback
* Ardour runtime
* Raspberry Pi runtime workloads

The guiding principle is:

Development and integration may be containerized.

Live performance execution should remain as simple and reliable as possible.

⸻

2. References

Apple Container

GitHub

https://github.com/apple/container

Apple Virtualization Framework

https://developer.apple.com/documentation/virtualization

OCI Container Specification

https://opencontainers.org

⸻

3. Why Apple Container Fits Pixstars

Pixstars consists of multiple systems:

* Ardour
* DigiScore
* Jess+
* Home Assistant
* OpenVoiceOS
* HiveMind
* Mission Control
* Lamp APIs
* AI Services
* Development Tools

Installing everything directly onto macOS creates:

* Dependency conflicts
* Upgrade complexity
* Difficult onboarding
* Configuration drift

Apple Container provides isolated environments while remaining lightweight on Apple Silicon.

Benefits:

* Reproducible environments
* Easy upgrades
* Easy resets
* Clean dependency separation
* Better contributor onboarding

⸻

4. Architectural Principles

Principle 1

Containerize services.

Do not containerize performances.

⸻

Principle 2

Containerize development.

Keep runtime simple.

⸻

Principle 3

Container failures must never stop a performance.

If a container crashes during rehearsal:

* Restart container

If a live cue system fails:

* Performance is impacted

Therefore:

Mission-critical runtime systems remain native.

⸻

Principle 4

Apple Container is infrastructure.

It is not part of the performance narrative.

The audience should never know containers exist.

⸻

5. Recommended Architecture
```
Mac Mini M4 Pro
│
├── Native Runtime
│   │
│   ├── Ardour
│   ├── DigiScore
│   ├── Jess+
│   ├── OBS
│   ├── Audio Drivers
│   ├── MIDI Drivers
│   └── Show Control
│
├── Apple Containers
│   │
│   ├── Home Assistant Services
│   ├── OpenVoiceOS
│   ├── HiveMind
│   ├── Mission Control API
│   ├── Documentation Services
│   ├── AI Services
│   ├── Development Utilities
│   └── Test Simulators
│
└── Raspberry Pi Zero 2 WH
    │
    ├── Camera
    ├── LEDs
    ├── Motion
    ├── Audio
    └── Wake Word Satellite
```
⸻

6. Pixstars Container Domains

Domain A

Development

Purpose:

Provide isolated development environments.

Examples:

* Python services
* FastAPI services
* Testing APIs
* Documentation tooling

Recommended:

Containerized

⸻

Domain B

AI Services

Purpose:

Provide intelligence capabilities.

Examples:

* OpenVoiceOS
* HiveMind
* Future LLM gateways
* Voice processing

Recommended:

Containerized

⸻

Domain C

Mission Control

Purpose:

Provide dashboards and monitoring.

Examples:

* Home Assistant integrations
* Monitoring services
* Telemetry services
* Rehearsal dashboards

Recommended:

Containerized

⸻

Domain D

Performance Runtime

Purpose:

Execute the live show.

Examples:

* Ardour
* Jess+
* DigiScore
* MIDI routing
* Audio playback

Recommended:

Native

Not containerized

⸻

7. Containerized Home Assistant Services

Recommended architecture:
```
Apple Container
│
├── Home Assistant Extensions
├── Automation APIs
├── Dashboard Services
├── Event Logging
└── Monitoring
```
Benefits:

* Isolation
* Easy updates
* Easy rollback

⸻

8. Containerized OpenVoiceOS

Recommended architecture:
```
Container
│
├── OVOS Core
├── Skill Runtime
├── Voice Services
└── API Layer
```
Benefits:

* Consistent dependencies
* Easy upgrades
* Independent lifecycle

⸻

9. Containerized HiveMind

Recommended architecture:
```
Container
│
├── HiveMind Server
├── Message Routing
├── Satellite Registry
└── Event Services
```
Benefits:

* Isolation
* Simpler maintenance
* Reproducible configuration

⸻

10. Lamp Simulator Container

One of the most valuable future uses.

Purpose:

Simulate the lamp without requiring physical hardware.

Example:
```
Lamp Simulator
│
├── Virtual Lamp Head
├── Virtual LEDs
├── Virtual Servo
├── Virtual Camera Feed
└── Event Playback
```
Benefits:

* Remote development
* Automated testing
* CI integration

⸻

11. Contributor Onboarding

Goal:

A contributor should be able to clone Pixstars and immediately start working.

Example:

git clone <repository>
cd pixstars
container compose up

Result:

* Home Assistant services running
* OVOS running
* HiveMind running
* Mission Control running
* Test environment available

No manual installation required.

⸻

12. Future Container Stack

Recommended future stack:
```
Apple Container
│
├── OVOS
├── HiveMind
├── Home Assistant Extensions
├── Mission Control
├── Documentation Services
├── Test Harness
├── Lamp Simulator
├── Telemetry Services
└── AI Character Services
```
⸻

13. What Must Remain Native

The following systems should never depend on container startup during a performance.

Ardour

Reason:

Audio latency

⸻

DigiScore

Reason:

Cue reliability

⸻

Jess+

Reason:

Show-critical control

⸻

MIDI Drivers

Reason:

Timing precision

⸻

Audio Drivers

Reason:

Low latency

⸻

OBS

Reason:

Video reliability

⸻

14. Alignment with Pixstars Architecture

Apple Container aligns with the Pixstars architecture principles:

* Kernel-first architecture
* Modular services
* Reproducible environments
* Contributor-friendly onboarding
* Isolated capabilities
* Portable development environments

Apple Container becomes a supporting infrastructure layer around Pixstars.

It does not become the runtime heart of the performance.

The heart of the performance remains:
```
Human
+
Lamp
+
Music
+
Story
```
Everything else exists to support that experience.

⸻

15. Final Recommendation

Recommendation Level:

★★★★★ Strongly Recommended

Use Apple Container as:

* Development Platform
* Integration Platform
* AI Services Platform
* Mission Control Platform
* Contributor Onboarding Platform

Do not use Apple Container as:

* Live cue engine
* Audio engine
* Motion engine
* Lamp runtime

Containerize development.

Keep performance execution native.

This provides the best balance between maintainability, portability, reliability, and live-show robustness.
