# Pixstars — Installation Progress

> Track your progress through the INSTALL.md phases.Mark each step as you complete it: change [ ] to [x].

## Phase 1 — Mac Mini Foundation

- [x] Review `README.md`
- [x] Review `docs/PIXSTARS_LAMP_COMPLETE_BUILD.md`
- [x] Review `docs/OPTIMIZED_PIXSTARS_ARCHITECTURE.md`
- [x] Run `bash mac/scripts/install_hivemind_server.sh`
- [x] Copy `mac/config/server.json.example` → `~/.config/hivemind-core/server.json`
- [x] Adjust wake-word model path
- [x] Adjust STT plugin
- [x] Adjust TTS plugin

## Phase 2 — Raspberry Pi Lamp Head

- [x] Flash microSD card with Raspberry Pi OS Lite (32-bit, Debian Trixie) via Raspberry Pi Imager
- [x] Configure: hostname `pixstars-lamp`, SSH, WiFi, username `pi`, Raspberry Pi Connect (optional)
- [x] Boot Pi and verify: `ping pixstars-lamp.local`
- [x] SSH into Pi: `ssh pi@pixstars-lamp.local`
- [x] Update system: `sudo apt update && sudo apt upgrade -y`
- [x] Install basics: `sudo apt install -y git python3-pip python3-venv alsa-utils`
- [x] Enable TRIM: `sudo systemctl enable fstrim.timer`
- [x] Optimize fstab: add `noatime,nodiratime` to root mount
- [x] Install log2ram: `sudo apt install -y log2ram`
- [x] Run `bash pi/scripts/install_pi_satellite.sh`
- [x] Copy `pi/config/mycroft.conf.example` → `~/.config/mycroft/mycroft.conf`
- [x] Test audio input: `arecord -d 5 test.wav` (needs USB audio hardware)

- [-] Test audio output: `aplay test.wav` (skipped — no speaker connected, Pi is thin endpoint)

## Phase 3 — Pairing

- [x] On Mac Mini: activate venv, run `hivemind-core add-client`
- [x] On Pi: activate venv, run `hivemind-client set-identity` with key, password, host, port, siteid

## Phase 4 — LED System (skipped — optional in Architecture v3)

- [-] Copy `pi/scripts/led_hivemind_states_filewatch.py` to Pi home directory
- [-] Copy `pi/systemd/pixstars-lamp-led.service` to `/etc/systemd/system/`
- [-] Run `sudo systemctl daemon-reload`
- [-] Run `sudo systemctl enable pixstars-lamp-led`
- [-] Run `sudo systemctl start pixstars-lamp-led`

## Phase 5 — HiveMind Satellite Service (skipped — optional in Architecture v3)

- [-] Copy `pi/systemd/pixstars-lamp-sat.service` to `/etc/systemd/system/`
- [-] Adjust `ExecStart` if needed
- [-] Run `sudo systemctl daemon-reload`
- [-] Run `sudo systemctl enable pixstars-lamp-sat`
- [-] Run `sudo systemctl start pixstars-lamp-sat`

## Phase 6 — Voice Scaffold

- [x] Run `python3 voice/scripts/extract_dialogue_template.py`
- [x] Edit `voice/data/dialogue.csv` (kept example placeholders — silent performance, revisit later)
- [x] Run `python3 voice/scripts/build_manifest.py`

## Phase 7 — Ardour Scaffold

- [x] Run `python3 ardour/scripts/generate_cue_manifest.py`
- [x] Test `ardour/scripts/emit_state.py` or `ardour/scripts/cue_wrapper_example.sh`

## Phase 8 — HiveMind Voice Automation

- [x] Install HiveMind on Mac Mini via upstream installer
- [x] Open `http://localhost:8080` and verify
- [x] Create workspace for Pixstars lamp voice workflow
- [x] Add agent briefs from `voice/orchestration/agents/`

- [-] Populate `voice/orchestration/state/episode_sources.txt` (skipped — silent performance, no episode sources yet)

- [x] Run `bash voice/scripts/run_voice_factory.sh` (prove local pipeline)

- [-] Move sequence into HiveMind saved workflow or heartbeat-scheduled task (deferred — will configure when real content is ready)

## Phase 9 — Real Render Backend and Review Queue

- [x] Copy `voice/config/render_backend.json.example` → `voice/config/render_backend.json`
- [x] Edit `command_template` to call real local voice renderer (already points to Coqui XTTS)
- [x] Configure review thresholds in `voice/config/review_policy.json` (defaults accepted)
- [x] Run `bash voice/scripts/run_voice_factory_real.sh`
- [x] Inspect `voice/review/approved/` (empty — no source dialogue yet)
- [x] Inspect `voice/review/needs_human_review/` (empty — no source dialogue yet)
- [x] Inspect `voice/review/rejected/` (empty — no source dialogue yet)
- [x] Regenerate Ardour cue data after approved batch (ran as part of pipeline)

## Phase 10 — Install Coqui XTTS Backend

