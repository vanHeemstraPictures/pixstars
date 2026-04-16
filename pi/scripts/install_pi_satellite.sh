#!/usr/bin/env bash
set -euo pipefail

VENV_PATH="${HOME}/venvs/hivemind-mic-sat"

sudo apt update
sudo apt install -y python3 python3-pip python3-venv git alsa-utils

python3 -m venv "${VENV_PATH}"
source "${VENV_PATH}/bin/activate"
python -m pip install --upgrade pip setuptools wheel

pip install   hivemind-mic-satellite   ovos-microphone-plugin-alsa   ovos-vad-plugin-silero   rpi_ws281x   adafruit-circuitpython-neopixel   numpy   sounddevice

mkdir -p "${HOME}/.config/mycroft"

echo
echo "Installed Pi satellite environment at ${VENV_PATH}"
echo "Next:"
echo "  1. Copy pi/config/mycroft.conf.example to ~/.config/mycroft/mycroft.conf"
echo "  2. Pair with the server using hivemind-client set-identity"
echo "  3. Test mic and speaker with arecord/aplay"
