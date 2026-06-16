# ax12a-buffer

Dynamixel AX-12A half-duplex TTL buffer for the cave ESP32-S3
(Cave Architecture v3).

## Purpose

The AX-12A (head nod servo, sitting in the lamp head) uses a single-wire,
half-duplex TTL serial bus. The ESP32-S3 only has full-duplex UARTs, so this
board provides:

- **74HCT245** (or 74HC241 + direction logic) bidirectional buffer that ties
  the ESP32 TX and RX onto a single Data line driven from a direction-control
  GPIO (typical Dynamixel TTL buffer topology)
- **Voltage divider / level shifter** to keep AX-12A logic levels in spec
  while presented to the 3.3V ESP32-S3 RX

The AX-12A motor power (typically ~9-12V) comes from the cave 12V rail via
the power-distribution board; this buffer only handles the signal bus.

## Connections

- ESP32-S3: TX, RX, DIR (GPIO), GND, 3.3V (buffer logic supply)
- AX-12A bus: Data (single wire), GND, VDD (motor rail, pass-through only)
- Routed through the central cable column to the lamp head AX-12A

## Notes

- Keep the buffer physically close to the ESP32 to minimize reflections on
  the ESP-side signals
- The AX-12A bus runs at 1 Mbps by default; series termination resistor
  footprint included on the bus side
- The AX-12A is explicitly NOT on the Pololu Mini Maestro -- the Maestro
  handles only the analog hobby servos (MG996R, MG90S)

## Status

Phase 1 -- documentation only. No .fzz yet (added in a separate task).
