#!/usr/bin/python
import signal
import os
import sys
import Interface

def signalHandler(signum, frame):
	print("Caught some kill signal, closing...")
	print("Closing")
	sys.exit()

signal.signal(signal.SIGABRT,signalHandler)
signal.signal(signal.SIGQUIT,signalHandler)
signal.signal(signal.SIGINT,signalHandler)
signal.signal(signal.SIGTERM,signalHandler)

# default values for host and port
mpdHost="localhost"
mpdPort=6600

# check commandline and environment variables for host
if(len(sys.argv)>=2):
	mpdHost=sys.argv[1]
elif(os.environ.get("MPD_HOST")!=None):
	mpdHost=os.environ.get("MPD_HOST")

# check commandline for port
if(len(sys.argv)>=3):
	mpdPort=sys.argv[2]

# setup the interface
interface=Interface.Interface(mpdHost,mpdPort)

interface.start()
