import configparser
import sys
import os

class Config:
	parser=configparser.ConfigParser()
	parser.read("mpdScheduler.ini")
	host=parser.get("general","host",fallback="localhost")
	port=parser.getint("general","port",fallback=6600)

	alarmDefaultSong=parser.get("alarm","defaultSong",fallback=None)
	alarmFadeTime=parser.getint("alarm","fadeTime",fallback=60)

	sleepFadeTime=parser.getint("sleep","fadeTime",fallback=60)
	
	# check commandline and environment variables for host
	if(len(sys.argv)>=2):
		host=sys.argv[1]
	elif(os.environ.get("MPD_HOST")!=None):
		host=os.environ.get("MPD_HOST")

	# check commandline for port
	if(len(sys.argv)>=3):
		port=sys.argv[2]
