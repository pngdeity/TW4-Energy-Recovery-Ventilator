# OpenERV Hardware Design

This directory contains all the mechanical and electrical design files for the OpenERV TW4 and WM12 units.

## Directory Structure

- **`parts/`**: 3D design files (STL for printing, STEP for CAD modeling).
  - **`common/`**: Parts shared by both TW4 and WM12 models (covers, plates, noise splitters).
  - **`tw4/`**: Parts unique to the TW4 model (e.g., flow straighteners).
  - **`wm12/`**: Parts unique to the WM12 model (e.g., window adapters).
- **`schematics/`**: Electrical schematics, PCB layouts, and sensor pinouts.
  - **`source/`**: Raw EasyEDA JSON source files.

## Manufacturing

For detailed assembly and manufacturing instructions, please refer to the documentation in the root `docs/` directory:
- [DIY Manufacturing Guide](../docs/Document%20to%20aid%20DIY%20manufacturing%20of%20the%20OpenERV%20TW4%20and%20WM12.md)
- [TW4 Manual](../docs/TW4%20manual%20-%20OpenERV.md)
- [WM12 Manual](../docs/OpenERV%20WM12%20manual.md)
