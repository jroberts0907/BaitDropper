# Hardware notes

Full BOM: [`bait_drone_parts_list.md`](../bait_drone_parts_list.md). This file
covers only the wiring/config decisions the param file and mission depend on.

## Frame / motors

650mm quad-X frame, 4× 3508 ~700kV motors, 40A ESCs, 14–15" props →
`FRAME_CLASS=1` (Quad), `FRAME_TYPE=1` (X) in
`params/quad-x-3508-650.param`. Motor/ESC/prop specifics don't have direct
ArduPilot params beyond this — real tuning happens via Autotune on the
physical airframe, not in the param file.

## Payload release (Gripper)

The release servo from the parts list ("Servo, 9–20kg·cm, metal gear") wires
to **AUX OUT 1** on the Pixhawk 2.4.8, which is `SERVO9` in ArduPilot's
numbering. The param file configures it as ArduPilot's built-in **Gripper**
function (`SERVO9_FUNCTION=28`), which exists specifically for
grab/release-on-command payloads:

- `GRIP_TYPE=1` — servo-based gripper (vs. EPM electromagnet)
- `GRIP_GRAB` / `GRIP_REGRAB` / `GRIP_RELEASE` — PWM values for closed/open
  positions. **The values in the param file (1300/1700/1700) are placeholders.**
  Once the real servo and release hook are mounted, bench-test with a servo
  tester or `RC_Passthru`/`Servo Test` in Mission Planner to find the actual
  PWM endpoints for "holding bait" vs. "released," then update the param file.
- `RC7_OPTION=19` — maps transmitter channel 7 (an aux switch on the FS-i6X)
  to manual gripper release, for a mid-flight manual override.

## Two ways to trigger release

1. **Manual** — flip the RC7 switch (per `RC7_OPTION` above) at any point in
   flight, in any mode.
2. **Autonomous** — a `DO_GRIPPER` command in the mission
   (`missions/bait-drop-demo.waypoints`, item 3) fires automatically when the
   drone reaches the drop waypoint while in AUTO mode.

## Battery

`BATT_CAPACITY=10000` matches the 6S 10,000mAh flight LiPo. Update this if
battery capacity changes, since it drives ArduPilot's remaining-capacity
failsafe estimate.
