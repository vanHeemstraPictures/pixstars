# power-distribution

Cave power distribution board (Cave Architecture v3).

## Purpose

Centralize the cave power rails so that logic, servos, LEDs, the laser
driver, and the stepper driver each get clean, separated power with proper
return paths and protection.

## Inputs

- **MEAN WELL LRS-50-5** -- 5V rail for servos and the WS2812 LED ring
  (kept separate from logic to avoid servo brownouts on the ESP32)
- **MEAN WELL LRS-50-12** -- shared cave 12V rail
- **+/-24V galvo PSU** -- dedicated dual-rail supply for the 40kpps galvo
  driver board (included with the galvo scanner set); routed through the
  cave but not generated here

## Outputs

- 5V to Pololu Mini Maestro and MG996R / MG90S servos
- 5V to the WS2812 LED ring (through the led-adapter board, then the central
  cable column up to the lamp head)
- 5V logic to the ESP32-S3 cave-controller (separately fused / filtered)
- 12V to the LPLDD-1A-16V-3CH laser driver (drives the Opt Lasers 300mW
  Micro RGB module)
- 12V to the TMC2209 stepper driver (NEMA 17 turntable motor)

## Notes

- Star-ground topology; servo and LED returns kept off the logic ground until
  a single tie point near the input
- Bulk capacitance on the 5V servo rail to absorb stall transients
- Fuse / polyfuse per major output
- Connector pinouts to mirror the cave layout (servo rail on top, ESP32 on
  end, lamp head cable column central)

## Status

Phase 1 -- documentation only. No .fzz yet (added in a separate task).
