# OPTIMIZED_PIXSTARS_ARCHITECTURE.md

## Best merged solution for Pixstars

This document merges the strongest ideas from:

- the existing Pixstars HiveMind + Pi + Mac Mini approach
- the thin-endpoint philosophy demonstrated by the Mark II Assist project

## Short conclusion

For Pixstars, the best architecture is:

### Lamp head = thin embodied endpoint

The lamp head should mainly provide:

- microphone
- speaker
- LED state system
- lightweight client software
- network connection

### Mac Mini M4 Pro = central brain

The Mac Mini should provide:

- HiveMind server
- STT
- wake-word pipeline coordination
- response orchestration
- synthetic voice generation
- Ardour cue integration
- optional Home Assistant / automation integration

## Why this is the best fit

The endpoint device is most reliable when it acts as a smart audio endpoint, while the heavier voice pipeline lives centrally.

For Pixstars, that maps beautifully onto your stage architecture:

- the audience sees the lamp
- the lamp emits sound and light
- the real intelligence lives offstage in the Mac Mini

This improves:

- thermal behavior inside the lamp
- maintainability
- debugging
- performance stability
- upgrade flexibility

## Practical architecture

Audience↓Lamp head (Pi: mic + speaker + LED + lightweight client)↓Local network↓Mac Mini M4 Pro (HiveMind + STT + synthetic voice + Ardour + orchestration)↓Reply audio + state↓Lamp head speaker + LED embodiment

## What stays on the Pi

Keep these responsibilities on the Pi:

- boot reliably
- join Wi-Fi
- expose mic and speaker
- run the LED state machine
- accept state updates
- play returned audio
- optionally host a very light satellite client

## What moves to the Mac Mini

Move these responsibilities to the Mac whenever possible:

- wake-word coordination
- speech recognition
- conversation logic
- synthetic voice generation
- voice-state logic
- emotional voice selection
- deterministic cue playback control
- logging and monitoring

## Wake word strategy

For your show, the best default is:

- keep the conceptual wake word as **Hey A.I.**
- do not over-optimize wake-word detection on the Pi until the core thin-endpoint path is stable
- let the Mac Mini remain the main control point for voice interaction

If you later want faster local responsiveness, you can add local wake-word handling as a second-phase optimization.

## LED integration principle

Keep the LED system on the Pi.

Recommended mapping:

- idle → warm amber breathing
- listening → blue pulse
- thinking → purple pulse
- speaking → orange/yellow tied to audio level
- error → red warning pulse

## Ardour integration principle

Use Ardour for:

- timing-critical lines
- exact music synchronization
- emotionally important cues that must land at precise times

Use HiveMind / interactive logic for:

- improvised moments
- live interaction
- reactive dialogue
- non-critical exchanges

## Recommended implementation order

1. Prove the Pi as a thin audio + LED endpoint
2. Prove the Mac Mini server stack
3. Prove pairing and roundtrip communication
4. Prove state-based LED behavior
5. Prove returned audio playback from the Mac
6. Add the “Hey A.I.” flow
7. Add synthetic voice
8. Add Ardour cue-state coupling
9. Only then refine latency and optional local wake-word handling

## References

- Open Source Conversational AI Community thread:[https://community.openconversational.ai/t/repurposing-the-mycroft-mark-ii-as-a-home-assistant-voice-satellite-mark2-assist/22044](https://community.openconversational.ai/t/repurposing-the-mycroft-mark-ii-as-a-home-assistant-voice-satellite-mark2-assist/22044)
- andlo/mark2-assist:[https://github.com/andlo/mark2-assist](https://github.com/andlo/mark2-assist)
- HiveMind Core:[https://github.com/JarbasHiveMind/HiveMind-core](https://github.com/JarbasHiveMind/HiveMind-core)
- HiveMind microphone satellite:[https://github.com/JarbasHiveMind/hivemind-mic-satellite](https://github.com/JarbasHiveMind/hivemind-mic-satellite)