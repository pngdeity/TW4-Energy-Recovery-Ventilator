from machine import Pin
from time import sleep

blue = Pin(16, Pin.OUT)
red = Pin(17, Pin.OUT)
green = Pin(21, Pin.OUT)
while True:
    red.on()
    sleep(0.3)
    red.off()
    green.on()
    sleep(0.3)
    green.off()
    blue.on()
    sleep(0.3)
    blue.off()
    sleep(0.3)