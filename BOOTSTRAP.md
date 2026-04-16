# BOOTSTRAP.md

## Pixstars Super Pack Bootstrap

This file helps you get from zero to first proof-of-life quickly.

## Goal of bootstrap day 1

Prove these 5 things:

1. The Pi boots and is reachable
2. The Pi microphone and speaker work
3. The Mac Mini HiveMind server starts
4. The Pi can pair with the Mac Mini
5. The LED ring can show `idle`, `listening`, `thinking`, and `speaking`

## Fastest practical sequence

### On the Mac Mini
```bash
bash mac/scripts/install_hivemind_server.sh
cp mac/config/server.json.example ~/.config/hivemind-core/server.json
```

Then edit `~/.config/hivemind-core/server.json`.

### On the Pi
```bash
bash pi/scripts/install_pi_satellite.sh
mkdir -p ~/.config/mycroft
cp pi/config/mycroft.conf.example ~/.config/mycroft/mycroft.conf
```

### Pairing
On the Mac:
```bash
source ~/venvs/hivemind-server/bin/activate
hivemind-core add-client
```

On the Pi:
```bash
source ~/venvs/hivemind-mic-sat/bin/activate
hivemind-client set-identity --key YOUR_KEY --password YOUR_PASSWORD --host MAC_MINI_IP --port 5678 --siteid pixstars-lamp
```

### LED proof
On the Pi:
```bash
python3 pi/scripts/led_hivemind_states.py
```

Use:
- `i`
- `l`
- `t`
- `s`
- `e`

### Audio proof
On the Pi:
```bash
arecord -d 5 test.wav
aplay test.wav
```

### Server proof
On the Mac:
```bash
source ~/venvs/hivemind-server/bin/activate
hivemind-core listen
```

## Thin-endpoint checkpoint

At the end of bootstrap day 1, ask:
- Can the Pi capture audio?
- Can the Pi play audio?
- Can the Pi show lamp states?
- Can the Mac Mini do the thinking?

If yes, the architecture is on the right track.


## Voice-factory checkpoint

After the lamp and server work, prove this next:

```bash
bash voice/scripts/run_voice_factory.sh
```

You are successful if:
- dialogue.csv is refreshed from episode markdown
- render_queue.json is created
- candidate WAV placeholders appear
- evaluation.csv is created
- approved files land in `voice/output/final_wav/`
- Ardour cue manifest regenerates


## Real renderer checkpoint

After the stubbed pipeline works, prove the real backend handoff:

```bash
cp voice/config/render_backend.json.example voice/config/render_backend.json
# edit voice/config/render_backend.json
bash voice/scripts/run_voice_factory_real.sh
python3 voice/scripts/review_summary.py
```

You are successful if:
- your backend creates real WAV files in `voice/output/candidates/`
- the evaluator writes `evaluation.csv`
- the review queue buckets are populated
- approved files land in `voice/output/final_wav/`
- the Ardour cue manifest regenerates


## Concrete renderer checkpoint

After installing the voice backend:

```bash
source ~/venvs/pixstars-voice/bin/activate
cp voice/config/coqui_xtts_backend.json.example voice/config/coqui_xtts_backend.json
cp voice/config/render_backend.json.example voice/config/render_backend.json
python3 voice/scripts/render_with_coqui_xtts.py --text '"Hello..."' --emotion '"curious"' --output '"voice/output/candidates/test.wav"'
bash voice/scripts/run_voice_factory_real.sh
```

You are successful if:
- `voice/output/candidates/test.wav` is created
- the full voice factory run publishes approved WAVs
- the Ardour cue manifest regenerates
