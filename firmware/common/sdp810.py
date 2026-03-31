# Licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
# Portions of this code may be based on the original OpenERV work by Anthony Douglas.

from machine import I2C, Pin
import time

class SDP810:
    """Driver for the SDP810 differential pressure sensor."""
    
    DEFAULT_ADDR = 0x25
    
    def __init__(self, i2c_bus, addr=DEFAULT_ADDR):
        self.i2c = i2c_bus
        self.addr = addr
        self._init_sensor()

    def _init_sensor(self):
        """Stop any continuous measurement and start mass flow average mode."""
        try:
            # Stop any continuous measurement
            self.i2c.writeto(self.addr, b'\x3F\xF9')
            time.sleep(0.01) # Reduced from 0.8 to be more responsive
            
            # Command code 0x3603 (Mass flow, Average till read)
            self.i2c.writeto(self.addr, b'\x36\x03')
        except Exception as e:
            print(f"Error initializing SDP810: {e}")

    def get_reading(self):
        """Retrieve the differential pressure reading."""
        try:
            # Command to read data (9 bytes: 2 pressure, 1 CRC, 2 temp, 1 CRC, 3 reserved)
            reading = self.i2c.readfrom(self.addr, 9)
            
            # Pressure Calculation
            pressure_value = reading[0] + float(reading[1]) / 255
            if 0 <= pressure_value < 128:
                differential_pressure = pressure_value * 240 / 256
            elif 128 < pressure_value <= 256:
                differential_pressure = -(256 - pressure_value) * 240 / 256
            elif pressure_value == 128:
                differential_pressure = float('inf')
            else:
                differential_pressure = 0.0
                
            # Temperature Calculation (Scale factor 200 per datasheet)
            temp_raw = reading[3] + float(reading[4]) / 255
            temperature = temp_raw * 255 / 200 
            
            return differential_pressure, temperature
        except Exception as e:
            print(f"Error reading from SDP810: {e}")
            return None, None
