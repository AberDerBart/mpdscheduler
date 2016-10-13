#!/usr/bin/python

import mpd
import threading
import time

def sleepTimer(client, timeout, fadeTime=30):
	def execute(client,fadeTime):
		startVol=int(client.status()["volume"])
		sleepInterval=fadeTime/float(startVol)

		print("sleepTimer: Fading for "+str(fadeTime)+"s from volume at "+str(startVol)+"%")

		for vol in range(startVol, 0, -1):
			print("sleepTimer: Setting volume to "+str(vol)+"%")
			client.setvol(vol)
			time.sleep(sleepInterval)
		print("sleepTimer: Stopping playback")
		client.stop()
		print("sleepTimer: Restoring volume to "+str(startVol)+"%")
		client.setvol(startVol)
		print("sleepTimer: finished")

		sleepTimer.timer=None

	client = client
	timeout = timeout
	fadeTime = fadeTime

	if(sleepTimer.timer!=None):
		print("SleepTimer: There is a sleepTimer active, stopping it.")
		sleepTimer.timer.cancel()

	sleepTimer.timer=threading.Timer(timeout,execute,(client,fadeTime))
	print("SleepTimer: Waiting for "+str(timeout)+"s")
	sleepTimer.timer.start()

# no thread is running in the beginning
sleepTimer.timer=None
		
