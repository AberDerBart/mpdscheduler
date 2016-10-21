#!/bin/python
from Sleep import gotoSleep
import Scheduler
import time
import parse

class Parser:
	def __init__(self,mpdHost,mpdPort):
		self.scheduler=Scheduler.Scheduler(mpdHost,mpdPort)
	def exit(self):
		self.scheduler.stop()
	def parse(self,msg):
		"""parses and executes the command given in msg"""
		command=msg["channel"]
		args=msg["message"]

		# activate sleep timer
		if(command=="sleep"):
			if(args.isdigit()):
				sleepTime=int(args)*60+time.time()
				self.scheduler.schedule(sleepTime,Scheduler.Job(gotoSleep,(60,),"Go to sleep"))
			else:
				print("Error parsing argument "+args)
		# add an alarm
		if(command=="alarm"):

			print("alarm not available yet")

	def parseTime(self,string):
		"""parses a timestamp given in [string] in the format hh:mm[:ss] or dd/MM/YYYY[ hh:mm[:ss]] or +m and returns it as datetime.datetime or None on failure"""
		# check, if a time string was given
		result=parse.parse("{:tt}",string)

		if(result):
			# TODO implement returning the next datetime with result[0] as time (either today or tomorrow)
		
		# check, if a date string was given
		result=parse.parse("{:tg}",string)

		if(result):
			return result[0]

		# no timestamp could be detected,
		return None
