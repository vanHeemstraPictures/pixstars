# Pixstars — Installation Progress

> Track your progress through the [INSTALL.md](./INSTALL.md) phases.
> Mark each step as you complete it: change `[ ]` to `[x]`.

---

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

- [ ] Flash Raspberry Pi OS Lite
- [ ] SSH into the Pi
- [ ] Run `bash pi/scripts/install_pi_satellite.sh`
- [ ] Copy `pi/config/mycroft.conf.example` → `~/.config/mycroft/mycroft.conf`
- [ ] Test audio: `arecord -d 5 test.wav && aplay test.wav`

## Phase 3 — Pairing

- [ ] On Mac Mini: activate venv, run `hivemind-core add-client`
- [ ] On Pi: activate venv, run `hivemind-client set-identity` with key, password, host, port, siteid

## Phase 4 — LED System

- [ ] Copy `pi/scripts/led_hivemind_states_filewatch.py` to Pi home directory
- [ ] Copy `pi/systemd/pixstars-lamp-led.service` to `/etc/systemd/system/`
- [ ] Run `sudo systemctl daemon-reload`
- [ ] Run `sudo systemctl enable pixstars-lamp-led`
- [ ] Run `sudo systemctl start pixstars-lamp-led`

## Phase 5 — HiveMind Satellite Service

- [ ] Copy `pi/systemd/pixstars-lamp-sat.service` to `/etc/systemd/system/`
- [ ] Adjust `ExecStart` if needed
- [ ] Run `sudo systemctl daemon-reload`
- [ ] Run `sudo systemctl enable pixstars-lamp-sat`
- [ ] Run `sudo systemctl start pixstars-lamp-sat`

## Phase 6 — Voice Scaffold

- [ ] Run `python3 voice/scripts/extract_dialogue_template.py`
- [ ] Edit `voice/data/dialogue.csv`
- [ ] Run `python3 voice/scripts/build_manifest.py`

## Phase 7 — Ardour Scaffold

- [ ] Run `python3 ardour/scripts/generate_cue_manifest.py`
- [ ] Test `ardour/scripts/emit_state.py` or `ardour/scripts/cue_wrapper_example.sh`

## Phase 8 — HiveMind Voice Automation

- [ ] Install HiveMind on Mac Mini via upstream installer
- [ ] Open `http://localhost:8080` and verify
- [ ] Create workspace for Pixstars lamp voice workflow
- [ ] Add agent briefs from `voice/orchestration/agents/`
- [ ] Populate `voice/orchestration/state/episode_sources.txt`
- [ ] Run `bash voice/scripts/run_voice_factory.sh` (prove local pipeline)
- [ ] Move sequence into HiveMind saved workflow or heartbeat-scheduled task

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

---

## Notes

_Add any notes, blockers, or decisions here as you go._

- 2026-04-17: Phase 1 complete. Pi Zero 2 WH ordered (Amazon.nl), arriving 2026-04-18. Phase 2 blocked until hardware arrives.

- 

