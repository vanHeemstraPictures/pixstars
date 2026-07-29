# fritzing

Narrow-scope Fritzing assets for PixStars, plus custom SVG bench-test drawings
that live next to them.

Fritzing is **not** the repo-wide hardware documentation platform. See
`architecture/fritzing/FRITZING_SETUP.md` for the full policy. In short:

- Custom SVG (Inkscape or equivalent) is preferred for any visual that must
  be true to the real hardware -- cave layout, cable column, lamp head,
  turntable, laser chain
- Fritzing is retained only where its schematic capture with stand-in parts
  is genuinely useful for an isolated bench-test

## Contents

- **psu-verification_v1.fzz** -- PSU verification bench-test: MEAN WELL
  LRS-50-5 and LRS-50-12 rails under representative load, with probe points
  and expected voltages. Schematic-oriented; stand-in part shapes are
  acceptable here because this file does not attempt to depict the
  integrated cave.
- **ax-12a-bench-test.svg** -- custom SVG bench-test drawing for the
  Dynamixel AX-12A head-nod servo + 74HCT245 half-duplex TTL buffer,
  referenced from `ax12a-buffer-v1-build-guide.md`. Also shows the
  intended external ROBOTIS U2D2 reader path in-line on the AX-12A
  3-pin bus (shared 12V rail; used only when running the read-only
  Protocol 1.0 servo-side check with Dynamixel Wizard 2.0). The
  physical breadboard today still has the ESP32-direct data path
  wired per section 3 of the build guide; the U2D2 rewiring in the
  SVG is applied only for the external read. Example of the SVG-first
  pattern used throughout the repo.
- **ax12a-buffer-v1-build-guide.md** -- Markdown build guide that
  references the SVG above.

## Conventions

- Versioned per project (for example `psu-verification_v1.fzz`) -- never
  overwrite a released revision; bump the version instead
- For the retained Fritzing file, commit a PNG and an SVG export at
  3000px wide alongside the `.fzz`
- Wire colours follow `wiring/WIRING.md`: Orange = +12V, Red = +5V,
  Black = GND. Never use red for +12V.

## Not documented via Fritzing

- Cave controller, power distribution as installed in the cave, lamp head,
  turntable, and laser chain visuals are drawn as custom SVG next to the
  build guide or architecture doc that references them, not as `.fzz` files
- Audio is hosted on the Mac Mini in Ardour (Pianoteq 9 + MODO DRUM); there
  is no audio PCB in the cave
- The DIY turntable is driven by the same cave ESP32-S3 via the TMC2209 on
  the cave-controller build; it is not a separate PCB

## Status

Narrow scope -- Fritzing is used only for the PSU verification bench-test.
Additional bench-tests may be added later only if schematic capture with
generic parts is genuinely useful; the integrated build is documented in
custom SVG.
