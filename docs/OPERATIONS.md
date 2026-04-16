# Operations

## Daily startup order

1. Boot the Mac Mini
2. Join the dedicated local network
3. Start the HiveMind server
4. Power on the Pi in the lamp
5. Confirm the satellite connects
6. Confirm LED service is running
7. Run a short mic / speaker test
8. Run a wake-word test
9. Run a short speaking-light test

## Daily shutdown order

1. Stop cue playback and interactions
2. Stop the Pi satellite if needed
3. Stop the HiveMind server
4. Power off the Pi
5. Power off the Mac Mini

## State file convention

The Pi LED service reads:

```text
/tmp/pixstars_lamp_state.txt
```

Supported values:

- `idle`
- `listening`
- `thinking`
- `speaking`
- `error`

## Practical rule

Use Ardour for exact-timing lines.
Use HiveMind for interactive lines.
