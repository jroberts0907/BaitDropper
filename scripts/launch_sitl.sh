#!/usr/bin/env bash
# Launches ArduCopter SITL as this build (quad X, 650mm frame) with the
# gripper/release param file pre-loaded. Run from WSL2 after completing
# docs/sitl_setup.md.
#
# To let a GCS on the Windows side (e.g. Mission Planner) connect, set
# WINDOWS_GCS_IP to the Windows host's IP as seen from WSL2 (the default
# gateway in NAT mode: `ip route show default | awk '{print $3}'`). See
# docs/windows_manual_control.md.
set -euo pipefail

ARDUPILOT_DIR="${ARDUPILOT_DIR:-$HOME/ardupilot}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -d "$ARDUPILOT_DIR" ]; then
  echo "ArduPilot checkout not found at $ARDUPILOT_DIR" >&2
  echo "Set ARDUPILOT_DIR or follow docs/sitl_setup.md first." >&2
  exit 1
fi

EXTRA_OUT=()
if [ -n "${WINDOWS_GCS_IP:-}" ]; then
  EXTRA_OUT=(--out "udp:${WINDOWS_GCS_IP}:14550")
  echo "Streaming MAVLink to Windows GCS at ${WINDOWS_GCS_IP}:14550"
fi

cd "$ARDUPILOT_DIR"
Tools/autotest/sim_vehicle.py \
  -v ArduCopter \
  -f quad \
  --add-param-file="$REPO_DIR/params/quad-x-3508-650.param" \
  "${EXTRA_OUT[@]}" \
  --console --map
