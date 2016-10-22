#!/bin/python
from Sleep import gotoSleep
import Scheduler
import time
import parse
import datetime
import Alarm

class Parser:
	def __init__(self,interface):
		self.scheduler=Scheduler.Scheduler()
		self.interface=interface
	def exit(self):
		self.scheduler.stop()
	def parse(self,msg):
		"""parses and executes the command given in msg"""
		command=msg["channel"]
		args=msg["message"]

		# activate sleep timer
		if(command=="sleep"):
			alarmTime=self.parseTime(args)

			if(alarmTime):
				self.scheduler.schedule(alarmTime,Scheduler.Job(gotoSleep,(self.interface,20),"Go to sleep"))
			else:
				print("Error parsing argument "+args)
		# add an alarm
		if(command=="alarm"):
			alarmTime=self.parseTime(args)

			if(alarmTime):
				self.scheduler.schedule(alarmTime,Scheduler.Job(Alarm.wakeUp,(self.interface,60),"Alarm"))
			else:
				print("Error parsing argument "+args)


	def parseTime(self,string):
		"""parses a timestamp given in [string] in the format hh:mm[:ss] or dd/MM/YYYY[ hh:mm[:ss]] or +m and returns it as datetime.datetime or None on failure"""
		# check, if a time string was given
		result=parse.parse("{:tt}",string)

		if(result):
			retn=datetime.datetime.combine(datetime.date.today(),result[0])

			# if the time already passed, increment the day
			if(retn < datetime.datetime.now()):
				retn += datetime.timedelta(days=1)
		
			return retn

		# check, if a date string was given
		result=parse.parse("{:tg}",string)

		if(result):
			return result[0]

		# check if a time offset was given
		result=parse.parse("+{:d}",string)

		if(result):
			# calculate the timestamp
			retn=datetime.datetime.now()
			retn+=datetime.timedelta(minutes=result[0])

			return retn 

		# no timestamp could be detected,
		return None
