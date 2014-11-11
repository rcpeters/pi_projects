import Adafruit_DHT
import bmp # Note this initialize the barometric sensor. See bmp.py
from ConfigParser import SafeConfigParser
import datetime
import gspread
import logging
import time

RAW_SENSOR_SHEET_NAME = 'RAW SENSOR DATA'

# parse the config.ini
parser = SafeConfigParser()
parser.read('config.ini')
g_email = parser.get('gspread', 'g_email')
g_password = parser.get('gspread', 'g_password')
g_spreadsheet = parser.get('gspread', 'g_spreadsheet')
g_worksheet = parser.get('gspread', 'g_worksheet')
sleep = eval(parser.get('polling', 'sleep'))
error_sleep = eval(parser.get('polling', 'error_sleep'))

def login_get_spread():
	print 'google spreadsheet login'
	return gspread.login(g_email, g_password).open(g_spreadsheet);

def getIsoTime():
	return datetime.datetime.utcnow().isoformat() + 'Z'

def init_sheet(name):
	sprd = login_get_spread()
	col_names = ['Time ms', 'P Pa'
		, 'Sea-P Pa', 'Alt M', 'Alt FT', 'Temp C(BMP)'
                , 'RH ', 'Temp C(RH)']
	wrk = None
	try:
		wrk = sprd.worksheet(name)
	except gspread.exceptions.WorksheetNotFound:
		print 'adding worksheet ' +  name 
		sprd.add_worksheet(name,1,len(col_names))
	if wrk is None:
		print "sleeping 5 seconds to give google API a chance to catch up....."
		time.sleep(5)
		sprd = login_get_spread()
		wrk = sprd.worksheet(name)
	print wrk.cell(1, 1).value
	if wrk.cell(1, 1).value != col_names[0]:
		header_cells = wrk.range('A1:'+ wrk.get_addr_int(1, len(col_names)))
		for i in range(len(col_names)):
			header_cells[i].value = col_names[i]
		wrk.update_cells(header_cells)
	return wrk

def add_raw_sensor_data(wrk, r_bmp, r_rh):
	rows = wrk.row_count;
	cols = wrk.col_count;
	if wrk.cell(rows, 1).value != '':
		wrk.add_rows(1)
		rows = rows+1
	cells = wrk.range('{0}:{1}'.format(wrk.get_addr_int(rows, 1), wrk.get_addr_int(rows, cols)))
	cells[0].value = getIsoTime() #A
	cells[1].value = r_bmp.pressure #B
	cells[2].value = r_bmp.sealevel_pressure #C
	cells[3].value = r_bmp.altitude #D
	cells[4].value = r_bmp.temp #E
	cells[5].value = r_rh[0] #F
	cells[6].value = r_rh[1] #G
	wrk.update_cells(cells)

def log_error_sleep(ex):
	print "An exception {0} occured. Arguments:\n{1!r}".format(type(ex).__name__, ex.args)
	print "retrying in {0} seconds".format(error_sleep)

	time.sleep(error_sleep)

   
# do to a ton of http errors with google
# keep trying until all steps complete
setup_success = False
while setup_success == False:
	try:
		print 'init sheet'
		init_sheet(RAW_SENSOR_SHEET_NAME)
		setup_success = True
	except Exception as ex:
		log_error_sleep(ex)


while True:
	success = False
	while success == False:
		try:
			print 'read sensors'
			r_bmp = bmp.getReading()
			print 'bmp result {0}, {1}, {2}, {3}'.format(r_bmp.temp, r_bmp.altitude, r_bmp.pressure, r_bmp.sealevel_pressure) 
			r_rh = Adafruit_DHT.read_retry(22, 22)
			print 'rh result {0}, {1}'.format(r_rh[0], r_rh[1]) 
			sensorWrk = login_get_spread().worksheet(RAW_SENSOR_SHEET_NAME)
			add_raw_sensor_data(sensorWrk, r_bmp, r_rh)
			print 'saved worked'
			success = True
			print
		except Exception as ex:
			log_error_sleep(ex)
	
	print 'Sleeping for {0} seconds'.format(sleep)
	time.sleep(sleep)
	print
	
