#!/usr/bin/python

import mpd
from Fade import fade

def wakeUp(client,fadeTime):
	"""starts playback and fades in for [fadeTime] seconds"""
	endVol=int(client.status()["volume"])

	print("wakeUp: starting playback")
	client.play()
	
	if(startVol>0):
		fade(client,fadeTime,0,endVol)
	else:
		print("Volume not available, skipping fade.")
