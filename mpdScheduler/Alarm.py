#!/usr/bin/python

import mpd
from .Fade import fade
from .Scheduler import Job
from .Config import Config

def alarm(fadeTime,song=None):
	"""starts playback and fades in for [fadeTime] seconds"""
	client=mpd.MPDClient()
	client.connect(Config.host,Config.port)

	endVol=int(client.status().get("volume",0))

	index=None
	
	if(song):
		try:
			print("alarm: adding song "+song)
			index=client.addid(song)
		except mpd.CommandError:
			print("alarm: song not found: "+song)

	if(len(client.playlist()) == 0):
		client.add(Config.alarmDefaultSong)

	if(endVol>0):
		client.setvol(0)

		print("alarm: starting playback")
		if(index!=None):
			client.playid(index)
		else:
			client.play()
		
		fade(client,fadeTime,0,endVol)
	else:
		print("Volume not available, skipping fade.")

		print("alarm: starting playback")
		if(index!=None):
			client.playid(index)
		else:
			client.play()

	client.close()

class Alarm(Job):
	"""a job starting the playback and fading in the music at given time"""
	def __init__(self,time,song=None,fadeTime=None):
		"""creates the job, does nothing special"""
		if(not fadeTime):
			fadeTime=Config.alarmFadeTime
		Job.__init__(self,time,alarm,(fadeTime,song),"Alarm")
