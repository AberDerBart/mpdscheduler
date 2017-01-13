#!/bin/python
from Sleep import SleepTimer
import Scheduler
import time
import parse
import datetime
from Alarm import Alarm

class Parser:
	def __init__(self,interface):
		"""instantiates Parser, using [interface.mpdHost] as reference mpd host and [interface.mpdPort] as reference mpd port"""
		self.scheduler=Scheduler.Scheduler()
		self.interface=interface
	def stop(self):
		"""stops the scheduler"""
		self.scheduler.stop()
	def parse(self,msg):
		"""parses and executes the command given in msg"""
		args=msg.split()
		command=args[0]

		# activate sleep timer
		if(command=="sleep" and len(args)>=2):
			sleepTime=self.parseTime(args[1])

			if(sleepTime):
				self.scheduler.schedule(SleepTimer(sleepTime,self.interface))
				return
		# add an alarm
		if(command=="alarm" and len(args)>=2):
			alarmTime=self.parseTime(args[1])

			if(len(args)>=3):
				song=msg.split(maxsplit=2)[2]
				if(int(self.interface.client.count("File",song)["songs"])==0):
					print("Parser: song not found: "+song)
					song=None
			else:
				song=None

			if(alarmTime):
				self.scheduler.schedule(Alarm(alarmTime,self.interface,song))
				return
		# list scheduled items
		if(parse.parse("list",msg)):
			for line in str(self.scheduler).split("\n"):
				self.interface.client.sendmessage("scheduled",line)
			return
		# list scheduled items in json format
		if(parse.parse("list_json",msg)):
			self.interface.client.sendmessage("scheduled",self.scheduler.toJson())
			return
		# cancel a job by index
		res=parse.parse("cancel {id:d}",msg)
		if(res):
			self.scheduler.cancel(res['id'])
			return
		# cancel a job by uuid
		res=parse.parse("cancel_uuid {uuid}",msg)
		if(res):
			self.scheduler.cancelUuid(res['uuid'])
			return
		# nothing could be parsed
		print("Error parsing string \""+msg+"\"")

	def parseTime(self,string):
		"""parses a timestamp given in [string] in the format hh:mm[:ss] or +m and returns it as datetime.datetime or None on failure"""
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
