import sys
import os
lib_path = os.path.abspath('w1thermsensor')
sys.path.append(lib_path)

from w1thermsensor import W1ThermSensor

sensor = W1ThermSensor()
while True:
   print  sensor.get_temperature();
