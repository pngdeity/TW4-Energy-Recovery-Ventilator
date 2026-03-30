# Licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
# Portions of this code may be based on the original OpenERV work by Anthony Douglas.

import network
import time
from machine import WLAN

class NetworkManager:
    """Manages WiFi connection and Access Point mode."""
    
    def __init__(self, wdt=None, led=None):
        self.wdt = wdt
        self.led = led
        self.wlan = WLAN(network.STA_IF)
        self.ap = WLAN(network.AP_IF)

    def _feed_wdt(self):
        if self.wdt:
            self.wdt.feed()

    def _toggle_led(self):
        if self.led:
            self.led.toggle()

    def connect_wifi(self, ssid, password, ip_follower=None, leader_or_follower="leader"):
        """Connect to a WiFi network as a station."""
        if ssid == "use_ap":
            return self.make_ap(), "none"

        self._feed_wdt()
        if self.wlan.active():
            self.wlan.active(False)
        self.wlan.active(True)
        
        self._feed_wdt()
        self.wlan.connect(ssid, password)
        
        x = 0
        while not self.wlan.isconnected():
            print(f"Waiting for connection to {ssid}... {x}")
            time.sleep(1)
            x += 1
            self._toggle_led()
            self._feed_wdt()
            if x > 20:
                print(f"Connection timeout after {x} seconds")
                return None, None
                
        ip = self.wlan.ifconfig()
        print(f"Connected to {ssid}, IP: {ip[0]}")
        
        if self.led:
            self.led.off()

        if leader_or_follower == "follower" and ip_follower:
            print(f"Assigning follower IP: {ip_follower}")
            new_ifconfig = (ip_follower, '255.255.255.0') + ip[2:4]
            self.wlan.ifconfig(new_ifconfig)
            ip = self.wlan.ifconfig()
            print(f"Updated follower IP: {ip[0]}")
            
        return ip[0], self.wlan

    def make_ap(self, ssid="OpenERV_AP", password="osrocks8882888"):
        """Start an Access Point."""
        print(f"Starting AP: {ssid}")
        self.ap.config(essid=ssid, password=password)
        self.ap.active(True)
        while not self.ap.active():
            pass
        ip = self.ap.ifconfig()[0]
        print(f"AP started, IP: {ip}")
        return ip
