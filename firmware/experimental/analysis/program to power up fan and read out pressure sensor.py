import sdp810_125
from combifan import combi_fan_spd
from machine import PWM, Pin, ADC
from simple_pid import PID
from time import sleep, ticks_ms, ticks_diff
combi_fan_spd(-90,0)
while True:
    print(sdp810_125.get_reading())
    sleep(0.1)