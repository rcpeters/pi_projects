# https://learn.adafruit.com/debugging-with-the-raspberry-pi-webide/debug-a-blinking-led
# See schematic raspberry_pi_Red_LED_Cobbler.png

import RPi.GPIO as GPIO 
from time import sleep
 
LED_PIN = 25
 
print "Setting up GPIO"
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
 
def enable_led(should_enable):
	if should_enable:
		GPIO.output(LED_PIN, False)
	else:
		GPIO.output(LED_PIN, True)

try: 
	while True:
		enable_led(True)
		print "LED is ON"
		sleep(2)
		enable_led(False)
		print "LED is OFF"
		sleep(2)
except KeyboardInterrupt:
	GPIO.cleanup()
	print "Cleanup GPIO"
