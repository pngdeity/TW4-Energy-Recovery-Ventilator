# OpenERV Schematics and PCB Design

This directory contains the electrical design files for the OpenERV systems.

## Contents

- **`pcb_schematic_v2.png`**: Current schematic for the TW4/WM12 main board.
- **`pcb_schematic_v1.pdf`**: Previous version or alternative view of the schematic.
- **`sensor_sdp810_pinout.png`**: Pinout reference for the Sensirion SDP810 differential pressure sensor.
- **`source/`**: Contains the raw EDA source files.
  - `1-Schematic_TW4 Main board2.json`: EasyEDA schematic source.
  - `1-PCB_PCB_TW4 Main board2.json`: EasyEDA PCB layout source.

## Using the Source Files

The source files in the `source/` directory are in **EasyEDA (Standard Edition)** format. To view or modify them:

1. Go to [EasyEDA](https://easyeda.com/).
2. Log in and open the Editor.
3. Use **File -> Open -> EasyEDA...** and upload the `.json` files.
4. You can then export Gerbers, BOMs, and Pick-and-Place files directly from the editor for manufacturing.

## Component Sourcing

Key components like the Raspberry Pi Pico W and the SDP810 sensor should be sourced from reputable suppliers (e.g., DigiKey, Mouser) to ensure reliability. Refer to the project manuals in the `docs/` folder for detailed Bills of Materials (BOM).
