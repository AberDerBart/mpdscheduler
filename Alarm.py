#!/usr/bin/python

import mpd
from Fade import fade

def wakeUp(interface,fadeTime):
	"""starts playback and fades in for [fadeTime] seconds"""
	client=mpd.MPDClient()
	client.connect(interface.host,interface.port)

	endVol=int(client.status()["volume"])

	if(endVol>0):
		client.setvol(0)

		print("alarm: starting playback")
		client.play()
		
		fade(client,fadeTime,0,endVol)
	else:
		print("Volume not available, skipping fade.")

		print("alarm: starting playback")
		client.play()

	client.close()
