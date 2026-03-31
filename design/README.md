# OpenERV Hardware Design

This directory contains all the mechanical and electrical design files for the OpenERV TW4 and WM12 units.

## Directory Structure

- **`parts/`**: 3D design files (STL for printing, STEP for CAD modeling).
  - **`common/`**: Parts shared by both TW4 and WM12 models (covers, plates, noise splitters).
  - **`tw4/`**: Parts unique to the TW4 model (e.g., flow straighteners).
  - **`wm12/`**: Parts unique to the WM12 model (e.g., window adapters).
- **`schematics/`**: Electrical schematics, PCB layouts, and sensor pinouts.
  - **`source/`**: Raw EasyEDA JSON source files.

## Bill of Materials (BOM)

Standardized Bills of Materials are provided in the [OSHWA](https://www.oshwa.org/) recommended CSV format:
- **`BOM_TW4.csv`**: Parts list for a single TW4 module.
- **`BOM_WM12.csv`**: Parts list for a complete WM12 window-mounted unit (includes 2x modules and adapter hardware).

These files include component names, quantities, technical descriptions, and suggested sourcing information (e.g., LCSC/DigiKey part numbers where applicable).

## Manufacturing

### Automated Manufacturing Reports
This repository uses **PrusaSlicer CLI** in a GitHub Action to automatically audit every 3D model change. On every push to the `main` branch, a report is generated containing:
- **Print Time Estimates**: Calculated using the project's manufacturing profile.
- **Material Usage**: Estimated weight in grams.
- **Physical Dimensions**: Precise bounding box measurements.

The latest report can be found in the `design/` directory as **`MANUFACTURING_REPORT.csv`**.

### 3D Printing Specifications
Material and slicer requirements are provided in **`print_specs.json`** files within each sub-directory. These files use a standardized schema to define:
- **Recommended Materials**: (e.g., MPLA for high thermal resistance).
- **Infill Settings**: Specific densities and patterns (e.g., 100% infill for mechanical regions).
- **Layer Details**: Wall counts and layer heights required for structural integrity.

For detailed assembly and manufacturing instructions, please refer to the documentation in the root `docs/` directory:
- [DIY Manufacturing Guide](../docs/Document%20to%20aid%20DIY%20manufacturing%20of%20the%20OpenERV%20TW4%20and%20WM12.md)
- [TW4 Manual](../docs/TW4%20manual%20-%20OpenERV.md)
- [WM12 Manual](../docs/OpenERV%20WM12%20manual.md)
