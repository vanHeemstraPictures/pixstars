# Pixstars Voice + Ardour Starter Pack

This pack extends the main Pixstars lamp starter with:

- a `voice/` scaffold for synthetic voice creation
- an `ardour/` scaffold for cue management and state integration

It is intended to be added into the `vanHeemstraDesigns/pixstars` repository next to the lamp/HiveMind starter files.

## Scope

This pack helps you:

- collect and structure dialogue
- prepare datasets for a synthetic lamp voice
- render WAV lines into a predictable output layout
- integrate state changes with cue playback
- keep Ardour and lamp-state logic aligned

## Main folders

```text
voice/
ardour/
shared/
```

## Optimized architecture update

This pack now reflects a merged Pixstars design:

- **thin lamp endpoint** inspired by mark2-assist style satellites
- **Mac Mini M4 Pro as the real brain**
- **HiveMind for distributed communication**
- **Ardour for deterministic stage cues**
- **synthetic voice pipeline on the Mac**
- **LED state embodiment on the Pi**

## Hivemind voice automation update

This version adds a **Mac-side Hivemind automation layer** for the synthetic lamp voice workflow.

### Purpose

Hivemind is used here as a **backstage orchestration system**, not as the real-time voice engine in the lamp path.

It can help automate:

- dialogue extraction from episode markdown
- dataset normalization
- render queue creation
- candidate evaluation
- promotion of approved WAV files
- Ardour cue manifest generation

### Real-time rule

Keep the real-time stage path lean:

- Pi = mic + speaker + LEDs + lightweight client
- Mac Mini = HiveMind + STT + synthetic voice + Ardour
- Hivemind = workflow automation around the voice pipeline

## v4 upgrade

This version replaces the earlier voice stubs with:

- a **real local render backend interface**
- a **review queue**
- a **publish-from-approved** flow
- a **Hivemind-friendly automation sequence** for the whole episode → voice → Ardour path

## v5 concrete renderer

This version wires the voice factory to a **concrete local backend on the Mac Mini**:

- Coqui XTTS-based renderer wrapper
- cached speaker identity
- reference-audio folder
- install script for the voice backend