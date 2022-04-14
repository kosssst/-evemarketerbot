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
		ws = sheet.worksheet(str(sheetname))
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
					buy_volume = data[0]["buy"]["volume"]
					buy_wavg = data[0]["buy"]["wavg"]
					buy_avg = data[0]["buy"]["avg"]
					buy_min = data[0]["buy"]["min"]
					buy_max = data[0]["buy"]["max"]
					buy_variance = data[0]["buy"]["variance"]
					buy_stddev = data[0]["buy"]["stdDev"]
					buy_median = data[0]["buy"]["median"]
					buy_five = data[0]["buy"]["fivePercent"]
					sell_volume = data[0]["sell"]["volume"]
					sell_wavg = data[0]["sell"]["wavg"]
					sell_avg = data[0]["sell"]["avg"]
					sell_min = data[0]["sell"]["min"]
					sell_max = data[0]["sell"]["max"]
					sell_variance = data[0]["sell"]["variance"]
					sell_stddev = data[0]["sell"]["stdDev"]
					sell_median = data[0]["sell"]["median"]
					sell_five = data[0]["sell"]["fivePercent"]

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
					ws.update(("A" + line), name)			
					ws.update(("B" + line), buy_volume)
					ws.update(("C" + line), buy_wavg)
					ws.update(("D" + line), buy_avg)
					ws.update(("E" + line), buy_min)
					ws.update(("F" + line), buy_max)
					ws.update(("G" + line), buy_variance)
					ws.update(("H" + line), buy_stddev)
					ws.update(("I" + line), buy_median)
					ws.update(("J" + line), buy_five)
					ws.update(("K" + line), sell_volume)
					ws.update(("L" + line), sell_wavg)
					ws.update(("M" + line), sell_avg)
					ws.update(("N" + line), sell_min)
					ws.update(("O" + line), sell_max)
					ws.update(("P" + line), sell_variance)
					ws.update(("Q" + line), sell_stddev)
					ws.update(("R" + line), sell_median)
					ws.update(("S" + line), sell_five)

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
				
				now = datetime.now()
				current_time = now.strftime("%H:%M:%S")
				print("[" + str(current_time) + "] [INFO/" + str(sheetname) + "]: Updated item " + str(name))
				logger.info("[" + str(current_time) + "] [INFO/" + str(sheetname) + "]: Updated item " + str(name))

				time.sleep(config.delay)

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


	