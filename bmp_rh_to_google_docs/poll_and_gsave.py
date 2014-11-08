import Adafruit_DHT
import bmp # Note this initialize the barometric sensor. See bmp.py
from ConfigParser import SafeConfigParser
import datetime
import gspread
import logging
import time



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
	col_names = ['Time ms', 'P Pa', 'P inH2O', 'P inHg'
		, 'Sea-P Pa', 'Sea-P inH2O', 'Sea-P inHg'
		, 'Alt M', 'Alt FT', 'Temp C(BMP)', 'Temp F(BMP)'
                , 'RH ', 'Temp C(RH)', 'Temp F(RH)']
	wrk = None
	try:
		wrk = sprd.worksheet(g_worksheet)
	except gspread.exceptions.WorksheetNotFound:
		print 'adding worksheet ' +  name 
		sprd.add_worksheet(g_worksheet,1,len(col_names))
	if wrk is None:
		wrk = sprd.worksheet(g_worksheet)
	print wrk.cell(1, 1).value
	if wrk.cell(1, 1).value == '':
		header_cells = wrk.range('A1:'+ wrk.get_addr_int(1, len(col_names)))
		for i in range(len(col_names)):
			header_cells[i].value = col_names[i]
		wrk.update_cells(header_cells)
	return wrk

def add_bmp_rh_row(wrk, r_bmp, r_rh):
	nextRow = wrk.row_count + 1
	vals = [ getIsoTime() #A
		, r_bmp.pressure #B
		, '=B{0} * 0.0040147421331128'.format(nextRow) #C
		, '=B{0} * 0.0002953337'.format(nextRow) #D
		, r_bmp.sealevel_pressure #E
		, '=E{0} * 0.0040147421331128'.format(nextRow) #F
		, '=E{0} * 0.0002953337'.format(nextRow) #G
		, r_bmp.altitude #H
		, '=H{0} * 3.28084'.format(nextRow) #I
		, r_bmp.temp #J
		, '=J{0} * 1.8 + 32'.format(nextRow) #K
		, r_rh[0] #L
		, r_rh[1] #M
		, '=M{0} * 1.8 + 32'.format(nextRow)] #N
	wrk.append_row(vals)

def add_rh_row(r):
	global rhWrk
	rh, temp = r
	nextRow = rhWrk.row_count + 1
	vals = [getIsoTime(), rh, temp, '=C{0} * 1.8 + 32'.format(nextRow)]
	rhWrk.append_row(vals)

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
		init_sheet(g_worksheet)
		setup_success = True
	except Exception as ex:
		log_error_sleep(ex)


while True:
	success = False
	while success == False:
		try:
			sprd = login_get_spread()
			wrk = sprd.worksheet(g_worksheet)
			print 'bmp read'
			r_bmp = bmp.getReading()
			print 'bmp result {0}, {1}, {2}, {3}'.format(r_bmp.temp, r_bmp.altitude, r_bmp.pressure, r_bmp.sealevel_pressure) 
			r_rh = Adafruit_DHT.read_retry(22, 22)
			print 'rh result {0}, {1}'.format(r_rh[0], r_rh[1]) 
			add_bmp_rh_row(wrk, r_bmp, r_rh)
			print 'saved worked'
			success = True
			print
		except Exception as ex:
			log_error_sleep(ex)
	
	print 'Sleeping for {0} seconds'.format(sleep)
	time.sleep(sleep)
	print
	
