#!/usr/bin/env bash
# Launches ArduCopter SITL as this build (quad X, 650mm frame) with the
# gripper/release param file pre-loaded. Run from WSL2 after completing
# docs/sitl_setup.md.
set -euo pipefail

ARDUPILOT_DIR="${ARDUPILOT_DIR:-$HOME/ardupilot}"
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ ! -d "$ARDUPILOT_DIR" ]; then
  echo "ArduPilot checkout not found at $ARDUPILOT_DIR" >&2
  echo "Set ARDUPILOT_DIR or follow docs/sitl_setup.md first." >&2
  exit 1
fi

cd "$ARDUPILOT_DIR"
Tools/autotest/sim_vehicle.py \
  -v ArduCopter \
  -f quad \
  --add-param-file="$REPO_DIR/params/quad-x-3508-650.param" \
  --console --map
