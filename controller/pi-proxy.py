#!/usr/bin/python

# time
from threading import Timer
import time
from time import sleep

# switch controller:
# from switchcontroller.switchcontroller import *

# twitch:
# from twitchbot.twitchbot import *

# socketio
from socketIO_client_nexus import SocketIO, LoggingNamespace, BaseNamespace
import logging
# logging.getLogger("socketIO-client").setLevel(logging.DEBUG)
logging.basicConfig()

from threading import Thread

# to get json info
import urllib.request, json

# to exit:
import sys
import os

# numpy
import numpy as np

# save info
import pickle


class Client(object):

	def __init__(self):
		self.socketio = SocketIO("http://twitchplaysnintendoswitch.com:8110")

		self.socketio.on("disableInternet", self.on_disable_internet)
		self.socketio.on("enableInternet", self.on_enable_internet)
		self.socketio.emit("join", "proxy")

		self.receive_events_thread = Thread(target=self._receive_events_thread)
		self.receive_events_thread.daemon = True
		self.receive_events_thread.start()

		self.start = time.clock()
		self.end = time.clock()


	def _receive_events_thread(self):
		self.socketio.wait()		

	def on_event(self, event):
		#print(event)
		pass

	def on_disable_internet(*args):
		print("disabling proxy!")
		sudoPassword = "raspberry"
		command = "service squid stop"
		p = os.system("echo %s|sudo -S %s" % (sudoPassword, command))

	def on_enable_internet(*args):
		print("enabling proxy!")
		sudoPassword = "raspberry"
		command = "service squid restart"
		p = os.system("echo %s|sudo -S %s" % (sudoPassword, command))

	def loop(self):
		self.end = time.clock()
		diffInMilliSeconds = (self.end - self.start)*1000
		if(diffInMilliSeconds > 1000*60*5):
			self.socketio.emit("join", "proxy")
			self.start = time.clock()

print("disabling proxy!")
sudoPassword = "raspberry"
command = "service squid stop"
p = os.system("echo %s|sudo -S %s" % (sudoPassword, command))

client = Client()
while True:
	client.loop()
	sleep(0.0001)