- [x] Run `bash mac/scripts/install_voice_backend_coqui.sh`
- [x] Copy `voice/config/coqui_xtts_backend.json.example` → `voice/config/coqui_xtts_backend.json`
- [x] Put reference WAV files in `voice/reference_audio/` (E.T. Phone Home reference clip)
- [x] Ensure `voice/config/render_backend.json` points at `render_with_coqui_xtts.py`
- [x] Activate voice venv: `source ~/venvs/pixstars-voice/bin/activate`
- [x] Test one render: rendered 'Hello...' with curious emotion, 0.535 real-time factor
- [x] Run full pipeline: `bash voice/scripts/run_voice_factory_real.sh`

## Phase 11 — AI Engineering Setup

- [x] Create ai/ directory structure (agents, memory, knowledge, tools, models)
- [x] Create lamp personality agent (ai/agents/lamp/personality.md)
- [x] Create lamp emotional model aligned with 14 lamp states (ai/agents/lamp/emotions.yaml)
- [x] Create lamp system prompt for Ollama (ai/agents/lamp/system_prompt.md)
- [x] Create Walt personality agent (ai/agents/walt/)
- [x] Create director rules referencing conductor/timeline.yaml (ai/agents/director/rules.md)
- [x] Create safety guardrails (ai/agents/safety/guardrails.md)
- [x] Create persistent memory scaffold (ai/memory/lamp_memory.yaml)
- [x] Create knowledge base placeholders (ai/knowledge/)
- [x] Move AI_ENGINEERING_SETUP.md to ai/AI_ENGINEERING_SETUP.md
- [ ] Install Ollama on Mac Mini
- [ ] Pull llama3.1 model
- [ ] Test Ollama with lamp system prompt

## Phase 12 — RK3588-40 Lamp Brain Integration

- [x] Deep research report completed (docs/architecture/deep-research-report.md)
- [x] RK3588-40 confirmed as lamp base AI brain
- [x] ARCHITECTURE.md updated with three-tier model (Director/Brain/Nervous System)
- [x] CLAUDE.md updated with RK3588-40 in hardware stack
- [x] HARDWARE_INVENTORY.md updated with RK3588-40 entry
- [x] ai/ agent files updated to reference RK3588-40 as inference host
- [ ] Procure Seeed Studio reComputer RK3588-40
- [ ] Initial OS and software setup on RK3588-40
- [ ] Test local inference (Whisper STT, Piper TTS)

## Phase 13 — Hardware Procurement and Build

- [x] ComXim MT200RUWSL20ProV3 selected (20cm, White, USB+WiFi, 20kg) — documented in LAMP_ARCHITECTURE_v3.md
- [ ] Order ComXim MT200RUWSL20ProV3 turntable
- [x] Olight Sphere received, fully charged, operations verified via iOS Olight App (latest firmware)
- [ ] Order ESP32 DevKit
- [ ] Order Pololu Mini Maestro 24-channel
- [ ] Order MG996R servos (x4) and MG90S servo (x1)
- [ ] Order Dynamixel AX-12A
- [ ] Order WS2812 5050 RGB LED Ring 16
- [ ] Order Arduino Nano
- [ ] Order MEAN WELL LRS-50-5 PSU
- [ ] Order Seeed Studio reComputer RK3588-40
- [ ] Build riser block (120-150mm, match ComXim footprint)
- [ ] Build cave servo rail assembly
- [ ] Assemble and wire complete lamp

## Notes

*Add any notes, blockers, or decisions here as you go.*

- 2026-04-17: Phase 1 complete. Pi Zero 2 WH ordered (Amazon.nl).
- 2026-04-18: Pi Zero 2 WH arrived. USB-C microSD card reader ordered. Phase 2 blocked until reader arrives.
- 2026-04-28: Phase 2 audio input test passed (USB PnP Sound Device on card 1). Output test skipped — no speaker; Pi is thin endpoint.
- 2026-04-28: Phase 6 complete. Dialogue CSV kept as placeholder examples (performance is silent). Manifest generated at voice/output/dialogue_manifest.json.
- 2026-04-28: Phase 7 complete. Cue manifest generated at ardour/cues/cue_manifest.csv. emit_state.py tested with 'idle' state.
- 2026-04-28: Phase 8 complete. HiveMind installed (Docker + 8-container stack), project 'Pixstars Voice Factory' created with 6 agents (Director, Dialogue Curator, Voice Designer, Render Operator, Evaluator, Publisher). Local pipeline proven with stub scripts.
- 2026-04-28: Phases 9 & 10 complete. Coqui XTTS v2 installed, voice cloning tested with E.T. reference audio. Real voice factory pipeline runs end-to-end. All 10 installation phases complete!
- 2026-05-31: Phase 11 (AI Engineering Setup) Wave 1 complete. ai/ directory created with 14 content files. PR #26 merged. Ollama install pending (Wave 2).
- 2026-05-31: RK3588-40 confirmed as lamp base AI brain. Three-tier architecture: Director (Mac Mini) / Brain (RK3588-40) / Nervous System (Pi Zero 2 WH). Architecture docs updated.
- 2026-05-31: Olight Sphere arrived, fully charged, operations verified via iOS Olight App (latest firmware). Ready for front-facing magnetic bulb integration.
- 2026-05-31: ComXim MT200RUWSL20ProV3 (20cm, White) confirmed as base rotation turntable. Documented in LAMP_ARCHITECTURE_v3.md section 12.