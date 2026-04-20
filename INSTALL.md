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
4. Run:`bash mac/scripts/install_hivemind_server.sh`
5. Copy:`mac/config/server.json.example`to:`~/.config/hivemind-core/server.json`
6. Adjust:

- wake-word model path
- STT plugin
- TTS plugin

### Phase 2 — Raspberry Pi lamp head

> **Recommended SD card:** Use a high-quality A2-rated microSD card (e.g. SanDisk Extreme
> 64GB A2). A fast card with good random I/O makes the Pi feel responsive instead of
> "slightly off" — your audience will notice a 20ms jitter that feels wrong, even if
> they can't name it.

#### Step 1 — Flash the microSD card

Use **Raspberry Pi Imager** (`brew install --cask raspberry-pi-imager`).

When flashing:

- **Device**: Raspberry Pi Zero 2 W
- **OS**: Raspberry Pi OS Lite (64-bit) — don't use a desktop image, you don't need it
- **Storage**: your microSD card

In **Edit Settings** (gear icon), configure:

- **Hostname**: `pixstars-lamp`
- **Username**: `pi`
- **Password**: set one you'll remember
- **WiFi**: your local network SSID and password
- **Locale**: your timezone and keyboard layout
- **Services tab**: Enable SSH (password authentication)

Click **Save**, then **Yes** to write. Takes about 5 minutes.

Insert the card into the Pi, power it on via micro-USB. Give it 2 minutes to boot.

```bash
ping pixstars-lamp.local
```

#### Step 2 — SSH into the Pi and update

```bash
ssh pi@pixstars-lamp.local
```

First boot optimization:

```bash
sudo apt update && sudo apt upgrade -y
```

Install basics:

```bash
sudo apt install -y git python3-pip python3-venv alsa-utils
```

#### Step 3 — Optimize the SD card (important for responsiveness)

Enable TRIM:

```bash
sudo systemctl enable fstrim.timer
```

Reduce unnecessary writes — edit `/etc/fstab`:

```bash
sudo nano /etc/fstab
```

Find the root (`/`) line and add `noatime,nodiratime` to the options. This reduces
constant disk writes and improves system smoothness.

Optional but recommended — move logs to RAM to protect the SD card:

```bash
sudo apt install -y log2ram
```

#### Step 4 — Install HiveMind satellite

```bash
bash pi/scripts/install_pi_satellite.sh
```

#### Step 5 — Configure HiveMind satellite

```bash
cp pi/config/mycroft.conf.example ~/.config/mycroft/mycroft.conf
```

Edit the config if needed (STT/TTS plugin, wake word, Mac Mini host IP).

#### Step 6 — Audio sanity check (critical for your project)

Test input (microphone):

```bash
arecord -d 5 test.wav
```

Test output (speaker):

```bash
aplay test.wav
```

If this is clean, your foundation is solid.

#### Architecture reminder

| Raspberry Pi (lamp) | Mac Mini (brain) |
|---------------------|------------------|
| Microphone input | HiveMind server |
| Speaker output | XTTS voice generation |
| LED control | Automation pipeline |
| Trigger playback | Storage of all audio |

Don't push heavy processing into the lamp head — keep the Pi as a thin endpoint.

### Phase 3 — Pairing

1. On Mac Mini:`source ~/venvs/hivemind-server/bin/activate hivemind-core add-client`
2. On Pi:`source ~/venvs/hivemind-mic-sat/bin/activate hivemind-client set-identity --key YOUR_KEY --password YOUR_PASSWORD --host MAC_MINI_IP --port 5678 --siteid pixstars-lamp`

### Phase 4 — LED system

1. Copy `pi/scripts/led_hivemind_states_filewatch.py` to the Pi home directory
2. Copy `pi/systemd/pixstars-lamp-led.service` to `/etc/systemd/system/`
3. Enable:`sudo systemctl daemon-reload sudo systemctl enable pixstars-lamp-led sudo systemctl start pixstars-lamp-led`

### Phase 5 — HiveMind satellite service

1. Copy `pi/systemd/pixstars-lamp-sat.service` to `/etc/systemd/system/`
2. Adjust `ExecStart` if needed
3. Enable:`sudo systemctl daemon-reload sudo systemctl enable pixstars-lamp-sat sudo systemctl start pixstars-lamp-sat`

### Phase 6 — Voice scaffold

1. Create starter dialogue file:`python3 voice/scripts/extract_dialogue_template.py`
2. Edit:`voice/data/dialogue.csv`
3. Build manifest:`python3 voice/scripts/build_manifest.py`

### Phase 7 — Ardour scaffold

1. Generate cue manifest:`python3 ardour/scripts/generate_cue_manifest.py`
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

1. Install Hivemind on the Mac Mini using the upstream installer:`curl -fsSL https://raw.githubusercontent.com/hivementality-ai/hivemind/main/install.sh | bash`
2. Open:`http://localhost:8080`
3. Create a workspace for the Pixstars lamp voice workflow
4. Add the agent briefs from:`voice/orchestration/agents/`
5. Populate:`voice/orchestration/state/episode_sources.txt`
6. Prove the local pipeline manually:`bash voice/scripts/run_voice_factory.sh`
7. After that works, move the same sequence into a Hivemind saved workflow or heartbeat-scheduled task

### Real-time warning

Use Hivemind to automate the **backstage voice factory**, not the low-latency on-stage lamp path.

### Phase 9 — Real render backend and review queue

1. Copy:`voice/config/render_backend.json.example`to:`voice/config/render_backend.json`
2. Edit `command_template` so it calls your real local voice renderer on the Mac Mini
3. Configure review thresholds in:`voice/config/review_policy.json`
4. Run:`bash voice/scripts/run_voice_factory_real.sh`
5. Inspect:

- `voice/review/approved/`
- `voice/review/needs_human_review/`
- `voice/review/rejected/`

1. Regenerate Ardour cue data after each approved batch

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

1. Run:`bash mac/scripts/install_voice_backend_coqui.sh`
2. Copy:`voice/config/coqui_xtts_backend.json.example`to:`voice/config/coqui_xtts_backend.json`
3. Put authorized reference WAV files in:`voice/reference_audio/`
4. Ensure `voice/config/render_backend.json` points at:`python3 voice/scripts/render_with_coqui_xtts.py --text {text_json} --emotion {emotion_json} --output {output_json}`
5. Activate the voice environment:`source ~/venvs/pixstars-voice/bin/activate`
6. Test one render:`python3 voice/scripts/render_with_coqui_xtts.py --text '"Hello..."' --emotion '"curious"' --output '"voice/output/candidates/test.wav"'`
7. Run the full pipeline:`bash voice/scripts/run_voice_factory_real.sh`

### Concrete backend note

This repository now defaults to a Coqui XTTS-based local renderer because it can clone and cache voices for reuse from reference audio, and the maintained `coqui-tts` package is the recommended installation path in the current docs.