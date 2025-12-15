from machine import I2C, Pin
import time
import machine
# Initialize I2C bus
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=100000)
#i2c = machine.I2C(1, scl=machine.Pin(19), sda=machine.Pin(18))
address = 0x25

def write_i2c_block_data(addr, cmd, val):
    data = bytearray([cmd] + val)
    i2c.writeto(addr, data)

def read_i2c_block_data(addr, cmd, length):
    i2c.writeto(addr, bytearray([cmd]))
    return i2c.readfrom(addr, length)

# Stop any continuous measurement of the sensor
write_i2c_block_data(address, 0x3F, [0xF9])
time.sleep(0.8)
#print("(Start Continuous Measurement (5.3.1 in Data sheet)")

# Command code 0x3603 (Mass flow, Average till read)
write_i2c_block_data(address, 0x36, [0x03])

def get_reading():
    reading = read_i2c_block_data(address, 0x00, 9)
    pressure_value = reading[0] + float(reading[1]) / 255
    if pressure_value >= 0 and pressure_value < 128:
        differential_pressure = pressure_value * 240 / 256  # scale factor adjustment
    elif pressure_value > 128 and pressure_value <= 256:
        differential_pressure = -(256 - pressure_value) * 240 / 256  # scale factor adjustment
    elif pressure_value == 128:
        differential_pressure = 99999999  # Out of range
    return differential_pressure
def get_temperature():
    reading=read_i2c_block_data(address,0x00, 9)
    temp_value=reading[3]+float(reading[4])/255
    if temp_value>=0 and temp_value<=100:
        temperature=temp_value*255/200 #scale factor adjustment
    if temp_value<=256 and temp_value>=200:
        temperature=-(256-temp_value)*255/200 #scale factor adjustment
    return temperature
