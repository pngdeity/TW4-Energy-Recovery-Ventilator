# DIY Manufacturing Guide: OpenERV TW4 and WM12

This guide provides technical specifications and requirements for the independent manufacture of OpenERV TW4 and WM12 units.

## Project Readiness
The OpenERV source code includes schematics, STEP/STL files, and a Bill of Materials (BOM). While the design is stable, some manufacturing-specific configuration files (such as Prusa `.3mf` slicer profiles) are not yet included.

## Additive Manufacturing (3D Printing) Specifications

### Material Requirements
Standard PLA is **not suitable** for these units as it lacks the required structural properties. The following materials are recommended:
- **Modified PLA (MPLA)**: Matter3D or Jayo brand.
- **High-Temp PLA**: Polymaker PLA Pro.
- **ABS**: Acceptable, though prone to warping/curling during large prints.
- **PETG**: Not recommended (insufficient rigidity).

**Thermal Limit**: The current polymers utilized start to soften at **55°C (131°F)**. This must be considered for hot climate installations or direct sunlight exposure.

### Slicer Calibration & Tolerances
To ensure parts fit correctly and maintain aerodynamic efficiency, the following slicer settings are recommended:

1. **Supports**: Use **Tree Supports** (Buildplate Only) for parts like the `combi_hood` and `noise_splitter`. This minimizes surface scarring inside critical airflow paths.
2. **Orientation**: Always align parts so that layer lines are parallel to the primary airflow direction. Refer to `print_specs.json` in the part directories for specific orientations.
3. **Dimensional Accuracy**: 3D printed holes (e.g., for the fan retention clamp) typically shrink. It is recommended to calibrate your slicer's **Hole Expansion** or **Horizontal Expansion** settings. 
   - A typical offset of **0.1mm to 0.2mm** is often required for a press-fit or screw-clearance fit.
4. **Bed Size**: Ensure your printer has a minimum bed dimension of **250mm x 250mm** for the `indoor_plate` and `outdoor_cover`.

### Component-Specific Settings
- **Noise Splitter**: Requires 100% infill in the pipe interface region for mechanical strength.
- **Regenerator**: Use the **Lines** infill pattern with **0 top and 0 bottom layers** to create the open-channel heat exchanger matrix.

## Assembly Requirements

### Electrical Specifications
- **Microcontroller**: Raspberry Pi Pico W.
- **Sensor Interface (I2C ID 1)**:
  - **SDA**: GP18 (Pin 24)
  - **SCL**: GP19 (Pin 25)
- **Power Control**: 10k Potentiometer on **GP28 / ADC2** (Pin 34).
- **Fan PWM Control**:
  - **Primary Fans (i0, e0)**: 70,000 Hz.
  - **Secondary Fans (i1, e1)**: 20,000 Hz.
- **Logic Level**: 3.3V (The Pico W is not 5V tolerant on GPIO).

### Hardware and Consumables
- **Wiring**: High-quality silicone-insulated wire (22-24 AWG) is recommended.
- **Insulation/Acoustics**: 
  - Sourced from indoor-side insulated ducts.
  - **Alternative**: 170 individual foam earplugs can be utilized as a high-performance acoustic damping medium.
- **Heat Exchanger Hats**: Currently require a custom mandrel for fabrication. (See `design/parts/common/stls/` for related components).

## System Architecture & Engineering Diagrams

### 1. Wiring Topology (Control Module)
The following diagram illustrates the standard wiring for the Control Module based on the Raspberry Pi Pico W.

```text
       +---------------------------------------+
       |         Raspberry Pi Pico W           |
       |                                       |
       |  [GP18] SDA <------> SDP810 SDA (Pin 4)|
       |  [GP19] SCL <------> SDP810 SCL (Pin 1)|
       |  [3V3]  VCC <------> SDP810 VDD (Pin 2)|
       |  [GND]  GND <------> SDP810 GND (Pin 3)|
       |                                       |
       |  [GP28] ADC2 <----- Potentiometer (W) |
       |                                       |
       |  [GP0]  PWM  ------> MOSFET Ingress   |
       |  [GP1]  PWM  ------> MOSFET Egress    |
       |                                       |
       |  [VSYS] 5V In <----- Buck Regulator   |
       +---------------------------------------+
```

### 2. Ventilation Cycle Timing
OpenERV utilizes a bidirectional airflow pattern. The timing is dynamically calculated based on the power level to maximize heat exchanger efficiency.

```text
Phase:     |   INGRESS (PID)   |   RAMP DOWN   |   EGRESS (PID)    |   RAMP DOWN   |
Direction: | <---------------  |      ---      |  ---------------> |      ---      |
Fans:      | In: ON / Ex: OFF  | All: COASTing | In: OFF / Ex: ON  | All: COASTing |
Duration:  | 45% of Cycle      | 5% of Cycle   | 45% of Cycle      | 5% of Cycle   |
```

## DIY Logistics
Specialized materials (polypropylene foam, specific acoustic fiberglass, electronic components) are typically sold in bulk. DIYers should account for the higher upfront cost of purchasing these materials compared to a pre-assembled kit.
