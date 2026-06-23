# ROBOTICS_VOICE.md

Version: 1.0

Purpose

Voice is the primary communication channel between PixStars and humans.

The audience should perceive:

* Thought
* Intent
* Emotion

through voice.

⸻

Voice Stack
```
Microphone
↓
Wake Word
↓
Speech Recognition
↓
Intent Processing
↓
Character Engine
↓
Speech Synthesis
↓
Speaker
```
⸻

Recommended Technologies

Wake Word

Hey A.I.

Technology:

* OpenVoiceOS
* HiveMind

⸻

Speech Recognition

Options:

* Vosk
* Whisper
* OVOS

⸻

Character Processing

Responsibilities:

* Context
* Emotion
* Memory
* Story Awareness

⸻

Speech Synthesis

Options:

* Piper
* OVOS TTS

Goal:

An E.T.-inspired character voice.

⸻

Voice States
```
Silent
Listening
Thinking
Speaking
Whispering
Performing
```
⸻

Emotional Voice Mapping

Curious:

* Slightly higher pitch
* Faster cadence

Proud:

* Stronger delivery

Sad:

* Slower delivery

Remorseful:

* Quiet delivery

⸻

MQTT Topics
```
pixstars/voice/input
pixstars/voice/output
pixstars/voice/state
pixstars/voice/emotion
```
⸻

Performance Mode

During live performance:

Timeline has priority.

Character voice remains synchronized with:

* Ardour
* Jess+
* Mission Control

⸻

References

ROBOTICS_CHARACTER_ARCHITECTURE.md

VOICE_SERVICE.md

OpenVoiceOS

HiveMind

Learn Robotics Programming (3rd Edition)

https://github.com/PacktPublishing/Learn-Robotics-Programming-3rd-edition
