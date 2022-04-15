import subprocess
from threading import Thread
import json
import config
import os
import time
import sys

keyfile = open(config.key, 'r')
data = json.load(keyfile)

if(not(os.path.exists("logs"))):
	os.makedirs("logs")

files = []
kfiles = []
sn = []

def start(file, key, sheetname, mode):
	subprocess.call("python writer.py " + str(file) + " " + str(key) + " " + str(sheetname) + " " + str(mode), shell=True)

def choice():
	global files
	global kfiles
	global sn
	print("You need to select which sheets you want to update (0 - No; 1 - Yes)")
	for i in data:
		while True:
			print(str(data[i]["sheetname"]) + ": ")
			num = int(input())
			if(num == 1):
				files.append(str(data[i]["data_file"]))
				kfiles.append(str(data[i]["key_file"]))
				sn.append(str(data[i]["sheetname"]))
				break
			elif(num == 0):
				break
			else:
				print("Invalid number!")



if __name__ == "__main__":
	modes = []
	k = 1
	for i in sys.argv:
		if(k == 1):
			k = k + 1
			continue
		else:
			modes.append(i)
			k = k + 1

	if "-c" in modes:
		choice()
		if "DEBUG" in modes:
			for i in range(len(sn)):
				Thread(target = start, args = (files[i], kfiles[i], sn[i], "DEBUG")).start()
				time.sleep(1)
		else:
			for i in range(len(sn)):
				Thread(target = start, args = (files[i], kfiles[i], sn[i], "INFO")).start()
				time.sleep(1)
	elif "-a" in modes:
		if "DEBUG" in modes:
			for i in data:
				Thread(target = start, args = (data[i]["data_file"], data[i]["key_file"], data[i]["sheetname"], "DEBUG")).start()
				time.sleep(1)
		else:
			for i in data:
				Thread(target = start, args = (data[i]["data_file"], data[i]["key_file"], data[i]["sheetname"], "INFO")).start()
				time.sleep(1)				
	else:
		print("Unavaliable mode")
		sys.exit()