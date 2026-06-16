# ax12a-buffer_v1.fzz -- Build Guide

Step-by-step instructions for assembling the Fritzing project
`ax12a-buffer_v1.fzz` from scratch. The circuit is a bench test of the
74HCT245 half-duplex TTL buffer that the cave ESP32-S3 uses to talk to
the Dynamixel AX-12A head nod servo (Cave Architecture v3).

Authoritative circuit spec: `wiring/ax12a-bench-test/codey-prompt.txt`.
Wire color conventions: `wiring/WIRING.md`. Board purpose:
`electronics/pcbs/ax12a-buffer/README.md`. File naming:
`electronics/fritzing/README.md`.

Use straight ASCII quotes only when typing labels in Fritzing.

------------------------------------------------------------------------

## 1. Parts list

Open Fritzing, switch to the Breadboard view, and search the Parts bin
(top-right) for each item. Drag onto the sketch:

| Qty | Component                | Fritzing search term                  | Notes / fallback |
|-----|--------------------------|---------------------------------------|------------------|
| 1   | Half-size breadboard     | `breadboard` -> "Breadboard Half+"    | 400 tie points (30 rows + 2 power rails per side). |
| 1   | ESP32-S3 N16R8 DevKitC   | `ESP32-S3` or `ESP32 DevKit`          | Fritzing core has no exact S3 N16R8 part. Use the generic "ESP32 DevKit" (or "ESP32-S3 DevKitC" if installed from a community parts bin). In the Inspector, rename to `ESP32-S3 N16R8 DevKitC` so the silkscreen label matches the bench build. |
| 1   | 74HCT245 octal buffer    | `74HCT245` or `octal bus transceiver` | If only `74HC245` is available, use it and rename to `74HCT245` in the Inspector -- the pinout is identical (DIP-20). |
| 1   | Resistor (1 kohm)        | `resistor`                            | Set value in Inspector. Axial through-hole. |
| 1   | Resistor (2.2 kohm)      | `resistor`                            | Set value in Inspector. Axial through-hole. |
| 1   | 3-pin male header        | `pin header` -> "Generic male header - 3 pins" | Acts as the AX-12A pigtail (VCC / DATA / GND). Label it `AX-12A` in the Inspector. |
| 1   | 2-pin screw terminal     | `screw terminal` -> "Screw terminal - 2 pins" | 12V input from MEAN WELL LRS-50-12. A `DC barrel jack` is also acceptable; either way label it `LRS-50-12 12V IN`. |

If a part is missing from the core library, install the official
Fritzing parts pack (`Part` -> `Import...`) or substitute the closest
generic equivalent and rename it. Do not invent custom parts for this
bench test.

------------------------------------------------------------------------

## 2. Breadboard placement strategy

Half-size breadboard orientation: long axis horizontal, two power rails
on top (red/blue), two on the bottom, and the center channel splitting
rows a-e (top half) from rows f-j (bottom half).

Rail assignments (label them in the sketch by double-clicking the rail
and typing the label):

- Top red rail   = `+5V`     (from ESP32 5V pin)
- Top blue rail  = `GND`     (common ground, shared by ESP32, AX-12A, PSU)
- Bottom red rail = `+12V`   (from MEAN WELL LRS-50-12)
- Bottom blue rail = `GND`   (tied to top blue rail via a black jumper)

Component placement:

1. **ESP32-S3 DevKit** -- straddle the center channel, USB-C facing
   left. With most generic ESP32 DevKit parts, the board lands on
   rows 1-19 (top half a-b and bottom half i-j). Exact row numbers
   depend on the specific Fritzing part footprint; the rule is
   "center channel, USB-C left, pin headers on both sides of the gap."
2. **74HCT245 DIP-20** -- straddle the center channel to the right of
   the ESP32, occupying rows 21-30 (pins 1-10 in the top half on
   rows e, pins 11-20 in the bottom half on row f). Pin 1 is the row
   nearest the notch.
3. **1 kohm resistor** -- between 74HCT245 pin 3 (A2) and a free
   junction row (e.g. row 25 column h). Place horizontally so one
   leg lands on the pin-3 row and the other on the junction row.
4. **2.2 kohm resistor** -- from the junction row to the GND rail
   (top blue). Place vertically.
5. **AX-12A 3-pin header** -- bottom-right of the board, rows 27-29
   in columns a-c (or any free 3-row block on the bottom half).
   Label pins top-to-bottom: `VCC (red)`, `DATA (yellow)`, `GND (black)`.
6. **12V screw terminal** -- bottom-left of the board, anchored to
   the +12V and bottom GND rails.

------------------------------------------------------------------------

## 3. Connection table (every wire)

All connections from `wiring/ax12a-bench-test/codey-prompt.txt`. Wire
colors per the codey prompt and `wiring/WIRING.md`:

- **Red**    = +5V signal/power
- **Orange** = +12V power
- **Black**  = GND
- **Yellow** = signal/data
- **Green**  = data (alternative; use for the GPIO 8 DIR line below
  so it visually separates control from UART data)

