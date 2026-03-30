# Licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
# Portions of this code may be based on the original OpenERV work by Anthony Douglas.

import sys
# Add common directory to sys.path for imports
sys.path.append('/firmware/common')

from core_logic import OpenERVCore

# TW4 Model Configuration
TW4_CONFIG = {
    "max_pressure": 34,
    "pressure_ratioa": 0.775,
    "pressure_ratiob": 0.9,
    "ADAFRUIT_IO_FEEDNAME": b'OpenERV_TW4-1',
    "ADAFRUIT_IO_FEEDNAME_publish": b'OpenERV_TW4-1_status',
}

if __name__ == "__main__":
    app = OpenERVCore(TW4_CONFIG)
    app.run()
