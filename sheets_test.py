import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'evemarketerbot-49efda14a63b.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

sheet = client.open('evemarketer').sheet1
python_sheet = sheet.get_all_records()
pp = pprint.PrettyPrinter()
pp.pprint(python_sheet)