#!/usr/bin/env bash
set -euo pipefail

VENV_PATH="${HOME}/venvs/pixstars-voice"

python3 -m venv "${VENV_PATH}"
source "${VENV_PATH}/bin/activate"
python -m pip install --upgrade pip setuptools wheel

pip install coqui-tts

mkdir -p voice/models/coqui_cached_voices
mkdir -p voice/reference_audio

echo
echo "Installed Coqui XTTS environment at ${VENV_PATH}"
echo "Next:"
echo "  1. Copy voice/config/coqui_xtts_backend.json.example to voice/config/coqui_xtts_backend.json"
echo "  2. Put authorized reference WAV files into voice/reference_audio/"
echo "  3. Run: source ${VENV_PATH}/bin/activate && python3 voice/scripts/render_with_coqui_xtts.py --text '"Hello..."' --emotion '"curious"' --output '"voice/output/candidates/test.wav"'"
