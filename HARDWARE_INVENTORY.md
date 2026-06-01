# Pixstars — Hardware Inventory

> All devices, ports, and drivers for the Pixstars show platform.Items marked MOCKED are not yet physically connected — the software uses mock/log output instead.

## Platform

| Item | Detail |
| --- | --- |
| Machine | Apple Mac Mini M4 Pro |
| OS | macOS |
| Python | 3.12.13 (Homebrew) |
| Virtual Env | .venv/ (Python 3.12) |

## OSC Port Assignments

All communication between subsystems uses OSC over localhost (`127.0.0.1`).

| Route | Port | Protocol |
| --- | --- | --- |
| Conductor → Ardour | 3819 | OSC (Ardour default) |
| Conductor → Jess+ (Lamp) | 9001 | OSC |
| Conductor → Projection | 9002 | OSC |
| Conductor → Lighting | 9003 | OSC |
| Conductor → Digital Twin | 9004 | OSC (→ WebSocket on port 8765) |

## Audio — Ardour DAW

| Item | Detail |
| --- | --- |
| Software | Ardour (open-source DAW) |
| Piano plugin | Pianoteq 9 (VST3, free trial) |
| Drum plugin | MODO DRUM 1.5 (VST3, licensed) |
| Drum kit | Rock Custom Sounds |
| MIDI file | november-rain-midi/ds1056-format1.mid |
| OSC control surface | TO BE ENABLED — Preferences → Control Surfaces → OSC |
| Status | INSTALLED |

## DMX Lighting Interface

| Item | Detail |
| --- | --- |
| Recommended | Enttec DMX USB Pro (~$170 / ~€160) |
| Protocol | Enttec Pro USB protocol (onboard microprocessor) |
| Features | DMX output, DMX input, RDM support |
| Driver | Standard USB serial (no FTDI D2XX needed) |
| Python library | DMXEnttecPro==0.4 (installed) |
| Auto-detect | get_port_by_product_id(24577) |
| Serial port | /dev/tty.usbserial-* (when connected) |
| Status | MOCKED — not yet purchased |

### Usage

```bash
python -m lighting.controller --device auto   # auto-detect Pro
python -m lighting.controller --device /dev/tty.usbserial-EN055555A
```

### Why Pro over Open DMX USB?

- Dedicated microprocessor handles DMX timing (no CPU bit-banging)
- Rock-solid reliability critical for live performance
- No FTDI driver issues on macOS Apple Silicon (M4 Pro)
- `DMXEnttecPro` Python library with clean API (`set_channel`, `submit`, `auto_submit`)
- DMX input + RDM support for future use

### Purchase link

