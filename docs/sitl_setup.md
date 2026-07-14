# SITL environment setup (one-time)

ArduPilot's SITL toolchain targets Linux. On Windows, run it under WSL2.

## 1. WSL2 + Ubuntu

```powershell
wsl --install -d Ubuntu-22.04
```

Restart if prompted, then open the Ubuntu shell for the rest of this guide.

## 2. Clone and build ArduPilot

```bash
cd ~
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
cd ardupilot
Tools/environment_install/install-prereqs-ubuntu.sh -y
. ~/.profile
./waf configure --board sitl
./waf copter
```

## 3. Python deps for the mission/test scripts

```bash
python3 -m venv ~/baitdropper-venv
source ~/baitdropper-venv/bin/activate
pip install pymavlink mavproxy
```

Activate this venv (`source ~/baitdropper-venv/bin/activate`) in any shell you
use to run `scripts/smoke_test.py`.

## 4. Get this repo into WSL

If you cloned `BaitDropper` on the Windows side, it's reachable from WSL at
`/mnt/c/Users/jacks/BaitDropper`. Either work from there directly, or `git
clone` a second copy into the Linux filesystem (faster I/O, recommended for
anything beyond occasional use):

```bash
cd ~
git clone https://github.com/jroberts0907/BaitDropper.git
```

## 5. Run it

```bash
cd ~/BaitDropper   # or /mnt/c/Users/jacks/BaitDropper
chmod +x scripts/launch_sitl.sh
./scripts/launch_sitl.sh
```

In a second WSL shell (with the venv activated):

```bash
python scripts/smoke_test.py
```

## Notes

- `missions/bait-drop-demo.waypoints` uses placeholder coordinates
  (40.0000000, -105.0000000). SITL's default start location is elsewhere, so
  either edit the mission's coordinates to sit near your SITL home position,
  or pass `--location` / a custom `.json` start location to `sim_vehicle.py`
  matching the mission file. Either way, keep them consistent.
- `sim_vehicle.py --console --map` opens MAVProxy's console and a moving map;
  close both with Ctrl-C in the terminal running `launch_sitl.sh`.
