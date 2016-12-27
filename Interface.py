#!/usr/bin/python

import threading
import mpd
import Parser

class Interface:
	def __init__(self,mpdHost,mpdPort):		
		"""establishes a connection to mpd host [mpdHost] on port [mpdPort]"""
		self.host=mpdHost
		self.port=mpdPort
		# connect
		self.client=mpd.MPDClient()
		print("Connecting to "+mpdHost+" on Port "+str(mpdPort))
		self.client.connect(mpdHost,mpdPort)

		# subscribe channels
		self.client.subscribe("scheduler")

		# subscribe answering channels (to avoid errors)
		self.client.subscribe("scheduled")

		# initialize parser
		self.parser=Parser.Parser(self)

		self.quit=False
	def stop(self):
		"""stops the main loop and all threads started by its children"""
		self.quit=True
		self.parser.stop()
		self.client.close()
	def start(self):
		"""starts the main loop, awaiting commands on the "scheduler" mpd channel"""
		while(not self.quit):
			self.client.idle()
			messages=self.client.readmessages()

			for msg in messages:
				if(msg["channel"]=="scheduler"):
					self.parser.parse(msg["message"])
