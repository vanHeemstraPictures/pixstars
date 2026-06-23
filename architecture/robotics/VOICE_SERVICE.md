# VOICE_SERVICE.md

Version: 1.0

Purpose

The Voice Service is responsible for everything spoken by PixStars.

⸻

Responsibilities

* Speech Recognition
* Speech Synthesis
* Voice State Management
* Character Voice Rendering

⸻

Architecture
```
Microphone
↓
Wake Word
↓
Speech Recognition
↓
Character Service
↓
Speech Synthesis
↓
Speaker
```
⸻

Recommended Technologies

Wake Word

Hey A.I.

Speech Recognition
```
OpenVoiceOS
Whisper
Vosk
```
Speech Synthesis
```
Piper
OVOS TTS
```
⸻

Voice States
```
Silent
Listening
Thinking
Speaking
Performing
```
⸻

MQTT Topics
```
pixstars/voice/input
pixstars/voice/output
pixstars/voice/state
pixstars/voice/command
```
⸻

Emotional Integration

Curious

* Faster cadence

Proud

* Strong delivery

Sad

* Slower delivery

Remorseful

* Soft delivery

⸻

References

ROBOTICS_VOICE.md

EMOTION_SERVICE.md
