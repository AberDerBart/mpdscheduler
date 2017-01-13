#!/usr/bin/python

import threading
import mpd
import Parser

class Interface:
	def __init__(self,mpdHost,mpdPort):		
		"""set the parameters and creates the client"""
		self.host=mpdHost
		self.port=mpdPort
		self.client=mpd.MPDClient()
		self.connect()

		# initialize parser
		self.parser=Parser.Parser(self)

		self.quit=False
	def connect(self):
		"""establishes a connection to mpd host [host] on port [port]"""
		print("Connecting to "+self.host+" on Port "+str(self.port))
		self.client.connect(self.host,self.port)

		# subscribe channels
		self.client.subscribe("scheduler")

		# subscribe answering channels (to avoid errors)
		self.client.subscribe("scheduled")
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
