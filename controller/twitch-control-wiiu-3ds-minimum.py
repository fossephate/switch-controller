#!/usr/bin/env python3
import argparse
import serial
from time import sleep
import pynput
import pyautogui
import win32api
import win32con
import random

# for time delaying the input:
from threading import Timer
import time
from math import sqrt

# switch controller:
# from switchcontroller.switchcontroller import *

# twitch:
from twitchbot.twitchbot import *

# for time delaying the input:
from threading import Timer

# for socketio
from socketIO_client_nexus import SocketIO, LoggingNamespace, BaseNamespace
import logging
# logging.getLogger("socketIO-client").setLevel(logging.DEBUG)
logging.basicConfig()

from threading import Thread

# OpenCV / image utils:
# import imutils
# import cv2
# from PIL import Image

# windows stuff
import ctypes
from ctypes import *
import win32api
import win32con
import win32com
import win32com.client
import win32gui
import win32ui

# to get json info
import urllib.request, json

# to exit:
import sys
import os

# numpy
import numpy as np

# save info
import pickle


screenWidth, screenHeight = pyautogui.size()
x = screenWidth/2
y = screenHeight/2
prevX = 0
prevY = 0

controller = SwitchController()
controller.connect("COM3")

controller2 = None
try:
	controller2 = SwitchController()
	controller2.connect("COM4")
except:
	print("second controller error")
	pass

twitchBot = TwitchBot()
twitchBot.connect(HOST, PASS2, PORT, CHAN, NICK2)

def delayed_reset(delay=0.1):
	Timer(delay, controller.reset).start()


def accurateSleep(duration):
	s = time.clock()
	e = time.clock()
	diffInMilliSeconds = 0

	while (diffInMilliSeconds < duration):
		e = time.clock()
		diffInMilliSeconds = (e - s)*1000

def send_and_reset(duration=0.1, reset=1):
	controller.getOutput()
	controller.send(controller.output)
	sleep(duration)
	if(reset):
		controller.reset()
		controller.getOutput()
		controller.send(controller.output)

# todo: combine
def send_and_reset2(duration=0.1, reset=1):
	controller2.getOutput()
	controller2.send(controller2.output)
	sleep(duration)
	if(reset):
		controller2.reset()
		controller2.getOutput()
		controller2.send(controller2.output)

def round_down(num, divisor):
    return num - (num%divisor)



gotoList = ["mk8", "human", "shovel", "octopath", "explosion", "jackbox4", "jackbox3", "fallout", "skyrim", "splatoon2", "celeste", "smo", "rocketleague", "pokemonquest", "wizard", "sonic", "arms", "kirby", "fortnite", "torquel", "botw"]
validCommands = ["!pluslist", "!unban", "!ban", "!removeplus", "!giveplus", "!goto human", "!goto shovel", "!goto octopath", "!goto explosion", "!goto jackbox4", "!goto jackbox3", "!commands", "!goto fallout", "!goto fortnite", "!goto torquel", "!goto pokemonquest", "!restart", "!restart1", "!restart2", "!restart3", "!restartscript", "!restartserver", "!help", "votenay", "voteyea", "!goto wizard", "!goto cave", "!goto sonic", "!goto skyrim", "!goto rocketleague", "!goto arms", "!goto celeste", "!goto mk8", "!goto splatoon2", "!goto isaac", "!goto mario", "!goto botw", "!goto kirby", "!goto smo", "!goto", "lockon", "hhsprint", "hsprint", "sprint", "!controls", "!goto", "home", "lstick", "rstick", "spin", "swim", "back flip", "ground pound", "groundpound", "gp", "bf", "cap bounce", "sdive", "sdive2", "hdive", "hdive2", "hdive3", "dive", "dive2", "dive3", "roll", "roll2", "backflip", "backflip2", "sssu", "sssd", "sssl", "sssr", "sb", "suu", "", "up", "down", "left", "right", "u", "d", "l", "r", "hup", "hdown", "hleft", "hright", "hhup", "hhdown", "hhleft", "hhright", "hu", "hd", "hl", "hr", "su", "sd", "sl", "sr", "sup", "sdown", "sleft", "sright", "ssu", "ssd", "ssl", "ssr", "ssup", "ssdown", "ssleft", "ssright", "look up", "look down", "look left", "look right", "lu", "ld", "ll", "lr", "hlu", "hld", "hll", "hlr", "slu", "sld", "sll", "slr", "dup", "ddown", "dleft", "dright", "du", "dd", "dl", "dr", "a", "b", "x", "y", "ha", "hb", "hx", "hy", "hhb", "hhhb", "l", "zl", "r", "zr", "plus", "minus", "long jump", "long jump2", "long jump3", "jump forward", "jump forward2", "jump back", "jump back2", "dive", "dive2"]
pluslist = ["vjezuz", "zellie", "generzon344", "joeakuaku", "azeywub", "alua2020", "grady404", "valentinvanelslandedev", "beanjr_yt", "yanchan230", "silvermagpi", "hoopa21", "opprose", "mrruidiazisthebestinsmo", "stravos96", "harmjan387", "twitchplaysconsoles", "fosseisanerd"]
modlist = ["stravos96", "yanchan230", "silvermagpi", "twitchplaysconsoles", "fosseisanerd", "tpnsbot"]
adminlist = ["silvermagpi", "twitchplaysconsoles", "fosseisanerd"]
banlist = []
voted = []

