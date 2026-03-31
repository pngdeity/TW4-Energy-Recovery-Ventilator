# OpenERV TW4 Frozen Manifest
# This file tells the MicroPython builder which modules to bake into the firmware.

# Include the standard board modules (required for WiFi on Pico W)
include("$(PORT_DIR)/boards/manifest.py")

# Freeze the shared library
freeze("common")

# Freeze the TW4 model entry point
# Note: We freeze it into the root namespace so it acts as the default main.py
freeze("tw4", "main.py")
