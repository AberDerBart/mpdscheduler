#!/bin/python
from Sleep import gotoSleep
import Scheduler
import time
import mpd

class Parser:
	def __init__(self,mpdHost,mpdPort):
		self.scheduler=Scheduler.Scheduler()
		self.client=mpd.MPDClient()
		self.client.connect(mpdHost,mpdPort)
	def parse(self,msg):
		"""parses and executes the command given in msg"""
		command=msg["channel"]
		args=msg["message"]

		# activate sleep timer
		if(command=="sleep"):
			if(args.isdigit()):
				sleepTime=int(args)*60+time.time()
				self.scheduler.schedule(sleepTime,Scheduler.Job(gotoSleep,(self.client,60),"Go to sleep"))
			else:
				print("Error parsing argument "+args)
