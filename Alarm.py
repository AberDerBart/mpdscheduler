#!/usr/bin/python

import mpd
from Fade import fade

def alarm(interface,fadeTime,song=None):
	"""starts playback and fades in for [fadeTime] seconds"""
	client=mpd.MPDClient()
	client.connect(interface.host,interface.port)

	endVol=int(client.status()["volume"])
	
	if(song):
		#add set the playlist to contain only [song]
		client.clear()
		client.add(song)
		#NOTE: actually the "insert" command is wanted here, but it seems not to be implemented in python-mpd2 - maybe a workaround can be found

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
