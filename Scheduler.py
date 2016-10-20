import time
import threading

class Job:
	"""Representation of a scheduled job"""
	def __init__(self,function,arguments,description):
		self.func=function
		self.args=arguments
		self.desc=description
	def execute(self):
		"""processes the job"""
		self.func(*self.args)
class Scheduler:
	"""Schedules jobs in a queue"""
	def __init__(self):
		self.timer=None
		self.queue=[]
	def schedule(self,startTime,job):
		"""Attaches [job] to the job queue"""
		self.queue.append((startTime,job))
		# sort queue by [startTime]
		self.queue.sort()

		# if the new job is first in the queue the timer has to be reset
		if(startTime == self.queue[0][0]):
			# (re)start the timer
			self.initTimer()
	def initTimer(self):
		"""(re)starts the timer for queue processing"""
		# stop running timer
		if(self.timer):
			self.timer.cancel()

		if(self.queue):
			waitTime=self.queue[0][0]-time.time()
			# start a new timer
			self.timer=threading.Timer(waitTime,self.processQueue,())
			self.timer.start()
		else:
			# disable the timer
			self.timer=None
	def processQueue(self):
		"""processes all due jobs in the queue"""
		# get the next job and execution time
		if(self.queue):
			nextTime,nextJob=self.queue[0]
		else:
			nextTime=None

		# process jobs until there is no due job left
		while(nextTime and nextTime<=time.time()):
			# remove the job from the queue
			self.queue.pop(0)

			nextJob.execute()

			# get the next job and execution time
			if(self.queue):
				nextTime,nextJob=self.queue[0]
			else:
				nextTime=None
			
		# reactivate the timer
		self.initTimer()
