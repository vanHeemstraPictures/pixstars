# AI Tools - Tool Calling Architecture

This folder holds the Python tool functions the local LLM (Ollama) can
call when the Director gives it a speaking / acting window. Tools are
how the lamp acts on the world.

## Planned tools

Stubs to be implemented (do not exist yet):

- home_assistant.py  - lighting, RGB ring colour/effect, Olight Sphere
                       bulb, smart device control via the Home Assistant
                       REST or WebSocket API
- ardour.py          - OSC commands to the running Ardour session
                       (transport, locate, mute/unmute stems, trigger
                       one-shot WAVs)
- digiscore.py       - send intent events to the show Director (e.g.
                       "lamp_is_alive") so the Director can decide
                       whether to honour them
- emotion_engine.py  - set the lamp's current state from the 14 canonical
                       states (INERT, FUNCTIONAL, CURIOUS, ... OFF) and
                       drive the LED ring + servo bounds accordingly

## Calling convention

Each tool exposes one or more plain Python functions with:

- type-annotated arguments
- a short docstring (this is what the LLM reads to decide whether to
  call the tool)
- a JSON-serialisable return value

The Ollama tool-calling adapter introspects the docstrings and signature
to build the tool schema. Do not hand-write JSON schemas; let the
adapter generate them.

## Authority boundary

Tools can request action. The Director decides whether the request is
allowed at the current cue. In show mode, most lamp-initiated state
changes are logged and ignored; in rehearsal mode they are honoured. See
ai/agents/director/rules.md for the contract.

## Safety boundary

Every tool call is logged. No tool may:

- speak as the lamp (that goes through the LLM + Safety agent)
- write to ai/memory/lamp_memory.yaml at runtime
- touch files outside this repo

## Reference

- Director rules: ai/agents/director/rules.md
- Safety rules:   ai/agents/safety/guardrails.md
- Lamp states:    lamp/states.py
- LED / movement: ai/agents/lamp/emotions.yaml
