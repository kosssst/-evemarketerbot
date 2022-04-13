import subprocess
from threading import Thread
import json
import config

keyfile = open(config.key, 'r')
data = json.load(keyfile)



def start(file, key, process):
	subprocess.call("python writer.py " + str(file) + " " + str(key) + " " + str(process), shell=True)

if __name__ == "__main__":
	for i in data:
		Thread(target = start, args = (data[i]["file"], data[i]["key"], data[i]["name"])).start()