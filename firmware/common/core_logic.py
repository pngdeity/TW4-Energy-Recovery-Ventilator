# Licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
# Portions of this code may be based on the original OpenERV work by Anthony Douglas.

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
    def __init__(self, model_config):
        # Default Config
        self.config = {
            "ssid_main_wifi": "use_ap",
            "password_main_wifi": "none",
            "ssid_ap": "OpenERV_AP",
            "ap_password": "osrocks8882888",
            "ip_leader": '192.168.4.1',
            "ip_follower": '192.168.4.2',
            "leader_or_follower": "leader",
            "ADAFRUIT_IO_URL": "io.adafruit.com",
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
        
        # Initialize components
        self.net = NetworkManager(wdt=self.wdt, led=self.led)
        self.i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=100000)
        self.sensor = SDP810(self.i2c)
        self.fans = FanManager()
        
        # PID Setup
        self.pid_ingress = PID(self.config['P_gain'], self.config['I_gain'], 0, setpoint=15)
        self.pid_ingress.output_limits = (-100, 100)
        self.pid_egress = PID(self.config['P_gain'], self.config['I_gain'], 0, setpoint=15)
        self.pid_egress.output_limits = (-100, 100)
        
        self.pot = ADC(Pin(28))
        self.oldpot_val = 0
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

    def load_persistent_vars(self):
        filename = "persistent_vars.json"
        try:
            with open(filename, "r") as f:
                self.config.update(json.load(f))
            print("Loaded persistent_vars.json")
        except Exception:
            print("Using default configuration")

    def save_vars(self):
        try:
            with open("persistent_vars.json", "w") as f:
                json.dump(self.config, f)
        except Exception as e:
            print(f"Error saving vars: {e}")

    def check_pot(self):
        read = self.pot.read_u16()
        if abs(read - self.oldpot_val) > 1600:
            self.oldpot_val = read
        return self.oldpot_val / 655.53

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

    def check_actual_pressure(self):
        correction_ratio = 3.45
        try:
            time.sleep(0.01)
            raw = self.sensor.get_reading()
            if raw is None: raise ValueError("Sensor read failed")
            pressure = correction_ratio * raw
            self.read_fail_strikes = 0
            self.oldpressure = pressure
            return pressure
        except Exception as e:
            print(f"Pressure sensor error: {e}")
            self.read_fail_strikes += 1
            if self.read_fail_strikes > 5:
                time.sleep(10) # Trigger WDT
            return self.oldpressure

    def mqtt_callback(self, topic, msg):
        try:
            self.mqtt_perc = int(msg.decode())
            print(f"MQTT command: {self.mqtt_perc}")
        except Exception as e:
            print(f"MQTT parse error: {e}")

    def connect_mqtt(self):
        if not self.config['ADAFRUIT_USERNAME'] or not self.config['ADAFRUIT_IO_KEY']:
            return 0, None
        mqtt_feedname = bytes('{:s}/feeds/{:s}'.format(self.config['ADAFRUIT_USERNAME'], self.config['ADAFRUIT_IO_FEEDNAME']), 'utf-8')
        self.mqtt_feedname_publish = bytes('{:s}/feeds/{:s}'.format(self.config['ADAFRUIT_USERNAME'], self.config['ADAFRUIT_IO_FEEDNAME_publish']), 'utf-8')
        client_id = bytes('client_' + str(int.from_bytes(os.urandom(3), 'little')), 'utf-8')
        client = MQTTClient(client_id=client_id, server=self.config['ADAFRUIT_IO_URL'], user=self.config['ADAFRUIT_USERNAME'], password=self.config['ADAFRUIT_IO_KEY'], ssl=False)
        client.set_callback(self.mqtt_callback)
        try:
            self.wdt.feed()
            client.connect()
            client.subscribe(mqtt_feedname)
            print("MQTT Connected")
            return 1, client
        except Exception as e:
            print(f"MQTT failed: {e}")
            return 0, None

    def send_synch_udp(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            for _ in range(3):
                reply = f"{time.ticks_ms()},{self.main_perc}"
                sock.sendto(reply.encode(), (self.config['ip_follower'], 12345))
                self.wdt.feed()
                time.sleep(0.1)
        except Exception as e:
            print(f"UDP Send error: {e}")
        finally:
            sock.close()

    def listen_udp_follower(self):
        timer = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), timer) < 100000:
            self.wdt.feed()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                sock.bind(('', 12345))
                sock.settimeout(3)
                data, addr = sock.recvfrom(1024)
                return data.decode()
            except Exception:
                time.sleep(1)
            finally:
                sock.close()
        return None

    def follower_sync(self):
        msg = self.listen_udp_follower()
        if msg:
            parts = msg.split(",")
            self.delta_from_internal_clock = time.ticks_diff(time.ticks_ms(), int(parts[0]))
            self.main_perc = float(parts[1])
            return True
        return False

    def ticks_ms_synced(self):
        if self.config['leader_or_follower'] == "leader":
            return time.ticks_ms()
        return time.ticks_diff(time.ticks_ms(), self.delta_from_internal_clock)

    def period_time_calc(self):
        power = max(0.1, self.main_perc)
        return min(120000, 50000 / (power / 100))

    def run(self):
        print("OpenERV starting...")
        self.load_persistent_vars()
        ip, wlan = self.net.connect_wifi(self.config['ssid_main_wifi'], self.config['password_main_wifi'], ip_follower=self.config.get('ip_follower'), leader_or_follower=self.config['leader_or_follower'])
        
        if self.config['leader_or_follower'] == "leader" and wlan and wlan.isconnected():
            self.mqtt_connected, self.client = self.connect_mqtt()

        while True:
            self.wdt.feed()
            self.fans.update(self.last_ingress_throttle, self.last_egress_throttle)
            
            if self.config['leader_or_follower'] == "leader":
                if self.mqtt_connected:
                    try:
                        self.client.publish(self.mqtt_feedname_publish, str(time.ticks_ms()).encode())
                        self.client.check_msg()
                    except: pass
                self.main_perc = self.check_pot() # Simplified combination logic
                self.send_synch_udp()
            else:
                if not self.follower_sync(): reset()

            period = self.period_time_calc()
            
            # Ingress Phase
            cp_ingress = self.check_cp_ingress() if self.config['leader_or_follower'] == "leader" else self.check_cp_ingress() * -1
            self.pid_ingress.setpoint = cp_ingress
            self.pid_ingress.set_auto_mode(True, last_output=self.last_ingress_throttle)
            while (self.ticks_ms_synced() % period) < period / 2:
                for _ in range(10):
                    self.last_ingress_throttle = self.pid_ingress(self.check_actual_pressure())
                    self.wdt.feed()
                print(f"Ingress SP: {self.pid_ingress.setpoint} P: {self.oldpressure} T: {self.last_ingress_throttle}")
            self.pid_ingress.set_auto_mode(False)

            # Egress Phase
            cp_egress = self.check_cp_egress() if self.config['leader_or_follower'] == "leader" else self.check_cp_egress() * -1
            self.pid_egress.setpoint = cp_egress
            self.pid_egress.set_auto_mode(True, last_output=self.last_egress_throttle)
            while (self.ticks_ms_synced() % period) >= period / 2:
                for _ in range(10):
                    self.last_egress_throttle = self.pid_egress(self.check_actual_pressure())
                    self.wdt.feed()
                print(f"Egress SP: {self.pid_egress.setpoint} P: {self.oldpressure} T: {self.last_egress_throttle}")
            self.pid_egress.set_auto_mode(False)
