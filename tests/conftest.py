import sys
import os
import types
import time as real_time

# Add mocks and common firmware to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'mocks')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../firmware/common')))

# Create basic mocks for modules that don't need full logic
m_network = types.ModuleType('network')
m_network.STA_IF = 0
m_network.AP_IF = 1
m_network.WLAN = lambda x: None
sys.modules['network'] = m_network

# Structured mock for umqtt.robust
m_umqtt = types.ModuleType('umqtt')
m_umqtt_robust = types.ModuleType('umqtt.robust')
class MQTTClient:
    def __init__(self, *args, **kwargs): pass
    def set_callback(self, cb): pass
    def connect(self): pass
    def subscribe(self, topic): pass
m_umqtt_robust.MQTTClient = MQTTClient
sys.modules['umqtt'] = m_umqtt
sys.modules['umqtt.robust'] = m_umqtt_robust

sys.modules['uping'] = types.ModuleType('uping')

# Mock ubinascii
m_ubinascii = types.ModuleType('ubinascii')
m_ubinascii.hexlify = lambda x: b'aabbccddeeff'
sys.modules['ubinascii'] = m_ubinascii

# Enhance machine mock if not already done via file replacement
# (but conftest here does manual sys.modules sometimes)
import machine
machine.unique_id = lambda: b'\xaa\xbb\xcc\xdd\xee\xff'

# Mock time for MicroPython specifics AND CPython compatibility
m_time = types.ModuleType('time')
m_time.sleep = real_time.sleep
m_time.time = real_time.time
m_time.monotonic = real_time.monotonic
m_time.ticks_ms = lambda: int(real_time.time() * 1000)
m_time.ticks_diff = lambda a, b: a - b
sys.modules['time'] = m_time
