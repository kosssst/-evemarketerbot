import subprocess
from threading import Thread

def ore():
	subprocess.call("python3 writer.py ore.json evemarketerbot-49efda14a63b.json", creationflags=subprocess.CREATE_NEW_CONSOLE)

def minerals():
	subprocess.call("python3 writer.py minerals.json evemarketerbotminerals-3fabc2f71956.json", creationflags=subprocess.CREATE_NEW_CONSOLE)


if __name__ == "__main__":
	Thread(target = ore).start()
	Thread(target = minerals).start()
		