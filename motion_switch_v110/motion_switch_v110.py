# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-13-power-control/hardware

import time 
import RPi.GPIO as io 
io.setmode(io.BCM) 
 
pir_pin = 24 
power_pin = 23
 
io.setup(pir_pin, io.IN) 
io.setup(power_pin, io.OUT)
io.output(power_pin, False)
 
while True:
    if io.input(pir_pin):
        print("POWER ON")
        io.output(power_pin, True)
        time.sleep(20);
        print("POWER OFF")
        io.output(power_pin, False)
        time.sleep(5)
    time.sleep(1)
