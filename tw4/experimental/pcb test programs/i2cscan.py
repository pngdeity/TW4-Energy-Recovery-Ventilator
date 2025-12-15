from machine import Pin, I2C
import time

# Initialize I2C on port 1, with SDA on GPIO 18 and SCL on GPIO 19
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)

def scan_i2c():
    print("Scanning I2C bus on I2C(1), SDA=18, SCL=19...")
    devices = i2c.scan()
    
    if devices:
        print("I2C devices found:")
        for device in devices:
            print("  - Address: 0x{:02X}".format(device))
    else:
        print("No I2C devices found.")

while True:
    scan_i2c()
    time.sleep(5)  # Scan every 5 seconds
