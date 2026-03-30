# OpenERV TW4 and WM12 - Fork

This repository contains firmware, design files, and documentation for the **OpenERV TW4** and **WM12** Energy Recovery Ventilators.

## Licensing

The original OpenERV project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

As a fork of the original work, all modifications and contributions in this repository are also licensed under **CC BY-NC-SA 4.0**, as required by the **ShareAlike** clause of the license.

### Key Terms:
- **Attribution**: You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **Non-Commercial**: You may not use the material for commercial purposes.
- **ShareAlike**: If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

For the full legal text, please refer to the `LICENSE` file.

## Project Structure

The repository is organized as follows:

- **`firmware/`**: Active source code for the devices.
  - `tw4/`: Stable firmware for the TW4 model.
  - `wm12/`: Stable firmware for the WM12 model.
  - `experimental/`: Test scripts, data loggers, and PCB test programs.
- **`design/`**: CAD and hardware design files.
  - `tw4/`, `wm12/`: STL and STEP files for 3D printing and modeling.
  - `schematics/`: Wiring diagrams and pinout references.
- **`docs/`**: Project documentation, manuals, and DIY guides in Markdown format.
- **`archives/`**: Legacy backups, original binary blobs (.uf2), and historical development data.

## Original Project & Attribution

This project is based on the OpenERV system by Anthony Douglas and the OpenERV community.

- **Original Author**: Anthony Douglas
- **Project Website**: [OpenERV](https://openerv.org)

## Documentation

Detailed manuals and assembly instructions:
- [DIY Manufacturing Guide](./docs/Document%20to%20aid%20DIY%20manufacturing%20of%20the%20OpenERV%20TW4%20and%20WM12.md)
- [TW4 Manual](./docs/TW4%20manual%20-%20OpenERV.md)
- [WM12 Manual](./docs/OpenERV%20WM12%20manual.md)

## Development

The OpenERV firmware is written in **MicroPython** and designed to run on the **Raspberry Pi Pico W**.

### Environment Setup
1. Install MicroPython on your Raspberry Pi Pico W.
2. Use an editor like Thonny or the VS Code MicroPython extension.
3. Upload the contents of the relevant `firmware/` directory (e.g., `firmware/tw4/`) to the root of the Pico's filesystem.

### Configuration
Device settings are stored in `persistent_vars.json`. This file includes:
- WiFi credentials (`ssid_main_wifi`, `password_main_wifi`)
- Adafruit IO configuration for MQTT telemetry.
- Device role (`leader` or `follower`).

**Note:** `persistent_vars.json` is ignored by git to prevent credential leaks. Use the template provided in the firmware folders to create your own.

### Key Components
- **`main.py`**: The entry point for the device logic.
- **`sdp810_125.py`**: Driver for the Sensirion differential pressure sensor.
- **`combifan.py`**: Logic for controlling the fan speeds.
- **`simple_pid/`**: PID control loop for maintaining optimal pressure/flow.
- **`umqtt/`**: MQTT client for remote monitoring and control.

### Contributing
When adding new features or fixing bugs:
1. Test your changes using the scripts in `firmware/experimental/`.
2. Ensure you maintain the CC BY-NC-SA 4.0 license headers in new files.
3. Follow the existing modular structure for drivers and utilities.
