import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json
import schedule
import config
import time
from datetime import datetime
import sys

def update(file, key):
	json_file = open(("json/"+file), 'r')
	json_data = json.load(json_file)

	try:
		creds = ServiceAccountCredentials.from_json_keyfile_name(("keys/"+key),config.scope)
		client = gspread.authorize(creds)
		sheet = client.open(config.tablename)
	except gspread.exceptions.APIError:
		print("[ERROR]: APIError")

	print("[STARTING]: Connected to Google Sheets API")
	time.sleep(2)
	print("[STARTING]: Bot started working")

	try:
		while True:
			for item_type in json_data:
				ws = sheet.worksheet(json_data[item_type]["sheetname"])

				for item in json_data[item_type]["items"]:
					itemid = json_data[item_type]["items"][item]["typeid"]
					line = json_data[item_type]["items"][item]["line"]
					name = json_data[item_type]["items"][item]["name"]
					try:
						resp = 	requests.get(config.marketurl, dict(typeid=itemid))
						# print("[INFO]: Sended request by typeid " + str(itemid) + " (" + str(name) + ")")
					except:
						now = datetime.now()
						current_time = now.strftime("%H:%M:%S")
						print("[" + str(current_time) + "] [ERROR]: Skipped " + str(name))
						continue
					data = resp.json()
					buy_volume = data[0]["buy"]["volume"]
					ws.update(("B" + line), buy_volume)
					buy_wavg = data[0]["buy"]["wavg"]
					ws.update(("C" + line), buy_wavg)
					buy_avg = data[0]["buy"]["avg"]
					ws.update(("D" + line), buy_avg)
					buy_min = data[0]["buy"]["min"]
					ws.update(("E" + line), buy_min)
					buy_max = data[0]["buy"]["max"]
					ws.update(("F" + line), buy_max)
					buy_variance = data[0]["buy"]["variance"]
					ws.update(("G" + line), buy_variance)
					buy_stddev = data[0]["buy"]["stdDev"]
					ws.update(("H" + line), buy_stddev)
					buy_median = data[0]["buy"]["median"]
					ws.update(("I" + line), buy_median)
					buy_five = data[0]["buy"]["fivePercent"]
					ws.update(("J" + line), buy_five)

					sell_volume = data[0]["sell"]["volume"]
					ws.update(("K" + line), sell_volume)
					sell_wavg = data[0]["sell"]["wavg"]
					ws.update(("L" + line), sell_wavg)
					sell_avg = data[0]["sell"]["avg"]
					ws.update(("M" + line), sell_avg)
					sell_min = data[0]["sell"]["min"]
					ws.update(("N" + line), sell_min)
					sell_max = data[0]["sell"]["max"]
					ws.update(("O" + line), sell_max)
					sell_variance = data[0]["sell"]["variance"]
					ws.update(("P" + line), sell_variance)
					sell_stddev = data[0]["sell"]["stdDev"]
					ws.update(("Q" + line), sell_stddev)
					sell_median = data[0]["sell"]["median"]
					ws.update(("R" + line), sell_median)
					sell_five = data[0]["sell"]["fivePercent"]
					ws.update(("S" + line), sell_five)
					
					now = datetime.now()
					current_time = now.strftime("%H:%M:%S")
					print("[" + str(current_time) + "] [INFO]: Updated item " + str(name))

					time.sleep(config.delay)
					
						
	except KeyboardInterrupt:
		pass


if __name__ == "__main__":
	update(sys.argv[1], sys.argv[2])