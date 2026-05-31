# WIRING.md

# Pixstars Lamp Wiring Guide

## Purpose

This document describes the physical wiring standards for the Pixstars
animatronic lamp.

The goal is to create a reliable, maintainable stage prop inspired by
Luxo Jr. where the electronics disappear and the audience experiences a
living character.

This guide covers Raspberry Pi Zero 2 WH GPIO wiring, WS2812 RGB LED
installation, soldering, JST connectors, Dupont connectors, wire colors,
speaker wiring, and cable routing. It also documents the cave servo
stack hidden under the ComXim turntable (ESP32 DevKit, Pololu Mini
Maestro 24-channel, MG996R and MG90S servos, MEAN WELL LRS-50-5 PSU)
and the ComXim MTxRUWSLPro programmable turntable used for base
rotation.

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

------------------------------------------------------------------------

# WS2812 LED Ring

The LED ring has:

-   PWR 5V
-   GND
-   D0
-   D1

Use:

    Pi Pin 2  (5V)      -> LED PWR 5V
    Pi Pin 6  (GND)     -> LED GND
    Pi Pin 12 (GPIO18)  -> 330 ohm resistor -> LED D0

D1 is unused unless another LED ring is chained.

------------------------------------------------------------------------

# 330 Ohm Resistor

Install in the data line:

    GPIO18
     |
    330 ohm resistor
     |
    LED D0

The resistor protects the first LED from signal spikes.

------------------------------------------------------------------------

# 1000uF Capacitor

Use:

    1000uF electrolytic capacitor
    10V or higher recommended

Connect:

    LED 5V  -> capacitor +
    LED GND -> capacitor -

The stripe on the capacitor indicates the negative side.

Place close to the LED ring.

------------------------------------------------------------------------

# JST-SM 3 Pin Connector

Recommended for the removable lamp head:

    LED Ring
       |
    short soldered wires
       |
    JST connector
       |
    lamp arm wiring
       |
    Raspberry Pi Zero 2 WH

Typical colors:

    Red   = 5V
    Green = Data
    Black = Ground

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

    WS2812 Ring

    PWR 5V -> Red wire
    D0     -> Green wire
    GND    -> Black wire

            |
            |
       JST connector

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

-   WS2812 5050 RGB LED Ring 16 (rear-facing, towards air vents)
-   Olight Sphere (front-facing bulb replacement, magnetic mount)
-   Dynamixel AX-12A (head nod servo, TTL serial from ESP32 in cave)
-   Logitech C920 webcam
-   Raspberry Pi Zero 2 WH (nervous system -- audio I/O, sensors,
    LED ring control)
-   Microphone
-   40mm speaker

Keep weight low.

------------------------------------------------------------------------

# Cave Components (Under ComXim Turntable)

The cave is the hidden enclosure beneath the ComXim turntable, sitting
on the riser block. The lamp itself contains no motors -- all servo
hardware lives here.

The cave contains:

-   ESP32 DevKit (WiFi bridge from Mac Mini, drives Maestro and AX-12A)
-   Pololu Mini Maestro 24-channel servo controller
-   4x MG996R servos (lower arm, elbow, spares)
-   1x MG90S servo (neck pan, carbon fibre push-pull rod)
-   MEAN WELL LRS-50-5 power supply (5V servo rail)
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
    - LED Ring (Pi GPIO)
    - Olight Sphere (magnetic, self-contained)
    - AX-12A (TTL serial via cable column)
    - Speaker, Mic
    - Pi Zero 2 WH
    - Webcam

         |

    Cable Column (central)

         |

    Cave (under ComXim turntable)
    - ESP32
    - Maestro + Servos
    - RK3588-40
    - MEAN WELL PSU

         |

    ComXim Turntable (base rotation)

         |

    Riser Block

         |

    Piano Top

------------------------------------------------------------------------

# Testing Before Assembly

Test:

1.  LED ring animations (Pi GPIO)
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
