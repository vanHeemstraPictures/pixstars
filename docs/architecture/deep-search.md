# PIXSTARS Architecture Update

## Executive Summary

The updated PIXSTARS architecture should be centered on a three-tier model: **Apple Mac mini M4 Pro backstage as director**, **Seeed reComputer RK3588-40 in the lamp base as brain**, and **Raspberry Pi Zero 2 WH in the lamp head as nervous system**. That mapping is supported by the hardware characteristics of each device: the Mac mini provides strong general-purpose orchestration I/O and is configurable up to 10Gb Ethernet; the RK3588-40 gives you the stronger Rockchip CPU/GPU/multimedia/networking profile plus 16GB LPDDR5 in the selected SKU; and the Pi Zero 2 W platform gives you a compact 5V, GPIO-capable, CSI-equipped controller that is physically well suited to head-local peripherals. citeturn24view0turn15view0turn2view0turn2view3turn16search1

The base-brain choice should now be treated as settled in favor of **RK3588-40 over RK3576-20**. Seeed currently markets both reComputer RK platforms with a 6 TOPS NPU, but the RK3588 platform materially improves the surrounding system that matters to PIXSTARS: Cortex-A76/A55 instead of Cortex-A72/A53, Mali-G610 instead of Mali-G52, richer PCIe, stronger 8K media capability, four-display support instead of three, and dual 2.5GbE instead of dual gigabit on the RK3576 family. In a lamp that is intended to do local voice, perception, behavior, and future robotics—not just blink and speak—that extra system headroom matters more than the on-paper NPU parity. citeturn9view0turn12search1turn15view0turn8view5

The PCIe/M.2 accelerator slot should be **reserved physically now but left logically unspecified**. Seeed markets the platform as expandable “up to 26 TOPS” via PCIe/M.2, and specifically points to Hailo and Rockchip accelerators in its launch material. But because the exact module has not been selected, the rigorous architecture treatment is to reserve the slot, cooling margin, and power budget without pretending the final accelerator behavior, framework, or total system TOPS are already fixed. citeturn2view0turn15view0turn22view0

The lamp’s optical model also needed correction. The **WS2812 LED ring is an indirect expressive source mounted to face the rear shade vents**, so it should be documented as vent glow rather than bulb light. The **forward-facing bulb role** belongs to the **magnet-mounted Olight Sphere ambient lamp** that replaces the original bulb position in the PIXSTARS design. Olight positions the Sphere as a self-contained 360° app-controlled ambient lamp, which means it should be modeled as a distinct smart-light subsystem rather than as a raw GPIO-driven emitter. citeturn25view1turn25view0

## Research Findings

The RK3588 case is especially strong for PIXSTARS because Rockchip’s own product material describes the chip as combining a 6.0 TOPS NPU, Mali-G610 MC4 graphics, 8K codec capability, multi-camera support, and rich high-speed interfaces including PCIe and high-bandwidth display/camera paths. The shorter Rockchip brief shows the same architecture from a silicon/I/O perspective: quad Cortex-A76 plus quad Cortex-A55, PCIe 3.0, multiple MIPI CSI lanes, and 8K media blocks. That is exactly the kind of platform that benefits a character device with local CV, audio, and timing logic. citeturn12search1turn10view3turn10view5turn10view4

The Pi Zero 2 W class hardware is a strong fit for the head because the official Raspberry Pi brief documents a 65 × 30 mm footprint, quad-core Cortex-A53 at 1 GHz, 512MB LPDDR2, CSI-2 camera connector, USB OTG, and 5V input. Those are the right traits for a near-device controller that should sit close to microphones, speakers, status lights, buttons, sensors, and future servos. That same brief is also why the Pi should stay out of the heavy-AI role: it is a compact embedded device controller, not the best place for sustained local STT, VLM/LLM experiments, or multi-stream CV. citeturn2view3turn16search1

The backstage Mac mini also needed a precision note in the documentation: **it is not natively a 2.5GbE machine**. Apple lists Gigabit Ethernet as standard and 10Gb Ethernet as a configurable option on the M4 Pro model. So the right wording for the PIXSTARS network is not “everything is 2.5GbE,” but rather “the Ethernet fabric is 2.5GbE-capable on the RK3588 nodes, with the Mac attached at GbE or optional 10GbE.” That small clarification makes the architecture more rigorous and avoids baking in an inaccurate port assumption. citeturn24view0

On the accelerator path, **Hailo-8 M.2** is the cleanest future-forward candidate if PIXSTARS really goes “full out on A.I.” Hailo’s official module page documents up to 26 TOPS, PCIe Gen 3, M.2 form factors, and support paths across TensorFlow, TFLite, ONNX, Keras, and PyTorch. Coral remains attractive for narrower fixed CV pipelines because Coral documents 4 TOPS for a single Edge TPU and still lists M.2 accelerator products; Intel’s Myriad X remains technically interesting for vision-specific pipelines, but Intel’s own materials show the consumer Neural Compute Stick 2 is discontinued, which weakens it as the best long-term default for a new stage platform. citeturn22view0turn19search9turn19search0turn18view0turn23search4turn23search13

## Deliverables

The updated architecture document and downloadable system diagrams have been created here:

