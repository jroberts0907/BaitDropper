# Bait-Drop Drone — Complete Parts List

**Target build:** ~3.5lb payload quadcopter, starting from zero RC gear, complete first multirotor build.
**Strategy reminder:** do ArduPilot SITL simulation (free) and a cheap practice drone/solder practice *before* this build — see earlier discussion. This list covers the real airframe.

---

## 1. Radio & Charging (buy once, reused on every future build)

| Item | Spec | Approx Price |
|---|---|---|
| Transmitter + Receiver | FlySky FS-i6X bundle, 6-10 channel | $55–60 |
| Battery Charger | Balance charger, 6S-capable (e.g. iMax B6 clone or similar) | $30–40 |

**Subtotal: ~$85–100**

---

## 2. Airframe

| Item | Spec | Approx Price |
|---|---|---|
| Frame | 650mm quad kit w/ landing gear *(trim option: 550mm frame, ~$80-100, still fits this motor class on 12-14" props)* | $90–140 |
| Motors (×4) | 3508–3510 size, ~700kV (e.g. MAD 3508 IPE, ~$31 each) | $120–125 |
| ESCs (×4) | 40A, matched to motor current draw | $50–60 |
| Props (2 pairs) | 14–15", matched to motor/frame | $20–25 |

**Subtotal: ~$280–350**

---

## 3. Flight Electronics

| Item | Spec | Approx Price |
|---|---|---|
| Flight Controller + GPS | Pixhawk 2.4.8 clone combo kit *(trim option: bare FC + separate basic GPS module instead of the full bundled kit)* | $60–90 |
| Flight Battery | 6S 10,000mAh LiPo | $65–75 |
| Power Distribution Board | Rated above your total ESC current draw | $10–15 |

**Subtotal: ~$135–180**

*(Consider a 2nd battery later once the build is proven — not required for first flights.)*

---

## 4. Payload Release System

| Item | Spec | Approx Price |
|---|---|---|
| Servo | 9–20kg·cm torque, metal gear | $12–18 |
| Release hook / hardware | 3D-printed drop hook or hobby-store release clip, mounted close to the drone's belly (short hang point — see earlier note on pendulum swing) | $8–12 |

**Subtotal: ~$20–30**

---

## 5. Camera System (optional — see chat notes on analog vs. digital, monitor vs. goggles)

| Item | Spec | Approx Price |
|---|---|---|
| AIO Camera + VTX | Analog, 5.8GHz (e.g. RunCam Spotter V2 or similar AIO unit) | $25–40 |
| Ground Monitor | 4.3" screen w/ built-in 40ch 5.8GHz receiver | $40–55 |

**Subtotal: ~$65–95**

*Wiring note: most AIO cams accept a wide 5–20V input directly off the main flight battery — no separate BEC usually needed, but confirm against your specific camera's spec sheet.*

---

## 6. Misc / Consumables

Wiring (16-18AWG silicone), XT60/XT90 connectors, heat-shrink, zip ties, threadlocker (blue), prop balancer, 1–2 sets of spare props, foam/case for transport.

**Subtotal: ~$30–40**

---

## Running Totals

| Scope | Total |
|---|---|
| Core flying build (no camera) | **~$610–700** |
| Core build, trimmed options taken | **~$530–580** |
| With camera system added | **~$675–800** |

$500 was always going to be tight for this spec — this is the honest, currently-priced version of that. To land closest to $500: 550mm frame, bare FC + separate GPS, one battery to start, skip the camera for the first build and add it once the airframe is proven.

## Not included here (need separately)
- Fishing-side hardware (leader, hooks, bait rig) — already covered in earlier discussion
- Tools: soldering iron, hex driver set, multimeter, LiPo safety bag
