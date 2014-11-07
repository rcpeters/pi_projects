from ConfigParser import SafeConfigParser
import gspread
import bmp # Note this initialize the barometric sensor. See bmp.py
import datetime
import Adafruit_DHT

BMP = 'BMP'


def init_sheet(sprd, name):
	try:
		wrk = sprd.worksheet(name)
	except gspread.exceptions.WorksheetNotFound:
		print 'adding worksheet ' +  name 
		if name == BMP:
			col_names = ['Time ms', 'P Pa', 'P inH2O', 'P inHg', 'Sea-P Pa', 'Sea-P inH2O', 'Sea-P inHg', 'Alt M', 'Alt FT', 'Temp C', 'Temp F']
		sprd.add_worksheet(name,1,len(col_names))
		wrk = sprd.worksheet(name)
		bmp_header_cells = wrk.range('A1:'+ wrk.get_addr_int(1, len(col_names)))
		for i in range(len(col_names)):
			bmp_header_cells[i].value = col_names[i]
			wrk.update_cells(bmp_header_cells)
	return wrk

def init_col_name(sht, name, col):
	if sht.cell(1,col).value != name:
		sht.update_cell(1,col,name)

def add_bmp_row(r):
	global bmpWrk
	nextRow = bmpWrk.row_count + 1
	bmpWrk.append_row([datetime.datetime.utcnow().isoformat() + 'Z'
		, r.pressure
		, '=B{0} * 0.0040147421331128'.format(nextRow)
		, '=B{0} * 0.0002953337'.format(nextRow)
		, r.sealevel_pressure
		, '=E{0} * 0.0040147421331128'.format(nextRow)
		, '=E{0} * 0.0002953337'.format(nextRow)
		, r.altitude
		, '=G{0} * 3.28084'.format(nextRow)
		, r.temp
		, '=J{0} * 1.8 + 32'.format(nextRow)])

# parse the config.ini
parser = SafeConfigParser()
parser.read('config.ini')

# login to google and get the spreadsheet
gc = gspread.login(parser.get('gspread', 'gmail_email'), parser.get('gspread', 'gmail_password'))
sprd = gc.open(parser.get('gspread', 'gSpreadSheetName'))

# initalize the barometric spreedsheet tab
bmpWrk = init_sheet(sprd, BMP)

add_bmp_row(bmp.getReading())
print Adafruit_DHT.read_retry(22, 22)

print bmp.getReading()
