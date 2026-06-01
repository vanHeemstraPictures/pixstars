# WIRING.md

# Pixstars Lamp Wiring Guide

## Purpose

This document describes the physical wiring standards for the Pixstars
animatronic lamp.

The goal is to create a reliable, maintainable stage prop inspired by
Luxo Jr. where the electronics disappear and the audience experiences a
living character.

This guide covers Raspberry Pi Zero 2 WH GPIO wiring (audio, sensors,
I2C to RK3588-40), WS2812 RGB LED installation (driven by the ESP32 in
the cave, not the Pi), soldering, JST connectors, Dupont connectors,
wire colors, speaker wiring, and cable routing. It also documents the
cave servo stack hidden under the ComXim turntable (ESP32 DevKit,
Pololu Mini Maestro 24-channel, MG996R and MG90S servos, MEAN WELL
LRS-50-5 PSU) and the ComXim MTxRUWSLPro programmable turntable used
for base rotation.

------------------------------------------------------------------------

# Design Philosophy

Avoid permanently wiring the entire lamp together.

A performance prop must be repairable.

The recommended pattern:

    Component
        |
    short soldered wires
        |
    removable connector
        |
    hidden cable route
        |
    controller electronics

------------------------------------------------------------------------

# Standard Wire Colors

  Function       Color             Purpose
  -------------- ----------------- ----------------
  +5V            Red               Power
  GND            Black             Ground
  DATA           Green / Yellow    Digital signal
  Servo signal   Orange / Yellow   PWM control
  Speaker +      Red               Audio
  Speaker -      Black             Audio return

------------------------------------------------------------------------

# Raspberry Pi Zero 2 WH Connections

The Pi Zero 2 WH already has a GPIO header.

Use:

    2.54mm Female Dupont jumper wires

The female Dupont connector slides over the Raspberry Pi pins.

The Pi handles audio I/O, sensors, and I2C to the RK3588-40.
The LED ring is NOT driven by the Pi -- it is driven by the ESP32
in the cave (see the WS2812 LED Ring section below).

------------------------------------------------------------------------

# WS2812 LED Ring

The LED ring has:

-   PWR 5V
-   GND
-   D0
-   D1

The LED ring lives in the lamp head. The driver electronics and power
sit in the cave. Three wires run through the cable column to reach the
ring:

    ESP32 GPIO (RMT) -> 330 ohm resistor -> DATA wire (cable column) -> LED D0
    MEAN WELL LRS-50-5 5V -> 5V wire (cable column) -> LED PWR 5V
    MEAN WELL LRS-50-5 GND -> GND wire (cable column) -> LED GND

The ESP32 logic ground and the MEAN WELL 5V ground must be tied
together (common GND) for the WS2812 data signal to be valid.

D1 is unused unless another LED ring is chained.

------------------------------------------------------------------------

# 330 Ohm Resistor

Install in the data line at the cave end, on the ESP32 GPIO output
before the wire enters the cable column:

    ESP32 GPIO
     |
    330 ohm resistor
     |
    DATA wire (cable column)
     |
    LED D0 (in the head)

The resistor protects the first LED from signal spikes.
Placing it at the cave end keeps the lamp head free of extra parts.

------------------------------------------------------------------------

# 1000uF Capacitor

Use:

    1000uF electrolytic capacitor
    10V or higher recommended

Connect:

    LED 5V  -> capacitor +
    LED GND -> capacitor -

The stripe on the capacitor indicates the negative side.

Place close to the LED ring, inside the lamp head.
This is the far end of the cable column 5V run, so the capacitor
smooths power right where the ring draws it.

------------------------------------------------------------------------

# JST-SM 3 Pin Connector

Recommended for the removable lamp head. The JST connector sits between
the cable column wires (coming up from the cave) and the LED ring's
short soldered tail in the head:

    LED Ring (in head)
       |
    short soldered tail
       |
    JST connector (mate point)
       |
    cable column wires
       |
    ESP32 / MEAN WELL PSU (in cave)

The three pins carry signals that all originate in the cave:

    Red   = 5V    (from MEAN WELL LRS-50-5)
    Green = Data  (from ESP32 GPIO via 330 ohm resistor)
    Black = Ground (common with ESP32 logic GND)

------------------------------------------------------------------------

# Soldering LED Ring

Do not solder long cables directly to the ring.

Create a short removable tail.

Steps:

1.  Tin the LED pad
2.  Tin the wire
3.  Join both briefly with the soldering iron

Recommended temperature:

    330 - 350 degrees Celsius

Avoid heating pads too long.

------------------------------------------------------------------------

# LED Ring Final Wiring

    WS2812 Ring (in head)

    PWR 5V -> Red wire
    D0     -> Green wire
    GND    -> Black wire

            |
            |
       JST connector
            |
            |
       Cable column (3 wires: 5V, DATA, GND)
            |
            |
       Cave:
         - DATA -> 330 ohm resistor -> ESP32 GPIO
         - 5V   -> MEAN WELL LRS-50-5 +5V
         - GND  -> MEAN WELL GND (common with ESP32 GND)

------------------------------------------------------------------------

# Strain Relief

A moving lamp head creates vibration.

Protect solder joints using:

-   heat shrink tubing
-   hot glue
-   internal cable fixing

The solder joint should carry electricity, not mechanical force.

------------------------------------------------------------------------

# Speaker Wiring

Architecture:

-   Anker speaker remains in the base
-   40mm 4 Ohm 3W speaker sits in the head
-   PAM8403 amplifier drives the head speaker

