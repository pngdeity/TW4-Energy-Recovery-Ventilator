# Project Plan: Phase 4 - Full Ecosystem & Reliability

This document outlines the multifaceted engineering efforts for Phase 4 of the OpenERV project. This phase focuses on maturing the unit from "Industrial Parity" to "Smart Home Native" while hardening the mechanical and software reliability for long-term (5-year+) deployment.

---

## 1. Workstreams

### WS1: Smart Home Integration (MQTT Discovery)
**Objective:** Enable zero-config integration with Home Assistant using MQTT Discovery.
- [ ] Implement `discovery.py` to broadcast HA-compliant JSON payloads.
- [ ] Add "Climate" entity support for mode switching (Heat Recovery vs. Free Cooling).
- [ ] Map SCD41 sensors to standard HA entities (CO2, Humidity, Temperature).

### WS2: Over-the-Air (OTA) Infrastructure
**Objective:** Allow users to update firmware without USB access.
- [ ] Implement a dual-bank bootloader logic in MicroPython.
- [ ] Create a `firmware/common/ota_manager.py` that verifies checksums before flashing.
- [ ] Integrate OTA triggering via the local web dashboard.

### WS3: Acoustic & Airflow Optimization (Mechanical)
**Objective:** Reduce unit noise by 5dB at high speeds.
- [ ] **Acoustic Baffles:** Design 3D-printable internal baffles for the `noise_splitter.stl` using the OpenSCAD parametric engine.
- [ ] **Vibration Isolation:** Create a TPU-based motor mount to isolate the high-RPM fans from the ASA housing.
- [ ] **Flow Straightener V2:** Optimize the 22-degree straightener for lower static pressure drop.

### WS4: Validation & Simulation (DevOps)
**Objective:** Improve "Hardware-in-the-Loop" (HIL) simulation.
- [ ] **Sensor Mocking:** Enhance `tests/mocks/machine.py` to simulate realistic sensor drift and I2C failures.
- [ ] **Nightly Builds:** Use the generalized GitHub Actions to run full UF2 builds every 24 hours against the `main` branch.

---

## 2. Essential Commands

### Firmware Operations
**Run Logic Tests:**
```bash
# Verify core logic and PID loops
pytest tests/
```

**Trigger a Remote UF2 Build (via GitHub CLI):**
```bash
# Triggers the optimized multi-stage build for the current branch
gh workflow run "Build Flashable Firmware (UF2)" --ref $(git branch --show-current)
```

**Watch Build Progress:**
```bash
# Monitor the latest run
gh run watch
```

### Mechanical / CAD Operations
**Update Window Mount Submodule:**
```bash
# Pull latest parametric updates
git submodule update --remote --merge design/universal_window_mount
```

**Commit Submodule Changes:**
```bash
# Must be done from within the submodule directory
cd design/universal_window_mount
git add .
git commit -m "Update parametric specs"
git push origin main
cd ../..
git add design/universal_window_mount
git commit -m "Ref: Bump window mount submodule"
```

### Infrastructure Operations
**Validate JSON Configs:**
```bash
# Ensure no syntax errors in templates
python3 -c "import json; [json.load(open(f)) for f in ['firmware/config_templates/tw4_persistent_vars.json', 'firmware/config_templates/wm12_persistent_vars.json']]"
```

---

## 3. Engineering Mandates for Phase 4
1. **No Hardcoding:** All branch-specific logic must be removed from YAML files (Use the "Generalize Branch Triggers" pattern).
2. **Node 24 Compliance:** Ensure all CI dependencies remain on the Node 24 runtime to prevent deprecation failures.
3. **Safety First:** Any logic change affecting fan speed or direction MUST be verified by `test_fan_manager.py` before merging.
4. **Surgical Submodules:** Always commit mechanical changes to the standalone `Universal-ERV-Window-Mount` repo first, then bump the reference in this repo.
