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
from switchcontroller.switchcontroller import *

# twitch:
from twitchbot.twitchbot import *

# for time delaying the input:
from threading import Timer

# for socketio
from socketIO_client_nexus import SocketIO, LoggingNamespace, BaseNamespace
import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()

from threading import Thread


screenWidth, screenHeight = pyautogui.size()
x = screenWidth/2
y = screenHeight/2
prevX = 0
prevY = 0

controller = SwitchController()
controller.connect("COM6")

twitchBot = TwitchBot()
twitchBot.connect(HOST, PASS2, PORT, CHAN, NICK2)

# start = time.clock()
# botstart = time.clock()

def delayed_reset(delay=0.1):
	Timer(delay, controller.reset).start()


def accurateSleep(duration):
	s = time.clock()
	e = time.clock()

	diffInSeconds = 0
	diffInMilliSeconds = 0

	while (diffInMilliSeconds < duration):
		e = time.clock()
		diffInSeconds = e - s
		diffInMilliSeconds = diffInSeconds*1000

def send_and_reset(duration=0.1, reset=1):
	controller.getOutput()
	controller.send(controller.output)
	sleep(duration)
	if(reset):
		controller.reset()
		controller.getOutput()
		controller.send(controller.output)

validCommands = ["lockon", "hhsprint", "hsprint", "sprint", "!controls", "home", "lstick", "rstick", "spin", "swim", "back flip", "ground pound", "groundpound", "gp", "bf", "cap bounce", "sdive", "sdive2", "hdive", "hdive2", "hdive3", "dive", "dive2", "dive3", "roll", "roll2", "backflip", "backflip2", "sssu", "sssd", "sssl", "sssr", "sb", "suu", "", "up", "down", "left", "right", "u", "d", "l", "r", "hup", "hdown", "hleft", "hright", "hhup", "hhdown", "hhleft", "hhright", "hu", "hd", "hl", "hr", "su", "sd", "sl", "sr", "sup", "sdown", "sleft", "sright", "ssu", "ssd", "ssl", "ssr", "ssup", "ssdown", "ssleft", "ssright", "look up", "look down", "look left", "look right", "lu", "ld", "ll", "lr", "hlu", "hld", "hll", "hlr", "slu", "sld", "sll", "slr", "dup", "ddown", "dleft", "dright", "du", "dd", "dl", "dr", "a", "b", "x", "y", "ha", "hb", "hx", "hy", "hhb", "hhhb", "l", "zl", "r", "zr", "plus", "minus", "long jump", "long jump2", "long jump3", "jump forward", "jump forward2", "jump back", "jump back2", "dive", "dive2"]
whitelist = ["valentinvanelslande", "beanjr_yt", "yanchan230", "silvermagpi", "hoopa21", "opprose", "mrruidiazisthebestinsmo", "stravos96", "harmjan387", "twitchplaysconsoles", "fosseisanerd"]
adminlist = ["twitchplaysconsoles", "fosseisanerd"]

commandQueue = []
nextCommands = []
#lockon = False
oldArgs = "800000000000000 128 128 128 128"


def on_ping2(*args):
	print("test")









