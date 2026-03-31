# OpenERV TW4 and WM12 - Fork

This repository contains firmware, design files, and documentation for the **OpenERV TW4** and **WM12** Energy Recovery Ventilators.

## Licensing

The original OpenERV project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/) license.

As a fork of the original work, all modifications and contributions in this repository are also licensed under **CC BY-NC-SA 4.0**, as required by the **ShareAlike** clause of the license.

For the full legal text, please refer to the `LICENSE` file.

## Project Structure

The repository is organized as follows:

- **`firmware/`**: Active source code for the devices.
  - `common/`: Shared core engine and drivers.
  - `tw4/`, `wm12/`: Model-specific entry points.
- **`design/`**: Mechanical and electrical design files (STLs, STEPs, Schematics).
- **`docs/`**: Project documentation and assembly guides.
- **`archives/`**: Legacy backups and historical data.

## Installation (Flashable Firmware)

The easiest way to install OpenERV is to use the pre-compiled **Flashable Firmware (UF2)** images:

1. Download the latest `.uf2` image for your model (TW4 or WM12) from the [GitHub Releases](https://github.com/pngdeity/TW4-Energy-Recovery-Ventilator/releases) page.
2. Hold the **BOOTSEL** button on your Raspberry Pi Pico W and connect it to your computer via USB.
3. Drag and drop the `.uf2` file into the RPI-RP2 drive. The device will reboot automatically.

## Configuration

After flashing, you must provide your local settings:
1. Copy `firmware/config_templates/[model]_persistent_vars.json` to the root of your Pico's filesystem.
2. Rename it to `persistent_vars.json`.
3. Edit the file to include your WiFi credentials and MQTT settings.

## Original Project & Attribution

This project is based on the OpenERV system by Anthony Douglas and the OpenERV community.
- **Original Author**: Anthony Douglas
- **Project Website**: [OpenERV](https://openerv.org)
