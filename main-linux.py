import subprocess
from threading import Thread
import json
import config

keyfile = open(config.key, 'r')
data = json.load(keyfile)


def ore():
	subprocess.call("python3 writer.py " + str(data["Ore"]["file"]) + " " + str(data["Ore"]["key"]), shell=True)

def minerals():
	subprocess.call("python3 writer.py " + str(data["Minerals"]["file"]) + " " + str(data["Minerals"]["key"]), shell=True)


if __name__ == "__main__":
	try:
		Thread(target = ore).start()
		Thread(target = minerals).start()
	except KeyboardInterrupt:
		print("[INFO]: Exiting")
		