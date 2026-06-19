# fritzing

Fritzing source files (.fzz) for the PixStars cave electronics.

## Conventions

- One .fzz per PCB; filename matches the directory name under
  electronics/pcbs/
- Versioned per board (e.g. cave-controller_v1.fzz) -- never overwrite a
  released revision; bump the version instead
- Exports (Gerbers, BOM, schematic PDF) live under electronics/exports/,
  not here
- Manufacturing drops (AISLER project files, README per order) live under
  electronics/manufacturing/aisler/

## Planned .fzz files (Cave Architecture v3)

- **cave-controller_v1.fzz** -- ESP32-S3 N16R8 DevKit carrier; routes to
  Maestro (UART), AX-12A buffer (UART + DIR), WS2812 ring (RMT GPIO), and
  TMC2209 stepper driver (STEP / DIR / ENABLE + Hall sensor input) for the
  DIY turntable
- **power-distribution_v1.fzz** -- cave power rails:
  5V (MEAN WELL LRS-50-5) for servos + LED ring, 12V (MEAN WELL LRS-50-12)
  for LPLDD-1A-16V-3CH laser driver and TMC2209 stepper, with star-ground
  topology
- **ax12a-buffer_v1.fzz** -- 74HCT245-based half-duplex TTL buffer +
  voltage divider for the lamp head Dynamixel AX-12A head-nod servo
- **led-adapter_v1.fzz** -- WS2812 ring break-in: 330 ohm series on DATA,
  1000 uF bulk near ring, JST-SM 3-pin connector at the lamp head end of
  the central cable column

## NOT planned as a PCB

- **audio** -- audio is hosted on the Mac Mini in Ardour
  (Pianoteq 9 + MODO DRUM); there is no audio PCB in the cave
- **turntable controller** -- the DIY turntable is driven by the same cave
  ESP32-S3 via the TMC2209 on the cave-controller board; it is not a
  separate PCB

## Status

Phase 1 -- documentation only. .fzz files are added in a separate task.