class Client(object):

	def __init__(self):
		self.socketio = SocketIO("http://fosse.co:8110")
		self.socketio.on("controllerState", self.on_controller_state)
		self.socketio.on("controllerCommand", self.on_controller_state)
		self.socketio.on("chat message", self.on_chat_message)
		self.socketio.emit("IamController")


		self.receive_events_thread = Thread(target=self._receive_events_thread)
		self.receive_events_thread.daemon = True
		self.receive_events_thread.start()

		self.start = time.clock()
		self.end = time.clock()
		
		self.botstart = time.clock()
		self.botend = time.clock()

		self.lockon = False

		self.oldArgs2 = "800000000000000 128 128 128 128"


		

	def on_event(self, event):
		print(event)

	def on_controller_command(*args):
		nextCommands.append(args)

	def on_chat_message(*args):
		print(args[1])

	def on_controller_state(*args, set=1):

		print("controller state:", args)

		#if(set):
		#oldArgs = args
		client.oldArgs2 = args[1]


		controller.reset()

		inputs = args[1].split()

		btns = inputs[0]
		LX = inputs[1]
		LY = inputs[2]
		RX = inputs[3]
		RY = inputs[4]

		controller.dpad = int(btns[0])
		if (btns[1] == '1'):
			controller.lclick = 1;
		if (btns[2] == '1'):
			controller.l = 1;
		if (btns[3] == '1'):
			controller.zl = 1;
		if (btns[4] == '1'):
			controller.minus = 1;
		if (btns[5] == '1'):
			controller.capture = 0;
		if (btns[6] == '1'):
			controller.a = 1;
		if (btns[7] == '1'):
			controller.b = 1;
		if (btns[8] == '1'):
			controller.x = 1;
		if (btns[9] == '1'):
			controller.y = 1;
		if (btns[10] == '1'):
			controller.rclick = 1;
		if (btns[11] == '1'):
			controller.r = 1;
		if (btns[12] == '1'):
			controller.zr = 1;
		if (btns[13] == '1'):
			controller.plus = 0
		if (btns[14] == '1'):
			controller.home = 0

		controller.LX = int(LX)
		controller.LY = 255-int(LY)
		controller.RX = int(RX)
		controller.RY = 255-int(RY)


		duration = 0.1
		reset = 0
		send_and_reset(duration, reset)



	def handleChat(self, username, message):
		return



	def loop(self):
		# control switch here:

		botend = time.clock()
		diffInSeconds = self.botend - self.botstart
		diffInMilliSeconds = diffInSeconds*1000

		if(diffInMilliSeconds > 1000*60*5):
			self.botstart = time.clock()
			msg = "Join the discord server! https://discord.gg/ARTbddH\
			hate the stream delay? go here! https://fosse.co/js/streamr/node/console/"
			twitchBot.chat(msg)

		response = twitchBot.stayConnected()
		#response = "none"
		if(response != "none"):
			username = re.search(r"\w+", response).group(0) # return the entire match
			username = username.lower()
			message = CHAT_MSG.sub("", response)
			message = message.strip()
			message = message.lower()

			commands = [x.strip() for x in message.split(',')]
			cmd = "none"

			if(commands[0] == "!controls"):
				msg = "@" + username + " look at the description Kappa (this is a bot)"
				msg = "\
	(Case does NOT matter)----------------------\
	(sleft/sright/sup/sdown holds for 0.1 seconds)-------------\
	(left/right/up/down holds for 0.3 seconds)----------------\
	(hleft/hright/hup/hdown holds for 1.5 seconds)-----------\
	(add 2 h's for 4 seconds held)-----------------------------\
	A/B/X/Y / HA/HB/HX/HY / L/R/ZL/ZR--------------------------\
	To press buttons together: (ex. a, up+b, x)----------------\
	To chain: (ex. up, up, up)---------------\
	"
				twitchBot.chat(msg)

			valid = True
			for cmd in commands:
				if (cmd not in validCommands and "+" not in cmd):
					valid = False
				if ("plus" in cmd and username not in whitelist):
					valid = False
				if ("home" in cmd and username not in adminlist):
					valid = False
				if ("lockon" in cmd):
					self.lockon = not self.lockon

			if (not valid):
				commands = ["none"]


			if(len(commands) > 20):
				commands = []
			for cmd in commands:
				commandQueue.append(cmd)


		sleep(0.01)

		self.end = time.clock()
		diffInSeconds = self.end - self.start
		diffInMilliSeconds = diffInSeconds*1000

		if(diffInMilliSeconds > 160):
			self.start = time.clock()
			#controller.send(controller.output)

			if(len(commandQueue) > 0):
				nextCommands.append(commandQueue[0])
				del commandQueue[0]

			duration = 0
			reset = 1

			if(self.lockon == True):
				controller.zl = 1
				reset = 0

			if(len(nextCommands) > 0):
				# print(nextCommands)
				cmd = nextCommands[-1]
				del nextCommands[-1]

				if(cmd == "sssleft" or cmd == "sssl"):
					controller.LX = STICK_MIN
					duration = 0.01
					reset = 1
				if(cmd == "sssright" or cmd == "sssr"):
					controller.LX = STICK_MAX
					duration = 0.01
					reset = 1
				if(cmd == "sssup" or cmd == "sssu"):
					controller.LY = STICK_MIN
					duration = 0.01
					reset = 1
				if(cmd == "sssdown" or cmd == "sssd"):
					controller.LY = STICK_MAX
					duration = 0.01
					reset = 1

				if(cmd == "ssleft" or cmd == "ssl"):
					controller.LX = STICK_MIN
					duration = 0.1
					reset = 1
				if(cmd == "ssright" or cmd == "ssr"):
					controller.LX = STICK_MAX
					duration = 0.1
					reset = 1
				if(cmd == "ssup" or cmd == "ssu"):
					controller.LY = STICK_MIN
					duration = 0.1
					reset = 1
				if(cmd == "ssdown" or cmd == "ssd"):
					controller.LY = STICK_MAX
					duration = 0.1
					reset = 1

				if(cmd == "sleft" or cmd == "sl"):
					controller.LX = STICK_MIN
					duration = 0.3
					reset = 1
				if(cmd == "sright" or cmd == "sr"):
					controller.LX = STICK_MAX
					duration = 0.3
					reset = 1
				if(cmd == "sup" or cmd == "su"):
					controller.LY = STICK_MIN
					duration = 0.3
					reset = 1
				if(cmd == "sdown" or cmd == "sd"):
					controller.LY = STICK_MAX
					duration = 0.3
					reset = 1

				if(cmd == "left" or cmd == "l"):
					controller.LX = STICK_MIN
					duration = 0.6
					reset = 1
				if(cmd == "right" or cmd == "r"):
					controller.LX = STICK_MAX
					duration = 0.6
					reset = 1
				if(cmd == "up" or cmd == "u"):
					controller.LY = STICK_MIN
					duration = 0.6
					reset = 1
				if(cmd == "down" or cmd == "d"):
					controller.LY = STICK_MAX
					duration = 0.6
					reset = 1

				if(cmd == "hleft" or cmd == "hl"):
					controller.LX = STICK_MIN
					duration = 1.5
					reset = 1
				if(cmd == "hright" or cmd == "hr"):
					controller.LX = STICK_MAX
					duration = 1.5
					reset = 1
				if(cmd == "hup" or cmd == "hu"):
					controller.LY = STICK_MIN
					duration = 1.5
					reset = 1
				if(cmd == "hdown" or cmd == "hd"):
					controller.LY = STICK_MAX
					duration = 1.5
					reset = 1

				if(cmd == "hhleft"):
					controller.LX = STICK_MIN
					duration = 4.0
					reset = 1
				if(cmd == "hhright"):
					controller.LX = STICK_MAX
					duration = 4.0
					reset = 1
				if(cmd == "hhup"):
					controller.LY = STICK_MIN
					duration = 4.0
					reset = 1
				if(cmd == "hhdown"):
					controller.LY = STICK_MAX
					duration = 4.0
					reset = 1

				
				if(cmd == "dleft" or cmd == "dl"):
					controller.dpad = DPAD_LEFT
					duration = 0.3
					reset = 1
				if(cmd == "dright" or cmd == "dr"):
					controller.dpad = DPAD_RIGHT
					duration = 0.3
					reset = 1
				if(cmd == "dup" or cmd == "du"):
					controller.dpad = DPAD_UP
					duration = 0.3
					reset = 1
				if(cmd == "ddown" or cmd == "dd"):
					controller.dpad = DPAD_DOWN
					duration = 0.3
					reset = 1



				if(cmd == "slook left" or cmd == "sll"):
					controller.RX = STICK_MIN
					duration = 0.1
					reset = 1
				if(cmd == "slook right" or cmd == "slr"):
					controller.RX = STICK_MAX
					duration = 0.1
					reset = 1
				if(cmd == "slook up" or cmd == "slu"):
					controller.RY = STICK_MIN
					duration = 0.1
					reset = 1
				if(cmd == "slook down" or cmd == "sld"):
					controller.RY = STICK_MAX
					duration = 0.1
					reset = 1

				if(cmd == "look left" or cmd == "ll"):
					controller.RX = STICK_MIN
					duration = 0.3
					reset = 1
				if(cmd == "look right" or cmd == "lr"):
					controller.RX = STICK_MAX
					duration = 0.3
					reset = 1
				if(cmd == "look up" or cmd == "lu"):
					controller.RY = STICK_MIN
					duration = 0.3
					reset = 1
				if(cmd == "look down" or cmd == "ld"):
					controller.RY = STICK_MAX
					duration = 0.3
					reset = 1

				if(cmd == "hlook left" or cmd == "hll"):
					controller.RX = STICK_MIN
					duration = 0.6
					reset = 1
				if(cmd == "hlook right" or cmd == "hlr"):
					controller.RX = STICK_MAX
					duration = 0.6
					reset = 1
				if(cmd == "hlook up" or cmd == "hlu"):
					controller.RY = STICK_MIN
					duration = 0.6
					reset = 1
				if(cmd == "hlook down" or cmd == "hld"):
					controller.RY = STICK_MAX
					duration = 0.6
					reset = 1
				
				if(cmd == "a"):
					controller.a = 1
					duration = 0.3
					reset = 1
				if(cmd == "ha"):
					controller.a = 1
					duration = 0.5
					reset = 1
				if(cmd == "sb"):
					controller.b = 1
					duration = 0.1
					reset = 1
				if(cmd == "b"):
					controller.b = 1
					duration = 0.4
					reset = 1
				if(cmd == "hb"):
					controller.b = 1
					duration = 0.5
					reset = 1
				if(cmd == "hhb"):
					controller.b = 1
					duration = 0.8
					reset = 1
				if(cmd == "hhhb"):
					controller.b = 1
					duration = 1.8
					reset = 1
				if(cmd == "x"):
					controller.x = 1
					duration = 0.3
					reset = 1
				if(cmd == "hx"):
					controller.y = 1
					duration = 0.5
					reset = 1
				if(cmd == "y"):
					controller.y = 1
					duration = 0.3
					reset = 1
				if(cmd == "hy"):
					controller.y = 1
					duration = 0.7
					reset = 1
				if(cmd == "lstick"):
					controller.lstick = 1
					duration = 0.1
					reset = 1
				if(cmd == "rstick"):
					controller.rstick = 1
					duration = 0.1
					reset = 1
				if(cmd == "l"):
					controller.l = 1
					duration = 0.1
					reset = 1
				if(cmd == "r"):
					controller.r = 1
					duration = 0.1
					reset = 1
				if(cmd == "hr"):
					controller.r = 1
					duration = 1
					reset = 1
				if(cmd == "zl"):
					controller.zl = 1
					duration = 0.1
					reset = 1
				if(cmd == "zr"):
					controller.zr = 1
					duration = 0.1
					reset = 1
				if(cmd == "minus"):
					controller.minus = 1
					duration = 0.1
					reset = 1
				if(cmd == "plus"):
					controller.plus = 1
					duration = 0.1
					reset = 1
				if(cmd == "home"):
					controller.home = 1
					duration = 0.1
					reset = 1

				if(cmd == "long jump"):
					controller.LY = STICK_MIN
					duration = 0.6
					nextCommands.insert(0, "long jump2")
					reset = 0
				if(cmd == "long jump2"):
					controller.LY = STICK_MIN
					controller.zl = 1
					duration = 0.01
					nextCommands.insert(0, "long jump3")
					reset = 0
				if(cmd == "long jump3"):
					controller.LY = STICK_MIN
					controller.b = 1
					duration = 0.1
					nextCommands.insert(0, "long jump4")
					reset = 0
				if(cmd == "long jump4"):
					controller.LY = STICK_MIN
					controller.b = 1
					controller.zl = 0
					duration = 1
					reset = 1

				if(cmd == "jump forward"):
					controller.LY = STICK_MIN
					duration = 0.3
					nextCommands.insert(0, "jump forward2")
					reset = 0
				if(cmd == "jump forward2"):
					controller.LY = STICK_MIN
					controller.b = 1
					duration = 0.4
					reset = 1

				if(cmd == "jump back"):
					controller.LY = STICK_MAX
					duration = 0.3
					nextCommands.insert(0, "jump forward2")
					reset = 0
				if(cmd == "jump back2"):
					controller.LY = STICK_MAX
					controller.b = 1
					duration = 0.4
					reset = 1

				if(cmd == "cap bounce"):
					# b, y, sdive, hy, y, sdive
					nextCommands.insert(0, "b")
					nextCommands.insert(0, "y")
					nextCommands.insert(0, "sdive")
					nextCommands.insert(0, "hy")
					nextCommands.insert(0, "y")
					nextCommands.insert(0, "sdive")

				if(cmd == "swim"):
					# b, b, b, b
					nextCommands.insert(0, "b")
					nextCommands.insert(0, "b")
					nextCommands.insert(0, "b")
					nextCommands.insert(0, "b")


				if(cmd == "sdive"):
					controller.zl = 1
					duration = 0.1
					nextCommands.insert(0, "sdive2")
					reset = 0
				if(cmd == "sdive2"):
					controller.y = 1
					duration = 0.1
					reset = 1

				if(cmd == "dive"):
					controller.b = 1
					duration = 0.1
					nextCommands.insert(0, "dive2")
					reset = 0
				if(cmd == "dive2"):
					controller.zl = 1
					duration = 0.01
					nextCommands.insert(0, "dive3")
					reset = 0
				if(cmd == "dive3"):
					controller.y = 1
					duration = 0.1
					reset = 1

				if(cmd == "hdive"):
					controller.b = 1
					duration = 0.2
					nextCommands.insert(0, "hdive2")
					reset = 0
				if(cmd == "hdive2"):
					controller.zl = 1
					duration = 0.01
					nextCommands.insert(0, "hdive3")
					reset = 0
				if(cmd == "hdive3"):
					controller.y = 1
					duration = 0.1
					reset = 1

				if(cmd == "roll"):
					controller.zl = 1
					duration = 0.01
					nextCommands.insert(0, "roll2")
					reset = 0
				if(cmd == "roll2"):
					controller.y = 1
					duration = 0.1
					reset = 1

				if(cmd == "backflip" or cmd == "bf" or cmd == "back flip"):
					controller.zl = 1
					duration = 0.01
					nextCommands.insert(0, "backflip2")
					reset = 0
				if(cmd == "backflip2"):
					controller.b = 1
					duration = 0.1
					reset = 1

				if(cmd == "ground pound" or cmd == "gp" or cmd == "groundpound"):
					controller.b = 1
					duration = 0.01
					nextCommands.insert(0, "ground pound2")
					reset = 0
				if(cmd == "ground pound2"):
					controller.zl = 1
					duration = 0.1
					reset = 1



				if(cmd == "sprint"):
					controller.LY = STICK_MIN
					controller.b = 1
					duration = 0.6
					reset = 1
				if(cmd == "hsprint"):
					controller.LY = STICK_MIN
					controller.b = 1
					duration = 1.5
					reset = 1
				if(cmd == "hhsprint"):
					controller.LY = STICK_MIN
					controller.b = 1
					duration = 3
					reset = 1




				d = 0.001

				if(cmd == "spin"):
					controller.LX = STICK_CENTER
					controller.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin2")
					reset = 0
				if(cmd == "spin2"):
					controller.LX = STICK_MAX
					controller.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin3")
					reset = 0
				if(cmd == "spin3"):
					controller.LX = STICK_MAX
					controller.LY = STICK_CENTER
					duration = d
					nextCommands.insert(0, "spin4")
					reset = 0
				if(cmd == "spin4"):
					controller.LX = STICK_CENTER
					controller.LY = STICK_MAX
					duration = d
					nextCommands.insert(0, "spin5")
					reset = 0
				if(cmd == "spin5"):
					controller.LX = STICK_MIN
					controller.LY = STICK_MAX
					duration = d
					nextCommands.insert(0, "spin6")
					reset = 0
				if(cmd == "spin6"):
					controller.LX = STICK_MIN
					controller.LY = STICK_CENTER
					duration = d
					nextCommands.insert(0, "spin7")
					reset = 0
				if(cmd == "spin7"):
					controller.LX = STICK_MIN
					controller.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin8")
					reset = 0
				if(cmd == "spin8"):
					controller.LX = STICK_CENTER
					controller.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin9")
					reset = 0
				if(cmd == "spin9"):
					controller.LX = STICK_CENTER
					controller.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin10")
					reset = 0
				if(cmd == "spin10"):
					controller.LX = STICK_MAX
					controller.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin11")
					reset = 0
				if(cmd == "spin11"):
					controller.LX = STICK_MAX
					controller.LY = STICK_CENTER
					duration = d
					nextCommands.insert(0, "spin12")
					reset = 0
				if(cmd == "spin12"):
					controller.LX = STICK_CENTER
					controller.LY = STICK_MAX
					duration = d
					nextCommands.insert(0, "spin13")
					reset = 0
				if(cmd == "spin13"):
					controller.LX = STICK_MIN
					controller.LY = STICK_MAX
					duration = d
					nextCommands.insert(0, "spin14")
					reset = 0
				if(cmd == "spin14"):
					controller.LX = STICK_MIN
					controller.LY = STICK_CENTER
					duration = d
					nextCommands.insert(0, "spin15")
					reset = 0
				if(cmd == "spin15"):
					controller.LX = STICK_MIN
					controller.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin16")
					reset = 0
				if(cmd == "spin16"):
					controller.LX = STICK_CENTER
					controller.LY = STICK_MIN
					duration = d
					#nextCommands.insert(0, "spin6")
					reset = 1

				if("+" in cmd):
					btns = [x.strip() for x in cmd.split('+')]

					for btn in btns:
						duration = 0.3
						reset = 1

						if("s" in btn):
							duration = 0.01
						if("h" in btn):
							duration = 0.6
						if("hh" in btn):
							duration = 1.5
						if("hhh" in btn):
							duration = 5

						btn = btn.replace("s","")
						btn = btn.replace("h","")

						if(btn == "left"):
							controller.LX = STICK_MIN
						if(btn == "rigt"):
							controller.LX = STICK_MAX
						if(btn == "up"):
							controller.LY = STICK_MIN
						if(btn == "down"):
							controller.LY = STICK_MAX
						if(btn == "dleft"):
							controller.dpad = DPAD_LEFT
						if(btn == "drigt"):
							controller.dpad = DPAD_RIGHT
						if(btn == "dup"):
							controller.dpad = DPAD_UP
						if(btn == "ddown"):
							controller.dpad = DPAD_DOWN
						
						if(btn == "look left"):
							controller.RX = STICK_MIN
						if(btn == "look rigt"):
							controller.RX = STICK_MAX
						if(btn == "look up"):
							controller.RY = STICK_MIN
						if(btn == "look down"):
							controller.RY = STICK_MAX
						if(btn == "a"):
							controller.a = 1
						if(btn == "b"):
							controller.b = 1
						if(btn == "x"):
							controller.x = 1
						if(btn == "y"):
							controller.y = 1
						if(btn == "l"):
							controller.l = 1
						if(btn == "r"):
							controller.r = 1
						if(btn == "zl"):
							controller.zl = 1
						if(btn == "zr"):
							controller.zr = 1
						if(btn == "minus"):
							controller.minus = 1
			send_and_reset(duration, reset)





	def _receive_events_thread(self):
		self.socketio.wait()

client = Client()

while True:

	# rnd = random.uniform(0, 1)
	# if(rnd > 0.99):
	client.on_controller_state(client.oldArgs2, 0)

	#print(client.oldArgs2)

	client.loop()

	sleep(0.0001)

	# so I don't get stuck:
	if(win32api.GetAsyncKeyState(win32con.VK_ESCAPE)):
		controller.send("RELEASE")
		controller.ser.close()
		exit()
