# DIY Manufacturing Guide: OpenERV TW4 and WM12

This guide provides technical specifications and requirements for the independent manufacture of OpenERV TW4 and WM12 units.

## Project Readiness
The OpenERV source code includes schematics, STEP/STL files, and a Bill of Materials (BOM). While the design is stable, some manufacturing-specific configuration files (such as Prusa `.3mf` slicer profiles) are not yet included.

## Additive Manufacturing (3D Printing) Specifications

### Material Requirements
Standard PLA is **not suitable** for these units as it lacks the required structural properties. The following materials are recommended:
- **MPLA**: Matter3D or Jayo brand.
- **PLA Pro**: Polymaker PLA Pro.
- **ABS**: Acceptable, though prone to warping/curling during large prints.
- **PETG**: Not recommended (insufficient rigidity).

**Thermal Limit**: The current polymers utilized start to soften at **55°C (131°F)**. This should be considered for hot climate installations.

### Component-Specific Settings
- **Noise Splitter**: Requires 100% infill in the pipe interface region for mechanical strength.
- **Indoor Cover**: This is a large-format part that requires a print bed capable of accommodating its full dimensions.

## Assembly Requirements

### Electronics and Wiring
- **Soldering**: Required for internal connections. Precision is necessary to avoid short circuits.
- **Wiring**: High-quality silicone-insulated wire is recommended for flexibility and durability.
- **PCB**: A transition to a dedicated PCB is in progress. However, point-to-point wiring using screw terminals remains a valid assembly method.

### Hardware and Consumables
- **Mechanical Fasteners**: Various screws and brackets are required (refer to model-specific BOMs).
- **Insulation/Acoustics**: 
  - Sourced from indoor-side insulated ducts.
  - **Alternative**: Approximately 170 pairs of foam earplugs can be utilized as a high-performance acoustic damping medium.
- **Heat Exchanger Hats**: Currently require a custom mandrel for fabrication (mandrel design files pending).

## DIY Logistics
Most specialized materials (polypropylene foam, specific fiberglass, electronic components) are typically sold in bulk quantities. DIYers should account for the higher upfront cost of purchasing these materials compared to a pre-assembled kit.