| #  | From                          | To                            | Color  | Purpose                          |
|----|-------------------------------|-------------------------------|--------|----------------------------------|
| 1  | ESP32 5V pin                  | +5V rail (top red)            | Red    | 5V supply for 74HCT245           |
| 2  | ESP32 GND pin                 | GND rail (top blue)           | Black  | Common ground                    |
| 3  | 74HCT245 pin 20 (VCC)         | +5V rail                      | Red    | Buffer logic supply              |
| 4  | 74HCT245 pin 10 (GND)         | GND rail                      | Black  | Buffer ground                    |
| 5  | 74HCT245 pin 19 (OE, active low) | GND rail                   | Black  | Always-enabled output            |
| 6  | ESP32 GPIO 8                  | 74HCT245 pin 1 (DIR)          | Green  | Half-duplex direction control    |
| 7  | ESP32 GPIO 15 (UART2 TX)      | 74HCT245 pin 2 (A1)           | Yellow | TX into low-voltage side         |
| 8  | 74HCT245 pin 3 (A2)           | 1 kohm resistor -> junction   | Yellow | RX from low-voltage side (series leg of divider) |
| 9  | Junction row                  | ESP32 GPIO 16 (UART2 RX)      | Yellow | Divided RX into ESP32 (~3.23V)   |
| 10 | Junction row                  | 2.2 kohm resistor -> GND rail | Black  | Lower leg of voltage divider     |
| 11 | 74HCT245 pin 17 (B2)          | 74HCT245 pin 18 (B1)          | Yellow | Bridge B1 and B2 (half-duplex bus) |
| 12 | 74HCT245 pin 18 (B1) / pin 17 (B2) bridge | AX-12A header DATA (middle pin) | Yellow | Single-wire data bus to servo |
| 13 | AX-12A header VCC (top pin)   | +12V rail (bottom red)        | Orange | Servo motor supply               |
| 14 | AX-12A header GND (bottom pin)| GND rail                      | Black  | Servo ground                     |
| 15 | 12V screw terminal V+         | +12V rail                     | Orange | PSU 12V input                    |
| 16 | 12V screw terminal V-         | GND rail (bottom blue)        | Black  | PSU return                       |
| 17 | Top GND rail (blue)           | Bottom GND rail (blue)        | Black  | Tie both GND rails together (single ground) |

Unused pins on the 74HCT245 (pins 4-9 = A3-A8, pins 11-16 = B3-B8) are
left unconnected -- do not jumper them anywhere.

------------------------------------------------------------------------

## 4. Fritzing UI tips

- **Set resistor values**: click the resistor, open the Inspector
  panel (right side), and change `Resistance` to `1k` or `2.2k`. The
  color bands and label update automatically. Repeat for both resistors.
- **Bridge B1 and B2**: drag a short yellow wire from row of pin 18
  to row of pin 17 across the center channel (a horizontal jumper on
  the breadboard back half).
- **Label wires**: double-click a wire to add a label such as
  `UART2 TX (GPIO 15 -> A1)`. Labels are visible in Schematic view too.
- **Label pin headers**: select the 3-pin AX-12A header, open the
  Inspector, and rename the part to `AX-12A`. To label each pin,
  switch to Schematic view and add a text note next to each terminal.
- **Switch views**: use the tabs at the top of the canvas to move
  between Breadboard, Schematic, and PCB. Schematic and PCB views are
  optional for this bench build but recommended for future fabrication.
- **Rail labels**: double-click a power rail (or use the small label
  swatch at the start of the rail in newer Fritzing builds) and type
  `+5V`, `+12V`, or `GND`.

------------------------------------------------------------------------

## 5. Save and export

1. `File` -> `Save As` -> `electronics/fritzing/ax12a-buffer_v1.fzz`
   (filename must match the planned name in
   `electronics/fritzing/README.md`).
2. `File` -> `Export` -> `as Image...` -> select `PNG`, set width to
   `3000 px`, save to `electronics/exports/ax12a-buffer_v1-breadboard.png`.
3. `File` -> `Export` -> `as Image...` -> select `SVG`, save to
   `electronics/exports/ax12a-buffer_v1-breadboard.svg`.
4. Switch to Schematic view and repeat the PNG + SVG exports with the
   `-schematic` suffix.
5. Do not commit Gerbers from this bench-test sketch -- those belong
   to the production PCB project, not this buffer breadboard.

------------------------------------------------------------------------

## 6. Verification checklist

Run through every item before saving and exporting:

- [ ] Top GND rail, bottom GND rail, ESP32 GND, 74HCT245 pin 10, AX-12A
      GND, and 12V PSU V- all share one continuous ground net.
- [ ] +5V rail only reaches 74HCT245 pin 20 and the ESP32 5V pin --
      it does NOT touch the AX-12A header.
- [ ] +12V rail only reaches the AX-12A header VCC pin and the 12V
      screw terminal -- it does NOT touch any 74HCT245 or ESP32 pin.
- [ ] Voltage divider on the RX path: 1 kohm in series from pin 3 (A2)
      to the junction, 2.2 kohm from the junction to GND, junction
      connects to ESP32 GPIO 16. No direct wire from pin 3 to GPIO 16.
- [ ] 74HCT245 pin 19 (OE) tied to GND.
- [ ] 74HCT245 pin 17 (B2) and pin 18 (B1) bridged with a single
      yellow jumper, and that bridge goes to the AX-12A DATA pin.
- [ ] No floating used pins on the 74HCT245 (pins 1, 2, 3, 10, 17,
      18, 19, 20 are all connected; pins 4-9 and 11-16 are
      intentionally unconnected).
- [ ] Every wire color matches the table in section 3.
- [ ] All labels typed in Fritzing use straight ASCII quotes only.

When all boxes are ticked, the sketch is ready for save and export.
