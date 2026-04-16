# Shared Lamp States

The Pixstars lamp uses these canonical states:

- `idle`
- `listening`
- `thinking`
- `speaking`
- `error`

These state names should be used consistently across:

- Pi LED service
- Pi playback wrapper
- Mac control scripts
- optional Home Assistant integration
- optional Ardour-triggered state hooks
