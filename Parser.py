#!/bin/python
from Sleep import SleepTimer
import Scheduler
import time
import parse
import datetime
from Alarm import Alarm
from advParse.advParse import optParse

class Parser:
	def __init__(self):
		"""instantiates Parser"""
		self.scheduler=Scheduler.Scheduler()
	def stop(self):
		"""stops the scheduler"""
		self.scheduler.stop()
	def parse(self,msg):
		"""parses and executes the command given in msg"""
		args=msg.split()
		command=args[0]

		# activate sleep timer
		res=parse.parse("sleep +{offset:d}", msg) or parse.parse("sleep {time:tt}", msg)
		if(res):
			self.scheduler.schedule(SleepTimer(self.getTime(res)))
			return None
		# add an alarm
		res=optParse("alarm +{offset:d}[ {song}]",msg) or optParse("alarm {time:tt}[ {song}]",msg)
		if(res):
			self.scheduler.schedule(Alarm(self.getTime(res),res.named.get("song")))
			return None
		# list scheduled items
		if(parse.parse("list",msg)):
			return str(self.scheduler)
		# list scheduled items in json format
		if(parse.parse("list_json",msg)):
			return self.scheduler.toJson()
		# cancel a job by index
		res=parse.parse("cancel {id:d}",msg)
		if(res):
			return None
		# cancel a job by uuid
		res=parse.parse("cancel_uuid {uuid}",msg)
		if(res):
			self.scheduler.cancelUuid(res['uuid'])
			return None
		# nothing could be parsed
		print("Error parsing string \""+msg+"\"")

	def getTime(self,parseRes):
		"""return the timestamp referred in [parseRes] (either given in an offset in minutes or as dataTime"""
		if("time" in parseRes.named):
			retn=datetime.datetime.combine(datetime.date.today(),parseRes["time"])

			# if the time already passed, increment the day
			if(retn < datetime.datetime.now()):
				retn += datetime.timedelta(days=1)
			return retn
		if("offset" in parseRes.named):
			# calculate the timestamp
			retn=datetime.datetime.now()
			retn+=datetime.timedelta(minutes=parseRes["offset"])
			return retn
		return None
