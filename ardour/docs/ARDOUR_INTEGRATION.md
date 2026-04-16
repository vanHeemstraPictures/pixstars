# Ardour Integration

## Goal

Use Ardour as the deterministic cue engine for Pixstars while preserving the lamp's state language.

## Recommended split

Use Ardour for:
- timing-critical lines
- exact musical sync points
- emotional beats that must land precisely

Use HiveMind for:
- interactive moments
- improvisational lines
- conversational responses

## Cue asset location

Place final imported WAV lines under a tracked manifest, for example:

```text
ardour/cues/cue_manifest.csv
```

## State integration

For each cue, define:

- cue id
- cue label
- audio file
- desired lamp state before cue
- desired lamp state during cue
- desired lamp state after cue
