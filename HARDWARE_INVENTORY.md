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
| RGB laser module | Opt Lasers 300mW Micro RGB (SKU 001311); 44 x 39 x 27 mm; ~50g estimated; R 638nm / G 520nm / B 450nm; 300mW combined (280mW min); collimated beam, divergence <1.3 mRad; 4x M3 mounting screws; Class 4 laser; source https://optlasers.com/free-space-multiwavelength/300mw-micro-rgb-laser-module ; $539 (tax excl.); SUPERSEDED (originally ORDERED 2 June 2026) -- SUPERSEDED by SM5 6W RGB (see SM5 entry below). Original Opt Lasers module ordered but may be repurposed or returned pending Opt Lasers reply on projection suitability. |
| Laser diode driver | Opt Lasers LPLDD-1A-16V-3CH (SKU 001516); 55 x 23.5 mm (bare PCB, no heatsink); 3 independent channels (R, G, B); 0-5V analog modulation input per channel, up to 100 kHz bandwidth; 1A max per channel; 7-16V DC input; soft-start, per-channel max current potentiometer; source https://optlasers.com/multichannel-drivers/lpldd-1a-16v-3ch ; $98 (tax excl.); SUPERSEDED (originally ORDERED 2 June 2026) -- no longer needed; SM5 6W module has integrated driver electronics. May be returned. |
| ILDA DAC | ILDAWaveX16 V2 (ESP32-S3 + RP2354, 16-bit DAC) in cave; generates ILDA DB25 output (+/-5V X/Y galvo signals, 0-5V RGB laser modulation) via Ether Dream or IDN protocol from Mac Mini |
| Galvo PSU | Dedicated +/-24V PSU in cave for 40kpps galvo driver board (included in galvo scanner set) |
| Laser driver PSU | MEAN WELL LRS-35-12 (or equivalent compact 12V ~3A PSU) - powers the SM5 6W RGB laser module (DC 12V input) via cable column; PLANNED |
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

## ILDAWaveX16 V2 (ILDA Laser DAC)

| Property | Value |
|---|---|
| Component | ILDAWaveX16 V2 |
| Type | ILDA Laser DAC |
| Manufacturer | StanleyProjects (Stanley Ondrus) |
| Description | All-in-one, dual-processor (ESP32-S3 + RP2354), high-resolution 16-bit laser DAC platform |
| Features | ILDA DB25 output, SD-card playback, Ethernet, Wi-Fi, USB, JST XH connectors, Ether Dream compatible, IDN (ILDA Digital Network), web UI, GPLv3 open-source firmware |
| Unit price | EUR 145 (excl. shipping) |
| Supplier stock | 2 units available |
| Supplier | Tindie / StanleyProjects |
| Project page | https://stanleyprojects.com/projects/ildawavex16v2 |
| GitHub | https://github.com/stanleyondrus/ILDAWaveX16V2 |
| Location in lamp | Cave (on servo rail, under ComXim turntable) |
| Purpose | ILDA DAC for driving the RGB laser galvo scanner in the lamp head. Receives laser cues from Mac Mini via WiFi/Ethernet (Ether Dream or IDN protocol), outputs standard ILDA DB25 analog signals through the cable column to the galvo scanner. SD card provides backup playback path. |
| V1 board dimensions | 55 x 53 mm (V2 is larger due to dual processor, Ethernet, DB25 -- exact dimensions TBD from supplier) |
| Notes | Opt Lasers Micro RGB has been superseded by SM5 6W RGB (Starshine) as the primary laser module. Awaiting Opt Lasers reply on projection suitability for potential secondary use. |
| Status | EVALUATING |

## SM5 6W RGB Laser Module