- [Download `docs/architecture/ARCHITECTURE.md`](sandbox:/mnt/data/docs/architecture/ARCHITECTURE.md)
- [Download `docs/architecture/PIXSTARS_SYSTEM_ARCHITECTURE.svg`](sandbox:/mnt/data/docs/architecture/PIXSTARS_SYSTEM_ARCHITECTURE.svg)
- [Download `docs/architecture/PIXSTARS_SYSTEM_ARCHITECTURE.png`](sandbox:/mnt/data/docs/architecture/PIXSTARS_SYSTEM_ARCHITECTURE.png)

![Updated PIXSTARS system architecture diagram](sandbox:/mnt/data/docs/architecture/PIXSTARS_SYSTEM_ARCHITECTURE.png)

The Markdown document includes an executive summary, physical topology, component-relationship Mermaid diagram, compute comparison table, networking/power guidance, PCIe accelerator strategy, optical clarification for the rear vent ring and front Olight Sphere bulb replacement, and an “open items” section that explicitly marks still-unspecified hardware choices rather than guessing them.

## Platform Comparison

The comparison below synthesizes the current Seeed product pages, Seeed’s launch matrix, and Rockchip’s official silicon documentation. citeturn2view0turn2view1turn15view0turn9view0turn12search1turn10view3turn10view5

| Platform | CPU / GPU | AI | RAM in analyzed SKU | Camera / media / network | Price and upgrade path |
|---|---|---|---|---|---|
| **RK3576-20** | 4× Cortex-A72 + 4× Cortex-A53; Mali-G52 MC3 | 6 TOPS NPU | 4GB LPDDR5 | 16MP ISP, triple CSI-2, Seeed markets 8K@30 decode / 4K@60 encode / 3 displays / dual gigabit family networking | $99; workable entry point, but tighter long-term ceiling |
| **RK3588-40** | 4× Cortex-A76 + 4× Cortex-A55; Mali-G610 MC4 | 6 TOPS NPU | 16GB LPDDR5 | Multi-camera RK3588 path, 8K-class media, Seeed markets 8K@60 decode / 8K@30 encode / 4 displays / dual 2.5GbE | $249; strongest default brain for PIXSTARS |
| **RK3588-40 + reserved PCIe/M.2 accelerator** | Same RK3588 base | 6 TOPS on-SoC plus external accelerator path | Same 16GB base RAM unless customized | Same media/I/O plus offload runway for heavier CV | Price depends on card; best upgrade path, but exact module still unspecified |

The most important architecture conclusion from that table is not just that RK3588 is faster; it is that **RK3588 buys margin**. It gives PIXSTARS room for simultaneous local voice, behavior, camera work, networking, and future expansion without forcing the head hardware to do jobs it should never own in the first place. citeturn15view0turn12search1turn9view0

## Design Decisions

The updated diagram and Markdown now treat the **head/base/backstage split as first-class**. The head owns local buses and peripherals such as microphone, speaker, sensors, camera termination if needed, and servo PWM/GPIO. The base owns the RK3588 brain, optional NVMe, power entry, cooling, and the reserved accelerator slot. Backstage owns the Mac mini, operator tooling, audio/session orchestration, and optional heavier services. That is both emotionally right for the “living lamp” illusion and mechanically right for cable length, serviceability, and thermal management. citeturn2view3turn15view0turn24view0

The network section of the documentation now reflects the actual transport stack you wanted: **Ethernet**, **Wi‑Fi**, **MQTT**, **WebSocket**, **REST**, plus explicit internal lamp buses such as **USB**, **UART**, **I²C**, **GPIO**, and **PWM**. The report also treats USB/IP between the Pi head and RK3588 base as the preferred internal strategy, with UART retained as a low-level fallback. That recommendation is an architectural choice rather than a vendor requirement, but it matches the goal of preserving message-oriented behavior across the whole character stack.

The power architecture is intentionally documented as **logical domains, not fake precision**, because several values remain unspecified. The hard facts are that Seeed documents 9–19V DC input for the reComputer RK family and Raspberry Pi documents 5V input for the Zero 2 W. Everything beyond that—base-brick wattage, servo rail current, amplifier topology, whether the Olight Sphere is separately charged or semi-integrated—should remain clearly labeled as open until the final mechanical and motion system are fixed. citeturn15view0turn2view3turn25view0

The front bulb replacement decision also changes the control story. Because Olight positions the Sphere as an app-controlled smart ambient lamp with built-in modes, group control, and phone-driven behavior, the architecture document now treats it as a **separate smart-light subsystem**. That keeps the documentation honest. If later you decide that the front lamp must become frame-accurate show-control hardware, the cleaner path is either BLE/API integration if practical or replacing it with a custom wired emitter module; until then, the architecture should not imply deterministic GPIO control that the product was never designed for. citeturn25view1turn25view0

## Open Questions

The generated `ARCHITECTURE.md` explicitly marks these as open rather than pretending they are fixed:

- **Exact PCIe accelerator model**: Hailo looks like the strongest first candidate, but the architecture currently leaves the module unspecified. citeturn22view0turn15view0
- **Exact base PSU rating and rail plan**: only the RK3588 input range and Pi 5V requirement are firm in the sources reviewed. citeturn15view0turn2view3
- **Servo count, torque, and driver topology**: not specified by the user, so the diagram correctly treats motion as future-capable rather than finalized.
- **Front Olight Sphere control path**: the physical bulb replacement role is clear, but whether it stays standalone, becomes BLE-controlled, or is later swapped for a wired front emitter remains open. citeturn25view1turn25view0

The attached deliverables are therefore rigorous where the public evidence is strong, and intentionally conservative where the project has not yet fixed a part choice.
