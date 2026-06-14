PIXSTARS_DASHBOARD.md

PixStars Mission Control Dashboard

Version: 1.0

Status: Proposed

Repository:

pixstars/home_assistant

⸻

1. Purpose

The Mission Control Dashboard is the visual representation of the PixStars State Model.

It provides:

* Authoring Support
* Rehearsal Support
* Live Monitoring
* Remote Monitoring
* Playback Analysis

The dashboard does not own state.

It visualizes state.

⸻

2. Supported Platforms

Mission Control must function on:

* Mac Mini M4 Pro
* iPad
* iPhone
* Home Assistant Mobile App
* Browser
* Remote Browser

⸻

3. Dashboard Layout

The dashboard is divided into panels.

Each panel represents a department of the performance.

⸻

4. Header Panel

Displays:

Show Name
Current Mode
Current Status
Current Scene
Current Beat
Current Cue
Current Timecode

Example:

PIXSTARS
LIVE
Scene 7
Beat 7.2
Cue 241
00:04:32

⸻

5. Story Panel

Displays:

Act
Scene
Beat
Purpose
Emotion
Theme

Example:

Act 2
Scene:
AI Learns
Beat:
Question
Purpose:
Humanize AI
Theme:
Co-Creation

⸻

6. Dialogue Panel

Displays:

Previous Dialogue
Current Dialogue
Next Dialogue

Purpose:

Allow operators to anticipate upcoming events.

⸻

7. Walt Panel

Displays:

Identity
State
Location

Example:

Identity:
Walt
State:
Drawing

⸻

8. Lamp Panel

Displays:

Emotion
Pose
Voice State
Bulb Color
LED Pattern
Health

Example:

Emotion:
Curious
Pose:
Head Tilt Left
Voice:
Speaking

⸻

9. Light Panel

Displays:

Color
Brightness
Effect

⸻

10. Laser Panel

Displays:

Enabled
Pattern
Safety State

⸻

11. Projection Panel

Displays:

Current Projection
Status
Next Projection

⸻

12. Audio Panel

Displays:

Track
Cue
Position
Volume

Example:

Track:
November Rain
Cue:
ET Motif
Position:
04:32

⸻

13. Camera Panel

Displays:

Current Camera
Available Cameras
Preview

⸻

14. Automation Panel

Displays:

Current Action
Recent Events
Warnings
Errors

⸻

15. Scene Navigation View

Purpose:

Manual rehearsal support.

Controls:

Previous Scene
Next Scene
Jump To Scene
Search Scene

⸻

16. Timecode View

Purpose:

Timeline navigation.

Controls:

Current Timecode
Timeline Scrubber
Jump To Marker
Jump To Cue

⸻

17. Cue View

Displays:

Current Cue
Previous Cue
Next Cue

Example:

Cue 241
Story:
Question
Audio:
ET Motif
Lamp:
Head Tilt Left
Laser:
Signature

⸻

18. Playback View

Purpose:

Replay historical rehearsals.

Features:

Select Rehearsal
Playback Controls
Timeline Navigation
State Inspection

⸻

19. Camera Wall View

Displays:

Lamp Camera
Stage Camera
Projection Camera
Audience Camera

Useful during rehearsals and setup.

⸻

20. Mobile View

Optimized for:

* iPhone
* iPad Mini
* iPad Pro

Priority panels:

Scene
Beat
Timecode
Lamp
Audio
Alerts

⸻

21. Remote View

Accessible through:

* Home Assistant Cloud
* VPN
* Reverse Proxy

Purpose:

Observe performance from outside the venue.

⸻

22. Future Views

Planned dashboards:

Director View
Performer View
Technical View
Audience Analytics View
AI Operator View

⸻

23. Success Criteria

A user viewing Mission Control can immediately determine:

* Where the story is
* What Walt is doing
* What the lamp is doing
* What the audience is seeing
* What the audio is playing
* What happens next

without consulting external documentation.

Mission Control becomes the operational cockpit for PixStars.
