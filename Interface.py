#!/usr/bin/python

import threading
import mpd
import Parser

class Interface:
	def __init__(self,mpdHost,mpdPort):		
		self.host=mpdHost
		self.port=mpdPort
		# connect
		self.client=mpd.MPDClient()
		print("Connecting to "+mpdHost+" on Port "+str(mpdPort))
		self.client.connect(mpdHost,mpdPort)

		# subscribe channels
		self.client.subscribe("sleep")
		self.client.subscribe("alarm")
		self.client.subscribe("schedule")
		self.client.subscribe("cancel")

		# subscribe answering channels (to avoid errors)
		self.client.subscribe("scheduled")

		# initialize parser
		self.parser=Parser.Parser(self)

		self.quit=False
	def stop(self):
		self.quit=True
		self.parser.stop()
		self.client.close()
	def start(self):
		while(not self.quit):
			self.client.idle()
			messages=self.client.readmessages()

			for msg in messages:
				self.parser.parse(msg)
