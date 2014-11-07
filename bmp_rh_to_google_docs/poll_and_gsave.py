from ConfigParser import SafeConfigParser
import gspread
import bmp # Note this initialize the barometric sensor. See bmp.py
import datetime
import Adafruit_DHT
import time

BMP = 'BMP'
RH = 'RH'

def getIsoTime():
	return datetime.datetime.utcnow().isoformat() + 'Z'

def init_sheet(sprd, name):
	if name == BMP:
		col_names = ['Time ms', 'P Pa', 'P inH2O', 'P inHg', 'Sea-P Pa', 'Sea-P inH2O', 'Sea-P inHg', 'Alt M', 'Alt FT', 'Temp C', 'Temp F']
	elif name == RH:
		col_names = ['Time ms', 'RH ', 'Temp C', 'Temp F']
	wrk = None
	try:
		wrk = sprd.worksheet(name)
	except gspread.exceptions.WorksheetNotFound:
		print 'adding worksheet ' +  name 
		sprd.add_worksheet(name,1,len(col_names))
	if wrk is None:
		wrk = sprd.worksheet(name)
	if wrk.cell(1, 1).value is None:
		header_cells = wrk.range('A1:'+ wrk.get_addr_int(1, len(col_names)))
		for i in range(len(col_names)):
			header_cells[i].value = col_names[i]
		wrk.update_cells(header_cells)
	return wrk

def add_bmp_row(r):
	global bmpWrk
	nextRow = bmpWrk.row_count + 1
	vals = [getIsoTime()
		, r.pressure
		, '=B{0} * 0.0040147421331128'.format(nextRow)
		, '=B{0} * 0.0002953337'.format(nextRow)
		, r.sealevel_pressure
		, '=E{0} * 0.0040147421331128'.format(nextRow)
		, '=E{0} * 0.0002953337'.format(nextRow)
		, r.altitude
		, '=G{0} * 3.28084'.format(nextRow)
		, r.temp
		, '=J{0} * 1.8 + 32'.format(nextRow)]
	bmpWrk.append_row(vals)

def add_rh_row(r):
	global rhWrk
	rh, temp = r
	nextRow = rhWrk.row_count + 1
	vals = [getIsoTime(), rh, temp, '=C{0} * 1.8 + 32'.format(nextRow)]
	rhWrk.append_row(vals)

def log_error_sleep(ex):
	print "An exception {0} occured. Arguments:\n{1!r}".format(type(ex).__name__, ex.args)
	print "retrying in 60 seconds"
	time.sleep(60)

# do to a tone of http errors with google
# keep trying until all steps complete
print 'starting settup'
setup_success = False
while setup_success == False:
	try:
		# parse the config.ini
		parser = SafeConfigParser()
		parser.read('config.ini')

		# login to google and get the spreadsheet
		print 'login'
		gc = gspread.login(parser.get('gspread', 'gmail_email'), parser.get('gspread', 'gmail_password'))
		sprd = gc.open(parser.get('gspread', 'gSpreadSheetName'))

		# initalize the barometric spreedsheet tab
		print 'init sheets'
		bmpWrk = init_sheet(sprd, BMP)
		rhWrk = init_sheet(sprd, RH)
		
		print 'clean Sheet1'
		# Clear out Sheet1 if still there
		try:
			sheet1 = sprd.worksheet('Sheet1')
			if sheet1 is not None:
				sprd.del_worksheet(sheet1)
		except gspread.exceptions.WorksheetNotFound:
			pass
		setup_success = True
	except Exception as ex:
		log_error_sleep(ex)

time.sleep(30)

while True:
	bmp_success = False
	while bmp_success == False:
		try:
			print 'bmp read'
			r = bmp.getReading()
			add_bmp_row(r)
			print 'result {0}, {1}, {2}, {3}'.format(r.temp, r.altitude, r.pressure, r.sealevel_pressure) 
			bmp_success = True
			print
		except Exception as ex:
			log_error_sleep(ex)
	
	rh_success = False
	while rh_success == False:
		try:
			print 'rh read'
			t = Adafruit_DHT.read_retry(22, 22)
			add_rh_row(t)
			print 'result {0}, {1}'.format(t[0], t[1])
			rh_success = True
			print
		except Exception as ex:
			log_error_sleep(ex)

	print 'Sleeping for 10 mintues'
	time.sleep(60 * 10)
	print
	
