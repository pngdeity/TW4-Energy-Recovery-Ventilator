# Licensed under CC BY-NC-SA 4.0
# Driver for Sensirion SCD4x CO2 Sensor (I2C)

import time
from machine import I2C

class SCD4X:
    DEFAULT_ADDR = 0x62

    def __init__(self, i2c, addr=DEFAULT_ADDR):
        self.i2c = i2c
        self.addr = addr
        self._init_sensor()

    def _init_sensor(self):
        """Initializes the sensor and starts periodic measurement."""
        try:
            # Stop periodic measurement to ensure we can send commands
            self.stop_periodic_measurement()
            time.sleep(0.5)
            # Start periodic measurement
            self.start_periodic_measurement()
        except Exception as e:
            print(f"Error initializing SCD4X: {e}")

    def start_periodic_measurement(self):
        """Starts periodic measurement, signal update interval is 5 seconds."""
        self.i2c.writeto(self.addr, b'\x21\xb1')

    def stop_periodic_measurement(self):
        """Stops periodic measurement to allow sending other commands."""
        self.i2c.writeto(self.addr, b'\x3f\x86')

    def get_reading(self):
        """Returns (CO2 ppm, Temperature C, Humidity RH%)."""
        try:
            # Command to read measurement (0xec05)
            self.i2c.writeto(self.addr, b'\xec\x05')
            time.sleep(0.01)
            data = self.i2c.readfrom(self.addr, 9)
            
            # CO2
            co2 = (data[0] << 8) | data[1]
            
            # Temperature: -45 + 175 * word / 2^16
            temp_raw = (data[3] << 8) | data[4]
            temperature = -45 + (175 * temp_raw / 65536)
            
            # Humidity: 100 * word / 2^16
            humi_raw = (data[6] << 8) | data[7]
            humidity = 100 * humi_raw / 65536
            
            return co2, temperature, humidity
        except Exception as e:
            # print(f"Error reading from SCD4X: {e}")
            return None, None, None
