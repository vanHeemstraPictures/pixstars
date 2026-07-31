# INTENT_MVP_2.md

Pixstars Intent Engine MVP 2 -- ROS Evaluation Brief (research-only)

Version: 2.0Status: ProposedRepository: pixstars/intent

## 1. Executive summary

This MVP is a research brief, not a build. It asks whether any ideas from the[Robot Operating System (ROS)](https://www.ros.org) ecosystem are worthborrowing to strengthen Pixstars show control for the October 2026 performance,without committing to adopt ROS as a runtime. The deliverable is a shortrecommendation memo that lands on exactly one of three outcomes: ignore,partially adopt (borrow ideas only), or adopt (evaluate as a runtime). Nothingin the current stack -- Ardour, the Python conductor, the ESP32 cave, theMaestro servo bus, the ILDA laser chain, or the rehearsal simulator -- ismodified as part of this MVP.

## 2. Scope

- In scope: desk research into ROS concepts (messaging, node lifecycle,message typing, rosbag-style capture, RViz-style visualisation, TF-styleframe transforms, launch/orchestration) against the actual Pixstars stack;a per-concept scoring pass; a single recommendation.
- Out of scope: installing ROS, selecting a ROS 2 distribution or middleware,writing prototypes, editing `conductor/`, `projection/`, ESP32 firmware, or`simulator/laser_galvo.py`, and any architecture migration.

## 3. Research question (single, precise)

For a silent, 20-minute, timecode-driven live performance with one animatroniclamp (cave ESP32 + Maestro servos + AX-12A + WS2812 + turntable stepper + ILDAlaser), a Mac Mini running Ardour and a Python conductor, a Roland keyboard,and a rear projector: does any part of the ROS ecosystem offer a materiallybetter return than the current OSC-plus-Python conductor, given a fixed showdate and a solo technical lead?

## 4. Evaluation criteria (Pixstars-specific)

Each ROS concept under review is scored against:

- **Orchestration fit** -- does it improve timecode-driven cue dispatch acrossArdour, ESP32 cave, projection, and laser?
- **Messaging fit** -- does it improve on OSC for the actual Pixstars topology(Mac Mini <-> one ESP32 cave <-> one projector <-> one ILDA DAC)?
- **Hardware abstraction** -- does it reduce coupling between the conductorand the specific servo/stepper/LED/laser hardware in the cave?
- **Simulation and rehearsal** -- does it improve dry-run and offlinerehearsal beyond what `conductor --dry-run` and `simulator/laser_galvo.py`already offer?
- **Operational overhead** -- install footprint, learning curve, on-the-nightfailure modes, and whether it survives a single-operator show environment.
- **Time-to-October-2026** -- can any concrete benefit land before theperformance without displacing screenplay, hardware, or Ardour work alreadyin flight.

Any concept that fails "operational overhead" or "time-to-October-2026" isrejected regardless of its score elsewhere.

## 5. Decision boundary (three permitted outcomes)

The research must recommend exactly one of:

1. **Ignore** -- ROS adds no value that is not already covered; no follow-up.
2. **Partially adopt (borrow ideas only)** -- name specific ROS concepts worthmirroring in the existing Python/OSC stack.
3. **Adopt (evaluate as a runtime)** -- justify why the operational cost ofintroducing ROS 2 before October 2026 is repaid within the show's scope.

Options 2 and 3 must include an explicit follow-up MVP proposal; option 1closes the topic.

## 6. Non-goals

- No ROS installation, packaging, or code changes in this MVP.
- No rewrite of `conductor/`, `projection/`, ESP32 firmware, or simulator.
- No selection of specific ROS 2 distributions or middleware.
- No generic robotics comparison; the frame is Pixstars-specific (one lamp,one show, one date).
- No commitment that a follow-up MVP will happen; the research maylegitimately conclude "ignore".

## 7. Expected recommendation output

A short memo appended to this file (or a sibling note) containing:

- The research question from section 3, verbatim.
- A per-concept table scored against the section 4 criteria.
- One of the three section 5 outcomes, stated plainly.
- If outcome 2 or 3: a one-paragraph sketch of a follow-up MVP -- not adesign, not a prototype, no diagrams beyond what the memo needs to bereadable.

## 8. Assumptions to confirm

- The likely output is a recommendation memo rather than a prototype.
- Pixstars is more likely to benefit from selected ROS ideas than from fullROS adoption.