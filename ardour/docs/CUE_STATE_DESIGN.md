# Cue State Design

## Standard state flow

For most spoken cues:

1. `thinking` just before playback
2. `speaking` during playback
3. `idle` after playback

## Optional richer sequence

1. `listening`
2. `thinking`
3. `speaking`
4. `idle`

## Example

A cue with a dramatic reveal might:

- set `thinking`
- wait 0.5 seconds
- start playback
- set `speaking`
- return to `idle` at end
