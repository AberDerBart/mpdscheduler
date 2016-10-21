#!/bin/python
from Sleep import gotoSleep
from Scheduler import Job
import time

def parse(client, scheduler, msg):
	"""parses and executes the command given in msg"""
	command=msg["channel"]
	args=msg["message"]

	# activate sleep timer
	if(command=="sleep"):
		if(args.isdigit()):
			sleepTime=int(args)*60+time.time()
			scheduler.schedule(sleepTime,Job(gotoSleep,(client,60),"Go to sleep"))
		else:
			print("Error parsing argument "+args)
