# AI Models - Model Configs

This folder holds local model configuration for the Pixstars AI stack.
The target deployment platform for local models is the RK3588-40
inference host inside the lamp cave: Ollama (local LLM), Whisper (STT),
and Piper (TTS) all run there. Everything in this folder is config
about which model to load and how to load it.

The Mac Mini M4 Pro is the show control host (Director, Ardour,
Pianoteq, ComXim / ESP32 bridges); it does not run inference for the
lamp brain. It talks to the RK3588-40 over HiveMind/MQTT.

## Default models

- Lamp agent: llama3.1 (Ollama default tag)
- Walt agent: llama3.1 (same model, different system prompt)
- Director:   none - the Director is deterministic, not an LLM

## What goes here

Per-agent or per-role config files. Examples (create as needed):

- lamp.json     - Ollama parameters for the lamp (temperature, top_p,
                  num_ctx, system prompt path, stop tokens)
- walt.json     - same shape, tuned for Walt's quieter cadence
- models.lock   - pinned model digests so the show machine cannot drift
                  between rehearsal and performance

## Why pin versions

The October 2026 performance must be reproducible. Model upgrades
between rehearsal and show have changed character voice in past
experiments. Always pin and verify with "ollama show <model>" before the
final tech week.

## What does not go here

- The model weights themselves (Ollama manages those in its own store).
- API keys (the entire AI stack is local; no remote APIs in the show
  path).
- The system prompts (those live in ai/agents/<role>/system_prompt.md).

## Recommended sampling for the lamp

Starting point, to be tuned:

- temperature: 0.7
- top_p:       0.9
- num_ctx:     2048
- stop:        ["\n\n"]

Short outputs are correct. If the model is producing paragraphs, lower
temperature first, then shorten num_ctx, then revisit the system prompt.

## Reference

- Ollama:   https://ollama.com
- Lamp prompt: ai/agents/lamp/system_prompt.md
- Walt prompt: ai/agents/walt/system_prompt.md
