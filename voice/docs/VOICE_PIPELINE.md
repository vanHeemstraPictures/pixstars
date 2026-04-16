# Voice Pipeline

## Goal

Create an original synthetic lamp voice for Pixstars.

## Recommended high-level path

1. Collect lamp dialogue from episodes
2. Normalize dialogue into a structured dataset
3. Label key emotional states
4. Generate or prepare a base voice corpus
5. Transform toward the lamp character
6. Train or fine-tune a compact model
7. Render final WAV lines
8. Import final WAV lines into Ardour

## Voice design target

The lamp voice should feel:

- small
- warm
- fragile
- curious
- slightly raspy
- emotionally readable

Avoid:

- chipmunk exaggeration
- metallic robot tone
- over-polished assistant voice

## Output conventions

Render final lines to:

```text
voice/output/final_wav/
```

Recommended naming:

```text
lamp_001_hello_curious.wav
lamp_002_please_stay_fragile.wav
lamp_003_i_remember_you_warm.wav
```


## Hivemind automation layer

This repository also supports a Hivemind-managed orchestration layer on the Mac Mini.

Recommended division:

- local scripts in `voice/scripts/` do the actual file and render work
- Hivemind agents decide when to run those scripts, inspect results, and promote approved assets

See:
- `docs/HIVEMIND_VOICE_AUTOMATION.md`
- `voice/orchestration/`
