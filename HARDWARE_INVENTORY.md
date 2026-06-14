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
| Model | Pololu Mini Maestro 24-Channel USB Servo Controller (Assembled), item #1356 |
| Channels | 24 |
| Interface | USB + TTL serial (300-200000 bps) |
| Servo resolution | 0.25 us |
| Pulse rate | up to 333 Hz |
| Operating voltage | 5-16V |
| Script memory | 8 KB |
| Connection to ESP32-S3 | UART1 (TX=GPIO 17, RX=GPIO 18, 9600 baud, compact binary protocol) |
| Python library | pyserial (for direct USB control during bench testing) |
| Serial port | /dev/tty.usbmodem* or /dev/tty.usbserial-* (when connected via USB) |
| Unit price | EUR 70.40 (incl. BTW) |
| Supplier | Opencircuit.nl -- https://opencircuit.nl/product/mini-maestro-24-kanaals-usb-servo-controller-2 |
| Status | ORDERED (Opencircuit.nl, EUR 70.40) |

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

## Base Rotation Turntable (DIY)

The lamp's base rotation is a DIY belt-driven turntable inspired by the MGX3D open-source design (https://github.com/MGX3D/Turntable). A GT2 belt is driven by a NEMA 17 / TMC2209 / ESP32 chain and wraps directly around the outer race of a 200mm lazy susan bearing (friction drive -- no 200T ring gear). A bilateral idler-bearing + spring tensioner maintains belt grip. Origin is detected by a Hall effect sensor + neodymium magnet. Replaces the previously planned ComXim MTxRUWSLPro (see SUPERSEDED entry below).

### ComXim MTxRUWSLPro Turntable (SUPERSEDED)

| Property | Value |
| --- | --- |
| Component | ComXim MTxRUWSLPro programmable turntable |
| Type | WiFi-controlled motorised turntable (CT command protocol) |
| Intended role | Lamp base rotation (precision 0.1 deg, controlled directly from Mac Mini via WiFi) |
| Status | SUPERSEDED -- supplier payment issues blocked procurement; DIY ESP32-driven turntable (NEMA 17 + TMC2209 + GT2 belt friction-drive on 200mm lazy susan) preferred. DIY solution integrates directly into existing OSC/ESP32 control stack (no separate CT protocol), costs ~EUR 50, and achieves ~0.007 deg resolution (better than 0.1 deg). |

### NEMA 17 Stepper Motor

