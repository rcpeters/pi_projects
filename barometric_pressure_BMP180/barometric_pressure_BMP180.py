# https://learn.adafruit.com/using-the-bmp085-with-raspberry-pi
#
#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Can enable debug output by uncommenting:
#import logging
#logging.basicConfig(level=logging.DEBUG)

import Adafruit_BMP.BMP085 as BMP085

# Default constructor will pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
#
# For the Beaglebone Black the library will assume bus 1 by default, which is
# exposed with SCL = P9_19 and SDA = P9_20.
sensor = BMP085.BMP085()

# Optionally you can override the bus number:
#sensor = BMP085.BMP085(busnum=2)

# You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER, 
# BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is STANDARD.
#sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

temp = sensor.read_temperature()
tempF = sensor.read_temperature() * 1.8 + 32
pressure = sensor.read_pressure()
pressureInH2O = sensor.read_pressure() * 0.0040147421331128 
pressureInHg = sensor.read_pressure() * 0.0002953337
seaPressure = sensor.read_sealevel_pressure()
seaPressureInH20 = sensor.read_sealevel_pressure() * 0.0040147421331128
seaPressureInHg = sensor.read_sealevel_pressure() * 0.0002953337
altitude = sensor.read_altitude()

print 'Temp = {0:0.2f}C'.format(temp, tempF)  + ', {0:0.2f}F'.format(tempF)
print 'Pressure = {0:0.2f}Pa'.format(pressure) + ', {0:0.2f}inH20'.format(pressureInH2O)+ ', {0:0.2f}inH2g'.format(pressureInHg)
print 'Altitude = {0:0.2f}m'.format(altitude)
print 'Sealevel Pressure = {0:0.2f}Pa'.format(seaPressure) + ', {0:0.2f}inH20'.format(seaPressureInH20) + ', {0:0.2f}inH2g'.format(seaPressureInHg)
