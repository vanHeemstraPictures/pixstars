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

## Laser Galvo Scanner

| Item | Detail |
| --- | --- |
| Galvo scanner set | 20kpps closed-loop galvanometer pair with X/Y mirrors and driver board |
| RGB laser module | Opt Lasers 300mW Micro RGB (SKU 001311); 44 x 39 x 27 mm; ~50g estimated; R 638nm / G 520nm / B 450nm; 300mW combined (280mW min); collimated beam, divergence <1.3 mRad; 4x M3 mounting screws; Class 4 laser; source https://optlasers.com/free-space-multiwavelength/300mw-micro-rgb-laser-module ; $539 (tax excl.); ORDERED (purchase date: 2 June 2026) |
| Laser diode driver | Opt Lasers LPLDD-1A-16V-3CH (SKU 001516); 55 x 23.5 mm (bare PCB, no heatsink); 3 independent channels (R, G, B); 0-5V analog modulation input per channel, up to 100 kHz bandwidth; 1A max per channel; 7-16V DC input; soft-start, per-channel max current potentiometer; source https://optlasers.com/multichannel-drivers/lpldd-1a-16v-3ch ; $98 (tax excl.); ORDERED (purchase date: 2 June 2026) |
| ILDA DAC | ESP32-based ILDA-compatible DAC in cave; generates X/Y analog (+/-5V) for galvos and RGB analog (0-5V) modulation for the LPLDD-1A-16V-3CH driver (not TTL) |
| Galvo PSU | Dedicated +/-15V linear PSU in cave for galvo driver board |
| Laser driver PSU | MEAN WELL LRS-35-12 (or equivalent compact 12V ~3A PSU) - powers the LPLDD-1A-16V-3CH laser diode driver in the cave; PLANNED |
| Purpose | In-head vector laser projector for theatrical visuals during performance |
| Mounting | Lamp head lower interior, projects along eye-line; analog signals routed through cable column to ILDA DAC in cave |
| Status | ORDERED (laser module + driver, 2 June 2026); galvo set, ILDA DAC, and 12V PSU PLANNED |

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

## Front Cone Beam LED Ring

| Property | Value |
|---|---|
| Model | WS2812B 35-LED Pixel Ring |
| Manufacturer | TOPXCDZ |
| Protocol | WS2812B (single-wire, 800kHz) |
| LED count | 35 |
| Outer diameter | 96mm |
| Inner diameter | 78mm |
| PCB width | 9mm |
| Voltage | DC 5V |
| Purpose | Forward-projecting cone beam from lampshade front -- frames the Olight Sphere C as a halo, creates stage-light cone effect |
| Amazon | https://www.amazon.nl/-/en/WS2812B-16-241-Leds-Addressable/dp/B0DZD6B9RC/ |
| Status | ORDERED -- arriving 2 June 2026 |

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
| Laser galvo scanner (20kpps galvos, Opt Lasers 300mW Micro RGB + LPLDD-1A-16V-3CH, ESP32 ILDA DAC, +/-15V PSU, 12V PSU for driver) | ORDERED (laser module + driver); galvos / DAC / PSUs PLANNED |
| LED strip connectors | ORDERED (arriving soon) |
| Soldering station | ORDERED (arriving soon) |
| Olight Obounds gateway | PLANNED (to order, fallback if Atom Lite spike fails) |
| M5Stack Atom Lite (BLE proxy) | ORDERED (arriving 2026-06-01) |
| M5Stack Atom Echo (wake word satellite) | IN HAND |
| WS2812B 35-LED front cone beam ring | ORDERED (arriving 2 June 2026) |

*Last updated: May 2026*