Connection:

    PAM8403 L+ -> Speaker +
    PAM8403 L- -> Speaker -

Place the amplifier in the base.

------------------------------------------------------------------------

# Lamp Head Components

The head contains:

-   WS2812 5050 RGB LED Ring 16 (rear-facing, towards air vents;
    controlled by ESP32 via cable column, powered by MEAN WELL PSU)
-   WS2812B 35-LED front ring (front-facing cone beam halo around
    the laser galvo aperture; separate data line from the rear
    ring, 5V from MEAN WELL PSU via cable column)
-   RGB Laser Galvo Scanner (vector laser galvo scanner that draws
    shapes/patterns via a steered laser beam -- NOT a video projector;
    2x galvo motors + mirrors and an RGB laser diode in the head,
    ~100-130 g total; analog X/Y signals (+/-5V differential, 4 wires),
    RGB TTL modulation (3 wires), and galvo motor power (+/-15V, 2
    wires) all arrive via the cable column from the cave galvo driver
    + ILDA DAC)
-   M5Stack Atom Echo (wake word capture; USB-serial / I2S audio to
    Pi Zero 2 WH)
-   Olight Sphere (front-facing bulb replacement, magnetic mount)
-   Dynamixel AX-12A (head nod servo, TTL serial from ESP32 in cave)
-   Logitech C920 webcam
-   Raspberry Pi Zero 2 WH (nervous system -- audio I/O, sensors,
    I2C to RK3588-40)
-   Microphone
-   40mm speaker

Keep weight low.

------------------------------------------------------------------------

# Cave Components (Under ComXim Turntable)

The cave is the hidden enclosure beneath the ComXim turntable, sitting
on the riser block. The lamp itself contains no motors -- all servo
hardware lives here.

The cave contains:

-   ESP32 DevKit (WiFi bridge from Mac Mini; drives Maestro, AX-12A,
    and the WS2812 LED ring via RMT GPIO + 330 ohm resistor through
    the cable column)
-   Pololu Mini Maestro 24-channel servo controller
-   4x MG996R servos (lower arm, elbow, spares)
-   1x MG90S servo (neck pan, carbon fibre push-pull rod)
-   MEAN WELL LRS-50-5 power supply (5V rail for servos and for the
    WS2812 LED ring via the cable column)
-   Seeed Studio reComputer RK3588-40 (lamp brain -- local AI inference)

------------------------------------------------------------------------

# Base Rotation

Base rotation is handled independently from the cave servo stack:

-   ComXim MTxRUWSLPro programmable turntable
-   Controlled via WiFi CT commands from Mac Mini (separate from
    ESP32 / Maestro)
-   Riser block (120-150mm) creates cave depth

------------------------------------------------------------------------

# Cable Routing

Recommended:

    Lamp Head
    - WS2812 LED Ring (rear, data + 5V + GND arrive via cable column)
    - WS2812B 35-LED front ring (data + 5V + GND, separate JST-SM
      3-pin from the rear ring)
    - RGB Laser Galvo Scanner (galvo motors + mirrors + RGB laser
      diode in the head; analog X/Y signals, RGB TTL modulation and
      galvo motor power all arrive via the cable column from the cave)
    - M5Stack Atom Echo (USB/serial to Pi Zero 2 WH inside the head)
    - Olight Sphere (magnetic, self-contained)
    - AX-12A (TTL serial via cable column)
    - Speaker, Mic
    - Pi Zero 2 WH
    - Webcam

         |

    Cable Column (central) -- bundle includes:
    - LED Ring rear (ESP32 GPIO via cable column): DATA + 5V + GND
    - LED Ring front 35-LED (separate JST-SM 3-pin): DATA + 5V + GND
    - Galvo X/Y analog signals: 4 wires (+/-5V differential)
    - Laser RGB TTL: 3 wires
    - Galvo motor power: 2 wires (+/-15V from cave PSU)
    - AX-12A TTL serial
    - Pi audio / sensor lines as needed

         |

    Cave (under ComXim turntable)
    - ESP32 (drives Maestro, AX-12A, and LED ring via RMT GPIO)
    - Maestro + Servos
    - RK3588-40
    - MEAN WELL PSU (5V to servos and to LED ring via cable column)

         |

    ComXim Turntable (base rotation)

         |

    Riser Block

         |

    Piano Top

------------------------------------------------------------------------

# Testing Before Assembly

Test:

1.  LED ring animations (ESP32 GPIO via cable column)
2.  Microphone input
3.  Speaker output
4.  AX-12A head nod sweep
5.  MG996R / MG90S servo sweep via Maestro
6.  ComXim base rotation (CW / CCW, origin return)
7.  ESP32 WiFi connectivity
8.  Cable reliability during full motion
9.  JST connector hold under vibration

Only close the lamp after movement testing.

------------------------------------------------------------------------

# Architecture Cross-Reference

This wiring guide describes the physical build. For the design
rationale and system-level overview, see:

-   architecture_decision_records/LAMP_ARCHITECTURE_v3.md
    -- full cave design and decisions
-   docs/architecture/ARCHITECTURE.md
    -- system overview
-   docs/architecture/architecture.png
    -- authoritative visual reference

If this guide and the architecture documents disagree, the
architecture documents are authoritative.

------------------------------------------------------------------------

# Final Principle

The audience sees a living character.

The builder creates a clean, modular, repairable system.

Good wiring is invisible magic.
