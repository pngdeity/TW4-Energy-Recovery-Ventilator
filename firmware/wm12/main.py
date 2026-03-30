# Licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
# Portions of this code may be based on the original OpenERV work by Anthony Douglas.

import sys
# Add common directory to sys.path for imports
sys.path.append('/firmware/common')

from core_logic import OpenERVCore

# WM12 Model Configuration
WM12_CONFIG = {
    "max_pressure": 30,
    "pressure_ratioa": 1.0,
    "pressure_ratiob": 1.0,
    "ADAFRUIT_IO_FEEDNAME": b'OpenERV_WM12-1',
    "ADAFRUIT_IO_FEEDNAME_publish": b'OpenERV_WM12-1_status',
}

if __name__ == "__main__":
    app = OpenERVCore(WM12_CONFIG)
    app.run()
