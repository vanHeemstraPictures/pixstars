#!/usr/bin/env bash
set -euo pipefail

VENV_PATH="${HOME}/venvs/hivemind-server"
WAKE_WORD_DIR="${HOME}/.local/share/pixstars/wake-words"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found"
  exit 1
fi

# Install system dependencies (Homebrew required)
if command -v brew >/dev/null 2>&1; then
  echo "Installing system dependencies via Homebrew..."
  brew install portaudio 2>/dev/null || echo "portaudio already installed"
else
  echo "WARNING: Homebrew not found. Install portaudio manually:"
  echo "  brew install portaudio"
  echo "Then re-run this script."
  exit 1
fi

python3 -m venv "${VENV_PATH}"
source "${VENV_PATH}/bin/activate"
python -m pip install --upgrade pip setuptools wheel

pip install \
  hivemind-core \
  hivemind-audio-binary-protocol \
  ovos-vad-plugin-silero \
  ovos-ww-plugin-precise-lite \
  ovos-stt-plugin-server \
  ovos-tts-plugin-piper

mkdir -p "${HOME}/.config/hivemind-core"

# Download wake-word model
# Using hey_mycroft for now. Replace with hey_ai.tflite once the
# custom model has been trained with Precise Lite training tools.
mkdir -p "${WAKE_WORD_DIR}"
if [ ! -f "${WAKE_WORD_DIR}/hey_mycroft.tflite" ]; then
  echo "Downloading hey_mycroft wake-word model..."
  curl -L -o "${WAKE_WORD_DIR}/hey_mycroft.tflite" \
    https://github.com/OpenVoiceOS/precise-lite-models/raw/master/wakewords/en/hey_mycroft.tflite
  echo "Wake-word model saved to ${WAKE_WORD_DIR}/hey_mycroft.tflite"
else
  echo "Wake-word model already exists at ${WAKE_WORD_DIR}/hey_mycroft.tflite"
fi

echo
echo "Installed HiveMind server environment at ${VENV_PATH}"
echo "Wake-word model at ${WAKE_WORD_DIR}/hey_mycroft.tflite"
echo
echo "Next:"
echo "  1. Copy mac/config/server.json.example to ~/.config/hivemind-core/server.json"
echo "  2. Adjust settings as needed"
echo "  3. Run: source ${VENV_PATH}/bin/activate && hivemind-core add-client"