| Property | Value |
|---|---|
| Component | SM5 6W RGB Laser Module |
| Type | OEM RGB Laser Module (show-grade) |
| Manufacturer | Starshine Lighting |
| Description | Compact fiber-shaped beam RGB laser module for laser projector integration. Designed for show/projection use with smooth analog modulation. |
| Specifications | 6W total (R 1.4W @ 638nm, G 1.6W @ 525nm, B 3.2W @ 450nm), 0-5V analog modulation per channel (~0.2-4.8V), fiber-shaped beam profile, DC 12V input, <1 min warmup, laser class 4 |
| Dimensions | 94 x 67 x 36 mm |
| Unit price | USD 530 (~EUR 490) |
| Supplier | starshinelights.com |
| Product page | https://www.starshinelights.com/collections/accessories (SM5 listing) |
| Location in lamp | Lamp head (projects beam into galvo mirrors along lamp eye-line) |
| Purpose | RGB laser source for vector laser projection from the lamp head. Paired with 40kpps galvo scanner set for full animation quality. Primary RGB laser source for vector laser projection from the lamp head. |
| Notes | 6W variant is same price as 4W. 94 x 67 x 36 mm needs to fit inside lampshade -- verify against lamphead SVG. Needs 12V DC power routed through cable column. Heat dissipation via lampshade air vents. |
| Status | EVALUATING |

## 40kpps High Speed Galvo Scanner Set

| Property | Value |
|---|---|
| Component | 40kpps High Speed Galvo Scanner Set |
| Type | ILDA Galvo Scanner (X/Y) |
| Manufacturer | Teclulu (GH40) or equivalent |
| Description | Complete galvo scanner kit for full-animation laser projection. Closed-loop moving magnet galvanometers with driver boards and PSU. |
| Specifications | 40kpps ILDA @ 8 degrees, scan angle +/-30 degrees (or larger), mirror size 7 x 12 x 0.8 mm, reflectivity >99% @ 400-700nm, input signal +/-5V (ILDA standard, matches ILDAWaveX16 V2 DB25 output), PSU +/-24V @ 1A |
| Driver board size | 110 x 68 x 35 mm |
| Kit includes | 2x galvo motors, 2x driver boards, 1x motor bracket/mount, 2x signal cables, 2x motor cables, 1x PSU (+/-24V), 1x PSU cable |
| Unit price | USD 150-230 (~EUR 140-210) |
| Supplier | teclulu.com |
| Product page | https://teclulu.com/products/40k-pps-high-speed-galvo-scanner-for-laser-show-lighting-rgb-laser-system-scanner |
| Location in lamp | Galvo motors + mirrors in lamp head (lightweight, ~50g); driver boards + PSU in cave (on servo rail) |
| Purpose | X/Y beam deflection for full-animation vector laser projection. 40kpps chosen over 30kpps for smooth animations, flowing text, logos, and organic shapes -- high entertainment value. Signal chain: ILDAWaveX16 V2 (cave) -> DB25 -> galvo driver (cave) -> cable column -> galvo motors (lamp head). |
| Notes | 40kpps is the professional animation sweet spot. 30kpps does clean graphics but animations look jittery with complex shapes. Only the galvo motors and mirrors go in the lamp head -- driver boards and PSU stay in the cave to keep head weight low. |
| Status | EVALUATING |

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
| Laser galvo scanner (SM5 6W RGB (Starshine) + ILDAWaveX16 V2, 40kpps galvo (Teclulu GH40), +/-24V PSU, 12V PSU for SM5) | EVALUATING (SM5 + ILDAWaveX16 V2 + 40kpps galvo); Opt Lasers + LPLDD SUPERSEDED |
| ILDAWaveX16 V2 (ILDA Laser DAC) | EVALUATING |
| SM5 6W RGB Laser Module (Starshine Lighting) | EVALUATING |
| 40kpps High Speed Galvo Scanner Set (Teclulu GH40 or equiv) | EVALUATING |
| LED strip connectors | ORDERED (arriving soon) |
| Soldering station | ORDERED (arriving soon) |
| Olight Obounds gateway | PLANNED (to order, fallback if Atom Lite spike fails) |
| M5Stack Atom Lite (BLE proxy) | ORDERED (arriving 2026-06-01) |
| M5Stack Atom Echo (wake word satellite) | IN HAND |
| WS2812B 35-LED front cone beam ring | ORDERED (arriving 2 June 2026) |

*Last updated: June 2026*