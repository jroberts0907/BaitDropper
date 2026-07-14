# BaitDropper

Software-in-the-loop (SITL) practice environment for a 650mm quadcopter bait-drop
drone, built around Pixhawk 2.4.8 + ArduPilot. This repo exists so the flight
logic, mission plan, and payload-release configuration can all be rehearsed in
simulation *before* the real airframe (see [`bait_drone_parts_list.md`](bait_drone_parts_list.md))
is assembled and flown.

Scope: this is intentionally RC + Pixhawk only — no onboard companion computer.
Payload release is handled by ArduPilot's built-in **Gripper** feature (a servo
output function meant for exactly this: grab/release on command), triggered
either by an RC switch (manual) or a `DO_GRIPPER` mission command (autonomous).

## Repo layout

| Path | Purpose |
|---|---|
| `bait_drone_parts_list.md` | Hardware BOM for the real build |
| `params/quad-x-3508-650.param` | ArduPilot params for this frame/motor/gripper combo |
| `missions/bait-drop-demo.waypoints` | Example autonomous mission: takeoff → fly to drop zone → release → RTL → land |
| `scripts/launch_sitl.sh` | Launches ArduCopter SITL with this build's params pre-loaded |
| `scripts/smoke_test.py` | pymavlink script: arms, flies the demo mission, verifies gripper fires |
| `docs/sitl_setup.md` | One-time environment setup (WSL2 + ArduPilot build) |
| `docs/windows_manual_control.md` | Fly the sim from Windows with an Xbox controller + Mission Planner |
| `docs/hardware.md` | Wiring notes tying the parts list to the param file |

## Quick start

1. Follow [`docs/sitl_setup.md`](docs/sitl_setup.md) once, to install ArduPilot's SITL toolchain.
2. `./scripts/launch_sitl.sh` — starts SITL with `params/quad-x-3508-650.param` loaded.
3. In another terminal: `python scripts/smoke_test.py` — arms, runs the demo mission, confirms the gripper releases at the drop waypoint.
4. To fly it yourself: follow [`docs/windows_manual_control.md`](docs/windows_manual_control.md) — connects Mission Planner (Windows) to SITL (WSL2) and sets up an Xbox controller as a virtual transmitter.

## Roadmap (once the physical airframe is built)

- Recalibrate ESCs and RC on real hardware; re-run compass/accel calibration.
- Bench-test the gripper servo's actual `GRIP_GRAB` / `GRIP_REGRAB` PWM values (placeholders in the param file — real servo will need its own endpoints).
- Run Autotune on the real motors/props/frame; the SITL param file's tuning gains are defaults, not a substitute.
- Ground-test the release mechanism under the real payload weight before the first autonomous flight.
