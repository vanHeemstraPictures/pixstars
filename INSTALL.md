# INSTALL.md

## Pixstars Super Pack Installation Guide

This pack combines:
- lamp head build files
- HiveMind / OVOS server setup
- LED state system
- wake-word notes
- synthetic voice scaffold
- Ardour cue/state scaffold

## Recommended installation order

### Phase 1 — Mac Mini foundation
1. Review `README.md`
2. Review `docs/PIXSTARS_LAMP_COMPLETE_BUILD.md`
3. Review `docs/OPTIMIZED_PIXSTARS_ARCHITECTURE.md`
4. Run:
   ```bash
   bash mac/scripts/install_hivemind_server.sh
   ```
5. Copy:
   ```text
   mac/config/server.json.example
   ```
   to:
   ```text
   ~/.config/hivemind-core/server.json
   ```
6. Adjust:
   - wake-word model path
   - STT plugin
   - TTS plugin

### Phase 2 — Raspberry Pi lamp head
1. Flash Raspberry Pi OS Lite
2. SSH into the Pi
3. Run:
   ```bash
   bash pi/scripts/install_pi_satellite.sh
   ```
4. Copy:
   ```text
   pi/config/mycroft.conf.example
   ```
   to:
   ```text
   ~/.config/mycroft/mycroft.conf
   ```
5. Test:
   ```bash
   arecord -d 5 test.wav
   aplay test.wav
   ```

### Phase 3 — Pairing
1. On Mac Mini:
   ```bash
   source ~/venvs/hivemind-server/bin/activate
   hivemind-core add-client
   ```
2. On Pi:
   ```bash
   source ~/venvs/hivemind-mic-sat/bin/activate
   hivemind-client set-identity --key YOUR_KEY --password YOUR_PASSWORD --host MAC_MINI_IP --port 5678 --siteid pixstars-lamp
   ```

### Phase 4 — LED system
1. Copy `pi/scripts/led_hivemind_states_filewatch.py` to the Pi home directory
2. Copy `pi/systemd/pixstars-lamp-led.service` to `/etc/systemd/system/`
3. Enable:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable pixstars-lamp-led
   sudo systemctl start pixstars-lamp-led
   ```

### Phase 5 — HiveMind satellite service
1. Copy `pi/systemd/pixstars-lamp-sat.service` to `/etc/systemd/system/`
2. Adjust `ExecStart` if needed
3. Enable:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable pixstars-lamp-sat
   sudo systemctl start pixstars-lamp-sat
   ```

### Phase 6 — Voice scaffold
1. Create starter dialogue file:
   ```bash
   python3 voice/scripts/extract_dialogue_template.py
   ```
2. Edit:
   ```text
   voice/data/dialogue.csv
   ```
3. Build manifest:
   ```bash
   python3 voice/scripts/build_manifest.py
   ```

### Phase 7 — Ardour scaffold
1. Generate cue manifest:
   ```bash
   python3 ardour/scripts/generate_cue_manifest.py
   ```
2. Use `ardour/scripts/emit_state.py` or `ardour/scripts/cue_wrapper_example.sh` as the first coupling point between cue playback and lamp states

## Optimized architecture note

### Pi = endpoint
Use the Pi primarily for:
- mic
- speaker
- LED
- lightweight connectivity

### Mac Mini = brain
Use the Mac Mini for:
- HiveMind server
- STT
- synthetic voice
- orchestration
- Ardour integration

Do not push heavy processing into the lamp head unless you have already proven that the thin-endpoint design is stable.


### Phase 8 — Hivemind voice automation
1. Install Hivemind on the Mac Mini using the upstream installer:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/hivementality-ai/hivemind/main/install.sh | bash
   ```
2. Open:
   ```text
   http://localhost:8080
   ```
3. Create a workspace for the Pixstars lamp voice workflow
4. Add the agent briefs from:
   ```text
   voice/orchestration/agents/
   ```
5. Populate:
   ```text
   voice/orchestration/state/episode_sources.txt
   ```
6. Prove the local pipeline manually:
   ```bash
   bash voice/scripts/run_voice_factory.sh
   ```
7. After that works, move the same sequence into a Hivemind saved workflow or heartbeat-scheduled task

### Real-time warning
Use Hivemind to automate the **backstage voice factory**, not the low-latency on-stage lamp path.


### Phase 9 — Real render backend and review queue
1. Copy:
   ```text
   voice/config/render_backend.json.example
   ```
   to:
   ```text
   voice/config/render_backend.json
   ```
2. Edit `command_template` so it calls your real local voice renderer on the Mac Mini
3. Configure review thresholds in:
   ```text
   voice/config/review_policy.json
   ```
4. Run:
   ```bash
   bash voice/scripts/run_voice_factory_real.sh
   ```
5. Inspect:
   - `voice/review/approved/`
   - `voice/review/needs_human_review/`
   - `voice/review/rejected/`
6. Regenerate Ardour cue data after each approved batch

### Hivemind saved workflow recommendation
Ask Hivemind to run this exact sequence:
1. extract dialogue
2. build manifest
3. create render queue
4. render candidates with the configured backend
5. evaluate candidates
6. build the review queue
7. publish approved assets
8. regenerate the Ardour cue manifest
9. summarize the review outcome


### Phase 10 — Install the concrete Coqui XTTS backend on the Mac Mini
1. Run:
   ```bash
   bash mac/scripts/install_voice_backend_coqui.sh
   ```
2. Copy:
   ```text
   voice/config/coqui_xtts_backend.json.example
   ```
   to:
   ```text
   voice/config/coqui_xtts_backend.json
   ```
3. Put authorized reference WAV files in:
   ```text
   voice/reference_audio/
   ```
4. Ensure `voice/config/render_backend.json` points at:
   ```text
   python3 voice/scripts/render_with_coqui_xtts.py --text {text_json} --emotion {emotion_json} --output {output_json}
   ```
5. Activate the voice environment:
   ```bash
   source ~/venvs/pixstars-voice/bin/activate
   ```
6. Test one render:
   ```bash
   python3 voice/scripts/render_with_coqui_xtts.py --text '"Hello..."' --emotion '"curious"' --output '"voice/output/candidates/test.wav"'
   ```
7. Run the full pipeline:
   ```bash
   bash voice/scripts/run_voice_factory_real.sh
   ```

### Concrete backend note
This repository now defaults to a Coqui XTTS-based local renderer because it can clone and cache voices for reuse from reference audio, and the maintained `coqui-tts` package is the recommended installation path in the current docs.
