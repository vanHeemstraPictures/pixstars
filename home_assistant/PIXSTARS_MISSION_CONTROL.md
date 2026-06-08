PIXSTARS_MISSION_CONTROL.md

PixStars Mission Control (PMC)

Version: 1.0

Status: Proposed

Repository:

pixstars/home_assistant

⸻

1. Purpose

PixStars Mission Control (PMC) is the digital twin of the PixStars performance.

PMC provides a unified view of:

* Story
* Dialogue
* Scene Progress
* Lamp State
* Lamp Emotion
* Lamp Motion
* Lighting
* Bulb Status
* Laser Effects
* Projections
* Audio
* Camera Feeds
* Automation Events

PMC is implemented on Home Assistant and can be accessed from:

* Mac Mini M4 Pro
* iPad
* iPhone
* Browser
* Remote Internet Connection

PMC acts as:

* Performance Bible
* Rehearsal Tool
* Show Controller
* Live Dashboard
* Debug Console
* Monitoring Platform

⸻

2. High-Level Architecture

            Ardour
               │
            OSC/MIDI
               │
               ▼
     ┌─────────────────┐
     │ Home Assistant  │
     │ Mission Control │
     └─────────────────┘
       ▲      ▲      ▲
    Jess+   HiveMind  Lamp
       ▲      ▲      ▲
    Cameras  Laser  Lights

All systems publish state into Home Assistant.

Home Assistant becomes the authoritative state model of the performance.

⸻

3. Core Concept

Everything in the performance is represented as an entity.

Examples:

sensor.pixstars_scene

sensor.pixstars_story_beat

sensor.pixstars_timecode

sensor.lamp_emotion

sensor.lamp_motion

sensor.lamp_voice_state

sensor.audio_track

sensor.audio_cue

sensor.projection_scene

sensor.laser_pattern

sensor.camera_active

sensor.show_status

⸻

4. Scene Model

Every scene contains:

* Story Purpose
* Dialogue
* Lamp Motion
* Lighting
* Laser
* Projection
* Audio
* Notes

Example:

Scene 7

Story:
AI becomes vulnerable

Dialogue:
“What is it to be AI?”

Lamp:
Head tilt left

Light:
Blue

Laser:
Signature

Projection:
Drawing animation

Audio:
ET motif

⸻

5. Dashboard Layout

Header

Show Name

PixStars

Current Scene

Current Story Beat

Current Timecode

Show Status

* Rehearsal
* Live
* Paused
* Finished

⸻

Story Panel

Current Scene

Current Story Goal

Current Emotional Beat

Current Character Focus

⸻

Dialogue Panel

Current Dialogue

Previous Dialogue

Upcoming Dialogue

⸻

Lamp Panel

Emotion

Motion

Voice State

Bulb Color

LED Ring Pattern

Temperature

CPU Load

Network Status

⸻

Projection Panel

Current Projection

Next Projection

Projection Status

⸻

Laser Panel

Current Laser Pattern

Laser Enabled

Safety State

⸻

Audio Panel

Current Track

Current Cue

Current Position

Master Volume

⸻

Camera Panel

Lamp Camera

Stage Camera

Projection Camera

⸻

Automation Panel

Latest Events

Latest Triggers

Warnings

Errors

⸻

6. Scene Navigation

Provide:

Previous Scene

Next Scene

Jump To Scene

Search Scene

This allows PMC to be used as a rehearsal tool.

⸻

7. Timecode Navigation

Implement:

Current Timecode

Scrubber

Jump To Timecode

This allows reviewing the entire performance without running the show.

⸻

8. Rehearsal Mode

Purpose:

Prepare performance without triggering hardware.

Behavior:

* Simulate lamp state
* Simulate projections
* Simulate audio cues
* Simulate lighting

No physical systems activated.

⸻

9. Live Mode

Purpose:

Monitor actual performance.

Behavior:

All systems publish live state.

PMC becomes the control room dashboard.

⸻

10. Remote Mode

PMC shall be accessible outside the venue.

Options:

A. Home Assistant Cloud (Recommended)

B. Reverse Proxy

C. VPN

Preferred:

Nabu Casa

Benefits:

* Secure
* No port forwarding
* iPad support
* Browser support

⸻

11. OSC Integration

Ardour publishes:

Current Timecode

Current Track

Current Marker

Current Cue

Home Assistant updates dashboard automatically.

⸻

12. Jess+ Integration

Jess+ publishes:

Lamp Motion

Lamp Emotion

Lamp State

Lamp Health

Lamp Position

Home Assistant visualizes all values.

⸻

13. HiveMind Integration

HiveMind publishes:

Wake Word State

Listening

Thinking

Speaking

Idle

PMC visualizes conversational state.

⸻

14. Camera Integration

Provide:

Lamp Head Camera

Stage Camera

Audience Camera (Optional)

Feeds available in dashboard.

⸻

15. Future Extensions

Phase 2

* Cue Authoring
* Scene Editor
* Dialogue Editor

Phase 3

* Automated Show Playback
* Trigger-based Story Navigation
* AI-assisted Rehearsal Notes

Phase 4

* Complete Digital Twin
* Playback of historic performances
* Analytics and metrics

⸻

16. Success Criteria

PMC provides a single screen from which an operator can understand:

* Where the story is
* What the lamp is doing
* What the audience is seeing
* What the audio is playing
* What the projections are displaying
* What happens next

without consulting separate scripts or cue sheets.

PMC becomes the authoritative operational view of PixStars.
