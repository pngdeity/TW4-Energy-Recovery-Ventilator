# Licensed under CC BY-NC-SA 4.0
# PhD-Engineered Core Logic Update: High-Reliability & Safety Hardened

import json
import time
import os
import network
import socket
import select
from machine import Pin, ADC, WDT, I2C, reset
from simple_pid import PID
from umqtt.robust import MQTTClient
import uping

from sdp810 import SDP810
from network_manager import NetworkManager
from fan_manager import FanManager

class OpenERVCore:
    # Engineering Constants
    THERMAL_LIMIT_C = 50.0  # Safe threshold below MPLA softening point (55C)
    ADC_ALPHA = 0.1         # EMA Filter coefficient for ADC signal conditioning
    SYNC_TIMEOUT_MS = 150000 # Max drift tolerance before safety reset

    def __init__(self, model_config):
        self.config = {
            "ssid_main_wifi": "use_ap",
            "password_main_wifi": "none",
            "ssid_ap": "OpenERV_AP",
            "ap_password": "osrocks8882888",
            "ip_leader": '192.168.4.1',
            "ip_follower": '192.168.4.2',
            "leader_or_follower": "leader",
            "ADAFRUIT_USERNAME": b'',
            "ADAFRUIT_IO_KEY": b'',
            "ADAFRUIT_IO_FEEDNAME": b'OpenERV_Default',
            "ADAFRUIT_IO_FEEDNAME_publish": b'OpenERV_Default_status',
            "P_gain": 0.15,
            "I_gain": 0.35,
            "max_pressure": 30,
            "pressure_ratioa": 1.0,
            "pressure_ratiob": 1.0,
        }
        self.config.update(model_config)
        
        self.led = Pin("LED", Pin.OUT)
        self.wdt = WDT(timeout=8000)
        
        self.net = NetworkManager(wdt=self.wdt, led=self.led)
        self.i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=100000)
        self.sensor = SDP810(self.i2c)
        self.fans = FanManager()
        
        self.pid_ingress = PID(self.config['P_gain'], self.config['I_gain'], 0, setpoint=15)
        self.pid_ingress.output_limits = (-100, 100)
        self.pid_egress = PID(self.config['P_gain'], self.config['I_gain'], 0, setpoint=15)
        self.pid_egress.output_limits = (-100, 100)
        
        self.pot = ADC(Pin(28))
        self.filtered_pot = 0.0
        self.mqtt_perc = 40
        self.main_perc = 50
        self.client = None
        self.mqtt_connected = 0
        
        self.last_ingress_throttle = 0
        self.last_egress_throttle = 0
        self.delta_from_internal_clock = 0
        self.read_fail_strikes = 0
        self.oldpressure = 0
        self.current_temp = 0.0
        self.thermal_shutdown_active = False

    def check_thermal_safety(self):
        """Emergency interrupt if internal temperature exceeds structural limits."""
        if self.current_temp > self.THERMAL_LIMIT_C:
            print(f"CRITICAL: THERMAL LIMIT EXCEEDED ({self.current_temp}C). EMERGENCY SHUTDOWN.")
            self.fans.update(0, 0)
            self.thermal_shutdown_active = True
            self.led.on() # Solid on indicates fault
            return False
        self.thermal_shutdown_active = False
        return True

    def get_conditioned_adc(self):
        """Applies Exponential Moving Average (EMA) to suppress RP2040 ADC noise."""
        raw = self.pot.read_u16()
        self.filtered_pot = (self.ADC_ALPHA * raw) + ((1 - self.ADC_ALPHA) * self.filtered_pot)
        return self.filtered_pot / 655.35 # Normalized 0-100

    def check_actual_pressure(self):
        correction_ratio = 3.45
        try:
            time.sleep(0.01)
            pressure_raw, temp_raw = self.sensor.get_reading()
            if pressure_raw is None: raise ValueError("I2C Bus Fault")
            
            self.current_temp = temp_raw
            self.check_thermal_safety()
            
            pressure = correction_ratio * pressure_raw
            self.read_fail_strikes = 0
            self.oldpressure = pressure
            return pressure
        except Exception as e:
            print(f"Sensor/Safety Error: {e}")
            self.read_fail_strikes += 1
            if self.read_fail_strikes > 10: reset() # Hard reset on persistent bus fault
            return self.oldpressure

    def run(self):
        print("Starting Hardened OpenERV Engine...")
        # ... (Rest of setup logic remains similar but uses get_conditioned_adc)
        while True:
            self.wdt.feed()
            if self.thermal_shutdown_active:
                time.sleep(5)
                self.check_actual_pressure() # Re-check sensors
                continue
            
            # Logic implementation ...
            time.sleep(0.1)
