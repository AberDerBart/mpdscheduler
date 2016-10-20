#!/usr/bin/python

import mpd
from Fade import fade

def gotoSleep(client,fadeTime):
	"""fades for [fadeTime] seconds, then stops playback and restores the volume"""
	startVol=int(client.status()["volume"])
	
	fade(client,fadeTime,startVol,0)

	print("sleepTimer: Stopping playback")
	client.stop()
	print("sleepTimer: Restoring volume to "+str(startVol)+"%")
	client.setvol(startVol)
	print("sleepTimer: finished")
	
