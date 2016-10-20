#!/bin/python
import Sleep

def parse(client, scheduler, msg):
	"""parses and executes the command given in msg"""
	params=msg.split(" ")
	command=params[0]

	# activate sleep timer
	if(command=="sleep"):
		if(len(params)==2):
