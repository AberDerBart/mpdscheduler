import time
import threading
import mpd
import datetime
import json

class Job:
	"""Representation of a scheduled job"""

	def __init__(self,function,arguments,description):
		self.func=function
		self.args=arguments
		self.desc=description

	def execute(self):
		"""processes the job"""
		self.func(*self.args)
	def __lt__(self,other):
		return False;

class Scheduler:
	"""Schedules jobs in a queue"""

	def __init__(self):
		self.timer=None
		self.queue=[]
		self.queueLock=threading.Lock()

	def schedule(self,startTime,job):
		"""Attaches [job] to the job queue"""
		print("Scheduling \""+job.desc+"\".")

		self.queueLock.acquire()

		self.queue.append((startTime,job))
		# sort queue by [startTime]
		self.queue.sort()

		# if the new job is first in the queue the timer has to be reset
		if(startTime == self.queue[0][0]):
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
			timeDiff=self.queue[0][0]-datetime.datetime.now()
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
			del self.queue[index]

		self.queueLock.release()


	def processQueue(self):
		"""processes all due jobs in the queue"""
		# get the next job and execution time

		self.queueLock.acquire()

		if(self.queue):
			nextTime,nextJob=self.queue[0]
		else:
			nextTime=None

		# process jobs until there is no due job left
		while(nextTime and nextTime<=datetime.datetime.now()):
			# remove the job from the queue
			self.queue.pop(0)

			self.queueLock.release()

			nextJob.execute()

			self.queueLock.acquire()

			# get the next job and execution time
			if(self.queue):
				nextTime,nextJob=self.queue[0]
			else:
				nextTime=None
			
		# reactivate the timer
		self.initTimer()

		self.queueLock.release()
	
	def __str__(self):
		retn="Scheduler queue:"
		for index,item in enumerate(self.queue):
			schedTime=item[0]
			job=item[1]

			timestr=str(schedTime.date())+" "
			timestr+=str(schedTime.time().hour)+":"+str(schedTime.time().minute)

			retn+="\n"+str(index)+" "+schedTime.strftime("%d/%m/%Y %H:%M")+" "+job.desc

		return retn
	def toJson(self):
		data=[]

		for index,item in enumerate(self.queue):
			schedTime=item[0]
			job=item[1]

			timestr=str(schedTime.date())+" "
			timestr+=str(schedTime.time().hour)+":"+str(schedTime.time().minute)

			data.append({"index":index,"time":timestr,"job":job.desc})

		jsonDict={"type":"scheduleList","data":data}

		return json.dumps(jsonDict,separators=(',',':'))
