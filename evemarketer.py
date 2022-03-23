import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json
import schedule
import config
import time

creds = ServiceAccountCredentials.from_json_keyfile_name(config.key,config.scope)
client = gspread.authorize(creds)
sheet = client.open('evemarketer')

print("[INFO]: Connected to Google Sheets API")

def update_prices():
	try:
		json_file = open(config.file, 'r')
	except:
		print("[ERROR]: Invalid file")
		return

	try:
		json_data = json.load(json_file)
	except:
		print("[ERROR]: Not json file")
		return

	for item_type in json_data:
		ws = sheet.worksheet(json_data[item_type]["sheetname"])

		for item in json_data[item_type]["items"]:
			itemid = json_data[item_type]["items"][item]["typeid"]
			cell = json_data[item_type]["items"][item]["cell"]
			resp = 	requests.get(config.marketurl, dict(typeid=itemid))
			print("[INFO]: Sended request by typeid " + str(itemid))
			data = resp.json()
			avg_price = data[0]["sell"]["avg"]
			ws.update(cell, avg_price)
			print("[INFO]: Updated cell " + cell + " by value " + str(avg_price))




schedule.every(1).minutes.do(update_prices)

while True:
    schedule.run_pending()
    time.sleep(1)