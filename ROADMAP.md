# OpenERV v1.0 Roadmap

This roadmap outlines the critical tasks and features required to reach a Version 1.0 milestone.

## 1. Hardware Completeness (Mechanical)
- [ ] **Release Mandrel CAD**: Publish the design files for the Heat Exchanger Hat forming mandrel.
- [ ] **Validated Assemblies**: Confirm that all renamed STEP files correctly resolve in standard CAD software (KiCad/FreeCAD).
- [ ] **Assembly Video/Guide**: Create a visual assembly guide to supplement the Markdown documentation.

## 2. Firmware Functionality & Safety
- [ ] **Automated Defrost Cycle**: Implement logic to detect frost accumulation (via pressure drop) and trigger a temporary exhaust-only purge.
- [ ] **PID Auto-Tuning**: Provide model-specific PID constants for TW4 and WM12 based on physical volume characterization.
- [ ] **Watchdog Hardening**: Refine WDT timeouts for critical networking handshakes to prevent false-positive reboots.

## 3. User Experience (UX)
- [ ] **IoT Provisioning (V1.0)**: Mature the Captive Portal to include a WiFi scanner (showing available SSIDs).
- [ ] **Persistent Variables Validation**: Add schema validation for `persistent_vars.json` to prevent boot loops from malformed JSON.
- [ ] **Home Assistant Discovery**: Implement MQTT discovery for smart home integration.

## 4. Electronics & Manufacturing
- [ ] **KiCad Migration**: Transition the main PCB from EasyEDA to KiCad for full open-source toolchain support.
- [ ] **Production Gerbers**: Include a verified set of Gerber files in each release.
- [ ] BOM Finalization: Finalize LCSC part mappings for all components to support automated PCBA services.

## 5. Universal Window Mount
- [ ] **Validated Pioneer Assembly**: Confirm physical fitment and weight distribution for Pioneer ECOasis 50 units.
- [ ] **Validated Vents-US Assembly**: Confirm dual-sill support integrity for the 19lb TwinFresh Comfo unit.
- [ ] **Parametric Engine Finalization**: Complete all OpenSCAD modules for auto-generating sliders and collars for any pipe diameter between 100mm and 200mm.

## 6. Community & Standards
- [ ] **OKH Certification**: Submit the project for official Open Source Hardware Association (OSHWA) certification.
- [ ] **Contributor Guide**: Expand `CONTRIBUTING.md` with technical environment setup instructions.
