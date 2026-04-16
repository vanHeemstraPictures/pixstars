#!/usr/bin/env bash
set -euo pipefail

STATE_EMITTER="python3 ardour/scripts/emit_state.py"
AUDIO_FILE="${1:-}"
if [[ -z "${AUDIO_FILE}" ]]; then
  echo "Usage: cue_wrapper_example.sh <audio-file>"
  exit 1
fi

${STATE_EMITTER} thinking
sleep 0.3
${STATE_EMITTER} speaking

# Replace with your actual playback command or Ardour hook
echo "Would now play: ${AUDIO_FILE}"

sleep 1
${STATE_EMITTER} idle
