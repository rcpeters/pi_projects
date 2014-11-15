import sys
import os
from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()
while True:
   print  sensor.get_temperature();
