# Hivemind Voice Automation

## Goal

Automate the creation of the Pixstars lamp voice using **Hivemind on the Mac Mini** while keeping the live lamp path separate and stable.

## Important distinction

This project uses two similarly named things for different jobs:

### 1. HiveMind (JarbasHiveMind / OVOS ecosystem)
Used for:
- lamp endpoint communication
- satellite pairing
- voice transport between the Pi and the Mac Mini

### 2. Hivemind (hivementality-ai platform)
Used for:
- multi-agent workflow automation
- workspace/task orchestration
- shell-driven voice-pipeline automation on the Mac Mini

Do not confuse them.

## Why this split is right for Pixstars

Hivemind is a self-hosted multi-agent platform with persistent workspaces, team chat, built-in tools such as shell and file-system access, support for multiple model providers, and heartbeat scheduling for autopilot workflows. That makes it well-suited to manage repetitive pipeline work around your voice assets. It is not the thing that should sit directly in the lamp’s real-time audio loop. citeturn275334view0turn275334view1turn275334view2

HiveMind Core remains the better fit for the Pi↔Mac Mini satellite path because its CLI and pairing model are built around clients/satellites and a listening server, with commands like `add-client`, `listen`, and `list-clients`. citeturn275334view4

## Recommended architecture

### Real-time stage path
- Pi in lamp: mic, speaker, LED state engine, lightweight client
- Mac Mini: HiveMind server, STT, synthetic voice rendering, Ardour cue integration

### Backstage automation path
- Mac Mini: Hivemind workspace with agents that prepare datasets, queue renders, score candidates, and publish approved assets

## What Hivemind automates

### Stage A — Dialogue extraction
Input:
- episode markdown files

Output:
- `voice/data/dialogue.csv`

### Stage B — Render queue generation
Input:
- `voice/data/dialogue.csv`

Output:
- `voice/orchestration/state/render_queue.json`

### Stage C — Candidate generation
Input:
- render queue

Output:
- `voice/output/candidates/`

### Stage D — Evaluation
Input:
- candidate manifest

Output:
- `voice/orchestration/state/evaluation.csv`

### Stage E — Publication
Input:
- approved rows

Output:
- `voice/output/final_wav/`
- `ardour/cues/cue_manifest.csv`

## Suggested Hivemind team

### Director
Decides what step runs next.

### Dialogue Curator
Extracts lamp lines from episode markdown.

### Voice Designer
Maintains the voice brief: small, warm, fragile, slightly raspy.

### Render Operator
Runs the local shell/python render pipeline.

### Evaluator
Scores outputs and rejects the wrong character qualities.

### Publisher
Promotes approved assets and updates Ardour manifests.

This structure maps naturally onto Hivemind’s persistent workspaces and collaborating agent model. citeturn275334view1turn275334view2

## Step-by-step setup

### Step 1 — Install Hivemind on the Mac Mini

Use the upstream quickstart:

```bash
curl -fsSL https://raw.githubusercontent.com/hivementality-ai/hivemind/main/install.sh | bash
```

Then open:

```text
http://localhost:8080
```

The README says the setup wizard guides you through the initial configuration and first team setup. citeturn275334view0turn275334view1

### Step 2 — Create a dedicated workspace

Create a workspace named for example:

```text
Pixstars Lamp Voice Factory
```

Mount or point the workspace at your local Pixstars repository on the Mac Mini.

### Step 3 — Give the workspace shell/file access

Your Hivemind workspace needs enough permissions to run the local pipeline scripts in:
- `voice/scripts/`
- `ardour/scripts/`

Do not give it direct control over the live performance path.

### Step 4 — Create the agent team

Create these agents inside the Hivemind workspace:
- Director
- Dialogue Curator
- Voice Designer
- Render Operator
- Evaluator
- Publisher

Use the agent briefs from:
- `voice/orchestration/agents/`

### Step 5 — Initialize the local pipeline files

Run:

```bash
python3 voice/scripts/extract_dialogue_from_episodes.py
python3 voice/scripts/build_manifest.py
python3 voice/scripts/create_render_queue.py
```

### Step 6 — Run a candidate batch

Run:

```bash
python3 voice/scripts/render_candidates_stub.py
python3 voice/scripts/evaluate_candidates_stub.py
python3 voice/scripts/publish_approved_stub.py
python3 ardour/scripts/generate_cue_manifest.py
```

### Step 7 — Turn that into Hivemind tasks

In Hivemind, create a repeating workflow:
1. scan for new episode markdown
2. update dialogue CSV
3. create render queue
4. run render step
5. evaluate candidates
6. publish approved lines
7. regenerate Ardour cue manifest

Use heartbeat scheduling only after the workflow is stable. The Hivemind README explicitly mentions autopilot via heartbeat scheduling. citeturn275334view2

## Safety rule

Keep Hivemind out of the millisecond-sensitive live lamp path.

Use it for:
- planning
- extraction
- rendering
- evaluation
- publishing
- housekeeping

Do not use it as the runtime controller for:
- live wake-word detection
- real-time playback timing
- critical on-stage LED transitions

## Recommended first success criteria

You are done with phase 1 when:
- a new episode markdown file can be turned into dialogue rows
- those rows create a render queue
- the queue creates candidate placeholders
- candidates can be scored
- approved files land in `voice/output/final_wav/`
- the Ardour cue manifest updates automatically


## Real backend interface

This repository now includes a **real backend interface** for rendering candidate WAV files on the Mac Mini.

### Configuration
Copy:

```text
voice/config/render_backend.json.example
```

to:

```text
voice/config/render_backend.json
```

Then set `command_template` to your real local renderer.

The renderer contract is simple:
- input text
- input emotion
- output WAV path

### Why this matters

The orchestration layer no longer depends on a fake placeholder renderer. It now has a stable handoff point where Hivemind can call your actual local voice generation process.

## Review queue

This repository now includes a structured review queue under:

```text
voice/review/
```

Use it to keep the best balance between automation and artistic control:
- high-scoring lines can be auto-approved
- medium-scoring lines go to human review
- poor fits are rejected

## Episode pipeline alignment

The extraction stage is episode-driven through:

```text
voice/orchestration/state/episode_sources.txt
```

That means your Hivemind workflow can scan new episode files, rebuild the dataset, rerender only missing lines, and refresh the Ardour cue manifest automatically.


## Concrete default renderer in this repository

This repository now ships with a concrete Mac-side renderer wrapper:

```text
voice/scripts/render_with_coqui_xtts.py
```

The default backend config points the render pipeline at that script.

### How it works
- reads `voice/config/coqui_xtts_backend.json`
- uses Coqui XTTS on the Mac Mini
- clones/caches a speaker identity from `voice/reference_audio/`
- renders candidate WAV files into `voice/output/candidates/`

### Why XTTS
XTTS in the current Coqui docs supports voice cloning and cached cloned voices, which is a strong fit for a reusable lamp-character voice workflow.
