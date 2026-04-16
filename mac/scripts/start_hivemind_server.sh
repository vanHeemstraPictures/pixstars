#!/usr/bin/env bash
set -euo pipefail
VENV_PATH="${HOME}/venvs/hivemind-server"
source "${VENV_PATH}/bin/activate"
exec hivemind-core listen
