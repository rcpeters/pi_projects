# Raw example of  using RaspiRobot_v2
# Find more info at
# https://github.com/simonmonk/raspirobotboard2

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# pin constants
COIL_A_1 = 17  # power coil a
COIL_A_2 = 04  # direction coil a
COIL_B_1 = 10  # power coil b
COIL_B_2 = 25  # direction coil b 

GPIO.setup(COIL_A_1, GPIO.OUT) 
GPIO.setup(COIL_A_2, GPIO.OUT) 
GPIO.setup(COIL_B_1, GPIO.OUT) 
GPIO.setup(COIL_B_2, GPIO.OUT)

dir = {}
dir['S'] = [False, False, False, False];
dir['F'] = [True, True, True, True];
dir['B'] = [True, False, True, False];
dir['CW'] = [True, True, True, False];
dir['CCW'] = [True, False, True, True];


def set_coils(step):
   GPIO.output(COIL_A_1, step[0])
   GPIO.output(COIL_A_2, step[1])
   GPIO.output(COIL_B_1, step[2])
   GPIO.output(COIL_B_2, step[3])

# go forward 5 seconds
set_coils(dir['F'])
time.sleep(5)

# stop
set_coils(dir['S'])
time.sleep(1)
set_coils(dir['B'])
time.sleep(5)

set_coils(dir['S'])
time.sleep(1)
set_coils(dir['CW'])
time.sleep(5)


set_coils(dir['S'])
time.sleep(1)
set_coils(dir['CCW'])
time.sleep(5)


GPIO.cleanup()
