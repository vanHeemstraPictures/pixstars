#!/usr/bin/env bash
set -euo pipefail

python3 voice/scripts/extract_dialogue_from_episodes.py
python3 voice/scripts/build_manifest.py
python3 voice/scripts/create_render_queue.py
python3 voice/scripts/render_candidates.py
python3 voice/scripts/evaluate_candidates.py
python3 voice/scripts/build_review_queue.py
python3 voice/scripts/publish_approved.py
python3 ardour/scripts/generate_cue_manifest.py

echo "Real voice factory workflow completed."
