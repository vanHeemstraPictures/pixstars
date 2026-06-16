# cave-controller

ESP32-S3 N16R8 DevKit carrier/breakout for the lamp cave (Cave Architecture v3).

## Purpose

Provide a clean, mountable interface between the cave ESP32-S3 and all
downstream cave subsystems. The ESP32-S3 is the single WiFi bridge from the
Mac Mini show-control host to the cave hardware; this board carries it.

## Interfaces

- **Pololu Mini Maestro 24-channel** servo controller (UART/serial from ESP32)
  - drives MG996R lower arm / elbow / spares + MG90S neck pan
- **Dynamixel AX-12A** head nod (TTL half-duplex serial via the
  ax12a-buffer board -- NOT on the Maestro)
- **WS2812 5050 RGB LED Ring 16** in the lamp head (ESP32 RMT peripheral GPIO,
  via the led-adapter board, through the central cable column)
- **TMC2209** stepper driver for the DIY ESP32-driven turntable
  (STEP / DIR / ENABLE), with a Hall effect sensor (SS49E/A3144) input for
  origin detection of the NEMA 17 + GT2 belt + 200mm lazy Susan bearing stack
- **ILDAWaveX16 V2** ILDA DAC -- not wired through this board; receives cues
  directly from the Mac Mini over WiFi/Ethernet (Ether Dream or IDN protocol)

## Power

- Logic 5V from the cave logic supply (separated from servo rail)
- Servo / LED 5V from MEAN WELL LRS-50-5 via the power-distribution board
- TMC2209 motor rail 12V from the shared cave 12V rail (MEAN WELL LRS-50-12)

## Status

Phase 1 -- documentation only. No .fzz yet (added in a separate task).
