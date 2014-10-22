# Builds off of ../led_blink, adds two colors and toggles them 
# via a switch and includes threading
# switch tutorial http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/

import RPi.GPIO as GPIO
import threading 
from time import sleep
 
G_LED_PIN = 22
R_LED_PIN = 23
SWITCH_PIN = 25
 
print "Setting up GPIO"
GPIO.setmode(GPIO.BCM)
GPIO.setup(G_LED_PIN, GPIO.OUT)
GPIO.setup(R_LED_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

blinkRunning = True;
stopped = True

def press(channel):
	global stopped
	if stopped:
		stopped = False
	else:
		stopped = True

def release(channel):
	hasFalled = true;
 
def enable_led(should_enable):
	global stopped
	if should_enable:
		GPIO.output(G_LED_PIN + stopped, True)
	else:
		GPIO.output(R_LED_PIN, False)
		GPIO.output(G_LED_PIN, False)

def blink():
	global blinkRunning
	print "startng"
	while blinkRunning:
		enable_led(True)
                sleep(1)
               	enable_led(False)
               	sleep(0.5)
	print "Cleanup GPIO"
        GPIO.cleanup() 

GPIO.add_event_detect(SWITCH_PIN, GPIO.RISING, callback=press, bouncetime=250)

t = threading.Thread(target=blink)
t.start()

try:
	while t.is_alive():
		t.join(10)
except (KeyboardInterrupt, SystemExit):
        blinkRunning = False

print "exiting"
