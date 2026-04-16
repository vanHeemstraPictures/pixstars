# Dataset Guide

## Core principle

Treat the Pixstars lamp as a character, not as a generic TTS voice.

## Dataset structure

Recommended CSV columns:

- `id`
- `episode`
- `scene`
- `text`
- `emotion`
- `delivery_notes`
- `filename_hint`

## Example

```csv
id,episode,scene,text,emotion,delivery_notes,filename_hint
1,1,opening,"Hello...",curious,"soft, hesitant, warm",lamp_001_hello_curious
2,1,opening,"I am here...",warm,"gentle, intimate",lamp_002_i_am_here_warm
3,2,conflict,"Please... stay.",fragile,"small, breath-led",lamp_003_please_stay_fragile
```

## Suggested emotions

- curious
- warm
- fragile
- wounded
- hopeful
- playful
- solemn

## Practical rule

Keep lines short. Let the lamp search for words. Use punctuation to create pauses.
