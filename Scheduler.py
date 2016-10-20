import time
import threading

class Job:
	"""Representation of a scheduled job"""
	def __init__(self,function,arguments,description):
		self.func=function
		self.args=arguments
		self.desc=description


class Scheduler:
	""""""
	def __init__(self):
		self.timer=None
		self.queue=[]
	def schedule(self,job):
		""""""
		self.queue.append(job)
		
