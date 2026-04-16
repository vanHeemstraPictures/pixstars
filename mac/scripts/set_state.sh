#!/usr/bin/env bash
set -euo pipefail

STATE_FILE="${STATE_FILE:-/tmp/pixstars_lamp_state.txt}"
STATE="${1:-idle}"

case "${STATE}" in
  idle|listening|thinking|speaking|error)
    printf "%s" "${STATE}" > "${STATE_FILE}"
    echo "State set to ${STATE}"
    ;;
  *)
    echo "Invalid state: ${STATE}"
    exit 1
    ;;
esac
