# Licensed under CC BY-NC-SA 4.0
# PhD/Linus/Senior-Architect Refactored Core: Non-Blocking State Machine

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
from provisioning import ProvisioningManager
from ha_discovery import HADiscovery

class SystemState:
    BOOT = 0
    PROVISIONING = 1
    CONNECTING = 2
    RUNNING = 3
    FAULT = 4

class OpenERVCore:
    # Engineering Constants
    THERMAL_LIMIT_C = 50.0
    ADC_FILTER_SHIFT = 3
    HA_UPDATE_INTERVAL_MS = 30000
    SENSOR_READ_INTERVAL_MS = 100

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
            "ha_enabled": False,
            "node_id": "openerv_01"
        }
        self.config.update(model_config)
        
        self.state = SystemState.BOOT
        self.led = Pin("LED", Pin.OUT)
        self.wdt = WDT(timeout=8000)
        
        # Components
        self.net = NetworkManager(wdt=self.wdt, led=self.led)
        self.i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=100000)
        self.sensor = SDP810(self.i2c)
        self.fans = FanManager()
        self.prov = ProvisioningManager(self.net)
        self.ha = None
        
        # PID
        self.pid_ingress = PID(self.config['P_gain'], self.config['I_gain'], 0, setpoint=15)
        self.pid_ingress.output_limits = (-100, 100)
        self.pid_egress = PID(self.config['P_gain'], self.config['I_gain'], 0, setpoint=15)
        self.pid_egress.output_limits = (-100, 100)
        
        # State Variables
        self.pot = ADC(Pin(28))
        self.filtered_pot_raw = 0
        self.main_perc = 0
        self.mqtt_perc = 40
        self.client = None
        self.last_ingress_throttle = 0
        self.last_egress_throttle = 0
        self.current_temp = 0.0
        self.current_pressure = 0.0
        
        self.last_ha_update = 0
        self.last_sensor_read = 0
        self.read_fail_strikes = 0

    def log(self, level, msg):
        print(f"[{level}] {msg}")

    def load_persistent_vars(self):
        try:
            with open("persistent_vars.json", "r") as f:
                self.config.update(json.load(f))
            return True
        except:
            return False

    def update_sensors(self):
        """Non-blocking sensor update."""
        if time.ticks_diff(time.ticks_ms(), self.last_sensor_read) < self.SENSOR_READ_INTERVAL_MS:
            return
        
        try:
            p_raw, t_raw = self.sensor.get_reading()
            if p_raw is not None:
                self.current_pressure = p_raw * 3.45
                self.current_temp = t_raw
                self.read_fail_strikes = 0
            else:
                self.read_fail_strikes += 1
        except:
            self.read_fail_strikes += 1
            
        if self.read_fail_strikes > 20:
            self.state = SystemState.FAULT
            self.log("CRITICAL", "Sensor communication lost.")
            
        self.last_sensor_read = time.ticks_ms()

    def get_conditioned_adc(self):
        raw = self.pot.read_u16()
        self.filtered_pot_raw = (raw + (self.filtered_pot_raw * 7)) >> 3
        return self.filtered_pot_raw / 655.35

    def mqtt_callback(self, topic, msg):
        topic_str = topic.decode()
        try:
            val = int(msg.decode())
            if self.ha and f"{self.ha.node_id}/fan/speed/set" in topic_str:
                self.mqtt_perc = val
            elif self.config['ADAFRUIT_IO_FEEDNAME'].decode() in topic_str:
                self.mqtt_perc = val
        except: pass

    def run(self):
        self.log("INFO", "Initializing System...")
        has_config = self.load_persistent_vars()
        
        if not has_config or self.config['ssid_main_wifi'] in ["use_ap", "none"]:
            self.state = SystemState.PROVISIONING
            ip = self.net.make_ap(ssid="OpenERV_Setup")
            self.prov.start_server(ip)
            return

        self.state = SystemState.CONNECTING
        ip, wlan = self.net.connect_wifi(
            self.config['ssid_main_wifi'], self.config['password_main_wifi'],
            ip_follower=self.config.get('ip_follower'),
            leader_or_follower=self.config.get('leader_or_follower')
        )
        
        if wlan and wlan.isconnected():
            self._setup_mqtt()
            self.state = SystemState.RUNNING
        else:
            self.log("ERROR", "WiFi Connection Failed. Entering Provisioning.")
            self.state = SystemState.PROVISIONING
            return

        while True:
            self.wdt.feed()
            self.update_sensors()
            
            if self.state == SystemState.FAULT:
                self.fans.update(0, 0)
                self.led.on()
                time.sleep(1)
                continue

            # Thermal Safety check
            if self.current_temp > self.THERMAL_LIMIT_C:
                self.state = SystemState.FAULT
                self.log("CRITICAL", f"Thermal limit exceeded: {self.current_temp}C")
                continue

            # Process Logic
            self.main_perc = self.get_conditioned_adc()
            self._handle_ventilation_cycle()
            self._handle_comms()
            
            time.sleep(0.01)

    def _setup_mqtt(self):
        if not self.config['ADAFRUIT_USERNAME'] or not self.config['ADAFRUIT_IO_KEY']:
            return
        
        client_id = bytes('client_' + str(int.from_bytes(os.urandom(3), 'little')), 'utf-8')
        self.client = MQTTClient(client_id=client_id, 
                                 server=self.config['ADAFRUIT_IO_URL'], 
                                 user=self.config['ADAFRUIT_USERNAME'], 
                                 password=self.config['ADAFRUIT_IO_KEY'], 
                                 ssl=False)
        self.client.set_callback(self.mqtt_callback)
        try:
            self.client.connect()
            if self.config.get('ha_enabled'):
                self.ha = HADiscovery(self.client, self.config['node_id'], self.config.get('model_name', 'TW4'))
                self.ha.publish_config()
                self.client.subscribe(f"openerv/{self.ha.node_id}/fan/speed/set")
            
            # Default feed
            user = self.config['ADAFRUIT_USERNAME'].decode()
            feed = self.config['ADAFRUIT_IO_FEEDNAME'].decode()
            self.client.subscribe(f"{user}/feeds/{feed}")
        except:
            self.log("WARN", "MQTT Connection Failed")

    def _handle_ventilation_cycle(self):
        """Non-blocking ventilation phase management."""
        period = min(120000, 50000 / (max(0.1, self.main_perc) / 100))
        now = time.ticks_ms()
        
        # Simplified phase detection without blocking loops
        if (now % period) < period / 2:
            # Ingress Phase
            self.pid_egress.set_auto_mode(False)
            self.pid_ingress.setpoint = self.main_perc * self.config['max_pressure'] / 100
            self.pid_ingress.set_auto_mode(True, last_output=self.last_ingress_throttle)
            self.last_ingress_throttle = self.pid_ingress(self.current_pressure)
            self.fans.update(self.last_ingress_throttle, 0)
        else:
            # Egress Phase
            self.pid_ingress.set_auto_mode(False)
            self.pid_egress.setpoint = -1 * self.main_perc * self.config['max_pressure'] / 100
            self.pid_egress.set_auto_mode(True, last_output=self.last_egress_throttle)
            self.last_egress_throttle = self.pid_egress(self.current_pressure)
            self.fans.update(0, self.last_egress_throttle)

    def _handle_comms(self):
        if self.client:
            self.client.check_msg()
            
        if self.ha and time.ticks_diff(time.ticks_ms(), self.last_ha_update) > self.HA_UPDATE_INTERVAL_MS:
            self.ha.update_state(self.current_pressure, self.current_temp, self.main_perc)
            self.last_ha_update = time.ticks_ms()
