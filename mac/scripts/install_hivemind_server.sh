#!/usr/bin/env bash
set -euo pipefail

VENV_PATH="${HOME}/venvs/hivemind-server"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found"
  exit 1
fi

python3 -m venv "${VENV_PATH}"
source "${VENV_PATH}/bin/activate"
python -m pip install --upgrade pip setuptools wheel

pip install   hivemind-core   hivemind-audio-binary-protocol   ovos-vad-plugin-silero   ovos-ww-plugin-precise-lite

mkdir -p "${HOME}/.config/hivemind-core"

echo
echo "Installed HiveMind server environment at ${VENV_PATH}"
echo "Next:"
echo "  1. Copy mac/config/server.json.example to ~/.config/hivemind-core/server.json"
echo "  2. Adjust the wake-word model path and STT/TTS plugins"
echo "  3. Run: source ${VENV_PATH}/bin/activate && hivemind-core add-client"
