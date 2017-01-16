import configparser

class Config:
	parser=configparser.ConfigParser()
	parser.read("mpdScheduler.ini")
	host=parser.get("general","host")
	port=parser.getint("general","port")
