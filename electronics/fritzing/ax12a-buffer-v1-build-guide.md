# ax12a-buffer_v1.fzz -- Build Guide

Step-by-step instructions for assembling the Fritzing project`ax12a-buffer_v1.fzz` from scratch. The circuit is a bench test of the74HCT245 half-duplex TTL buffer that the cave ESP32-S3 uses to talk tothe Dynamixel AX-12A head nod servo (Cave Architecture v3).

Authoritative circuit spec: `wiring/ax12a-bench-test/codey-prompt.txt`.Wire color conventions: `wiring/WIRING.md`. Board purpose:`electronics/pcbs/ax12a-buffer/README.md`. File naming:`electronics/fritzing/README.md`.

Use straight ASCII quotes only when typing labels in Fritzing.

> IMPORTANT -- Fritzing stand-in part. The Fritzing parts bin on macOS does not ship an ESP32-S3 N16R8 DevKitC. This sketch uses the Adafruit Feather ESP32-C1 (#5933) as a visual stand-in for documentation only. The physical build uses the ESP32-S3 N16R8 DevKitC -- the Feather has a different form factor and pin layout, so always cross-reference the Pin Mapping section below before wiring real hardware. Rename the Feather to ESP32-S3 N16R8 DevKitC in the Inspector so the sketch label matches the bench build.

> IMPORTANT -- 74LVC245 vs 74HCT245. Fritzing's parts bin on macOS ships 74LVC245 (low-voltage CMOS) instead of 74HCT245. The DIP-20 pinout is identical -- only the logic family differs. Place the 74LVC245 in the sketch, then rename it to 74HCT245 in the Inspector so the silkscreen label matches the physical board. The bench build uses an actual 74HCT245.

> IMPORTANT -- Two-breadboard Fritzing stand-in. The ESP32-S3 stand-in and the 74HCT245 (plus its RX divider network) do not fit comfortably on a single half-size breadboard. The sketch therefore uses **two half-size breadboards stacked vertically** (upper + lower) and treats the matching rails between them as one continuous rail: **red-rail-to-red-rail** (+5V and +12V feeds continue across both boards) and **blue-rail-to-blue-rail** (GND is a single continuous net). "Red-rail-to-red-rail" and "blue-rail-to-blue-rail" describe which physical breadboard rails are bridged, not the jumper wire color -- the jumper wire color still follows the +12V = orange, +5V = red, GND = black convention. See Section 2 for the upper/lower role split. In the physical bench build these two stand-in boards collapse onto **one extended breadboard** with enough length for all components; Fritzing does not ship an extended breadboard in its parts bin, which is why the sketch uses two half-size boards to represent it. Any placement wording in this guide that refers to "the breadboard" without an upper/lower qualifier refers to the lower board in the Fritzing sketch and to the single extended board in the physical build.

## Wire color vs breadboard rail color

The physically red-striped power rails on the breadboard carry +5V (top rail) and +12V (bottom rail) in this bench build, and the physically blue-striped rails carry GND. That is a property of the breadboard silkscreen, not a wire color choice. The wire color convention in this bench build is separate and unchanged:

- **Orange** = +12V wires (NOT red)
- **Red** = +5V wires
- **Black** = GND wires
- **Yellow** = DATA / UART signal
- **Green** = DIR (control)

Wherever this guide refers to a "red rail" it means the physically red-striped breadboard power rail; the jumper landed on that rail is still orange when it carries +12V and red only when it carries +5V. This applies equally to the inter-board rail bridges in section 2.

## 1. Parts list

Open Fritzing, switch to the Breadboard view, and search the Parts bin(top-right) for each item. Drag onto the sketch:

| Qty | Component | Fritzing part (exact name) | Notes |
| --- | --- | --- | --- |
| 2 | Half-size breadboard (Fritzing stand-in) | Breadboard Half + | 400 tie points each (30 rows + 2 power rails per side). Stacked upper + lower to stand in for a single extended breadboard; matching rails are treated as continuous (red-rail-to-red-rail, blue-rail-to-blue-rail -- the wire color of each rail-bridging jumper still follows the +12V = orange, +5V = red, GND = black convention). See Section 2. |
| 1 | ESP32-S3 N16R8 DevKitC (stand-in) | Adafruit Feather ESP32-C1 (#5933) | Visual stand-in only. Rename to ESP32-S3 N16R8 DevKitC in the Inspector. See Pin Mapping section -- the Feather's labelled pins do NOT line up with the actual ESP32-S3 GPIO numbers. |
| 1 | 74HCT245 octal buffer | 74LVC245 | Same DIP-20 pinout as 74HCT245. Rename to 74HCT245 in the Inspector. The physical build uses a real 74HCT245. |
| 1 | Resistor (1 kohm) | Resistor | Set Resistance to 1k in the Inspector. Axial through-hole. |
| 1 | Resistor (2.2 kohm) | Resistor | Set Resistance to 2.2k in the Inspector. Axial through-hole. |
| 1 | 3-pin male header | Sparkfun Pin Header (3 pin) | Acts as the AX-12A pigtail. Pin order (measured): Pin 1 = GND (black), Pin 2 = VCC (red), Pin 3 = DATA (yellow). Both 3-pin sockets on the AX-12A servo share the same daisy-chain pinout, so the pigtail can plug into either socket. Label it AX-12A in the Inspector. |
| 1 | 2-pin screw terminal | 2-pin screw terminal | 12V input from MEAN WELL LRS-50-12. A DC barrel jack is also acceptable; either way label it LRS-50-12 12V IN. |

All parts above are in the Fritzing core library on macOS -- no extraparts packs required. Do not invent custom parts for this bench test.

## 1a. Pin mapping (Feather stand-in -> actual ESP32-S3 DevKitC)

The Adafruit Feather ESP32-C1 (#5933) used in this Fritzing sketch hasa **different pinout** from the ESP32-S3 N16R8 DevKitC used in thephysical build. When wiring the sketch, attach jumpers to the **Featherpin labels** in the left column; the middle column is the actualESP32-S3 GPIO that this represents on real hardware. The right columnis the destination on the 74HCT245 buffer (DIP-20 pin numbering).

| Actual ESP32-S3 pin | Feather stand-in pin | Wire to |
| --- | --- | --- |
| GPIO 15 (UART2 TX) | TX | 74HCT245 pin 2 (A1) |
| GPIO 16 (UART2 RX) | RX | 1 kohm resistor from 74HCT245 pin 3 (A2) (divider junction) |
| GPIO 8 (DIR) | IO0 | 74HCT245 pin 1 (DIR) |
| 5V | USB | +5V rail (top red) |
| GND | GND | GND rail (top blue) |

When the firmware is flashed to the real ESP32-S3 DevKitC, the GPIOnumbers in the firmware match the left column. The Feather pin labelsin the middle column exist only inside Fritzing -- ignore them outsideof this sketch.

## 1b. PSU mains wiring (MEAN WELL LRS-50-12)

Wire the MEAN WELL LRS-50-12 to wall power *before* placing anything on the breadboard. The bench test runs on **Netherlands 230V mains** -- the AC side is dangerous, the DC side is not. Treat them accordingly.

### AC input (Mains -- 230V, DANGEROUS)

| Terminal | Connect to | Wire color (EU standard) |
| --- | --- | --- |
| L | Live | Brown |
| N | Neutral | Blue |
| FG (the earth symbol) | Earth / Ground | Green-yellow |

**Recommended approach for bench test:** Use the Handson Aansluitsnoer 2.5m from GAMMA (3x1.50mm2, randaarde plug, KEMA certified, product B186276, EUR 6.99). Cut the socket end off, strip the 3 wires (brown=L, blue=N, green-yellow=FG), and screw them into the L, N, and FG terminals on the PSU. For production, use an IEC C14 panel-mount inlet on the cave enclosure instead of a cut cable.

### DC output

In the Fritzing stand-in the PSU screw terminal sits on the **lower breadboard**; in the physical build it sits at the corresponding end of the single extended breadboard. Either way the target rails are the +12V and GND rails on that board.

| Terminal | Connect to | Wire color |
| --- | --- | --- |
| V+ | +12V rail on the lower breadboard (bottom red) | Orange |
| V- | GND rail on the lower breadboard (bottom blue) | Black |

### PSU DC output to breadboard

Use two Kitronik M/M jumper wires to connect the PSU DC output screw terminals to the lower-breadboard power rails:

| Wire | Color | From (PSU terminal) | To (lower breadboard) |
| --- | --- | --- | --- |
| 1 | Orange | V+ (+12V) screw terminal | Left red rail, row 2 (+12V) |
| 2 | Black | V- (COM/GND) screw terminal | Left blue rail, row 2 (GND) |

Steps:

1. Ensure the PSU is unplugged from mains
2. Loosen the V+ screw terminal on the PSU DC output side
3. Insert the stripped/bare end of an orange jumper wire, tighten the screw
4. Push the pin end of the orange wire into the left red (+) rail on the lower breadboard (row 2)
5. Repeat with a black jumper wire: stripped end into the V- (COM) screw terminal, pin end into the left blue (-) rail on the lower breadboard (row 2)
6. Verify: orange wire bridges PSU V+ to the lower-breadboard +12V rail, black wire bridges PSU V- to the lower-breadboard GND rail. Because the upper and lower boards' matching rails are treated as continuous (red-rail-to-red-rail, blue-rail-to-blue-rail), the +12V and GND nets are also live on the upper board.

### Safety checklist

- [ ] Verify the PSU voltage selector is set to 230V (or confirm universal input 85-264VAC printed on the label -- the LRS-50-12 is universal, but check).
- [ ] Earth / ground wire MUST be connected to the FG terminal.
- [ ] No exposed mains wiring -- use heat-shrink tubing on all AC connections.
- [ ] Test the DC output with the UNI-T UT139C (Kyoritsu 7066A leads: black -> COM, red -> V/Ohm; range switch on V DC) before connecting to the breadboard -- expect ~12.0V between V+ and V-.
- [ ] NEVER touch the AC terminals while the cord is plugged in.
- [ ] Unplug from the wall before making any wiring changes on the PSU.

Once the UT139C reads ~12.0V across PSU V+ and V- and nothing on the AC side is exposed, you are ready to place components on the breadboard.

## 1c. PSU power verification (Step 0)

A pre-flight smoke test: confirm the MEAN WELL LRS-50-12 is actually outputting 12V at the breadboard rails before connecting any expensive components (ESP32, 74HCT245, AX-12A). Drives a single LED through a current-limiting resistor -- a visual go/no-go.

### Circuit

A simple LED + current-limiting resistor to visually confirm 12V is present on the breadboard rails.

R = (12V - 2V) / 20mA = 500 ohm. Use a 1K ohm resistor (safer, ~10mA, LED still lights clearly).

LRS-50-12 V+ (+12V rail) -> 1K ohm resistor -> LED anode (long leg) -> LED cathode (short leg) -> GND rail -> LRS-50-12 V-

### Parts

- 1x LED (any color, standard 5mm or 3mm through-hole) -- from Kitronik kit
- 1x 1K ohm resistor -- IN HAND from TinyTronics (the Kitronik kit does NOT reliably supply the 1K ohm value; the 2.2K ohm resistor needed elsewhere in the AX-12A divider is likewise sourced from TinyTronics via the 10Ω-1MΩ resistor set -- IN HAND, see HARDWARE_INVENTORY.md)

### Steps

1. Complete section 1b (PSU mains wiring) first -- PSU must be wired to the Handson cord but NOT plugged in yet
2. Wire PSU DC output to breadboard: V+ to bottom red rail (+12V), V- to bottom blue rail (GND)
3. Place 1K ohm resistor: one leg in the +12V rail, other leg in a free row
4. Place LED: anode (long leg) in the same row as the resistor's free leg, cathode (short leg) in the GND rail
5. Double-check: resistor bridges +12V to LED anode, LED cathode connects to GND. No direct 12V-to-LED connection without the resistor.
6. Plug in the Handson cord to mains
7. LED lights up = 12V rail confirmed. If LED does not light, unplug immediately and check polarity/connections.
8. (Optional) Measure with the UT139C across +12V and GND rails (V DC range, 7066A leads: black -> COM/GND rail, red -> V/Ohm/+12V rail) -- expect ~12.0V.
9. Unplug from mains
10. Remove the LED and resistor -- they were only for verification. The breadboard is now ready for the AX-12A circuit (section 2 onwards).

### Safety

- NEVER touch the PSU AC terminals while plugged in
- If the LED does not light, unplug FIRST, then troubleshoot
- The LED test draws ~10mA -- negligible load, safe for the PSU

### Status: PASSED

The PSU smoke test has been completed on physical hardware. The MEAN WELL LRS-50-12 powered the breadboard rails correctly and the verification LED lit as expected in the ON state. Photo evidence:

- `electronics/pcbs/psu-verification/psu_verification_off.png` -- mains unplugged, LED dark
- `electronics/pcbs/psu-verification/psu_verification_on.png` -- mains plugged in, LED lit (12V rail confirmed)

Always unplug from mains before making any wiring changes on the breadboard, even after a successful smoke test.

## 2. Breadboard placement strategy

### Same-row jumper convention (reading the Fritzing image)

In the updated Fritzing export, a component leg and a jumper wire that connect to it are often drawn into two different holes on the same breadboard row rather than sharing a single hole. This is a drawing convention -- a real breadboard hole only reliably accepts one lead at a time, and Fritzing likewise does not stack a leg and a wire pin in the same hole in the exported image. Every hole a-e in a given row (and every hole f-j in the row below the center channel) is tied to the other holes in the same half-row by the internal spring clip, so a jumper in one hole and a component leg in another hole on the same half-row sit on the same electrical node.

When reading the image, treat "same row" as "same electrical node" even if the wire lands in a hole adjacent to the leg it is connecting to. In the physical build, pick any free hole in the same half-row -- no single hole ever has to take both a component leg and a jumper at the same time. The Connection table in section 3 and the Verification checklist in section 6 describe electrical nets, not literal hole coordinates, so both remain unchanged by this convention. Continuity checks in the bench note likewise probe electrical nets and will beep across any two holes in the same half-row.

### Two-breadboard Fritzing stand-in (upper + lower)

The Fritzing sketch places components on **two half-size breadboards stacked vertically** because the ESP32-S3 stand-in and the 74HCT245 with its RX divider network do not fit comfortably on a single half-size board. The two boards represent one continuous board:

- **Rails are matched across the gap**: red-rail-to-red-rail, blue-rail-to-blue-rail (these describe which physical breadboard rails are bridged, not the jumper wire color). The upper board's red-striped rails are jumpered to the lower board's red-striped rails, and the upper board's blue-striped rails are jumpered to the lower board's blue-striped rails. There is a single GND net and a single +5V net across both boards, and the +12V feed reaches whichever board needs it via the bottom red-rail bridge (an orange jumper wire per the +12V = orange convention).
- **Physical build**: on the actual bench hardware the same layout collapses onto **one extended breadboard** long enough to hold everything. Fritzing's parts bin does not ship an extended breadboard, so the two half-size boards in the sketch are the stand-in for it. All electrical nets in Section 3 are identical either way.

Half-size breadboard orientation (both boards): long axis horizontal, two power rails on top (red/blue), two on the bottom, and the center channel splitting rows a-e (top half) from rows f-j (bottom half).

### Rail assignments

Label the rails in the sketch by double-clicking each rail and typing the label. In the exported image the upper board's top rails carry the `+5 Volt` and `+12 Volt` tags used to feed both boards.

- Top red rail (upper + lower, continuous) = `+5V` (from Feather `USB` pin, representing ESP32-S3 5V)
- Top blue rail (upper + lower, continuous) = `GND` (common ground, shared by ESP32, 74HCT245, AX-12A, PSU)
- Bottom red rail (upper + lower, continuous) = `+12V` (from MEAN WELL LRS-50-12)
- Bottom blue rail (upper + lower, continuous) = `GND` (tied to top blue rail via a black jumper on the lower board so all four blue rails are one net)

### Upper breadboard -- buffer + RX divider

The upper board (labeled `Breadboard1` in the sketch) hosts the logic-level side of the circuit:

1. **74HCT245 DIP-20** (placed as `74LVC245` from the bin, renamed to `74HCT245` in the Inspector) -- straddle the center channel with the notch pointing up, occupying roughly rows 20-29 (pins 1-10 in the top half on row e, pins 11-20 in the bottom half on row f). Pin 1 is the row nearest the notch.
2. **1 kohm resistor** (R5) -- horizontal, between 74HCT245 pin 3 (A2) and a free junction row just to the right of the chip. One leg lands on the pin-3 row, the other on the junction row.
3. **2.2 kohm resistor** (R4) -- horizontal, from the junction row down to the top GND rail (blue) of the upper board.

Nothing else lives on the upper board; the +5V, +12V, and GND rails on it are energised via the inter-board rail bridges from the lower board (see the "Inter-board rail bridges" subsection below for jumper wire colors -- +12V is bridged with an orange jumper, +5V with a red jumper, GND with a black jumper).

### Lower breadboard -- ESP32 stand-in, servo pigtail, PSU input

The lower board (labeled `Breadboard` in the sketch) hosts everything the performer plugs into physically:

1. **Adafruit Feather ESP32-C1 (stand-in for ESP32-S3 DevKitC)** -- straddle the center channel with USB-C facing down toward the front edge. The Feather is physically smaller than the ESP32-S3 DevKitC (~25 mm wide vs 28 mm, ~51 mm long vs ~74 mm) and occupies fewer rows than the real DevKitC would. The Feather pin labels (`USB`, `GND`, `TX`, `RX`, `IO0`, etc.) are visible directly on the sketch; use those labels when attaching wires and consult the Pin Mapping section (1a) for the corresponding ESP32-S3 GPIO numbers.
2. **AX-12A 3-pin header** (`Sparkfun Pin Header (3 pin)`, renamed to `AX-12A`) -- placed on the right-hand side of the lower board, on the bottom half. Label pins in AX-12A pin order (Pin 1 -> Pin 3, measured pinout): `GND (black, Pin 1)`, `VCC (red, Pin 2)`, `DATA (yellow, Pin 3)`.
3. **12V screw terminal** (`2-pin screw terminal`, labeled `LRS-50-12 12V IN` / `MEAN WELL LRS-50-12 12V IN Power Supply`) -- bottom-right corner of the lower board, anchored to the +12V (bottom red) and GND (bottom blue) rails.

### Inter-board rail bridges

Add the following jumper wires between the two boards so the matched rails behave as one continuous rail:

- Bridge the two boards' top red-striped rails together (+5V continuous across upper and lower; per wire color convention this bridge uses a red jumper wire)
- Bridge the two boards' top blue-striped rails together (GND continuous across upper and lower; per wire color convention this bridge uses a black jumper wire)
- Bridge the two boards' bottom red-striped rails together (+12V continuous across upper and lower; per wire color convention this bridge uses an orange jumper wire, NOT red -- +12V is never color coded red on this bench)
- Bridge the two boards' bottom blue-striped rails together (GND continuous across upper and lower; per wire color convention this bridge uses a black jumper wire)

In the physical single-extended-breadboard build these bridges are not needed -- the rails are already one continuous piece.

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
| 1 | Feather USB (ESP32-S3 5V) | +5V rail (top red) | Red | 5V supply for 74HCT245 |
| 2 | Feather GND (ESP32-S3 GND) | GND rail (top blue) | Black | Common ground |
| 3 | 74HCT245 pin 20 (VCC) | +5V rail | Red | Buffer logic supply |
| 4 | 74HCT245 pin 10 (GND) | GND rail | Black | Buffer ground |
| 5 | 74HCT245 pin 19 (OE, active low) | GND rail | Black | Always-enabled output |
| 6 | Feather IO0 (ESP32-S3 GPIO 8) | 74HCT245 pin 1 (DIR) | Green | Half-duplex direction control |
| 7 | Feather TX (ESP32-S3 GPIO 15, UART2 TX) | 74HCT245 pin 2 (A1) | Yellow | TX into low-voltage side |
| 8 | 74HCT245 pin 3 (A2) | 1 kohm resistor -> junction | Yellow | RX from low-voltage side (series leg of divider) |
| 9 | Junction row | Feather RX (ESP32-S3 GPIO 16, UART2 RX) | Yellow | Divided RX into ESP32 (~3.23V) |
| 10 | Junction row | 2.2 kohm resistor -> GND rail | Black | Lower leg of voltage divider |
| 11 | 74HCT245 pin 17 (B2) | 74HCT245 pin 18 (B1) | Yellow | Bridge B1 and B2 (half-duplex bus) |
| 12 | 74HCT245 pin 18 (B1) / pin 17 (B2) bridge | AX-12A header DATA (Pin 3) | Yellow | Single-wire data bus to servo |
| 13 | AX-12A header VCC (Pin 2, middle pin) | +12V rail (bottom red) | Orange | Servo motor supply |
| 14 | AX-12A header GND (Pin 1) | GND rail | Black | Servo ground |
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

Physical continuity verification of the built breadboard uses the UNI-T UT139C multimeter and the Kyoritsu 7066A red/black lead set. Follow the "Continuity check procedure (UT139C + Kyoritsu 7066A)" section in the bench note (`ccc1bd61-a938-4f77-a036-9895b5924559`) for the exact meter setup (COM / V-Ohm jack assignment, SELECT button to reach the buzzer icon) and the probe-by-probe checklist (26 probe placements covering common GND, +5V, +12V isolation, DATA bus bridge, and RX divider). Do not substitute a generic multimeter procedure -- the tool-specific steps ensure the buzzer threshold, lead polarity, and jack assignments match the bench hardware.

## 7. Bench wiring check: PASSED

The pin-by-pin breadboard wiring check has been completed against the latest Fritzing sketch and verified on physical hardware before any live power-up. All wires match the Connection table in section 3 and the Verification checklist in section 6 is fully satisfied.

Reference assets:

- `electronics/fritzing/ax-12a-bench-test.fzz` -- source sketch used as the wiring reference
- `electronics/exports/ax-12a-bench-test_v1-breadboard.png` -- breadboard export used during the bench check

Confirmed results:

- 5V and +12V rails are physically separated: +5V reaches only the 74HCT245 pin 20 (VCC) and the ESP32 5V pin; +12V reaches only the AX-12A header VCC pin and the 12V screw terminal. There is no wire bridging the +5V and +12V rails at any point.
- Common ground is a single continuous net across ESP32 GND, 74HCT245 pin 10, 74HCT245 pin 19 (OE), the 2.2 kohm divider lower leg, the AX-12A GND pin, the PSU V-, and both blue rails.
- RX voltage divider is in place: 1 kohm in series from 74HCT245 pin 3 (A2) to the junction, 2.2 kohm from the junction to GND, and the junction routed to ESP32 GPIO 16 -- no direct wire from pin 3 to GPIO 16.
- B1 (pin 18) and B2 (pin 17) are bridged and routed to the AX-12A DATA pin; DIR is wired from ESP32 GPIO 8 to 74HCT245 pin 1; TX from ESP32 GPIO 15 to 74HCT245 pin 2 (A1).
- No floating pins on the buffer beyond the intentionally unconnected A3-A8 and B3-B8.

Safety reminder: keep the Handson cord unplugged from mains until the live power-up procedure begins. The wiring check above was performed with the PSU disconnected from mains and the ESP32 USB-C cable unplugged.