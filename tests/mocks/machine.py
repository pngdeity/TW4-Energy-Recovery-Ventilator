# Mock for MicroPython 'machine' module
class Pin:
    OUT = 1
    IN = 0
    PULL_UP = 1
    PULL_DOWN = 2
    def __init__(self, pin, mode=-1, pull=-1, value=None):
        self._value = 0
    def value(self, val=None):
        if val is not None: self._value = val
        return self._value
    def on(self): self._value = 1
    def off(self): self._value = 0
    def toggle(self): self._value = 1 - self._value

class PWM:
    def __init__(self, pin):
        self._freq = 0
        self._duty = 0
    def freq(self, f): self._freq = f
    def duty_u16(self, d): self._duty = d

class ADC:
    def __init__(self, pin):
        self._value = 32768
    def read_u16(self): return self._value

class I2C:
    def __init__(self, id, scl=None, sda=None, freq=400000):
        self.fail_mode = False
        self.drift_offset = 0.0
        self._read_count = 0

    def writeto(self, addr, data): 
        if self.fail_mode: raise Exception("I2C Bus Error")
        pass

    def readfrom(self, addr, nbytes):
        if self.fail_mode: raise Exception("I2C Bus Error")
        
        # Simulate intermittent failures every 100 reads
        self._read_count += 1
        if self._read_count % 100 == 0:
            return b'\xFF' * nbytes # Garbage data
            
        return b'\x00' * nbytes # Default mock data

class WDT:
    def __init__(self, timeout): pass
    def feed(self): pass

class WLAN:
    def __init__(self, interface): pass
    def active(self, state=None): return True
    def connect(self, ssid, password): pass
    def isconnected(self): return True
    def ifconfig(self, config=None): return ('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8')
    def config(self, *args, **kwargs): pass

def reset(): pass
