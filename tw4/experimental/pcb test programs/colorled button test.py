from machine import Pin
from time import sleep

blue = Pin(16, Pin.OUT)
red = Pin(17, Pin.OUT)
green = Pin(21, Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_DOWN)
val=1
while True:
    if button.value() == 1:
        val = val + 1
    if val > 3:
        val = 1
    if val == 1:
        blue.on()
        red.off()
        green.off()
    if val == 2:
        blue.off()
        red.on()
        green.off()
    if val == 3:
        blue.off()
        red.off()
        green.on()
    sleep(0.3)