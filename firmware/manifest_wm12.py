# OpenERV WM12 Frozen Manifest
# This file tells the MicroPython builder which modules to bake into the firmware.

# Include the standard board modules (required for WiFi on Pico W)
include("$(PORT_DIR)/boards/manifest.py")

# Freeze the shared library
freeze("common")

# Freeze the WM12 model entry point
freeze("wm12", "main.py")
