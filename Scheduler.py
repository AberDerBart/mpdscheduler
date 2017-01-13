import time
import threading
import mpd
import datetime
import json
import uuid

class Job:
	"""Representation of a scheduled job"""

	def __init__(self,time,function,arguments,description):
		"""instantiates a Job with the given parameters, using a timestamp-based uuid"""
		self.time=time
		self.func=function
		self.args=arguments
		self.desc=description
		self.uuid=uuid.uuid1()
	def execute(self):
		"""processes the job"""
		self.func(*self.args)
	def __lt__(self,other):
		"""order by time"""
		return self.time < other.time

class Scheduler:
	"""Schedules jobs in a queue"""

	def __init__(self):
		"""instantiates a Scheduler"""
		self.timer=None
		self.queue=[]
		self.queueLock=threading.Lock()

	def schedule(self,job):
		"""Attaches [job] to the job queue"""
		print("Scheduling \""+job.desc+"\" at "+str(job.time)+".")

		self.queueLock.acquire()

		self.queue.append(job)
		# sort queue by [startTime]
		self.queue.sort()

		# if the new job is first in the queue the timer has to be reset
		if(job == self.queue[0]):
			# (re)start the timer
			self.initTimer()

		self.queueLock.release()

	def initTimer(self):
		"""(re)starts the timer for queue processing"""
		# stop running timer
		if(self.timer):
			self.timer.cancel()

		if(self.queue):
			# calculate waiting time
			timeDiff=self.queue[0].time-datetime.datetime.now()
			waitTime=timeDiff.total_seconds()

			# start a new timer
			self.timer=threading.Timer(waitTime,self.processQueue,())
			self.timer.start()
		else:
			# disable the timer
			self.timer=None

	def stop(self):
		"""stops the scheduler"""
		if(self.timer):
			self.timer.cancel()
	def cancel(self,index):
		"""cancels the job at the given index in the queue"""
		self.queueLock.acquire()

		if(len(self.queue)>index):
			print("canceling job #"+str(index)+": "+self.queue[index].desc)
			del self.queue[index]

		self.queueLock.release()

	def cancelUuid(self,uuid):
		"""cancels the job with the given uuid (as string)"""
		# NOTE: the approach to iterate the queue to find the uuid might be considered ugly
		# still, as the queue is expected to be short (as you dont set a lot of sleep timers or alarms),
		# this is more efficient than maintaining a dictionary of jobs by uuid
		delIndex=-1
		
		for index,job in enumerate(self.queue):
			if str(job.uuid)==uuid:
				delIndex=index

		if(delIndex!=-1):
			self.cancel(delIndex)

	def processQueue(self):
		"""processes all due jobs in the queue"""
		# get the next job and execution time

		self.queueLock.acquire()

		if(self.queue):
			nextJob=self.queue[0]
		else:
			nextJob=None

		# process jobs until there is no due job left
		while(nextJob and nextJob.time<=datetime.datetime.now()):
			# remove the job from the queue
			self.queue.pop(0)

			self.queueLock.release()

			nextJob.execute()

			self.queueLock.acquire()

			# get the next job and execution time
			if(self.queue):
				nextJob=self.queue[0]
			else:
				nextJob=None
			
		# reactivate the timer
		self.initTimer()

		self.queueLock.release()
	
	def __str__(self):
		retn="Scheduler queue:"
		for index,job in enumerate(self.queue):
			schedTime=job.time

			timestr=str(schedTime.date())+" "
			timestr+=str(schedTime.time().hour)+":"+str(schedTime.time().minute)

			retn+="\n"+str(index)+" "+schedTime.strftime("%d/%m/%Y %H:%M")+" "+job.desc

		return retn
	def toJson(self):
		"""gives a json representation of the queue"""
		data=[]

		for index,job in enumerate(self.queue):
			schedTime=job.time

			timestr=str(schedTime.date())+" "
			timestr+=str(schedTime.time().hour)+":"+str(schedTime.time().minute)

			data.append({"index":index,"time":timestr,"job":job.desc,"uuid":str(job.uuid)})

		jsonDict={"type":"scheduleList","data":data}

		return json.dumps(jsonDict,separators=(',',':'))
