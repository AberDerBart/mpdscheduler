#!/usr/bin/python

import mpd
import threading
import time

def sleepTimer(client, timeout, fadeTime=30):
	"""waits for [timeout] seconds, then fades out for [fadeTime] seconds (asynchronously)"""
	def fade(client,fadeTime):
		"""fades for [fadeTime] seconds (synchronously)"""
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

		#reset the sleep timer
		sleepTimer.timer=None

	#check for existing sleep timer and stop it if necessary
	if(sleepTimer.timer!=None):
		print("SleepTimer: There is a sleepTimer active, stopping it.")
		sleepTimer.timer.cancel()

	#create a new timer to start fading after [fadeTime] seconds
	sleepTimer.timer=threading.Timer(timeout,fade,(client,fadeTime))
	print("SleepTimer: Waiting for "+str(timeout)+"s")
	sleepTimer.timer.start()

# no thread is running in the beginning
sleepTimer.timer=None
		