commandQueue = []
nextCommands = []
#lockon = False
oldArgs = "800000000000000 128 128 128 128"


# load plus list:
if(os.path.exists("pluslist.pkl")):
    with open("pluslist.pkl", "rb") as f:
        pluslist = pickle.load(f)[0]



class Client(object):

	def __init__(self):
		self.socketio = SocketIO("http://twitchplaysnintendoswitch.com:8110")

		self.socketio.on("controllerState", self.on_controller_state)
		self.socketio.on("turnTimeLeft", self.on_turn_time_left)
		self.socketio.emit("join", "wiiu3dscontroller")

		self.currentPlayer = ""


		self.receive_events_thread = Thread(target=self._receive_events_thread)
		self.receive_events_thread.daemon = True
		self.receive_events_thread.start()

		self.start = time.clock()
		self.end = time.clock()
		
		self.botstart = time.clock()
		self.botend = time.clock()

		self.controllerStart = time.clock()
		self.controllerEnd = time.clock()

		self.lockon = False

		self.yeaVotes = 0
		self.nayVotes = 0
		self.voting = False

		self.laglessEnabled = True
		self.currentGame = "none"

		self.oldArgs2 = "800000000000000 128 128 128 128"

		

	def on_event(self, event):
		#print(event)
		pass

	def on_controller_command(*args):
		nextCommands.append(args)

	def on_turn_time_left(*args):
		try:
			 client.currentPlayer = args[1]["username"]
		except:
			pass

	def on_controller_state(*args, controllerNum=1):

		if(not client.laglessEnabled):
			return

		state = args[1]

		print("controller state:", state)

		client.oldArgs2 = state

		cont = controller

		cont.reset()

		inputs = state.split()

		btns = inputs[0]
		LX = inputs[1]
		LY = inputs[2]
		RX = inputs[3]
		RY = inputs[4]

		cont.dpad = int(btns[0])
		if (btns[1] == "1"):
			cont.lstick = 1;
		if (btns[2] == "1"):
			cont.l = 1;
		if (btns[3] == "1"):
			cont.zl = 1;
		if (btns[4] == "1"):
			cont.minus = 1;
		if (btns[5] == "1"):
			try:
				if (client.currentPlayer.lower() in modlist):
					cont.capture = 1
				else:
					cont.capture = 0
			except:
				cont.capture = 0
		if (btns[6] == "1"):
			cont.a = 1;
		if (btns[7] == "1"):
			cont.b = 1;
		if (btns[8] == "1"):
			cont.x = 1;
		if (btns[9] == "1"):
			cont.y = 1;
		if (btns[10] == "1"):
			cont.rstick = 1;
		if (btns[11] == "1"):
			cont.r = 1;
		if (btns[12] == "1"):
			cont.zr = 1;
		if (btns[13] == "1"):
			try:
				if (client.currentPlayer.lower() in pluslist):
					cont.plus = 1
				else:
					cont.plus = 0
			except:
				cont.plus = 0
		if (btns[14] == "1"):
			try:
				if (client.currentPlayer.lower() in modlist):
					cont.home = 1
				else:
					cont.home = 0
			except:
				cont.home = 0

		try:
			cont.LX = int(LX)
			cont.LY = 255-int(LY)
			cont.RX = int(RX)
			cont.RY = 255-int(RY)
		except:
			pass

		duration = 0.01
		reset = 0
		send_and_reset(duration, reset)

	# player 2:
	def on_controller_state2(*args):
		client.on_controller_state(args[1], 2)

	def handleChat(self, username, message):
		print(message)

		# handle chat messages here

	def decreaseQueue(self):

		# handle queue from handlechat


	def loop(self):

		# control switch here:

		# every 5 minutes:
		self.botend = time.clock()
		diffInMilliSeconds = (self.botend - self.botstart)*1000
		if(diffInMilliSeconds > 1000*60*5):
			self.socketio.emit("join", "wiiu3dscontroller")
			self.botstart = time.clock()
			# msg = "Join the discord server! https://discord.gg/ARTbddH\
			# hate the stream delay? go here! https://twitchplaysnintendoswitch.com"
			# twitchBot.chat(msg)

		# every 6 seconds, probably doesn't need to do this so often:
		self.controllerEnd = time.clock()
		diffInMilliSeconds2 = (self.controllerEnd - self.controllerStart)*1000
		if(diffInMilliSeconds2 > 6000):
			self.socketio.emit("join", "wiiu3dscontroller")
			self.controllerStart = time.clock()


		response = twitchBot.stayConnected()
		if(response != "none"):
			# prevent crash
			try:
				username = re.search(r"\w+", response).group(0) # return the entire match
				username = username.lower()
				message = CHAT_MSG.sub("", response)
				message = message.strip()
				message = message.lower()
				self.handleChat(username, message)
			except:
				pass

		self.decreaseQueue()

	def _receive_events_thread(self):
		self.socketio.wait()

client = Client()
while True:
	client.loop()
	sleep(0.0001)
