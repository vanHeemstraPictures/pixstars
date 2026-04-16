# Render Workflow

## Goal

Turn structured dialogue into final WAV assets for the show.

## Steps

1. Prepare `voice/data/dialogue.csv`
2. Filter dialogue by episode, scene, or emotion
3. Render dry WAV lines using your chosen synthetic voice engine
4. Optionally post-process variants
5. Export the selected final lines to `voice/output/final_wav/`
6. Generate a cue manifest for Ardour

## Render targets

Recommended final format:

- WAV
- mono
- 48 kHz
- 24-bit if convenient

## Variant strategy

Create 2 to 3 emotional variants for important lines.

Example:
- curious
- fragile
- reborn
