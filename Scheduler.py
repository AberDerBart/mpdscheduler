import time
import threading
import mpd

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
			waitTime=self.queue[0][0]-time.time()
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

	def processQueue(self):
		"""processes all due jobs in the queue"""
		# get the next job and execution time

		self.queueLock.acquire()

		if(self.queue):
			nextTime,nextJob=self.queue[0]
		else:
			nextTime=None

		# process jobs until there is no due job left
		while(nextTime and nextTime<=time.time()):
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
