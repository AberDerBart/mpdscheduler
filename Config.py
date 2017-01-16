import configparser

class Config:
	parser=configparser.ConfigParser()
	parser.read("mpdScheduler.ini")
	host=parser.get("general","host")
	port=parser.getint("general","port")

	alarmDefaultSong=parser.get("alarm","defaultSong")
	alarmFadeTime=parser.getint("alarm","fadeTime")

	sleepFadeTime=parser.getint("sleep","fadeTime")
