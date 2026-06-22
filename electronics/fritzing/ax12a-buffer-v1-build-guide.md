# ax12a-buffer_v1.fzz -- Build Guide

Step-by-step instructions for assembling the Fritzing project`ax12a-buffer_v1.fzz` from scratch. The circuit is a bench test of the74HCT245 half-duplex TTL buffer that the cave ESP32-S3 uses to talk tothe Dynamixel AX-12A head nod servo (Cave Architecture v3).

Authoritative circuit spec: `wiring/ax12a-bench-test/codey-prompt.txt`.Wire color conventions: `wiring/WIRING.md`. Board purpose:`electronics/pcbs/ax12a-buffer/README.md`. File naming:`electronics/fritzing/README.md`.

Use straight ASCII quotes only when typing labels in Fritzing.

> **IMPORTANT -- Fritzing stand-in part.** The Fritzing parts bin on macOS does not ship an ESP32-S3 N16R8 DevKitC. This sketch uses the **Adafruit Feather ESP32-C1 (#5933)** as a visual stand-in for documentation only. The **physical build uses the ESP32-S3 N16R8 DevKitC** -- the Feather has a different form factor and pin layout, so always cross-reference the Pin Mapping section below before wiring real hardware. Rename the Feather to `ESP32-S3 N16R8 DevKitC` in the Inspector so the sketch label matches the bench build.

> **IMPORTANT -- 74LVC245 vs 74HCT245.** Fritzing's parts bin on macOS ships **74LVC245** (low-voltage CMOS) instead of 74HCT245. The DIP-20 **pinout is identical** -- only the logic family differs. Place the 74LVC245 in the sketch, then rename it to `74HCT245` in the Inspector so the silkscreen label matches the physical board. The bench build uses an actual 74HCT245.

## 1. Parts list

Open Fritzing, switch to the Breadboard view, and search the Parts bin(top-right) for each item. Drag onto the sketch:

| Qty | Component | Fritzing part (exact name) | Notes |
| --- | --- | --- | --- |
| 1 | Half-size breadboard | `Breadboard Half +` | 400 tie points (30 rows + 2 power rails per side). |
| 1 | ESP32-S3 N16R8 DevKitC (stand-in) | `Adafruit Feather ESP32-C1 (#5933)` | Visual stand-in only. Rename to `ESP32-S3 N16R8 DevKitC` in the Inspector. See Pin Mapping section -- the Feather's labelled pins do NOT line up with the actual ESP32-S3 GPIO numbers. |
| 1 | 74HCT245 octal buffer | `74LVC245` | Same DIP-20 pinout as 74HCT245. Rename to `74HCT245` in the Inspector. The physical build uses a real 74HCT245. |
| 1 | Resistor (1 kohm) | `Resistor` | Set `Resistance` to `1k` in the Inspector. Axial through-hole. |
| 1 | Resistor (2.2 kohm) | `Resistor` | Set `Resistance` to `2.2k` in the Inspector. Axial through-hole. |
| 1 | 3-pin male header | `Sparkfun Pin Header (3 pin)` | Acts as the AX-12A pigtail (VCC / DATA / GND). Label it `AX-12A` in the Inspector. |
| 1 | 2-pin screw terminal | `2-pin screw terminal` | 12V input from MEAN WELL LRS-50-12. A DC barrel jack is also acceptable; either way label it `LRS-50-12 12V IN`. |

All parts above are in the Fritzing core library on macOS -- no extraparts packs required. Do not invent custom parts for this bench test.

## 1a. Pin mapping (Feather stand-in -> actual ESP32-S3 DevKitC)

The Adafruit Feather ESP32-C1 (#5933) used in this Fritzing sketch hasa **different pinout** from the ESP32-S3 N16R8 DevKitC used in thephysical build. When wiring the sketch, attach jumpers to the **Featherpin labels** in the left column; the middle column is the actualESP32-S3 GPIO that this represents on real hardware. The right columnis the destination on the 74HCT245 buffer (DIP-20 pin numbering).

| Actual ESP32-S3 pin | Feather stand-in pin | Wire to |
| --- | --- | --- |
| GPIO 15 (UART2 TX) | `TX` | 74HCT245 pin 2 (A1) |
| GPIO 16 (UART2 RX) | `RX` | 1 kohm resistor from 74HCT245 pin 3 (A2) (divider junction) |
| GPIO 8 (DIR) | `IO0` | 74HCT245 pin 1 (DIR) |
| 5V | `USB` | +5V rail (top red) |
| GND | `GND` | GND rail (top blue) |

When the firmware is flashed to the real ESP32-S3 DevKitC, the GPIOnumbers in the firmware match the left column. The Feather pin labelsin the middle column exist only inside Fritzing -- ignore them outsideof this sketch.

## 1b. PSU mains wiring (MEAN WELL LRS-50-12)

Wire the MEAN WELL LRS-50-12 to wall power *before* placing anything on the breadboard. The bench test runs on **Netherlands 230V mains** -- the AC side is dangerous, the DC side is not. Treat them accordingly.

### AC input (Mains -- 230V, DANGEROUS)

| Terminal | Connect to | Wire color (EU standard) |
|----------|-----------|--------------------------|
| L | Live | Brown |
| N | Neutral | Blue |
| FG (the earth symbol) | Earth / Ground | Green-yellow |

**Recommended approach for bench test:** Use the Handson Aansluitsnoer 2.5m from GAMMA (3x1.50mm2, randaarde plug, KEMA certified, product B186276, EUR 6.99). Cut the socket end off, strip the 3 wires (brown=L, blue=N, green-yellow=FG), and screw them into the L, N, and FG terminals on the PSU. For production, use an IEC C14 panel-mount inlet on the cave enclosure instead of a cut cable.

### DC output

| Terminal | Connect to | Wire color |
|----------|-----------|------------|
| V+ | +12V rail on breadboard (bottom red) | Orange |
| V- | GND rail on breadboard (bottom blue) | Black |

### Safety checklist

- [ ] Verify the PSU voltage selector is set to 230V (or confirm universal input 85-264VAC printed on the label -- the LRS-50-12 is universal, but check).
- [ ] Earth / ground wire MUST be connected to the FG terminal.
- [ ] No exposed mains wiring -- use heat-shrink tubing on all AC connections.
- [ ] Test the DC output with a multimeter before connecting to the breadboard (expect ~12.0V between V+ and V-).
- [ ] NEVER touch the AC terminals while the cord is plugged in.
- [ ] Unplug from the wall before making any wiring changes on the PSU.

Once the PSU reads ~12.0V on the multimeter and nothing on the AC side is exposed, you are ready to place components on the breadboard.

## 1c. PSU power verification (Step 0)

A pre-flight smoke test: confirm the MEAN WELL LRS-50-12 is actually outputting 12V at the breadboard rails before connecting any expensive components (ESP32, 74HCT245, AX-12A). Drives a single LED through a current-limiting resistor -- a visual go/no-go.

### Circuit

A simple LED + current-limiting resistor to visually confirm 12V is present on the breadboard rails.

R = (12V - 2V) / 20mA = 500 ohm. Use a 1K ohm resistor (safer, ~10mA, LED still lights clearly).

LRS-50-12 V+ (+12V rail) -> 1K ohm resistor -> LED anode (long leg) -> LED cathode (short leg) -> GND rail -> LRS-50-12 V-

### Parts
- 1x LED (any color, standard 5mm or 3mm through-hole) -- from Kitronik kit
- 1x 1K ohm resistor -- ORDERED from TinyTronics (the Kitronik kit does NOT contain 1K ohm resistors; it ships 220 ohm, 2.2K ohm, and 10K ohm only)

### Steps
1. Complete section 1b (PSU mains wiring) first -- PSU must be wired to the Handson cord but NOT plugged in yet
2. Wire PSU DC output to breadboard: V+ to bottom red rail (+12V), V- to bottom blue rail (GND)
3. Place 1K ohm resistor: one leg in the +12V rail, other leg in a free row
4. Place LED: anode (long leg) in the same row as the resistor's free leg, cathode (short leg) in the GND rail
5. Double-check: resistor bridges +12V to LED anode, LED cathode connects to GND. No direct 12V-to-LED connection without the resistor.
6. Plug in the Handson cord to mains
7. LED lights up = 12V rail confirmed. If LED does not light, unplug immediately and check polarity/connections.
8. (Optional) Measure with multimeter across +12V and GND rails -- expect ~12.0V
9. Unplug from mains
10. Remove the LED and resistor -- they were only for verification. The breadboard is now ready for the AX-12A circuit (section 2 onwards).

### Safety
- NEVER touch the PSU AC terminals while plugged in
- If the LED does not light, unplug FIRST, then troubleshoot
- The LED test draws ~10mA -- negligible load, safe for the PSU

## 2. Breadboard placement strategy

Half-size breadboard orientation: long axis horizontal, two power railson top (red/blue), two on the bottom, and the center channel splittingrows a-e (top half) from rows f-j (bottom half).

Rail assignments (label them in the sketch by double-clicking the railand typing the label):

- Top red rail = `+5V` (from Feather `USB` pin, representingESP32-S3 5V)
- Top blue rail = `GND` (common ground, shared by ESP32, AX-12A, PSU)
- Bottom red rail = `+12V` (from MEAN WELL LRS-50-12)
- Bottom blue rail = `GND` (tied to top blue rail via a black jumper)

Component placement:

1. **Adafruit Feather ESP32-C1 (stand-in for ESP32-S3 DevKitC)** --straddle the center channel, USB-C facing left. The Feather isphysically smaller than the ESP32-S3 DevKitC (28 mm wide vs ~25 mmfor the Feather, ~51 mm long vs ~74 mm) and occupies fewer rows --roughly rows 1-16 on the breadboard, with the 12-pin header on oneside and the 16-pin header on the other. The Feather pin labels(`USB`, `GND`, `TX`, `RX`, `IO0`, etc.) are visible directly onthe sketch; use those labels when attaching wires and consult thePin Mapping section (1a) for the corresponding ESP32-S3 GPIOnumbers.
2. **74HCT245 DIP-20** (placed as `74LVC245` from the bin, renamedin Inspector) -- straddle the center channel to the right of theFeather, occupying rows 18-27 (pins 1-10 in the top half on row e,pins 11-20 in the bottom half on row f). Pin 1 is the row nearestthe notch.
3. **1 kohm resistor** -- between 74HCT245 pin 3 (A2) and a freejunction row (e.g. row 22 column h). Place horizontally so oneleg lands on the pin-3 row and the other on the junction row.
4. **2.2 kohm resistor** -- from the junction row to the GND rail(top blue). Place vertically.
5. **AX-12A 3-pin header** (`Sparkfun Pin Header (3 pin)`, renamedto `AX-12A`) -- bottom-right of the board, rows 27-29 incolumns a-c (or any free 3-row block on the bottom half). Labelpins top-to-bottom: `VCC (red)`, `DATA (yellow)`, `GND (black)`.
6. **12V screw terminal** (`2-pin screw terminal`) -- bottom-left ofthe board, anchored to the +12V and bottom GND rails.

## 3. Connection table (every wire)

All connections from `wiring/ax12a-bench-test/codey-prompt.txt`. Wirecolors per the codey prompt and `wiring/WIRING.md`:

- **Red** = +5V signal/power
- **Orange** = +12V power
- **Black** = GND
- **Yellow** = signal/data
- **Green** = data (alternative; use for the GPIO 8 DIR line belowso it visually separates control from UART data)

The **From** column lists the Feather stand-in pin label that appearson the Fritzing sketch, with the actual ESP32-S3 GPIO inparentheses. Always wire to the Feather label in the sketch; thefirmware on real hardware uses the GPIO numbers in parentheses.

| # | From | To | Color | Purpose |
| --- | --- | --- | --- | --- |
| 1 | Feather `USB` (ESP32-S3 5V) | +5V rail (top red) | Red | 5V supply for 74HCT245 |
| 2 | Feather `GND` (ESP32-S3 GND) | GND rail (top blue) | Black | Common ground |
| 3 | 74HCT245 pin 20 (VCC) | +5V rail | Red | Buffer logic supply |
| 4 | 74HCT245 pin 10 (GND) | GND rail | Black | Buffer ground |
| 5 | 74HCT245 pin 19 (OE, active low) | GND rail | Black | Always-enabled output |
| 6 | Feather `IO0` (ESP32-S3 GPIO 8) | 74HCT245 pin 1 (DIR) | Green | Half-duplex direction control |
| 7 | Feather `TX` (ESP32-S3 GPIO 15, UART2 TX) | 74HCT245 pin 2 (A1) | Yellow | TX into low-voltage side |
| 8 | 74HCT245 pin 3 (A2) | 1 kohm resistor -> junction | Yellow | RX from low-voltage side (series leg of divider) |
| 9 | Junction row | Feather `RX` (ESP32-S3 GPIO 16, UART2 RX) | Yellow | Divided RX into ESP32 (~3.23V) |
| 10 | Junction row | 2.2 kohm resistor -> GND rail | Black | Lower leg of voltage divider |
| 11 | 74HCT245 pin 17 (B2) | 74HCT245 pin 18 (B1) | Yellow | Bridge B1 and B2 (half-duplex bus) |
| 12 | 74HCT245 pin 18 (B1) / pin 17 (B2) bridge | AX-12A header DATA (middle pin) | Yellow | Single-wire data bus to servo |
| 13 | AX-12A header VCC (top pin) | +12V rail (bottom red) | Orange | Servo motor supply |
| 14 | AX-12A header GND (bottom pin) | GND rail | Black | Servo ground |
| 15 | 12V screw terminal V+ | +12V rail | Orange | PSU 12V input |
| 16 | 12V screw terminal V- | GND rail (bottom blue) | Black | PSU return |
| 17 | Top GND rail (blue) | Bottom GND rail (blue) | Black | Tie both GND rails together (single ground) |

Unused pins on the 74HCT245 (pins 4-9 = A3-A8, pins 11-16 = B3-B8) areleft unconnected -- do not jumper them anywhere.

## 4. Fritzing UI tips

- **Set resistor values**: click the resistor, open the Inspectorpanel (right side), and change `Resistance` to `1k` or `2.2k`. Thecolor bands and label update automatically. Repeat for both resistors.
- **Bridge B1 and B2**: drag a short yellow wire from row of pin 18to row of pin 17 across the center channel (a horizontal jumper onthe breadboard back half).
- **Label wires**: double-click a wire to add a label such as`UART2 TX (Feather TX = GPIO 15 -> A1)`. Labels are visible inSchematic view too. Include both the Feather stand-in label andthe actual ESP32-S3 GPIO so the sketch stays self-documenting.
- **Label pin headers**: select the 3-pin AX-12A header, open theInspector, and rename the part to `AX-12A`. To label each pin,switch to Schematic view and add a text note next to each terminal.
- **Switch views**: use the tabs at the top of the canvas to movebetween Breadboard, Schematic, and PCB. Schematic and PCB views areoptional for this bench build but recommended for future fabrication.
- **Rail labels**: double-click a power rail (or use the small labelswatch at the start of the rail in newer Fritzing builds) and type`+5V`, `+12V`, or `GND`.

## 5. Save and export

1. `File` -> `Save As` -> `electronics/fritzing/ax12a-buffer_v1.fzz`(filename must match the planned name in`electronics/fritzing/README.md`).
2. `File` -> `Export` -> `as Image...` -> select `PNG`, set width to`3000 px`, save to `electronics/exports/ax12a-buffer_v1-breadboard.png`.
3. `File` -> `Export` -> `as Image...` -> select `SVG`, save to`electronics/exports/ax12a-buffer_v1-breadboard.svg`.
4. Switch to Schematic view and repeat the PNG + SVG exports with the`-schematic` suffix.
5. Do not commit Gerbers from this bench-test sketch -- those belongto the production PCB project, not this buffer breadboard.

## 6. Verification checklist

Run through every item before saving and exporting:

- [ ] Top GND rail, bottom GND rail, ESP32 GND, 74HCT245 pin 10, AX-12AGND, and 12V PSU V- all share one continuous ground net.
- [ ] +5V rail only reaches 74HCT245 pin 20 and the ESP32 5V pin --it does NOT touch the AX-12A header.
- [ ] +12V rail only reaches the AX-12A header VCC pin and the 12Vscrew terminal -- it does NOT touch any 74HCT245 or ESP32 pin.
- [ ] Voltage divider on the RX path: 1 kohm in series from pin 3 (A2)to the junction, 2.2 kohm from the junction to GND, junctionconnects to ESP32 GPIO 16. No direct wire from pin 3 to GPIO 16.
- [ ] 74HCT245 pin 19 (OE) tied to GND.
- [ ] 74HCT245 pin 17 (B2) and pin 18 (B1) bridged with a singleyellow jumper, and that bridge goes to the AX-12A DATA pin.
- [ ] No floating used pins on the 74HCT245 (pins 1, 2, 3, 10, 17,18, 19, 20 are all connected; pins 4-9 and 11-16 areintentionally unconnected).
- [ ] Every wire color matches the table in section 3.
- [ ] All labels typed in Fritzing use straight ASCII quotes only.

When all boxes are ticked, the sketch is ready for save and export.