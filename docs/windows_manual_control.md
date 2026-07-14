# Manual control from Windows (Xbox controller + Mission Planner)

Goal: fly the SITL sim (running inside WSL2) from the Windows side, using an
Xbox controller over Bluetooth as your virtual transmitter, with Mission
Planner as the ground control station.

Complete [`sitl_setup.md`](sitl_setup.md) first.

## 1. Bridge SITL (in WSL2) to Windows

WSL2's network namespace is separate from Windows', so SITL's default
`127.0.0.1:14550` output stays inside WSL2 and Windows can't see it. Point
SITL's MAVLink output at the Windows host explicitly:

```bash
# inside WSL2
export WINDOWS_GCS_IP=$(ip route show default | awk '{print $3}')
echo "$WINDOWS_GCS_IP"   # sanity check — should look like 172.x.x.1
./scripts/launch_sitl.sh
```

`launch_sitl.sh` picks up `WINDOWS_GCS_IP` and adds
`--out udp:$WINDOWS_GCS_IP:14550` to `sim_vehicle.py`, streaming MAVLink to
the Windows host. This works over WSL2's default NAT networking on any
Windows 10/11 build — no extra config needed.

(If you're on Windows 11 22H2+ and prefer, enabling WSL2 "mirrored"
networking mode — add `networkingMode=mirrored` under `[wsl2]` in
`%UserProfile%\.wslconfig`, then `wsl --shutdown` — makes `127.0.0.1` shared
between Windows and WSL2 and you can skip `WINDOWS_GCS_IP` entirely. Either
approach works; the gateway-IP method above is the more broadly compatible
default.)

## 2. Install Mission Planner (Windows)

Download and install from the official ArduPilot site:
https://ardupilot.org/planner/docs/mission-planner-installation.html

## 3. Connect Mission Planner to SITL

1. Launch SITL as in step 1 and wait for it to fully boot (console shows
   `Ready to FLY`).
2. In Mission Planner, set the connection dropdown (top right) to **UDP**
   and click **Connect**.
3. When prompted for a port, enter **14550**.
4. The HUD should come alive with attitude, altitude, and a GPS fix within
   a few seconds. If nothing happens, re-check `WINDOWS_GCS_IP` and that
   Windows Firewall isn't blocking Mission Planner on private networks.

## 4. Set up the Xbox controller as a virtual transmitter

1. Pair the Xbox One controller over Bluetooth in Windows Settings (you've
   already done this).
2. In Mission Planner: **Config** (wrench icon) → **Optional Hardware** →
   **Joystick**.
3. Check **Enable Joystick**, select the Xbox controller from the device
   list, and step through calibration (move each stick and trigger fully).
4. Map channels — a natural mapping for Copter:
   - Left stick Y-axis → **Throttle**
   - Left stick X-axis → **Yaw**
   - Right stick Y-axis → **Pitch**
   - Right stick X-axis → **Roll**
5. Map spare buttons to actions using the button dropdowns on the same
   screen — at minimum, map one to **Arm/Disarm** and one to **RTL** (your
   panic button), plus one or two to flight-mode changes (see below).

### Important gotcha: self-centering sticks

The Xbox controller's sticks spring back to center — unlike a real
transmitter's throttle stick, which stays wherever you leave it. If you fly
in **Stabilize**, a centered throttle stick means "cut power" and the
aircraft will drop. Instead, fly in a mode where centered throttle means
"hold current altitude":

- **AltHold** — centered throttle holds altitude; push up/down to climb/descend. Manual roll/pitch/yaw otherwise.
- **Loiter** — same throttle behavior as AltHold, plus GPS-based position hold on roll/pitch release.

Map a button to switch into AltHold or Loiter right after arming, and
practice there rather than in Stabilize.

## 5. First simulated flight

1. Arm (mapped button, or Mission Planner's Actions tab).
2. Switch to AltHold or Loiter.
3. Ease the throttle stick up to climb a few meters, center it to hold,
   practice roll/pitch/yaw, then ease down to descend and land.
4. Try `missions/bait-drop-demo.waypoints` in AUTO mode once comfortable —
   load it via Mission Planner's **Flight Plan** tab, switch to **AUTO**, and
   watch the gripper (`SERVO9`) fire at the drop waypoint (visible in
   Mission Planner's Status tab servo output, or Ctrl+F → "Servo Output").
5. Keep RTL mapped to a button the whole time — it's your safety net if a
   maneuver goes wrong.
