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

- [ ] Copy `voice/config/render_backend.json.example` → `voice/config/render_backend.json`
- [ ] Edit `command_template` to call real local voice renderer
- [ ] Configure review thresholds in `voice/config/review_policy.json`
- [ ] Run `bash voice/scripts/run_voice_factory_real.sh`
- [ ] Inspect `voice/review/approved/`
- [ ] Inspect `voice/review/needs_human_review/`
- [ ] Inspect `voice/review/rejected/`
- [ ] Regenerate Ardour cue data after approved batch

## Phase 10 — Install Coqui XTTS Backend

- [ ] Run `bash mac/scripts/install_voice_backend_coqui.sh`
- [ ] Copy `voice/config/coqui_xtts_backend.json.example` → `voice/config/coqui_xtts_backend.json`
- [ ] Put reference WAV files in `voice/reference_audio/`
- [ ] Ensure `voice/config/render_backend.json` points at `render_with_coqui_xtts.py`
- [ ] Activate voice venv: `source ~/venvs/pixstars-voice/bin/activate`
- [ ] Test one render: `python3 voice/scripts/render_with_coqui_xtts.py --text '"Hello..."' --emotion '"curious"' --output '"voice/output/candidates/test.wav"'`
- [ ] Run full pipeline: `bash voice/scripts/run_voice_factory_real.sh`

## Notes

*Add any notes, blockers, or decisions here as you go.*

- 2026-04-17: Phase 1 complete. Pi Zero 2 WH ordered (Amazon.nl).
- 2026-04-18: Pi Zero 2 WH arrived. USB-C microSD card reader ordered. Phase 2 blocked until reader arrives.
- 2026-04-28: Phase 2 audio input test passed (USB PnP Sound Device on card 1). Output test skipped — no speaker; Pi is thin endpoint.
- 2026-04-28: Phase 6 complete. Dialogue CSV kept as placeholder examples (performance is silent). Manifest generated at voice/output/dialogue_manifest.json.
- 2026-04-28: Phase 7 complete. Cue manifest generated at ardour/cues/cue_manifest.csv. emit_state.py tested with 'idle' state.
- 2026-04-28: Phase 8 complete. HiveMind installed (Docker + 8-container stack), project 'Pixstars Voice Factory' created with 6 agents (Director, Dialogue Curator, Voice Designer, Render Operator, Evaluator, Publisher). Local pipeline proven with stub scripts.