# Technical Audit: OpenERV Design Assets

This document details the findings of a technical audit performed on the mechanical and electrical design files within the `design/` directory.

## 1. Summary of STL Analysis

All STL files were analyzed using `admesh` for geometric integrity and physical dimensions.

| Part Name | Status | Parts | Volume (mm³) | Bounding Box (mm) | Issues Found |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `combi_hood.stl` | Healthy | 1 | 158,890 | 166.6 x 175.6 x 151.6 | None |
| `fiberglass_grid.stl` | Healthy | 1 | 11,696 | 195.6 x 166.6 x 3.0 | None |
| `filter_clamp.stl` | Healthy | 1 | 17,450 | 208.5 x 101.5 x 33.5 | None |
| `filter_seat.stl` | Healthy | 1 | 80,682 | 214.9 x 182.0 x 20.0 | None |
| `hat_seat.stl` | Healthy | 1 | 34,282 | 173.0 x 177.3 x 12.0 | None |
| `indoor_plate.stl` | Healthy | 1 | 161,253 | 187.7 x 219.1 x 14.5 | Tight fit for 220mm beds. |
| `interior_cover.stl` | Healthy (Fixed) | 1 | 180,584 | 200.0 x 220.8 x 75.1 | Normals repaired. |
| `noise_splitter.stl` | Healthy | 2 | 669,905 | 184.0 x 166.9 x 218.8 | Multi-body part (intentional?). |
| `outdoor_cover.stl` | Healthy (Fixed) | 1 | 394,679 | 223.0 x 230.8 x 146.8 | Normals repaired. Requires 250mm+ bed. |
| `outdoor_plate.stl` | Healthy (Fixed) | 1 | 462,341 | 215.0 x 220.0 x 18.0 | Normals repaired. |
| `pipe_extension.stl` | Healthy | 1 | 31,915 | 111.6 x 111.6 x 33.0 | None |
| `pot_mount.stl` | Healthy | 1 | 3,914 | 23.0 x 23.0 x 29.2 | None |
| `pot.stl` | Healthy | 1 | 2,712 | 24.0 x 16.4 x 23.8 | None |
| `regen.stl` | Healthy | 1 | 3,096,175| 148.5 x 148.8 x 180.0 | High volume print. |
| `std_filter_plate.stl`| Healthy | 1 | 66,482 | 209.3 x 182.0 x 20.0 | None |
| `clamp_v2.stl` | Healthy | 1 | 69,363 | 159.0 x 159.0 x 10.0 | None |
| `flow_straightener.stl`| Healthy | 1 | 59,999 | 120.4 x 120.4 x 19.0 | None |

## 2. Integrity Issues & Proposed Changes

### A. Surface Normal Correction
Several files exhibit "Flipped Normals" or "Backwards Edges." While most modern slicers (Cura, PrusaSlicer) can auto-repair these on import, they can cause issues with professional CNC or injection molding software.
- **Proposed Change**: Re-export `interior_cover.stl`, `outdoor_cover.stl`, and `outdoor_plate.stl` from the source CAD with unified surface normals to ensure manifold integrity.

### B. Printer Bed Compatibility
- **`outdoor_cover.stl`**: At 223mm x 230mm, this file exceeds the standard 220mm (Ender 3 class) print bed.
- **`interior_cover.stl`**: At 220.8mm, it may fail on printers with strict software endstops.
- **Proposed Change**: Consider a minor design revision to the `outdoor_cover` to bring the largest dimension under 215mm, or explicitly mark this part as "Large Format Only" in the filename.

### C. Multi-Body Parts
- **`noise_splitter.stl`**: Contains 2 distinct shells. This can sometimes cause slicers to treat them as overlapping solids, leading to over-extrusion at the boundary.
- **Proposed Change**: Merge shells into a single manifold boolean object before re-exporting.

## 3. STEP File Verification
The STEP files (`rev_11_tw4_v35.step`, etc.) are in standard ISO-10303-21 format.
- **Observation**: The filenames are inconsistent with the STL counterparts.
- **Proposed Change**: Rename STEP files to match the part names used in the `stls/` directory for better cross-referencing.

## 4. Electrical Schematics
The EasyEDA source files are current but use proprietary JSON schema.
- **Proposed Change**: In the next design cycle, include an **IPC-2581** or **ODB++** export in the `schematics/source` directory to provide a software-agnostic manufacturing exchange format.
