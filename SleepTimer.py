#!/usr/bin/python

import mpd
import threading
import time

def sleepTimer(client, timeout, fadeTime=30):
	def execTimer(client,timeout,fadeTime):
		print("SleepTimer: Waiting for "+str(timeout)+"s")
		time.sleep(timeout)

		startVol=int(client.status()["volume"])
		sleepInterval=fadeTime/float(startVol)

		print("SleepTimer: Fading for "+str(fadeTime)+"s from volume at "+str(startVol)+"%")

		for vol in range(startVol, 0, -1):
			print("SleepTimer: Setting volume to "+str(vol)+"%")
			client.setvol(vol)
			time.sleep(sleepInterval)
		print("SleepTimer: Stopping playback")
		client.stop()
		print("SleepTimer: Restoring volume to "+str(startVol)+"%")
		client.setvol(startVol)
		print("SleepTimer: finished")

	client = client
	timeout = timeout
	fadeTime = fadeTime

	sleepTimer.thread=threading.Thread(None,execTimer,"sleepTimer",(client,timeout,fadeTime))
	sleepTimer.thread.start()

# no thread is running in the beginning
sleepTimer.thread=None
		
