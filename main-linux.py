import subprocess
from threading import Thread

def ore():
	subprocess.call("python3 writer.py ore.json evemarketerbot-49efda14a63b.json", shell=True)

def minerals():
	subprocess.call("python3 writer.py minerals.json evemarketerbotminerals-3fabc2f71956.json", shell=True)


if __name__ == "__main__":
	try:
		Thread(target = ore).start()
		Thread(target = minerals).start()
	except KeyboardInterrupt:
		print("[INFO]: Exiting")
		