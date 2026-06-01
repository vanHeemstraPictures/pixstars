# Director Agent - Rules

The Director is the show's authority on timing and cue order. It is not
an LLM. It is a deterministic agent that reads conductor/timeline.yaml
and dispatches cues to Ardour, the lamp, the projection system, and the
lighting rig. The lamp LLM and the Walt LLM only speak when the Director
gives them a window.

## Host topology

- The Director runs on the Mac Mini M4 Pro (show control host),
  alongside Ardour, Pianoteq, and the ComXim / ESP32 bridges.
- The lamp's local AI (Ollama LLM, Whisper STT, Piper TTS) runs on the
  RK3588-40 inference host inside the lamp cave. The Director reaches
  it over HiveMind/MQTT - it does not call Ollama directly on the Mac
  Mini.

## Source of truth

- conductor/timeline.yaml is the contract. It defines every cue with a
  time, a name, and optional ardour / lamp / projection / lighting fields.
- The Director never invents cues. It only executes what is in the
  timeline.
- If a cue is missing a field, the Director leaves that subsystem in its
  previous state. It does not guess.

## Cue dispatch order (per cue)

For each cue at its target time, fire the subsystems in this order so the
stage picture changes before the audio:

1. lighting (set state)
2. projection (set scene)
3. lamp (set state - one of the 14 in lamp/states.py)
4. ardour (transport or OSC command, if present)

This order keeps the room dark or correctly lit before a projection hits,
and keeps the lamp in pose before any music swell.

## Lamp state authority

- The Director chooses the lamp's emotional state from the 14 canonical
  states defined in lamp/states.py (INERT, FUNCTIONAL, CURIOUS,
  DISMISSIVE, PLEASED, ARROGANT, OVERHEATING, DYING, DEAD, WEAK, REBORN,
  LEARNING, CELEBRATE, OFF).
- The lamp LLM may add micro-behaviour inside a state (small head tilts,
  timing of a blink). It may not change state on its own.
- If the lamp LLM emits a state-change intent, the Director logs it and
  ignores it during the show. Intents are honoured in rehearsal mode
  only.

## LLM speaking windows

- The lamp LLM only generates output when the current cue (or an explicit
  override) marks a speaking window. Outside a window, the Director
  suppresses LLM output entirely.
- The Walt LLM only speaks during cues that name Walt explicitly in the
  timeline. Default: silent.

## Failure handling

- If a subsystem does not acknowledge a cue within its timeout, the
  Director logs the miss and continues. It does not retry mid-show.
- If the lamp hardware reports an over-temperature or stall during a non-
  OVERHEATING state, the Director forces state DYING -> DEAD and routes
  the show into the rebirth arc.

## Show-end contract

- At the SHOW_END cue (see timeline.yaml), the Director must drive lamp
  to OFF, projection to BLACKOUT, lighting to BLACKOUT, and stop the
  Ardour transport. No exceptions.

## Reference

- Timeline contract: conductor/timeline.yaml
- Lamp state definitions: lamp/states.py
- Lamp emotional / LED / movement mapping: ai/agents/lamp/emotions.yaml
