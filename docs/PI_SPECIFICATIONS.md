# Raspberry Pi Specifications

## Raspberry Pi Zero 2 WH (Pre-Soldered Headers)

> Source: Amazon.nl

### Product Details

| Field | Value |
| --- | --- |
| Brand | Raspberry Pi |
| Model | SC0721 |
| Product | Raspberry Pi Zero 2 WH |
| ASIN | B0DB2JBD9C |
| Variant | WH (WiFi + pre-soldered Headers) |
| Vendor | Amazon.nl |
| Price | EUR 25.99 (as of April 2026) |

### Processor

| Spec | Value |
| --- | --- |
| SoC | Broadcom BCM2710A1 (RP3A0 system-in-package) |
| CPU | Quad-core 64-bit ARM Cortex-A53 @ 1GHz |
| GPU | VideoCore IV |
| Video decode | H.264, MPEG-4 (1080p30) |
| Video encode | H.264 (1080p30) |
| Graphics API | OpenGL ES 1.1, 2.0 |

### Memory & Storage

| Spec | Value |
| --- | --- |
| RAM | 512MB LPDDR2 |
| Storage | microSD card slot |

### Connectivity

| Spec | Value |
| --- | --- |
| WiFi | 2.4GHz IEEE 802.11 b/g/n, onboard antenna |
| Bluetooth | 4.2 / Bluetooth Low Energy (BLE) |
| USB | 1x Micro USB 2.0 OTG |
| Video output | 1x Mini HDMI |
| Camera | CSI-2 camera connector |
| GPIO | HAT-compatible 40-pin header (pre-soldered) |
| Composite video | Via solder test points |
| Reset | Via solder test points |

### Physical

| Spec | Value |
| --- | --- |
| Dimensions | 65mm x 30mm |
| Weight | 10g |
| Operating temperature | -20C to +70C |

### Power

| Spec | Value |
| --- | --- |
| Input | 5V DC via Micro USB |
| Recommended supply | 5V 2.5A |

### Why This Model

- **Pre-soldered headers** (WH variant) — no soldering required, plug directly into breadboard or servo controller
- **Same SoC as Raspberry Pi 3** — proven compatibility with HiveMind satellite, OVOS, and Python 3.12
- **Tiny form factor** (65x30mm) — fits inside or underneath the Anglepoise lamp base
- **WiFi built-in** — connects to Mac Mini over local network without USB dongles
- **5V input** — shares the MEAN WELL LRS-50-5 power supply rail with the servos

### Role in Pixstars

The Pi Zero 2 WH serves as the **lamp head controller**, running:

- HiveMind satellite client (communicating with Mac Mini server)
- LED state control script (`led_hivemind_states_filewatch.py`)
- GPIO interface to the Arduino Nano (serial bridge for NeoPixel RGBW ring)

See [Complete Lamp Build Guide](./docs/PIXSTARS_LAMP_COMPLETE_BUILD.md) for integration instructions.See [Raspberry Pi Setup](./pi/) for configuration files and systemd services.