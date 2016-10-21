#!/usr/bin/python

import os
import mpd
import sys
import Parser
import Scheduler
import signal

mpdHost="localhost"
mpdPort=6600

if(len(sys.argv)>=2):
	mpdHost=sys.argv[1]
elif(os.environ.get("MPD_HOST")!=None):
	mpdHost=os.environ.get("MPD_HOST")

if(len(sys.argv)>=3):
	mpdPort=sys.argv[2]

client=mpd.MPDClient()
print("Connecting to "+mpdHost+" on Port "+str(mpdPort))
client.connect(mpdHost,mpdPort)

client.subscribe("sleep")
client.subscribe("alarm")

parser=Parser.Parser(mpdHost,mpdPort)

quit=False

def signalHandler(signum, frame):
	print("Caught some kill signal, closing...")
	parser.exit()
	client.close()
	print("Closing")
	sys.exit()

signal.signal(signal.SIGABRT,signalHandler)
signal.signal(signal.SIGQUIT,signalHandler)
signal.signal(signal.SIGINT,signalHandler)
signal.signal(signal.SIGTERM,signalHandler)


while(not quit):
	client.idle("message")
	messages=client.readmessages()

	for msg in messages:
		parser.parse(msg)
