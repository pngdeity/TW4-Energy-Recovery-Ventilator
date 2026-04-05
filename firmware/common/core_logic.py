# Licensed under CC BY-NC-SA 4.0
# Core Logic: Reliability & Safety Improvements

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
from scd4x import SCD4X
from sync_manager import SyncManager
from network_manager import NetworkManager
from fan_manager import FanManager
from provisioning import ProvisioningManager

class OpenERVCore:
    # Engineering Constants
    THERMAL_LIMIT_C = 50.0  # Safe threshold below MPLA softening point (55C)
    CO2_BOOST_THRESHOLD = 800 # ppm - Start ramping up above this
    CO2_MAX_THRESHOLD = 1200  # ppm - Forced Max speed
    FROST_LIMIT_C = -5.0      # Trigger defrost below this
    DEFROST_DURATION_S = 300  # 5 minutes of exhaust to melt core
    SYNC_INTERVAL_S = 10      # How often to send sync (UDP)
    # Using shift-based EMA: filtered = (raw + (filtered * (2^N - 1))) >> N
    # This is efficient on small MCUs
    ADC_FILTER_SHIFT = 3    # N=3 -> approx 0.125 alpha

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
            "enable_co2": False,
        }
        self.config.update(model_config)
        
        self.led = Pin("LED", Pin.OUT)
        self.wdt = WDT(timeout=8000)
        
        # Initialize components
        self.net = NetworkManager(wdt=self.wdt, led=self.led)
        self.i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=100000)
        self.sensor = SDP810(self.i2c)
        self.co2_sensor = None
        if self.config.get('enable_co2'):
            self.co2_sensor = SCD4X(self.i2c)
        
        self.sync = SyncManager(self.config, wdt=self.wdt)
        self.fans = FanManager()
        self.prov = ProvisioningManager(self.net)
        
        self.pid_ingress = PID(self.config['P_gain'], self.config['I_gain'], 0, setpoint=15)
        self.pid_ingress.output_limits = (-100, 100)
        self.pid_egress = PID(self.config['P_gain'], self.config['I_gain'], 0, setpoint=15)
        self.pid_egress.output_limits = (-100, 100)
        
        self.pot = ADC(Pin(28))
        self.filtered_pot_raw = 0  # Store as integer for bit-shifting
        self.mqtt_perc = 40
        self.main_perc = 50
        self.client = None
        self.mqtt_connected = 0
        self.mqtt_feedname_publish = None
        
        self.last_ingress_throttle = 0
        self.last_egress_throttle = 0
        self.delta_from_internal_clock = 0
        self.read_fail_strikes = 0
        self.oldpressure = 0
        self.current_temp = 0.0
        self.current_co2 = 400
        self.sync_pressure_offset = 0.0
        self.last_sync_time = 0
        self.thermal_shutdown_active = False
        self.defrost_active = False
        self.last_defrost_time = 0

    def load_persistent_vars(self):
        filename = "persistent_vars.json"
        try:
            with open(filename, "r") as f:
                self.config.update(json.load(f))
            print("Loaded persistent_vars.json")
            return True
        except Exception:
            print("No persistent_vars.json found.")
            return False

    def handle_safety_checks(self):
        """Global safety state machine. Run this every loop iteration."""
        # 1. Thermal Safety
        if self.current_temp > self.THERMAL_LIMIT_C:
            if not self.thermal_shutdown_active:
                print(f"CRITICAL: THERMAL LIMIT EXCEEDED ({self.current_temp}C). EMERGENCY SHUTDOWN.")
                self.fans.update(0, 0)
                self.thermal_shutdown_active = True
                self.led.on()
            return False
        
        # 2. Frost Protection (Defrost Mode)
        # Trigger if temp is below limit and it's been long enough since last defrost
        if self.current_temp < self.FROST_LIMIT_C and not self.defrost_active:
            if time.time() - self.last_defrost_time > 1800: # Max once every 30 mins
                print(f"Frost detected ({self.current_temp}C). Entering Defrost Mode...")
                self.defrost_active = True
                self.last_defrost_time = time.time()
        
        # 3. CO2 Monitoring (Optional)
        if self.co2_sensor:
            co2, _, _ = self.co2_sensor.get_reading()
            if co2:
                self.current_co2 = co2
                if self.current_co2 > self.CO2_MAX_THRESHOLD:
                    print(f"High CO2 ({self.current_co2} ppm). Boosting to MAX.")
                elif self.current_co2 > self.CO2_BOOST_THRESHOLD:
                    print(f"CO2 Rising ({self.current_co2} ppm). Ramping up.")

        self.thermal_shutdown_active = False
        return True

    def get_conditioned_adc(self):
        """Integer-based EMA filter with 8-sample accumulation."""
        raw = self.pot.read_u16()
        # Scale up the input to match the 8-sample accumulator
        # filtered = (new_scaled + (old_accum * 7)) / 8
        self.filtered_pot_raw = (raw + (self.filtered_pot_raw * 7)) >> 3
        return self.filtered_pot_raw / 655.35 # Normalized 0-100

    def get_effective_power(self):
        """Adjusts pot value based on CO2 levels (Demand Controlled Ventilation)."""
        base_power = self.get_conditioned_adc()
        
        if not self.co2_sensor:
            return base_power
            
        # If CO2 is critical, force MAX speed
        if self.current_co2 > self.CO2_MAX_THRESHOLD:
            return 100.0
            
        # If CO2 is rising, ramp up power proportionally
        if self.current_co2 > self.CO2_BOOST_THRESHOLD:
            # Linear ramp from base_power to 100 between thresholds
            range = self.CO2_MAX_THRESHOLD - self.CO2_BOOST_THRESHOLD
            extra = (self.current_co2 - self.CO2_BOOST_THRESHOLD) / range
            return min(100.0, base_power + (extra * (100.0 - base_power)))
            
        return base_power

    def check_actual_pressure(self):
        correction_ratio = 3.45
        try:
            time.sleep(0.01)
            pressure_raw, temp_raw = self.sensor.get_reading()
            if pressure_raw is None:
                self.read_fail_strikes += 1
                if self.read_fail_strikes > 10: reset()
                return self.oldpressure
            
            self.current_temp = temp_raw
            self.oldpressure = correction_ratio * pressure_raw
            self.read_fail_strikes = 0
            return self.oldpressure
        except Exception as e:
            print(f"I2C Read Error: {e}")
            self.read_fail_strikes += 1
            return self.oldpressure

    def percent_to_pressure(self, perc):
        max_p = self.config['max_pressure']
        pressure = perc * max_p / 100
        pressure = max(-max_p, min(max_p, pressure))
        if -4 < pressure < 4:
            pressure = 0
        return pressure

    def check_cp_ingress(self):
        if self.main_perc < 40:
            return self.percent_to_pressure(self.main_perc) * self.config['pressure_ratiob']
        return self.percent_to_pressure(self.main_perc) * self.config['pressure_ratioa']

    def check_cp_egress(self):
        if self.main_perc < 40:
            return -1 * self.percent_to_pressure(self.main_perc) / self.config['pressure_ratiob']
        return -1 * self.percent_to_pressure(self.main_perc) / self.config['pressure_ratioa']

    def mqtt_callback(self, topic, msg):
        try:
            self.mqtt_perc = int(msg.decode())
            print(f"MQTT command: {self.mqtt_perc}")
        except: pass

    def connect_mqtt(self):
        if not self.config['ADAFRUIT_USERNAME'] or not self.config['ADAFRUIT_IO_KEY']:
            return 0, None
        mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(self.config['ADAFRUIT_USERNAME'].decode(), self.config['ADAFRUIT_IO_FEEDNAME'].decode()), 'utf-8')
        self.mqtt_feedname_publish = bytes('{:s}/feeds/{:s}'.format(self.config['ADAFRUIT_USERNAME'].decode(), self.config['ADAFRUIT_IO_FEEDNAME_publish'].decode()), 'utf-8')
        client_id = bytes('client_' + str(int.from_bytes(os.urandom(3), 'little')), 'utf-8')
        client = MQTTClient(client_id=client_id, server=self.config['ADAFRUIT_IO_URL'], user=self.config['ADAFRUIT_USERNAME'], password=self.config['ADAFRUIT_IO_KEY'], ssl=False)
        client.set_callback(self.mqtt_callback)
        try:
            self.wdt.feed()
            client.connect()
            client.subscribe(mqtt_feedname)
            print("MQTT Connected")
            return 1, client
        except:
            return 0, None

    def period_time_calc(self):
        power = max(0.1, self.main_perc)
        return min(120000, 50000 / (power / 100))

    def ticks_ms_synced(self):
        if self.config['leader_or_follower'] == "leader":
            return time.ticks_ms()
        return time.ticks_diff(time.ticks_ms(), self.delta_from_internal_clock)

    def handle_sync(self):
        """Manages UDP sync timing and pressure offsets."""
        if self.config['leader_or_follower'] == "leader":
            if time.time() - self.last_sync_time > self.SYNC_INTERVAL_S:
                # Leader: Calculate pressure offset to maintain 0 Pa
                # If pressure is positive, Follower needs to exhaust more (offset < 0)
                # If pressure is negative, Follower needs to supply more (offset > 0)
                # This is a simple proportional correction for now
                self.sync_pressure_offset = -0.5 * self.oldpressure
                self.sync.send_sync(time.ticks_ms(), self.sync_pressure_offset)
                self.last_sync_time = time.time()
                print(f"Sync sent: Offset={self.sync_pressure_offset}")
        else:
            # Follower: Listen for sync
            new_ticks, new_offset = self.sync.receive_sync()
            if new_ticks is not None:
                self.delta_from_internal_clock = time.ticks_diff(time.ticks_ms(), new_ticks)
                self.sync_pressure_offset = new_offset
                print(f"Sync received: Offset={self.sync_pressure_offset}")

    def run(self):
        print("Starting OpenERV Core Engine...")
        has_config = self.load_persistent_vars()
        
        # Provisioning Check
        if not has_config or self.config['ssid_main_wifi'] in ["use_ap", "none"]:
            print("No valid WiFi config. Entering Provisioning Mode...")
            ip = self.net.make_ap(ssid="OpenERV_Setup")
            self.prov.start_server(ip)
            return

        # Normal Startup
        ip, wlan = self.net.connect_wifi(
            self.config['ssid_main_wifi'], 
            self.config['password_main_wifi'],
            ip_follower=self.config.get('ip_follower'),
            leader_or_follower=self.config.get('leader_or_follower', 'leader')
        )
        
        if self.config['leader_or_follower'] == "leader" and wlan and wlan.isconnected():
            self.mqtt_connected, self.client = self.connect_mqtt()

        while True:
            self.wdt.feed()
            pressure = self.check_actual_pressure()
            
            if not self.handle_safety_checks():
                time.sleep(5)
                continue

            self.handle_sync()
            self.fans.update(self.last_ingress_throttle, self.last_egress_throttle)
            
            # 1. Defrost Logic (Exhaust-only to melt ice)
            if self.defrost_active:
                print("DEFROST START: Running exhaust-only for 5 minutes.")
                cp_egress = self.percent_to_pressure(100) # Full power exhaust
                self.pid_egress.setpoint = -cp_egress
                self.pid_egress.set_auto_mode(True, last_output=self.last_egress_throttle)
                
                start_defrost = time.time()
                while time.time() - start_defrost < self.DEFROST_DURATION_S:
                    self.wdt.feed()
                    self.last_egress_throttle = self.pid_egress(self.check_actual_pressure())
                    self.fans.update(0, self.last_egress_throttle)
                    time.sleep(0.1)
                
                self.pid_egress.set_auto_mode(False)
                self.defrost_active = False
                print("DEFROST COMPLETE: Returning to normal cycle.")
                continue

            # 2. Normal State-machine logic
            self.main_perc = self.get_effective_power()
            
            period = self.period_time_calc()
            
            # Ingress Phase
            cp_ingress = self.check_cp_ingress()
            if self.config['leader_or_follower'] == "follower":
                cp_ingress += self.sync_pressure_offset
            
            self.pid_ingress.setpoint = cp_ingress
            self.pid_ingress.set_auto_mode(True, last_output=self.last_ingress_throttle)
            while (self.ticks_ms_synced() % period) < period / 2:
                self.handle_sync() # Keep sync active during loops
                self.last_ingress_throttle = self.pid_ingress(self.check_actual_pressure())
                self.wdt.feed()
                time.sleep(0.1)
            self.pid_ingress.set_auto_mode(False)

            # Egress Phase
            cp_egress = self.check_cp_egress()
            if self.config['leader_or_follower'] == "follower":
                cp_egress += self.sync_pressure_offset
            
            self.pid_egress.setpoint = cp_egress
            self.pid_egress.set_auto_mode(True, last_output=self.last_egress_throttle)
            while (self.ticks_ms_synced() % period) >= period / 2:
                self.handle_sync() # Keep sync active during loops
                self.last_egress_throttle = self.pid_egress(self.check_actual_pressure())
                self.wdt.feed()
                time.sleep(0.1)
            self.pid_egress.set_auto_mode(False)
