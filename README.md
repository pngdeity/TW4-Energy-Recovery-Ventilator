<p align="center">
  <img src="docs/images/logo.png" alt="OpenERV Logo" width="400">
</p>

# OpenERV TW4 and WM12

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![OKH Compliance](https://img.shields.io/badge/OKH-v1.0%20Compliant-green.svg)](okh.yml)
[![Build Flashable Firmware](https://github.com/pngdeity/TW4-Energy-Recovery-Ventilator/actions/workflows/build-firmware.yml/badge.svg)](https://github.com/pngdeity/TW4-Energy-Recovery-Ventilator/actions/workflows/build-firmware.yml)
[![STL Manufacturing Analysis](https://github.com/pngdeity/TW4-Energy-Recovery-Ventilator/actions/workflows/stl-analysis.yml/badge.svg)](https://github.com/pngdeity/TW4-Energy-Recovery-Ventilator/actions/workflows/stl-analysis.yml)

OpenERV is a high-efficiency, low-cost DIY **Energy Recovery Ventilator (ERV)** system designed to provide fresh outdoor air while recovering heat and moisture from the exhaust stream. This repository contains the complete firmware, mechanical designs, and documentation for the **TW4** (Through-Wall) and **WM12** (Window-Mounted) models.

## Key Features
- **High Efficiency**: 87%+ heat recovery efficiency at 60 CFM.
- **Precision Control**: Integrated PID loops for automated pressure regulation using Sensirion SDP810 sensors.
- **IoT Enabled**: Built-in WiFi and MQTT support for remote monitoring and automation.
- **DIY Friendly**: Optimized for 3D printing and off-the-shelf components.
- **Smart Synchronization**: Leader/Follower UDP synchronization for multi-module installations.

## Project Structure

- **`firmware/`**: Hardened MicroPython source code for the Raspberry Pi Pico W.
  - `common/`: Modular core engine, drivers, and safety state machine.
  - `tw4/`, `wm12/`: Model-specific entry points.
- **`design/`**: Mechanical and electrical design assets.
  - `parts/`: STL and STEP files for all printable components.
  - `schematics/`: PCB designs and wiring diagrams.
- **`docs/`**: Comprehensive manuals, assembly guides, and technical specifications.
- **`research/`**: Historical CAD iterations and experimental validation data.
- **`scripts/`**: Automation utilities for manufacturing analysis and BOM extraction.

## Installation (Flashable Firmware)

The fastest way to deploy OpenERV is to use our pre-compiled firmware images:

1. Download the latest **`.uf2`** binary for your model from the [GitHub Releases](https://github.com/pngdeity/TW4-Energy-Recovery-Ventilator/releases) page.
2. Hold the **BOOTSEL** button on your Raspberry Pi Pico W and connect it to your computer via USB.
3. Drag and drop the `.uf2` file into the `RPI-RP2` drive. The unit will automatically reboot into the OpenERV engine.

## Configuration

After flashing, you must configure your local environment:
1. Locate the relevant template in `firmware/config_templates/`.
2. Copy it to the root of your Pico's filesystem as `persistent_vars.json`.
3. Edit the file to include your WiFi credentials, model ID, and optional Adafruit IO keys.

## Original Project & Attribution

This project is a formalized fork of the OpenERV system originally developed by **Anthony Douglas**.
- **Original Website**: [openerv.ca](https://www.openerv.ca)
- **Licensing**: This project is licensed under **CC BY-NC-SA 4.0**. See [LICENSE](LICENSE) for details.

---
<p align="center">
  <i>Making high-performance residential ventilation accessible to everyone.</i>
</p>
