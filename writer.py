import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json
import schedule
import config
import time
from datetime import datetime
from datetime import date
import sys
import logging
import os

def update_item(data_file, key_file, sheetname, logger):
	json_file = open(("json/"+data_file), 'r')
	json_data = json.load(json_file)
	# print(json_data)

	try:
		creds = ServiceAccountCredentials.from_json_keyfile_name(("keys/"+key_file),config.scope)
		client = gspread.authorize(creds)
		sheet = client.open(config.tablename)
		ws = sheet.worksheet("Test")
		# str(sheetname)
	except:
		print("[ERROR]: APIError " + str(sheetname))
		logger.error("Not connected to Google Sheets API")
		return

	print("[STARTING/" + str(sheetname) + "]: Connected to Google Sheets API")
	time.sleep(2)
	print("[STARTING/" + str(sheetname) + "]: Bot started working")
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	logger.info("[" + str(current_time) + "] Bot started working")

	while True:
		for item in json_data[str(sheetname)]:	
			for i in item:
				name = item[i]["name"]
				itemid = item[i]["typeid"]
				line = item[i]["line"]
				try:
					resp = 	requests.get(config.marketurl, dict(typeid=itemid))
					data = resp.json()
					buy_volume = str(data[0]["buy"]["volume"])
					buy_wavg = str(data[0]["buy"]["wavg"])
					buy_avg = str(data[0]["buy"]["avg"])
					buy_min = str(data[0]["buy"]["min"])
					buy_max = str(data[0]["buy"]["max"])
					buy_variance = str(data[0]["buy"]["variance"])
					buy_stddev = str(data[0]["buy"]["stdDev"])
					buy_median = str(data[0]["buy"]["median"])
					buy_five = str(data[0]["buy"]["fivePercent"])
					sell_volume = str(data[0]["sell"]["volume"])
					sell_wavg = str(data[0]["sell"]["wavg"])
					sell_avg = str(data[0]["sell"]["avg"])
					sell_min = str(data[0]["sell"]["min"])
					sell_max = str(data[0]["sell"]["max"])
					sell_variance = str(data[0]["sell"]["variance"])
					sell_stddev = str(data[0]["sell"]["stdDev"])
					sell_median = str(data[0]["sell"]["median"])
					sell_five = str(data[0]["sell"]["fivePercent"])

				except KeyboardInterrupt:
					now = datetime.now()
					current_time = now.strftime("%H:%M:%S")
					logger.info("[" + str(current_time) + "] Bot stoped")
					sys.exit()
					
				except:
					now = datetime.now()
					current_time = now.strftime("%H:%M:%S")
					print("[" + str(current_time) + "] [ERROR/" + str(sheetname) + "]: Skipped " + str(name) + " (Evemarketer API)")
					logger.error("[" + str(current_time) + "] [ERROR/" + str(sheetname) + "]: Skipped " + str(name) + " (Evemarketer API)")
					time.sleep(config.error_delay)
					continue
				try:
					cell_list = ws.range(("A" + str(line) + ":S" + str(line)))
					cell_values = [name, buy_volume, buy_wavg, buy_avg, buy_min, buy_max, buy_variance, buy_stddev, buy_median, buy_five, sell_volume, sell_wavg, sell_avg, sell_min, sell_max, sell_variance, sell_stddev, sell_median, sell_five]
					for i, val in enumerate(cell_values):
						cell_list[i].value = val
					ws.update_cells(cell_list)
				except KeyboardInterrupt:
					now = datetime.now()
					current_time = now.strftime("%H:%M:%S")
					logger.info("[" + str(current_time) + "] Bot stoped")
					sys.exit()

				except:
					now = datetime.now()
					current_time = now.strftime("%H:%M:%S")
					print("[" + str(current_time) + "] [ERROR/" + str(sheetname) + "]: Skipped " + str(name) + " (Google Sheets API)")
					logger.error("[" + str(current_time) + "] [ERROR/" + str(sheetname) + "]: Skipped " + str(name) + " (Google Sheets API)")
					time.sleep(config.error_delay)
					continue
				
				try:
					now = datetime.now()
					current_time = now.strftime("%H:%M:%S")
					print("[" + str(current_time) + "] [INFO/" + str(sheetname) + "]: Updated item " + str(name))
					logger.info("[" + str(current_time) + "] [INFO/" + str(sheetname) + "]: Updated item " + str(name))

					time.sleep(config.delay)
				except KeyboardInterrupt:
					now = datetime.now()
					current_time = now.strftime("%H:%M:%S")
					logger.info("[" + str(current_time) + "] Bot stoped")
					sys.exit()

if __name__ == "__main__":
	now = datetime.now()
	today = date.today()
	current_time = now.strftime("%H_%M_%S")
	current_day = today.strftime("%d_%m_%y")

	if(not(os.path.exists("logs/"+str(sys.argv[3])))):
		os.makedirs("logs/"+str(sys.argv[3]))

	log_file_name = ("logs/" + str(sys.argv[3]) + "/" + str(sys.argv[4]) + "_" + str(current_day) + "_" + str(current_time) + ".log")
	logging.basicConfig(filename=log_file_name,  encoding='utf-8', level=logging.DEBUG)
	update_item(sys.argv[1], sys.argv[2], sys.argv[3], logging)


	