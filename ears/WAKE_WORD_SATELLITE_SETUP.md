# WAKE_WORD_SATELLITE_SETUP.md

# Pixstars Wake Word Satellite Setup

## Purpose

This document describes the wake word satellite architecture for the Pixstars animatronic lamp.

The goal is to allow the lamp to react naturally when someone says:

> "Hey A.I."

The wake word system acts as the ears of the character, while the rest of the Pixstars architecture remains responsible for intelligence, voice, movement, and emotion.

Selected device:

M5Stack Atom Echo Programmable Smart Speaker

Purchase references:

Amazon Netherlands:
https://www.amazon.nl/-/en/M5Stack-Atom-Echo-Programmable-Mini-Smart/dp/B0F6M8L6XF/

Manufacturer:
https://shop.m5stack.com/

---

# Architecture Decision

The M5Stack Atom Echo does not replace the existing Pixstars architecture.

It does NOT replace:

- Raspberry Pi Zero 2 WH
- WS2812 LED brain ring
- 40mm speaker in the lamp head
- Anker speaker in the lamp base
- Mac Mini M4 Pro AI processing

Instead, it becomes an optional dedicated voice satellite.

---

# Final Pixstars Architecture

```
                         Mac Mini M4 Pro

                   OpenVoiceOS / HiveMind
                   XTTS Voice Generation
                   Ardour Show Control

                            |
          ----------------------------------------
          |                                      |

 Raspberry Pi Zero 2 WH                 M5Stack Atom Echo

 Controls:                              Handles:

 - audio I/O (mic, speaker)             - Wake word
 - sensor polling                       - microphone input
 - heartbeat monitor                    - voice capture
 - local device management              - experiments


 ESP32 DevKit (Cave)

 Controls:

 - WS2812 5050 RGB LED Ring 16
 - servo movement (via Maestro)
 - AX-12A head nod
 - lamp expressions


 Seeed Studio reComputer RK3588-40

 Controls:

 - local AI inference
 - wake word processing
 - STT / TTS
 - behavior and state logic


Audio:

Mac Mini M4 Pro
        |
        |
        +--> Anker Soundcore Mini
        |    (lamp base)
        |
        +--> PAM8403 amplifier
                |
                |
           40mm full range speaker
           (lamp head)
```

---

# Why Use a Separate Wake Word Satellite?

Pixstars is a stage character.

The audience should experience:

- fast reaction
- reliable listening
- natural interaction

A distributed architecture improves reliability:

The Atom Echo listens.

The Raspberry Pi performs.

The Mac Mini thinks and speaks.

---

# What Is Inside Atom Echo?

The device contains:

- ESP32 controller
- WiFi
- Bluetooth
- microphone
- small speaker
- RGB LED
- button

For Pixstars we mainly use:

- microphone experiments
- wake word detection
- WiFi communication

---

# Why Not Use The Atom Echo Speaker?

The internal speaker is useful for testing but too small for the final character.

The Pixstars voice architecture remains:

```
Mac Mini generated voice

          |

Anker base speaker
+
40mm head speaker
```

The head speaker creates location.

The base speaker creates warmth.

Together they create the illusion.

---

# Why Keep The Raspberry Pi Zero 2 WH?

The Raspberry Pi remains the lamp nervous system.

Responsibilities:

- audio I/O and sensor polling
- heartbeat and diagnostics
- local device management
- HiveMind communication

The Pi is better suited for physical control.

---

# Why Keep The WS2812 LED Ring?

The Atom Echo has a single RGB LED.

The lamp uses a WS2812 5050 RGB LED Ring 16 as its emotional brain, driven by the ESP32 in the cave.

Example states:

Idle:

Soft blue breathing pulse

Listening:

Bright blue attention state

Thinking:

Purple animation

Speaking:

Warm yellow/orange movement

Error:

Red flicker

---

# Development Usage

Before the physical lamp is complete:

```
Developer

"Hey A.I."

        |

M5Stack Atom Echo

        |

WiFi

        |

Mac Mini M4 Pro

        |

AI response
```

This allows the AI interaction pipeline to be tested independently.

---

# Stage Usage

The Atom Echo can become a backup input path.

If another microphone fails:

- commands can still be received
- show control remains possible
- debugging is easier

---

# Home Assistant Assist Compatibility

Atom Echo is commonly used as a small Home Assistant Assist satellite.

This fits the Pixstars philosophy:

- local first
- modular
- replaceable components
- no single point of failure

---

# Recommended Placement

## Development

Place Atom Echo on the desk.

Use it for:

- wake word experiments
- AI testing
- Home Assistant testing

## Final Lamp

Preferred:

Keep the dedicated USB microphone in the lamp head.

Use Atom Echo as:

- backup
- experimental satellite
- additional controller

---

# Setup Flow

1. Install Atom Echo firmware

2. Connect Atom Echo to WiFi

3. Configure wake phrase:

```
Hey A.I.
```

4. Send detected commands to:

```
Mac Mini M4 Pro

OpenVoiceOS / HiveMind
```

5. Generate voice response

6. Trigger:

- speech
- LED emotion
- movement

---

# Final Decision

The Atom Echo becomes an optional Pixstars voice satellite.

It adds:

- easier development
- reliable wake word testing
- backup interaction
- experimentation platform

It does not replace the main character system.

The final illusion:

The audience sees a living lamp.

Behind the curtain:

Atom Echo listens.

Mac Mini thinks.

ESP32 and servos move.

The lamp speaks.
