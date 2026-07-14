#!/usr/bin/env python3
"""Automated smoke test against a running SITL instance (see launch_sitl.sh).

Arms, takes off, flies the demo mission, and confirms the gripper servo
(SERVO9 / AUX1) toggles when the DO_GRIPPER waypoint fires. Run after
launch_sitl.sh is up and printing "Waiting for heartbeat".
"""
import sys
import time

from pymavlink import mavutil

CONNECTION = "udp:127.0.0.1:14550"
MISSION_FILE = "missions/bait-drop-demo.waypoints"
GRIPPER_SERVO_CHANNEL = 9
ARM_TIMEOUT_S = 30
MISSION_TIMEOUT_S = 300


def load_mission(master, path):
    with open(path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    assert lines[0].startswith("QGC WPL"), "unrecognized mission file header"

    items = []
    for line in lines[1:]:
        fields = line.split("\t")
        seq, current, frame, cmd, p1, p2, p3, p4, x, y, z, autocontinue = fields
        items.append(
            master.mav.mission_item_int_encode(
                master.target_system,
                master.target_component,
                int(seq),
                int(frame),
                int(cmd),
                int(current),
                int(autocontinue),
                float(p1), float(p2), float(p3), float(p4),
                int(float(x) * 1e7), int(float(y) * 1e7), float(z),
                mavutil.mavlink.MAV_MISSION_TYPE_MISSION,
            )
        )

    master.mav.mission_count_send(master.target_system, master.target_component, len(items))
    for _ in items:
        req = master.recv_match(type=["MISSION_REQUEST", "MISSION_REQUEST_INT"], blocking=True, timeout=10)
        if req is None:
            raise RuntimeError("mission upload stalled waiting for MISSION_REQUEST")
        master.mav.send(items[req.seq])

    ack = master.recv_match(type="MISSION_ACK", blocking=True, timeout=10)
    if ack is None or ack.type != mavutil.mavlink.MAV_MISSION_ACCEPTED:
        raise RuntimeError(f"mission upload rejected: {ack}")
    print(f"Uploaded {len(items)} mission items.")


def wait_for_gripper_toggle(master, timeout_s):
    start = time.time()
    baseline = None
    while time.time() - start < timeout_s:
        msg = master.recv_match(type="SERVO_OUTPUT_RAW", blocking=True, timeout=5)
        if msg is None:
            continue
        pwm = getattr(msg, f"servo{GRIPPER_SERVO_CHANNEL}_raw")
        if baseline is None:
            baseline = pwm
            continue
        if abs(pwm - baseline) > 50:
            print(f"Gripper servo moved: {baseline} -> {pwm}")
            return True
    return False


def main():
    master = mavutil.mavlink_connection(CONNECTION)
    print("Waiting for heartbeat...")
    master.wait_heartbeat()
    print("Heartbeat received. Loading mission...")
    load_mission(master, MISSION_FILE)

    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_DO_SET_MODE, 0,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, 3, 0, 0, 0, 0, 0,  # AUTO
    )

    print("Arming...")
    master.mav.command_long_send(
        master.target_system, master.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0,
        1, 0, 0, 0, 0, 0, 0,
    )

    armed = False
    start = time.time()
    while time.time() - start < ARM_TIMEOUT_S:
        hb = master.recv_match(type="HEARTBEAT", blocking=True, timeout=5)
        if hb and (hb.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED):
            armed = True
            break
    if not armed:
        print("FAIL: did not arm in time", file=sys.stderr)
        sys.exit(1)

    print("Waiting for gripper release during mission...")
    if wait_for_gripper_toggle(master, MISSION_TIMEOUT_S):
        print("PASS: gripper triggered during autonomous mission.")
    else:
        print("FAIL: gripper never toggled within timeout.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
