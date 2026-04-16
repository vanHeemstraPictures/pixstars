# Voice Automation Runbook

## Purpose

This runbook tells you exactly what to do to automate the voice pipeline around Hivemind.

## Pre-conditions

Before using this runbook, you should already have:
- the Pi lamp endpoint working
- the Mac Mini HiveMind server working
- the basic `voice/` and `ardour/` scaffolds in place

## Daily operator workflow

### 1. Start the local voice stack on the Mac Mini
- ensure the Pixstars repo is present
- ensure your Python environment for voice scripts is ready
- ensure Hivemind is running on `localhost:8080`

### 2. Open the Hivemind workspace
Open the workspace dedicated to the lamp voice.

### 3. Ask the Director agent to run the voice factory workflow
Suggested instruction:

```text
Run the Pixstars lamp voice workflow:
1. scan the episode markdown files
2. refresh dialogue.csv
3. rebuild the render queue
4. create candidate outputs for missing lines
5. evaluate all new candidates
6. publish approved assets
7. regenerate the Ardour cue manifest
```

### 4. Review the shortlist only
Do not review everything manually.
Review:
- rejected lines with low scores
- lines that feel too robotic
- lines that feel too comic
- lines selected as “best” for final use

### 5. Import or refresh assets in Ardour
Use the regenerated manifest and final WAV folder.

## First integration recipe

### A. Populate the episode list file
Edit:

```text
voice/orchestration/state/episode_sources.txt
```

Add one markdown file path per line.

### B. Run the pipeline manually first
```bash
python3 voice/scripts/extract_dialogue_from_episodes.py
python3 voice/scripts/build_manifest.py
python3 voice/scripts/create_render_queue.py
python3 voice/scripts/render_candidates_stub.py
python3 voice/scripts/evaluate_candidates_stub.py
python3 voice/scripts/publish_approved_stub.py
python3 ardour/scripts/generate_cue_manifest.py
```

### C. Move the same sequence into Hivemind
In the Hivemind workspace, create a saved workflow task using the same step order.

## Approval policy

A line should be approved only if it is:
- intelligible
- emotionally readable
- small and warm
- not too adult
- not too metallic
- not too comic

## Stage-use rule

Final approved assets go to:
- `voice/output/final_wav/`

Only those files should be considered for on-stage deterministic playback.


## Real renderer hookup

### 1. Configure the backend
Copy:

```text
voice/config/render_backend.json.example
```

to:

```text
voice/config/render_backend.json
```

Then edit the `command_template`.

### 2. Test one line manually
Run:

```bash
python3 voice/scripts/render_candidates.py
```

This will:
- read the render queue
- call your configured backend command
- write candidate WAV files into `voice/output/candidates/`

### 3. Review the queue
Run:

```bash
python3 voice/scripts/build_review_queue.py
```

Then inspect:
- `voice/review/approved/`
- `voice/review/needs_human_review/`
- `voice/review/rejected/`

### 4. Publish approved assets
Run:

```bash
python3 voice/scripts/publish_approved.py
python3 ardour/scripts/generate_cue_manifest.py
```

## Suggested Hivemind saved workflow

1. extract dialogue from episodes
2. build manifest
3. create render queue
4. render candidates with real backend
5. evaluate candidates
6. build review queue
7. publish approved assets
8. regenerate Ardour cue manifest


## Concrete default backend path

### Install
```bash
bash mac/scripts/install_voice_backend_coqui.sh
```

### Configure
```bash
cp voice/config/coqui_xtts_backend.json.example voice/config/coqui_xtts_backend.json
cp voice/config/render_backend.json.example voice/config/render_backend.json
```

### Add references
Place authorized reference WAVs into:
```text
voice/reference_audio/
```

### Render one line
```bash
source ~/venvs/pixstars-voice/bin/activate
python3 voice/scripts/render_with_coqui_xtts.py --text '"Please... stay."' --emotion '"fragile"' --output '"voice/output/candidates/please_stay.wav"'
```

### Run full automation
```bash
bash voice/scripts/run_voice_factory_real.sh
python3 voice/scripts/review_summary.py
```