| Property | Value |
| --- | --- |
| Component | NEMA 17 bipolar stepper motor |
| Step angle | 1.8 deg (200 steps/rev) |
| Drive | Microstepped 1/16 via TMC2209 -> 3,200 microsteps/rev |
| Effective resolution at turntable | ~50,240 steps/rev = ~0.00717 deg (after ~15.7:1 belt ratio: 200mm bearing circumference ~628mm / 20T GT2 pulley ~40mm) |
| Power | 12V (shared with LPLDD laser driver from MEAN WELL LRS-50-12); ~1.5A during rotation |
| Location in lamp | Cave (on servo rail), drives GT2 pulley up to turntable bearing |
| Purpose | Primary motive force for base rotation in the DIY turntable |
| Reference | MGX3D open-source turntable (https://github.com/MGX3D/Turntable) |
| Status | PLANNED |

### TMC2209 Stepper Driver

| Property | Value |
| --- | --- |
| Component | TMC2209 silent stepper driver (Trinamic) |
| Interface | STEP / DIR / ENABLE from ESP32 (GPIO 25 STEP, GPIO 26 DIR, GPIO 14 EN) |
| Features | StealthChop2 (near-silent operation), CoolStep, 1/16 microstepping (configured), up to 2A RMS |
| Software | FastAccelStepper library on ESP32 (hardware pulse generation) |
| Power | 12V motor supply (MEAN WELL LRS-50-12), 3.3V logic from ESP32 |
| Location in lamp | Cave (on servo rail, next to ESP32 DevKit) |
| Purpose | Silent, microstepped drive for the NEMA 17 turntable motor |
| Status | PLANNED |

### Hall Effect Sensor + Magnet (Turntable Origin)

| Property | Value |
| --- | --- |
| Component | Hall effect sensor (SS49E linear or A3144 digital) + small neodymium magnet |
| Interface | Single GPIO input to ESP32 (GPIO 27) |
| Mounting | Sensor fixed to cave/turntable frame; magnet bonded to underside of rotating platform |
| Purpose | Origin detection / home position for the DIY turntable; triggered each revolution as the magnet passes the sensor. Used by ESP32 firmware to handle `/turntable/origin` OSC command and to absolutely reference the stepper position. |
| Status | PLANNED |

### GT2 20T Pulley

| Property | Value |
| --- | --- |
| Component | GT2 timing pulley, 20 teeth |
| Bore | 5mm (matches NEMA 17 shaft) |
| Belt width | 6mm (matches GT2 6mm belt) |
| Pitch circumference | ~40mm (20T x 2mm pitch) |
| Mounting | Direct on NEMA 17 motor shaft (set screw on flat) |
| Purpose | Drives the GT2 belt that wraps around the 200mm lazy susan bearing outer race (friction drive); establishes the ~15.7:1 reduction ratio |
| Status | PLANNED |

### GT2 Closed-Loop Belt

| Property | Value |
| --- | --- |
| Component | GT2 closed-loop timing belt, 6mm wide |
| Pitch | 2mm GT2 |
| Length | TBD -- sized to wrap once around the 200mm lazy susan bearing outer race (~628mm circumference) + reach NEMA 17 pulley + idler tensioners (likely ~800-900mm closed-loop, exact length set during build) |
| Drive style | Friction drive -- belt wraps around the smooth outer race of the lazy susan bearing (no 200T ring gear / no toothed engagement with the platform). Tensioner provides the friction grip. |
| Reference | MGX3D open-source turntable (https://github.com/MGX3D/Turntable) |
| Status | PLANNED -- exact length finalised during physical build |

### Lazy Susan 200mm Aluminum Bearing

| Property | Value |
| --- | --- |
| Component | Lazy Susan swivel plate bearing, 200mm |
| Material | Aluminum |
| Outer diameter | 200mm (~628mm circumference -- acts as the "large pulley" for the friction belt drive) |
| Load capacity | Sized for lamp + cave assembly (reference design supports 100kg+) |
| Mounting | Top of riser block; lamp platform mounts on rotating top plate; static plate fixed to cave/riser |
| Purpose | Primary rotational bearing for the lamp platform; its smooth aluminum outer race is the friction-drive surface the GT2 belt wraps around |
| Status | PLANNED |

### Bilateral Belt Tensioner Hardware

| Property | Value |
| --- | --- |
| Component | Bilateral belt tensioner assembly (idler bearings + tension spring) |
| Parts | 2x small ball-bearing idler pulleys (one each side of the NEMA 17 pulley), mounting bracket, extension/compression spring, adjustment hardware |
| Purpose | Maintains belt tension and friction grip against the 200mm lazy susan bearing outer race; bilateral layout (idlers on both sides of the drive pulley) increases belt wrap angle around the bearing and equalises load on the motor shaft |
| Reference | MGX3D open-source turntable (https://github.com/MGX3D/Turntable) |
| Status | PLANNED |


## MEAN WELL LRS-50-12 (Cave 12V Rail)

| Property | Value |
| --- | --- |
| Component | MEAN WELL LRS-50-12 |
| Type | Enclosed switching power supply |
| Output | 12V DC, 4.2A (50.4W) |
| Input | AC mains (universal input) |
| Role | Cave 12V rail -- powers the LPLDD-1A-16V-3CH laser driver and the TMC2209 stepper driver; also used for AX-12A (9-12V) bench testing |
| Location in lamp | Cave (on servo rail) |
| Supplier | Reichelt (https://www.reichelt.com/nl) |
| Status | ORDERED (Reichelt) |

## ESP32-S3 N16R8 DevKitC (Cave Controller)

| Property | Value |
| --- | --- |
| Component | ESP32-S3 N16R8 DevKitC (ESP32-S3-WROOM-1-N16R8) |
| Type | Cave controller / central nervous system for all physical actuators |
| SoC | ESP32-S3 (Xtensa LX7 dual-core @ 240 MHz) |
| Memory | 512 KB SRAM, 8 MB PSRAM, 16 MB flash |
| Radios | 2.4 GHz WiFi 802.11 b/g/n (40 MHz bandwidth), Bluetooth 5.0 LE + Mesh |
| GPIO | 44 programmable pins |
| UARTs | 3 |
| RMT channels | 8 |
| USB | Dual USB-C (CH343P serial + USB OTG) |
| AI | Vector instructions for ML inference |
| Role | WiFi bridge from Mac Mini (OSC); drives Pololu Mini Maestro 24ch (UART), Dynamixel AX-12A head nod (UART half-duplex), WS2812 LED rings (RMT), TMC2209 turntable stepper (STEP/DIR/EN), Hall sensor input |
| Pin assignments | Turntable (TMC2209): STEP=GPIO 4, DIR=GPIO 5, EN=GPIO 6, HALL=GPIO 7. AX-12A: DIR=GPIO 8, UART2 TX=GPIO 15, UART2 RX=GPIO 16. WS2812 rings (RMT): rear (16 LEDs)=GPIO 9, front (35 LEDs)=GPIO 10. Maestro (UART1): TX=GPIO 17, RX=GPIO 18. Status LED: GPIO 48 (onboard WS2812). Reserved/unavailable on N16R8: GPIO 19/20 (USB), 22-25 (do not exist), 26-37 (octal SPI flash/PSRAM), 43/44 (UART0/USB-UART), 0/3/45/46 (strapping). See `firmware/cave-esp32/src/config.h.example` for the full pin map. |
| Location in lamp | Cave (on servo rail, next to Maestro and TMC2209) |
| Power | 5V via USB-C or VIN; logic 3.3V |
| Firmware | Arduino / PlatformIO -- FastAccelStepper (stepper), Dynamixel2Arduino (AX-12A), FastLED or Adafruit_NeoPixel (WS2812), python-osc compatible OSC server |
| Unit price | EUR 12.95 |
| Supplier | Otronic.nl -- https://www.otronic.nl/en/esp32-s3-n16r8-devboard-16mb-flash-en-8mb-psram.html |
| Notes | Replaces the originally planned ESP32 DevKit V1 (WROOM-32). The S3 offers 44 GPIOs (vs 34), 16 MB flash (vs 4 MB), 8 MB PSRAM, USB OTG, BT 5.0, and AI vector instructions for EUR 12.95. The M5Stack Atom Lite (IN HAND) remains as a WiFi/OSC test device. |
| Status | IN HAND (Otronic.nl, EUR 12.95) |


## Dynamixel AX-12A (Head Nod Servo)

| Property | Value |
| --- | --- |
| Component | ROBOTIS Dynamixel AX-12A |
| Model | AX-12A (item 902-0003-001) |
| Protocol | Dynamixel Protocol 1.0 (half-duplex TTL serial) |
| Baud | 1 Mbps (default) |
| Resolution | 1024 positions (0-300 degrees) |
| Stall torque | 1.5 N*m (12V) |
| Gear ratio | 254:1 |
| Operating voltage | 9-12V |
| Weight | 53.5g |
| Feedback | Position, speed, load, voltage, temperature |
| Connection to ESP32-S3 | UART2 half-duplex (TX=GPIO 15, RX=GPIO 16, DIR=GPIO 8, 1 Mbps) |
| Role | Head nod actuator in lamp head |
| Location in lamp | Lamp head (cable through central column to ESP32 in cave) |
| Unit price | EUR 59.08 |
| Supplier | Reichelt.nl -- https://www.reichelt.com/nl/nl/shop/product/servomotor_robotica_9_0_-_12_v_dc-249909 |
| Status | IN HAND (Reichelt.nl, EUR 59.08) |

## Laser Galvo Scanner

| Item | Detail |
| --- | --- |
| Galvo scanner set | 20kpps closed-loop galvanometer pair with X/Y mirrors and driver board |
| RGB laser module | Opt Lasers 300mW Micro RGB (SKU 001311); 44 x 39 x 27 mm; ~55g; R 638nm / G 520nm / B 450nm; 300mW combined (280mW min); collimated beam, divergence <1.3 mRad; 4x M3 mounting screws; Class 4 laser; source https://optlasers.com/free-space-multiwavelength/300mw-micro-rgb-laser-module ; $539 (tax excl.); PRIMARY -- selected for low head weight. Opt Lasers confirmed (June 2026, Dr. Michal Piotrowicz, Lead Diode Laser Engineer) the module is suitable for laser projection / laser show use. |
| Laser diode driver | Opt Lasers LPLDD-1A-16V-3CH (SKU 001516); 55 x 23.5 mm (bare PCB, no heatsink); 3 independent channels (R, G, B); 0-5V analog modulation input per channel, up to 100 kHz bandwidth; 1A max per channel; 7-16V DC input; soft-start, per-channel max current potentiometer; source https://optlasers.com/multichannel-drivers/lpldd-1a-16v-3ch ; $98 (tax excl.); ACTIVE -- drives the Opt Lasers 300mW Micro RGB module from the cave 12V rail. |
| ILDA DAC | ILDAWaveX16 V2 (ESP32-S3 + RP2354, 16-bit DAC) in cave; generates ILDA DB25 output (+/-5V X/Y galvo signals, 0-5V RGB laser modulation) via Ether Dream or IDN protocol from Mac Mini |
| Galvo PSU | Dedicated +/-24V PSU in cave for 40kpps galvo driver board (included in galvo scanner set) |
| Laser driver PSU | MEAN WELL LRS-35-12 (or equivalent compact 12V ~3A PSU) - powers the LPLDD-1A-16V-3CH driver, which in turn powers the Opt Lasers 300mW Micro RGB module (DC 12V input); PLANNED |
| Purpose | In-head vector laser projector for theatrical visuals during performance |
| Mounting | Lamp head lower interior, projects along eye-line; analog signals routed through cable column to ILDA DAC in cave |
| Status | IN HAND -- Opt Lasers 300mW Micro RGB received; LPLDD-1A-16V-3CH driver + ILDAWaveX16 V2 + 40kpps galvo selected and pending procurement; physical fit check in lamp head pending |

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
| Notes | Pack of 20 3-wire cables (red/green/white) with JST SM 3-pin connectors attached. |
| Status | IN HAND |

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
| Status | IN HAND |

## Kitronik Inventor's Kit for Arduino

| Item | Detail |
| --- | --- |
| Product | Kitronik Inventor's Kit for Arduino |
| Includes | 400-point breadboard, jumper wires (M/M), assorted resistors (various values including 470 ohm), LEDs, push buttons, potentiometer |
| Purpose | Solderless prototyping of the AX-12A bench test wiring and the WS2812 LED ring data line (330 ohm series resistor breadboard mock-up, signal validation before final soldering) |
| Source | elektronicavoorjou.nl |
| Notes | Expected delivery start of next week. |
| Status | ORDERED (elektronicavoorjou.nl) |

## Olight Obounds Smart Wireless Gateway

| Property | Value |
| --- | --- |
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
| Firmware | ESPHome bluetooth_proxy (board target: m5stack-atom) |
| Purpose | Spike candidate to replace Olight Obounds -- ESP32 BLE proxy that bridges the Sphere C to Home Assistant via the 11z4t/tuya-ble-mesh HACS integration |
| Source | Amazon.nl |
| Price | EUR 19.35 |
| Status | IN HAND |

## Wake Word Satellite

| Property | Value |
| --- | --- |
| Model | M5Stack Atom Echo Programmable Smart Speaker |
| Manufacturer | M5Stack |
| Controller | ESP32 (built-in) |
| Connectivity | WiFi, Bluetooth |
| Features | Microphone, small speaker, RGB LED, button |
| Purpose | Wake word satellite -- dedicated "Hey A.I." listener for development and backup stage input |
| Amazon | https://www.amazon.nl/-/en/M5Stack-Atom-Echo-Programmable-Mini-Smart/dp/B0F6M8L6XF/ |
| Manufacturer site | https://shop.m5stack.com/ |
| Notes | Ships with ESPHome firmware pre-installed (device label: "ESPHome FW Pre-installed for Home Assistant"). No manual flashing needed for initial Home Assistant voice satellite setup. |
| Status | IN HAND |

## Front Cone Beam LED Ring

| Property | Value |
| --- | --- |
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
| Notes | Arrived with two pre-soldered 3-wire cables (red/green/white) with JST SM 3-pin connectors attached. |
| Status | IN HAND |

## ILDAWaveX16 V2 (ILDA Laser DAC)

| Property | Value |
| --- | --- |
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
| Notes | Opt Lasers confirmed their Micro RGB is suitable for laser projection (June 2026, Dr. Michal Piotrowicz). The ILDAWaveX16 V2 board selection is independent of the laser module choice. |
| Status | EVALUATING |

## SM5 6W RGB Laser Module (SUPERSEDED)

| Property | Value |
| --- | --- |
| Component | SM5 6W RGB Laser Module |
| Type | OEM RGB Laser Module (show-grade) |
| Manufacturer | Starshine Lighting |
| Description | Compact fiber-shaped beam RGB laser module for laser projector integration. Designed for show/projection use with smooth analog modulation. |
| Specifications | 6W total (R 1.4W @ 638nm, G 1.6W @ 525nm, B 3.2W @ 450nm), 0-5V analog modulation per channel (~0.2-4.8V), fiber-shaped beam profile, DC 12V input, <1 min warmup, laser class 4 |
| Dimensions | 94 x 67 x 36 mm |
| Weight | ~200g |
| Unit price | USD 530 (~EUR 490) |
| Supplier | starshinelights.com |
| Product page | https://www.starshinelights.com/collections/accessories (SM5 listing) |
| Location in lamp | Lamp head (projects beam into galvo mirrors along lamp eye-line) |
| Purpose | RGB laser source for vector laser projection from the lamp head. |
| Notes | 6W variant is same price as 4W. |
| Status | SUPERSEDED -- too heavy for lamp head (200g); Opt Lasers 300mW Micro RGB (55g) selected instead. |

## 40kpps High Speed Galvo Scanner Set

| Property | Value |
| --- | --- |
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

## Epson EB-W05 Projector

| Property | Value |
| --- | --- |
| Component | Epson EB-W05 3LCD Projector |
| Type | Rear projection (behind screen) |
| Manufacturer | Epson |
| Description | 3LCD WXGA rear projector for theater-scale imagery on rear-projection screen. Connected to Mac Mini via HDMI. Controlled via remote or Mac Mini. |
| Specifications | 3,300 lumens (white and colour), WXGA (1280x800, 16:10), 15,000:1 contrast, 3LCD, projection ratio 1.30-1.56:1, image size 33-320 inches, 1.2x optical zoom, manual focus, horizontal keystone slider |
| Dimensions | 302 x 237 x 82 mm |
| Weight | 2.5 kg |
| Connectivity | HDMI, VGA, USB-B, USB-A (WiFi dongle), composite video, audio in |
| Power | AC mains |
| Location in lamp | Backstage (behind rear-projection screen) |
| Purpose | Projects theater-scale imagery (Disney castle, GNR logo, AI iterations, signatures) onto rear-projection screen. Driven by the projection/ subsystem (pygame, OSC port 9002) on the Mac Mini via HDMI. |
| Status | IN HAND |

## Rear-Projection Screen

| Property | Value |
| --- | --- |
| Component | Rear-projection screen |
| Type | Rear-projection surface |
| Description | Translucent screen placed between the rear projector and the audience. Receives imagery from behind (Epson EB-W05) and laser vector drawings from the front (lamp laser). |
| Specifications | TBD -- size depends on venue. Should support both rear projection and front laser marking. |
| Location in lamp | Stage (between performer/lamp and audience backdrop) |
| Purpose | Primary visual surface for all projected imagery and lamp laser drawings. |
| Status | PLANNED -- to be purchased or rented for the October 2026 performance |

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
| Laser galvo scanner (Opt Lasers 300mW Micro RGB + LPLDD-1A-16V-3CH driver + ILDAWaveX16 V2, 40kpps galvo (Teclulu GH40), +/-24V PSU, 12V PSU for LPLDD) | Opt Lasers 300mW Micro RGB IN HAND; EVALUATING (LPLDD + ILDAWaveX16 V2 + 40kpps galvo); SM5 6W RGB (Starshine) SUPERSEDED -- too heavy |
| ILDAWaveX16 V2 (ILDA Laser DAC) | EVALUATING |
| Opt Lasers 300mW Micro RGB Laser Module | IN HAND |
| ESP32-S3 N16R8 DevKitC (cave controller) | IN HAND |
| MEAN WELL LRS-50-12 (cave 12V rail: LPLDD laser driver + TMC2209 + AX-12A bench) | ORDERED (Reichelt) |
| Dynamixel AX-12A (head nod servo) | IN HAND |
| Opt Lasers LPLDD-1A-16V-3CH laser driver | EVALUATING (ACTIVE) |
| SM5 6W RGB Laser Module (Starshine Lighting) | SUPERSEDED -- too heavy for lamp head |
| 40kpps High Speed Galvo Scanner Set (Teclulu GH40 or equiv) | EVALUATING |
| LED strip connectors | IN HAND |
| Soldering station | IN HAND |
| Kitronik Inventor's Kit for Arduino (breadboard, jumpers, resistors, LEDs, buttons, potentiometer) | ORDERED |
| Olight Obounds gateway | PLANNED (to order, fallback if Atom Lite spike fails) |
| M5Stack Atom Lite (BLE proxy) | IN HAND |
| M5Stack Atom Echo (wake word satellite) | IN HAND |
| WS2812B 35-LED front cone beam ring | IN HAND |
| Epson EB-W05 3LCD projector (rear projection) | IN HAND |
| Rear-projection screen | PLANNED (to be purchased or rented) |

*Last updated: June 2026*