[https://www.enttec.com/product/dmx-usb-interfaces/dmx-usb-pro-professional-1u-usb-to-dmx512-converter/](https://www.enttec.com/product/dmx-usb-interfaces/dmx-usb-pro-professional-1u-usb-to-dmx512-converter/)

## Lamp Servo Controller

| Item | Detail |
| --- | --- |
| Type | Direct USB servo controller |
| Connection | USB serial |
| Python library | pyserial |
| Serial port | /dev/tty.usbmodem* or /dev/tty.usbserial-* (when connected) |
| Protocol | Serial commands (TBD based on specific controller) |
| Status | MOCKED — controller to be connected |

## Lamp Base AI

| Item | Detail |
| --- | --- |
| Device | Seeed Studio reComputer RK3588-40 |
| SoC | Rockchip RK3588 (4x Cortex-A76 + 4x Cortex-A55) |
| NPU | 6 TOPS (INT8), expandable to 26 TOPS via PCIe accelerator |
| RAM | 16GB LPDDR5 |
| Storage | 128GB eMMC + M.2 NVMe slot |
| Connectivity | Gigabit Ethernet, WiFi 6, Bluetooth 5.2 |
| Role | Local AI brain in lamp base |
| Runs | Wake word, STT, TTS, local LLM, computer vision, emotional state engine, HiveMind client |
| Status | PLANNED — confirmed, not yet procured |

## Projector

| Item | Detail |
| --- | --- |
| Type | External projector via HDMI/DisplayPort |
| Connection | Second display output from Mac Mini |
| Software | pygame fullscreen on secondary display |
| Status | MOCKED — using windowed pygame display |

## LED Strip Connectors

| Item | Detail |
| --- | --- |
| Product | JST SM 3-pin LED strip connectors (20 pcs) |
| ASIN | B0DXQ23CKB |
| Specs | 3-pin, 22 AWG, 15-16cm cable, male+female pairs |
| Compatible | WS2812B, WS2811, WS2812, WS2814, SK6812, CCT LED strips |
| Purpose | WS2812 5050 RGB LED Ring 16 wiring connections |
| Source | Amazon.nl |
| Price | EUR 9.99 |
| Status | ORDERED -- arriving soon |

## Soldering Station

| Item | Detail |
| --- | --- |
| Product | Grantop 14-in-1 soldering iron kit |
| ASIN | B0DHJQ4NTX |
| Specs | 60W/220V, adjustable 200-450C, on/off switch |
| Includes | 5 soldering tips, desoldering pump, solder wire, tweezers, wire stripper, cutter, stand with sponge, carry case |
| Purpose | Assembly and wiring of lamp electronics (cave servos, WS2812 5050 RGB LED Ring 16, ESP32 connections) |
| Source | Amazon.nl |
| Price | EUR 15.99 |
| Status | ORDERED -- arriving soon |

## Olight Obounds Smart Wireless Gateway

| Property | Value |
|---|---|
| Model | Obounds Smart Wireless Multi-Protocol Gateway |
| Manufacturer | Olight |
| Protocols | WiFi (2.4G), Bluetooth SIG Mesh, Zigbee |
| Capacity | Up to 128 sub-devices |
| Purpose | BLE Mesh bridge for Olight Sphere C front light -- enables Home Assistant control via tuya-local integration |
| Price | EUR 25-42 (varies by store) |
| Status | PLANNED -- to be ordered |

## M5Stack Atom Lite (ESP32 BLE Proxy)

| Item | Detail |
| --- | --- |
| Product | M5Stack Atom Lite ESP32 IoT Development Kit (C008) |
| ASIN | B0CTGKJPRW |
| MCU | ESP32-PICO-D4 (dual-core 240 MHz, 4 MB flash) |
| Radios | 2.4 GHz WiFi, Bluetooth 4.2 LE |
| Connectivity | USB-C, HY2.0 (Grove-compatible), 6 GPIO |
| Form factor | 24 x 24 mm enclosed plastic case |
| Firmware | ESPHome `bluetooth_proxy` (board target: `m5stack-atom`) |
| Purpose | Spike candidate to replace Olight Obounds -- ESP32 BLE proxy that bridges the Sphere C to Home Assistant via the `11z4t/tuya-ble-mesh` HACS integration |
| Source | Amazon.nl |
| Price | EUR 19.35 |
| Status | ORDERED -- arriving 2026-06-01 |

## Wake Word Satellite

| Property | Value |
|---|---|
| Model | M5Stack Atom Echo Programmable Smart Speaker |
| Manufacturer | M5Stack |
| Controller | ESP32 (built-in) |
| Connectivity | WiFi, Bluetooth |
| Features | Microphone, small speaker, RGB LED, button |
| Purpose | Wake word satellite -- dedicated "Hey A.I." listener for development and backup stage input |
| Amazon | https://www.amazon.nl/-/en/M5Stack-Atom-Echo-Programmable-Mini-Smart/dp/B0F6M8L6XF/ |
| Manufacturer site | https://shop.m5stack.com/ |
| Status | IN HAND |

## Summary

| Component | Status |
| --- | --- |
| Python 3.12 | ✅ Installed |
| Virtual environment | ✅ Created |
| OSC (python-osc) | ✅ Installed |
| pyserial | ✅ Installed |
| pygame | ✅ Installed |
| PyYAML | ✅ Installed |
| Ardour | ✅ Installed (OSC to be enabled) |
| DMX interface | 🟡 MOCKED (purchase Enttec DMX USB Pro) |
| Servo controller | 🟡 MOCKED (connect USB servo) |
| Projector | 🟡 MOCKED (connect when available) |
| LED strip connectors | ORDERED (arriving soon) |
| Soldering station | ORDERED (arriving soon) |
| Olight Obounds gateway | PLANNED (to order, fallback if Atom Lite spike fails) |
| M5Stack Atom Lite (BLE proxy) | ORDERED (arriving 2026-06-01) |
| M5Stack Atom Echo (wake word satellite) | IN HAND |

*Last updated: May 2026*