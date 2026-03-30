# Licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
# Portions of this code may be based on the original OpenERV work by Anthony Douglas.

from machine import PWM, Pin
import time

class Fan:
    """Represents a single fan controlled via PWM."""
    
    def __init__(self, pin_num, freq=70000):
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(freq)
        self.old_throttle = 0.0

    def set_speed(self, spd_prcnt):
        """Set fan speed (0-100%)."""
        spd_prcnt = max(0, min(100, spd_prcnt))
        if spd_prcnt < 7.5:
            spd_prcnt = 0
            
        duty = int(spd_prcnt * 65530 / 100)
        self.pwm.duty_u16(duty)
        return spd_prcnt

class FanManager:
    """Manages pairs of fans and handles coordinated ramping."""
    
    def __init__(self, ingress_pins=(0, 2), egress_pins=(1, 3)):
        self.fans = {
            'i0': Fan(ingress_pins[0], 70000),
            'i1': Fan(ingress_pins[1], 20000),
            'e0': Fan(egress_pins[0], 70000),
            'e1': Fan(egress_pins[1], 20000)
        }
        self.start_clock_ms = 0

    def calc_persistence_time(self, old_throttle, destination_throttle):
        diff = old_throttle - destination_throttle
        if old_throttle >= 80:
            return diff * 0.0002 * 1000
        elif 40 < old_throttle < 80:
            return diff * 0.02 * 1000
        else:
            return diff * 0.13 * 1000

    def _physthrottle_asfuncoftime(self, fan_key, destination_throttle):
        fan = self.fans[fan_key]
        time_elapsed = time.ticks_diff(time.ticks_ms(), self.start_clock_ms)
        
        if destination_throttle == 0:
            persistence_time = self.calc_persistence_time(fan.old_throttle, destination_throttle)
            if time_elapsed < persistence_time:
                return fan.old_throttle
            
            # Simplified ramp down logic
            ramp_down_time_ms = fan.old_throttle * 0.03 * 1000 + 1
            fraction_done = (time_elapsed - persistence_time) / ramp_down_time_ms
            if fraction_done >= 1:
                return 0
            return fan.old_throttle * (1 - fraction_done)
        else:
            return destination_throttle

    def _update_fan_object(self, fan_key, destination_throttle):
        fan = self.fans[fan_key]
        adjusted_throttle = self._physthrottle_asfuncoftime(fan_key, destination_throttle)
        fan.set_speed(adjusted_throttle)
        
        if adjusted_throttle == destination_throttle:
            fan.old_throttle = destination_throttle
            return True
        return False

    def speed_to_action(self, speed, pair_index):
        i_key = f'i{pair_index}'
        e_key = f'e{pair_index}'
        
        if speed < 0:
            r1 = self._update_fan_object(i_key, 0)
            r2 = self._update_fan_object(e_key, abs(speed))
        else:
            r1 = self._update_fan_object(i_key, speed)
            r2 = self._update_fan_object(e_key, 0)
        return r1, r2

    def update(self, spd1, spd2):
        """Update both fan pairs towards their target speeds."""
        self.start_clock_ms = time.ticks_ms()
        r1, r2, r3, r4 = False, False, False, False
        while not (r1 and r2 and r3 and r4):
            r1, r2 = self.speed_to_action(spd1, 0)
            r3, r4 = self.speed_to_action(spd2, 1)
