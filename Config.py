import configparser

class Config:
	parser=configparser.ConfigParser()
	parser.read("mpdScheduler.ini")
	host=parser.get("general","host",fallback="localhost")
	port=parser.getint("general","port",fallback=6600)

	alarmDefaultSong=parser.get("alarm","defaultSong",fallback=None)
	alarmFadeTime=parser.getint("alarm","fadeTime",fallback=60)

	sleepFadeTime=parser.getint("sleep","fadeTime",fallback=60)
