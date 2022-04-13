import subprocess
from threading import Thread
import json
import config

keyfile = open(config.key, 'r')
data = json.load(keyfile)



def start(file, key, sheetname):
	subprocess.call("python writer.py " + str(file) + " " + str(key) + " " + str(sheetname), shell=True)

if __name__ == "__main__":
	for i in data:
		Thread(target = start, args = (data[i]["data_file"], data[i]["key_file"], data[i]["sheetname"])).start()