# OpenERV Firmware

This directory contains the MicroPython firmware for the OpenERV TW4 and WM12 units. The firmware has been refactored into a modular, object-oriented architecture to maximize code reuse and reliability across different hardware models.

## Software Architecture

The firmware follows a **Core-Wrapper** pattern. The heavy lifting is handled by a shared core library, while model-specific directories contain minimal configuration and entry logic.

### 1. Model Entry Points (`/tw4` and `/wm12`)
These directories contain the `main.py` files that serve as the entry point for the Raspberry Pi Pico W.
- **`main.py`**: A "thin wrapper" that defines model-specific constants (like pressure gains and I/O pins) and instantiates the `OpenERVCore`.
- **`persistent_vars.json`**: (User-created) Local configuration file containing WiFi credentials and device-specific settings.

### 2. Common Library (`/common`)
This directory contains the engine of the project. By centralizing this logic, we ensure that improvements to the PID loop or networking stability benefit all models simultaneously.
- **`core_logic.py`**: Contains the `OpenERVCore` class.
- **`ha_discovery.py`**: Implements Home Assistant MQTT Discovery for automatic dashboard integration.
- **`sdp810.py`**: A robust, class-based driver for the Sensirion SDP810.
- **`fan_manager.py`**: Manages fan pairs and implements the coordinated ramp-down logic required for efficient energy recovery.
- **`network_manager.py`**: Handles WiFi station connections and Access Point (AP) mode.
- **`simple_pid/`, `umqtt/`, `uping.py`**: Standardized third-party libraries for PID control, MQTT communication, and network diagnostics.

### 3. Configuration Templates (`/config_templates`)
Contains example `persistent_vars.json` files for each model. To configure a new device:
1. Copy the relevant template to the root of your Pico.
2. Rename it to `persistent_vars.json`.
3. Update it with your WiFi and Adafruit IO credentials.

### 4. Experimental Scripts (`/experimental`)
Diagnostic and characterization tools used for hardware validation and efficiency measurements. See the [Experimental README](./experimental/README.md) (if available) for more details.

## Control Logic Flow

1. **Initialization**: The device loads configuration, initializes the I2C sensor, and sets up PWM for the fans.
2. **Connectivity**: The unit attempts to connect to WiFi. If configured as a **Leader**, it optionally connects to MQTT for telemetry. If a connection fails, it may fall back to **Access Point** mode.
3. **Synchronization**:
   - **Leaders** broadcast their internal clock and power settings via UDP.
   - **Followers** listen for these UDP packets to synchronize their cycles with the leader.
4. **The Loop**:
   - **Ingress Phase**: The unit runs a PID loop to maintain the target pressure for incoming air.
   - **Egress Phase**: The unit reverses the cycle, running a PID loop for outgoing air.
   - **Ramping**: The `FanManager` ensures that fans don't snap between speeds, protecting the hardware and reducing noise.

## Development Guidelines

- **Stay Modular**: Do not add hardware-specific logic to `core_logic.py`. Instead, add a configuration parameter to the `OpenERVCore` constructor.
- **Error Resilience**: Always use `try/except` blocks when communicating with I2C sensors or network sockets to prevent the device from hanging.
- **WDT**: The Watchdog Timer is enabled by default. Ensure that any long-running operations (like network handshakes) "feed" the watchdog to avoid unintended resets.
