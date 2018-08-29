
# time
from threading import Timer
import time
from time import sleep

# switch controller:
from switchcontroller.switchcontroller import *

# twitch:
from twitchbot.twitchbot import *

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

# vjoy
import pyvjoy


screenWidth, screenHeight = pyautogui.size()
x = screenWidth/2
y = screenHeight/2
prevX = 0
prevY = 0

controller1 = SwitchController()
# controller1.connect("COM3")

vjoy = pyvjoy.VJoyDevice(1)

# controller2 = None
# try:
# 	controller2 = SwitchController()
# 	controller2.connect("COM4")
# except:
# 	print("second controller error")
# 	pass

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

def send_and_reset(duration=0.1, reset=1, cNum=0):

	if(cNum == 0):
		controller = controller1
	elif(cNum == 1):
		controller = controller2
	elif(cNum == 2):
		controller = controller3
	elif(cNum == 3):
		controller = controller4

	sleep(duration)

	if (controller.dpad == 7):
		controller.up = 1
		controller.left = 1
	elif (controller.dpad == 1):
		controller.up = 1
		controller.right = 1
	elif (controller.dpad == 5):
		controller.down = 1
		controller.left = 1
	elif (controller.dpad == 3):
		controller.down = 1
		controller.right = 1
	elif (controller.dpad == 0):
		controller.up = 1
	elif (controller.dpad == 4):
		controller.down = 1
	elif (controller.dpad == 6):
		controller.left = 1
	elif (controller.dpad == 2):
		controller.right = 1

	vjoy.reset()
	btns = []
	btnNum = 0

	if (controller.up):
		btns.append(1)
	if (controller.down):
		btns.append(2)
	if (controller.left):
		btns.append(3)
	if (controller.right):
		btns.append(4)
	if (controller.lstick):
		btns.append(5)
	if (controller.l):
		btns.append(6)
	if (controller.zl):
		btns.append(7)
	if (controller.minus):
		btns.append(8)
	if (controller.capture):
		btns.append(9)
	if (controller.a):
		btns.append(10)
	if (controller.b):
		btns.append(11)
	if (controller.x):
		btns.append(12)
	if (controller.y):
		btns.append(13)
	if (controller.rstick):
		btns.append(14)
	if (controller.r):
		btns.append(15)
	if (controller.zr):
		btns.append(16)
	if (controller.plus):
		btns.append(17)
	if (controller.home):
		btns.append(18)

	for n in btns:
		btnNum += 2**n

	vjoy.data.lButtons = btnNum
	vjoy.data.wAxisX = controller.LX * 128
	vjoy.data.wAxisY = controller.LY * 128
	vjoy.data.wAxisXRot = controller.RX * 128
	vjoy.data.wAxisYRot = controller.RY * 128

	vjoy.update()

def round_down(num, divisor):
    return num - (num%divisor)



