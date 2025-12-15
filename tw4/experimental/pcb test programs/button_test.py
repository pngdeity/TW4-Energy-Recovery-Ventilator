from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)
button = Pin(20, Pin.IN, Pin.PULL_DOWN)
while True:
    if button.value() == 1:
        led.toggle()
    sleep(0.3)
    