#!/usr/bin/python

import mpd
from Fade import fade

def gotoSleep(client,fadeTime):
	"""fades for [fadeTime] seconds, then stops playback and restores the volume"""
	startVol=int(client.status()["volume"])
	
	if(startVol>0):
		fade(client,fadeTime,startVol,0)
	else:
		print("Volume not available, skipping fade.")

	print("sleepTimer: Stopping playback")
	client.stop()

	if(startVol>0):
		print("sleepTimer: Restoring volume to "+str(startVol)+"%")
		client.setvol(startVol)
	