gotoList = ["mk8", "human", "shovel", "octopath", "explosion", "jackbox4", "jackbox3", "fallout", "skyrim", "splatoon2", "celeste", "smo", "rocketleague", "pokemonquest", "wizard", "sonic", "arms", "kirby", "fortnite", "torquel", "botw"]
validCommands = ["!pluslist", "!unban", "!ban", "!removeplus", "!giveplus", "!goto human", "!goto shovel", "!goto octopath", "!goto explosion", "!goto jackbox4", "!goto jackbox3", "!commands", "!goto fallout", "!goto fortnite", "!goto torquel", "!goto pokemonquest", "!restart", "!restart1", "!restart2", "!restart3", "!restartscript", "!restartserver", "!help", "votenay", "voteyea", "!goto wizard", "!goto cave", "!goto sonic", "!goto skyrim", "!goto rocketleague", "!goto arms", "!goto celeste", "!goto mk8", "!goto splatoon2", "!goto isaac", "!goto mario", "!goto botw", "!goto kirby", "!goto smo", "!goto", "lockon", "hhsprint", "hsprint", "sprint", "!controls", "!goto", "home", "lstick", "rstick", "spin", "swim", "back flip", "ground pound", "groundpound", "gp", "bf", "cap bounce", "sdive", "sdive2", "hdive", "hdive2", "hdive3", "dive", "dive2", "dive3", "roll", "roll2", "backflip", "backflip2", "sssu", "sssd", "sssl", "sssr", "sb", "suu", "", "up", "down", "left", "right", "u", "d", "l", "r", "hup", "hdown", "hleft", "hright", "hhup", "hhdown", "hhleft", "hhright", "hu", "hd", "hl", "hr", "su", "sd", "sl", "sr", "sup", "sdown", "sleft", "sright", "ssu", "ssd", "ssl", "ssr", "ssup", "ssdown", "ssleft", "ssright", "look up", "look down", "look left", "look right", "lu", "ld", "ll", "lr", "hlu", "hld", "hll", "hlr", "slu", "sld", "sll", "slr", "dup", "ddown", "dleft", "dright", "du", "dd", "dl", "dr", "a", "b", "x", "y", "ha", "hb", "hx", "hy", "hhb", "hhhb", "l", "zl", "r", "zr", "plus", "minus", "long jump", "long jump2", "long jump3", "jump forward", "jump forward2", "jump back", "jump back2", "dive", "dive2"]
pluslist = []
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

		# self.socketio.on("controllerState1", self.on_controller_state1)
		# self.socketio.on("controllerState2", self.on_controller_state2)
		# self.socketio.on("controllerState3", self.on_controller_state3)
		self.socketio.on("controllerState5", self.on_controller_state1)
		self.socketio.on("turnTimesLeft", self.on_turn_times_left)
		self.socketio.emit("joinSecure", {"room": "controller", "password": ROOM_SECRET})

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
		self.gotoUsed = False
		self.gotoLeft = False
		self.chatEnabled = True
		self.controllerEnabled = True
		self.currentPlayers = []
		self.currentGame = "none"


		self.oldArgs2 = "800000000000000 128 128 128 128"


	def _receive_events_thread(self):
		self.socketio.wait()		

	def on_event(self, event):
		#print(event)
		pass

	def on_controller_command(*args):
		nextCommands.append(args)

	def on_turn_times_left(*args):
		try:
			client.currentPlayers = args[1]["usernames"]
		except:
			pass

	def on_controller_state(*args):

		if(not client.controllerEnabled):
			return

		state = args[1]
		cNum = args[2]

		print("controller state" + str(cNum) + ":", state)

		client.oldArgs2 = state

		controller = None

		if(cNum == 0):
			controller = controller1
		else:
			return

		controller.reset()

		inputs = state.split()
		cPlayer = ""
		try:
			cPlayer = client.currentPlayers[cNum]
		except:
			pass

		btns = inputs[0]
		LX = inputs[1]
		LY = inputs[2]
		RX = inputs[3]
		RY = inputs[4]

		controller.dpad = int(btns[0])
		if (btns[1] == "1"):
			controller.lstick = 1;
		if (btns[2] == "1"):
			controller.l = 1;
		if (btns[3] == "1"):
			controller.zl = 1;
		if (btns[4] == "1"):
			controller.minus = 1;
		if (btns[5] == "1"):
			try:
				if (cPlayer.lower() in modlist):
					controller.capture = 1
				else:
					controller.capture = 0
			except:
				controller.capture = 0
		if (btns[6] == "1"):
			controller.a = 1;
		if (btns[7] == "1"):
			controller.b = 1;
		if (btns[8] == "1"):
			controller.x = 1;
		if (btns[9] == "1"):
			controller.y = 1;
		if (btns[10] == "1"):
			controller.rstick = 1;
		if (btns[11] == "1"):
			controller.r = 1;
		if (btns[12] == "1"):
			controller.zr = 1;
		if (btns[13] == "1"):
			try:
				if (cPlayer.lower() in pluslist):
					controller.plus = 1
				else:
					controller.plus = 0
			except:
				controller.plus = 0
		if (btns[14] == "1"):
			try:
				if (cPlayer.lower() in modlist):
					controller.home = 1
				else:
					controller.home = 0
			except:
				controller.home = 0

		try:
			controller.LX = int(LX)
			controller.LY = 255-int(LY)
			controller.RX = int(RX)
			controller.RY = 255-int(RY)
		except:
			pass

		duration = 0.001
		reset = 0
		send_and_reset(duration, reset, cNum)


	# player 1:
	def on_controller_state1(*args):
		client.on_controller_state(args[1], 0)


	def handleChat(self, username, message):
		print(message)

		# handle chat messages here

	def decreaseQueue(self):

		# handle queue from handlechat
		pass


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