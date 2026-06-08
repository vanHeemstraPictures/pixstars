PIXSTARS_STATE_MODEL.md

PixStars State Model

Version: 1.0

Status: Proposed

Repository:

pixstars/home_assistant

⸻

1. Purpose

The PixStars State Model defines the authoritative representation of the performance.

All systems publish and consume state through this model.

The State Model is independent of:

* Home Assistant
* Ardour
* Jess+
* HiveMind
* Raspberry Pi
* Dashboard implementations

These systems are integrations.

The State Model is the source of truth.

⸻

2. Design Principles

Single Source of Truth

All performance state is represented once.

Example:

Current Scene = 7

must not exist independently in multiple systems.

⸻

Event Driven

State changes are published as events.

Example:

Scene Changed

Beat Changed

Projection Changed

Lamp Emotion Changed

⸻

Human Readable

State names should be understandable by:

* Performers
* Directors
* Operators
* Developers

⸻

Story First

The story drives technology.

Not the other way around.

⸻

3. Top-Level Structure

show:
story:
walt:
lamp:
light:
laser:
projection:
audio:
camera:
automation:
system:

⸻

4. Show Domain

Represents overall performance state.

show:
  mode:
  status:
  scene:
  beat:
  cue:
  timecode:

⸻

Mode

Allowed values:

authoring
rehearsal
live
playback
maintenance

⸻

Status

Allowed values:

stopped
starting
running
paused
finished
error

⸻

5. Story Domain

Represents narrative state.

story:
  act:
  scene:
  beat:
  purpose:
  emotion:
  theme:

Example:

story:
  act: 2
  scene: AI Learns
  beat: Question
  purpose: Humanize AI
  emotion: Curiosity
  theme: Co-Creation

⸻

6. Walt Domain

Represents the performer.

walt:
  identity:
  state:
  location:

⸻

Identity

axel
man
walt

⸻

State

playing
drawing
speaking
thinking
observing

⸻

7. Lamp Domain

Represents the character AI.

lamp:
  emotion:
  pose:
  voice_state:
  bulb_color:
  led_pattern:
  health:

⸻

Emotion

idle
curious
playful
confident
confused
hurt
learning
connected
joyful

⸻

Pose

neutral
look_left
look_right
look_up
look_down
head_tilt_left
head_tilt_right
celebrate

⸻

Voice State

idle
listening
thinking
speaking

⸻

8. Light Domain

light:
  color:
  brightness:
  effect:

Example:

light:
  color: warm_yellow
  brightness: 80
  effect: steady

⸻

9. Laser Domain

laser:
  enabled:
  pattern:
  safety_state:

Patterns:

off
signature
castle
mickey
we
team_rockstars

⸻

10. Projection Domain

projection:
  scene:
  status:

Examples:

guns_roses
castle
drawing
logo
off

⸻

11. Audio Domain

audio:
  track:
  cue:
  position:
  volume:

Example:

audio:
  track: november_rain
  cue: et_motif
  position: 272
  volume: 85

⸻

12. Camera Domain

camera:
  active:
  source:

Sources:

lamp_head
stage
projection
audience

⸻

13. Automation Domain

automation:
  current_action:
  last_event:

⸻

14. System Domain

system:
  health:
  network:
  cpu:
  memory:

⸻

15. Event Types

Required event categories:

scene_changed
beat_changed
cue_triggered
lamp_changed
projection_changed
laser_changed
audio_changed
camera_changed
system_warning
system_error

⸻

16. Historical Recording

All state changes should be retained.

Purpose:

* Replay rehearsals
* Analyze performances
* Debug failures
* Compare versions

⸻

17. Future Extensions

Future domains:

audience:
metrics:
analytics:
ai_assistant:

⸻

18. Success Criteria

Any subsystem can determine the complete state of the performance by querying the State Model.

No subsystem becomes the owner of performance state.

The State Model remains the authoritative representation of PixStars.
