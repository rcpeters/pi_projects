import Adafruit_BMP.BMP085 as BMP085

bmpSensor = BMP085.BMP085()

class Reading(object):
	def __init__(self, temp, altitude, pressure, sealevel_pressure):
		self.temp = temp
		self.altitude = altitude
		self.pressure = pressure
		self.sealevel_pressure = sealevel_pressure

def getReading():
 return Reading(bmpSensor.read_temperature(), 
		 bmpSensor.read_altitude(), 
		 bmpSensor.read_pressure(), 
		 bmpSensor.read_sealevel_pressure())


