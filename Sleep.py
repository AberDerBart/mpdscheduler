#!/usr/bin/python

import mpd
from Fade import fade
from Scheduler import Job

def gotoSleep(interface,fadeTime):
	"""fades for [fadeTime] seconds, then stops playback and restores the volume"""
	client=mpd.MPDClient()
	client.connect(interface.host,interface.port)

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

	client.close()
	
class SleepTimer(Job):
	"""a job fading out the music and stopping playback at given time"""
	def __init__(self,time,interface,fadeTime=60):
		"""creates the job, does nothing special"""
		super().__init__(time,gotoSleep,(interface,fadeTime),"Go to sleep")
