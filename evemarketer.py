import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
# import json

itemid = 18

marketurl = "https://api.evemarketer.com/ec/marketstat/json"

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'evemarketerbot-49efda14a63b.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

param = dict(typeid=itemid)

resp = requests.get(marketurl, param)
data = resp.json()

avg_price = data[0]["sell"]["avg"]

sheet = client.open('evemarketer')

ws = sheet.worksheet("Ore")

ws.update('B2', avg_price)