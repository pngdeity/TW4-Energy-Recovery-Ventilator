# OpenERV TW4 Frozen Manifest
# This file tells the MicroPython builder which modules to bake into the firmware.

# Include the standard board modules (required for WiFi on Pico W)
include("$(PORT_DIR)/boards/manifest.py")

# Freeze the shared library
# $(FROZEN_DIR) is set in the GitHub Action to point to firmware/
freeze("$(FROZEN_DIR)/common")

# Freeze the TW4 model entry point
freeze("$(FROZEN_DIR)/tw4", "main.py")
