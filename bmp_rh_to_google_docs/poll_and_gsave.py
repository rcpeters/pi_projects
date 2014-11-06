from ConfigParser import SafeConfigParser
import gspread

parser = SafeConfigParser()
parser.read('config.ini')

gc = gspread.login(parser.get('gspread', 'gmail_email'), parser.get('gspread', 'gmail_password'))




