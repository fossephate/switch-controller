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
logging.getLogger("socketIO-client").setLevel(logging.DEBUG)
logging.basicConfig()

from threading import Thread

# OpenCV / image utils:
import imutils
import cv2
from PIL import Image

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


screenWidth, screenHeight = pyautogui.size()
x = screenWidth/2
y = screenHeight/2
prevX = 0
prevY = 0

controller = SwitchController()
controller.connect("COM3")

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

def round_down(num, divisor):
    return num - (num%divisor)





validCommands = ["!commands", "goto torquel", "goto pokemon quest", "restart", "restart1", "restart2", "restart3", "restart script", "restart video", "restart video1", "restart video2", "restart video3", "restart server", "!help", "votenay", "voteyea", "goto wizard", "goto cave", "goto sonic", "goto skyrim", "goto rocket league", "goto arms", "goto celeste", "goto mk8", "goto splatoon2", "goto isaac", "goto mario", "goto botw", "goto kirby", "goto smo", "goto", "lockon", "hhsprint", "hsprint", "sprint", "!controls", "!goto", "home", "lstick", "rstick", "spin", "swim", "back flip", "ground pound", "groundpound", "gp", "bf", "cap bounce", "sdive", "sdive2", "hdive", "hdive2", "hdive3", "dive", "dive2", "dive3", "roll", "roll2", "backflip", "backflip2", "sssu", "sssd", "sssl", "sssr", "sb", "suu", "", "up", "down", "left", "right", "u", "d", "l", "r", "hup", "hdown", "hleft", "hright", "hhup", "hhdown", "hhleft", "hhright", "hu", "hd", "hl", "hr", "su", "sd", "sl", "sr", "sup", "sdown", "sleft", "sright", "ssu", "ssd", "ssl", "ssr", "ssup", "ssdown", "ssleft", "ssright", "look up", "look down", "look left", "look right", "lu", "ld", "ll", "lr", "hlu", "hld", "hll", "hlr", "slu", "sld", "sll", "slr", "dup", "ddown", "dleft", "dright", "du", "dd", "dl", "dr", "a", "b", "x", "y", "ha", "hb", "hx", "hy", "hhb", "hhhb", "l", "zl", "r", "zr", "plus", "minus", "long jump", "long jump2", "long jump3", "jump forward", "jump forward2", "jump back", "jump back2", "dive", "dive2"]
pluslist = ["zellie", "generzon344", "joeakuaku", "azeywub", "alua2020", "grady404", "valentinvanelslande", "beanjr_yt", "yanchan230", "silvermagpi", "hoopa21", "opprose", "mrruidiazisthebestinsmo", "stravos96", "harmjan387", "twitchplaysconsoles", "fosseisanerd"]
modlist = ["stravos96", "yanchan230", "silvermagpi", "twitchplaysconsoles", "fosseisanerd", "tpnsbot"]
adminlist = ["silvermagpi", "twitchplaysconsoles", "fosseisanerd"]

commandQueue = []
nextCommands = []
#lockon = False
oldArgs = "800000000000000 128 128 128 128"










class Client(object):

	def __init__(self):
		# self.socketio = SocketIO("http://fosse.co:8110")
		# self.socketio = SocketIO("127.0.0.1:8110")
		self.socketio = SocketIO("http://twitchplaysnintendoswitch.com:8110")

		self.socketio.on("controllerState", self.on_controller_state)
		self.socketio.on("controllerCommand", self.on_controller_state)
		self.socketio.on("chat message", self.on_chat_message)
		self.socketio.on("turnTimeLeft", self.on_turn_time_left)
		self.socketio.emit("IamController")

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

	def on_chat_message(*args):
		
		message = args[1]
		message = message.strip()
		message = message.lower()

		username = "streamrChat"

		client.handleChat(username, message)

	def on_controller_state(*args, set=1):

		if(not client.laglessEnabled):
			return

		print("controller state:", args[1])

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
		if (btns[1] == "1"):
			controller.lstick = 1;
		if (btns[2] == "1"):
			controller.l = 1;
		if (btns[3] == "1"):
			controller.zl = 1;
		if (btns[4] == "1"):
			controller.minus = 1;
		if (btns[5] == "1"):
			if (client.currentPlayer in modlist):
				controller.capture = 1
			else:
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
			if (client.currentPlayer in pluslist):
				controller.plus = 1
			else:
				controller.plus = 0
		if (btns[14] == "1"):
			if (client.currentPlayer in modlist):
				controller.home = 1
			else:
				controller.home = 0

		try:
			controller.LX = int(LX)
			controller.LY = 255-int(LY)
			controller.RX = int(RX)
			controller.RY = 255-int(RY)
		except:
			pass


		duration = 0.01
		reset = 0
		send_and_reset(duration, reset)





	def findImage(self, frame, imagefile):


		img_rgb = frame# where we're looking for the icon
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		template = cv2.imread(imagefile, 0)
		w, h = template.shape[::-1]

		iconLocationX = -1
		iconLocationY = -1

		res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
		threshold = 0.6
		loc = np.where(res >= threshold)
		location = None
		# for pt in zip(*loc[::-1]):
		for pt in zip(*[loc[-1], loc[-2]]):
			# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
			# pt = max_loc
			cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
			iconLocationX = pt[0] + (w/2)
			iconLocationX = pt[1] + (h/2)
			cv2.circle(img_rgb, (int(iconLocationX), int(iconLocationY)), int(2), (0, 255, 255), 2)
			# print(pt)
			location = [pt[0], pt[1]]
		
		# cv2.imshow("icon match", img_rgb)
		# cv2.waitKey(10)

		return location


		# img = cv2.imread("messi5.jpg",0)
		# img = frame
		# img2 = img.copy()
		# template = cv2.imread("icons/SMO.png", 0)
		# w, h = template.shape[::-1]


		# # All the 6 methods for comparison in a list
		# img = img2.copy()
		# method = eval("cv2.TM_CCOEFF_NORMED")
		# # Apply template Matching
		# res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
		# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		# # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
		# if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
		#     top_left = min_loc
		# else:
		#     top_left = max_loc
		# bottom_right = (top_left[0] + w, top_left[1] + h)
		# cv2.rectangle(img, top_left, bottom_right, 255, 2)
		# plt.subplot(121),plt.imshow(res,cmap = "gray")
		# plt.title("Matching Result"), plt.xticks([]), plt.yticks([])
		# plt.subplot(122),plt.imshow(img,cmap = "gray")
		# plt.title("Detected Point"), plt.xticks([]), plt.yticks([])
		# plt.suptitle(meth)
		# plt.show()



	def goto_game(self, imagefile, delay=50, nameofgame="Twitch Plays"):

		# disable lagless while we do this:
		self.laglessEnabled = False

		# get to game selection screen:
		controller.reset()
		controller.home = 1
		send_and_reset(0.1, 1)
		sleep(2)
		controller.LX = STICK_MAX
		send_and_reset(3, 1)
		controller.a = 1
		send_and_reset(0.1)

		sleep(2)

		


		# SSx1 = 255 - 1920;# left monitor
		# SSy1 = 70;
		# SSWidth = 1280
		# SSHeight = 720
		SSx1 = 319 - 1920;# left monitor
		SSy1 = 61;
		SSWidth = 1280
		SSHeight = 720

		#get window position and info
		hwnd = win32gui.FindWindow(None, "OBS")
		# hwnd = win32gui.GetDesktopWindow()#for screenshot of entire screen

		wDC = win32gui.GetWindowDC(hwnd)
		myDC = win32ui.CreateDCFromHandle(wDC)
		newDC = myDC.CreateCompatibleDC()
		myBitMap = win32ui.CreateBitmap()
		myBitMap.CreateCompatibleBitmap(myDC, SSWidth, SSHeight)
		newDC.SelectObject(myBitMap)
		newDC.BitBlt((0,0),(SSWidth, SSHeight) , myDC, (SSx1,SSy1), win32con.SRCCOPY)

		bmpinfo = myBitMap.GetInfo()
		bmpstr = myBitMap.GetBitmapBits(True)
		img = Image.frombuffer(
		    "RGB",
		    (bmpinfo["bmWidth"], bmpinfo["bmHeight"]),
		    bmpstr, "raw", "BGRX", 0, 1)

		# Free Resources
		myDC.DeleteDC()
		newDC.DeleteDC()
		win32gui.ReleaseDC(hwnd, wDC)
		win32gui.DeleteObject(myBitMap.GetHandle())

		#img = ImageGrab.grab(bbox=(x1, y1, x2, y2))#.crop(box) #x, y, w, h
		img_np = np.array(img)
		frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
		hsv = cv2.cvtColor(img_np, cv2.COLOR_BGR2HSV)


		iconLoc = self.findImage(frame, imagefile)
		# cursorLoc = self.findImage(frame, "icons/selectbar.png")


		if iconLoc == None:
			controller.a = 1
			send_and_reset(0.1)
			self.laglessEnabled = True
			return


		print(iconLoc)


		# iconLoc[0] = int(round(iconLoc[0]/100)-1)# the number of times to move right
		# iconLoc[1] = int(round(iconLoc[1]/100)-2)# the number of times to move down

		# so that when we round down it always above the nearest multiple of 185
		iconLoc[0] += 10
		iconLoc[1] += 10

		iconLoc[0] = int((round_down(iconLoc[0], 185)/185))# the number of times to move right
		iconLoc[1] = int((round_down(iconLoc[1], 185)/185)-1)# the number of times to move down

		# iconLoc[0] = int(iconLoc[0]/2)
		# iconLoc[1] = int(iconLoc[1]/2)

		print(iconLoc)


		for i in range(0, iconLoc[0]):
			controller.LX = STICK_MAX
			send_and_reset(0.1, 1)
			sleep(0.5)
		for i in range(0, iconLoc[1]):
			controller.LY = STICK_MAX
			send_and_reset(0.1, 1)
			sleep(0.5)

		controller.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller.a = 1
		send_and_reset(0.1)
		sleep(delay)
		controller.a = 1
		send_and_reset(0.1)
		controller.a = 1
		send_and_reset(0.1)
		controller.a = 1
		send_and_reset(0.1)
		controller.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller.a = 1
		send_and_reset(0.1)
		controller.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller.a = 1
		send_and_reset(0.1)

		twitchBot.chat("!game " + nameofgame)

		
		# draw a circle on the image:
		# x = 200
		# y = 200
		# r = 5
		# cv2.circle(frame, (int(x), int(y)), int(r), (0, 255, 255), 2)

		# show screen capture and mask
		#cv2.imshow("screen capture", frame)

		# mask = cv2.inRange(hsv, colorLower1, colorUpper1)
		# cv2.imshow("mask", mask)
		cv2.waitKey(1)


		self.laglessEnabled = True

		return

	def end_goto_vote(self, imagefile, delay, nameofgame="Twitch Plays"):
		# twitchBot.chat("Voting has ended!")
		msg = "With " + str(self.yeaVotes) + " VoteYea and " + str(self.nayVotes) + " VoteNay"
		
		leaving = False

		if(self.yeaVotes > self.nayVotes):
			msg = msg + " We will be LEAVING"
			leaving = True
		else:
			msg = msg + " We will be STAYING"

		twitchBot.chat(msg)

		self.voting = False

		if(leaving):
			self.goto_game(imagefile, delay, nameofgame)


	def goto_game_vote(self, imagefile, delay=50, nameofgame="Twitch Plays"):

		if(self.voting == True):
			return

		self.yeaVotes = 0
		self.nayVotes = 0
		twitchBot.chat("A vote has been started to goto " + nameofgame + "! vote now with VoteYea to LEAVE and VoteNay to STAY! Voting ends in 20 seconds!")
		self.voting = True

		voteTimer = Timer(20.0, self.end_goto_vote, (imagefile, delay, nameofgame))
		voteTimer.start()

		return



	def handleChat(self, username, message):
		print(message)

		commands = [x.strip() for x in message.split(",")]
		cmd = "none"

		if(commands[0] == "!controls" or commands[0] == "!help"):
			msg = "goto https://twitchplaysnintendoswitch.com or look at the description for the chat controls,\
			 you can also type \"goto [game]\" (without brackets) to switch games. use !goto for a list of games! use !commands for a list of commands!"
			twitchBot.chat(msg)

		if(commands[0] == "!goto"):
			msg = "use \"goto [game]\" (without brackets) to switch games! list: smo, botw, kirby, wizard, splatoon2, skyrim, sonic, celeste, torquel, pokemon quest, mk8, arms"
			twitchBot.chat(msg)

		if(commands[0] == "!commands"):
			msg = "(mods only): \"restart script\", \"restart server\" (anyone): \"restart video1\", \"restart video2\", \"restart video3\""
			twitchBot.chat(msg)

		valid = True
		for cmd in commands:
			if (cmd not in validCommands and "+" not in cmd):
				valid = False
			if ("plus" in cmd and username not in pluslist):
				valid = False
			if ("home" in cmd and username not in adminlist):
				valid = False

			# if ("restart video" in cmd and username not in modlist):
			# 	valid = False
			if ("restart server" in cmd and username not in modlist):
				valid = False
			if ("restart script" in cmd and username not in modlist):
				valid = False

			# if ("goto smo" in cmd and username not in adminlist):
			# 	valid = False
			# if ("goto botw" in cmd and username not in adminlist):
			# 	valid = False
			# if ("goto celeste" in cmd and username not in adminlist):
			# 	valid = False
			# if ("goto kirby" in cmd and username not in adminlist):
			# 	valid = False
			if ("lockon" in cmd):
				self.lockon = not self.lockon

		if(len(commands) > 20):
			valid = False

		if (not valid):
			commands = []

		for cmd in commands:
			commandQueue.append(cmd)



	def decreaseQueue(self):

		#sleep(0.0001)

		self.end = time.clock()
		diffInSeconds = self.end - self.start
		diffInMilliSeconds = diffInSeconds*1000

		if(diffInMilliSeconds > 8.33333):
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
				# if(cmd == "left"):
					controller.LX = STICK_MIN
					duration = 0.6
					reset = 1
				if(cmd == "right" or cmd == "r"):
				# if(cmd == "right"):
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

				if(cmd == "goto smo"):
					self.goto_game_vote("icons/smo.png", 30, "Super Mario Odyssey")
				if(cmd == "goto botw"):
					self.goto_game_vote("icons/botw.png", 20, "The Legend of Zelda: Breath of the Wild")
				if(cmd == "goto celeste"):
					self.goto_game_vote("icons/celeste.png", 10, "Celeste")
				if(cmd == "goto kirby"):
					self.goto_game_vote("icons/kirby.png", 10)
				if(cmd == "goto splatoon2"):
					self.goto_game_vote("icons/splatoon2.png", 10, "Splatoon 2")
				if(cmd == "goto sonic"):
					self.goto_game_vote("icons/sonic.png", 10, "Sonic Mania")
				if(cmd == "goto mk8"):
					self.goto_game_vote("icons/mk8.png", 10, "Mario Kart 8")
				if(cmd == "goto arms"):
					self.goto_game_vote("icons/arms.png", 10)
				if(cmd == "goto skyrim"):
					self.goto_game_vote("icons/skyrim.png", 40, "The Elder Scrolls V: Skyrim")
				if(cmd == "goto rocket league"):
					self.goto_game_vote("icons/rocketleague.png", 10, "Rocket League")
				if(cmd == "goto wizard"):
					self.goto_game_vote("icons/wizard.png", 10, "Wizard of Legend")
				if(cmd == "goto pokemon quest"):
					self.goto_game_vote("icons/pokemonquest.png", 10, "Pokemon Quest")
				if(cmd == "goto torquel"):
					self.goto_game_vote("icons/torquel.png", 10)
				# if(cmd == "goto cave"):
				# 	self.goto_game("icons/cave.png", 10)
				# if(cmd == "goto isaac"):
				# 	self.goto_game("icons/isaac.png", 10)
				# if(cmd == "goto mario"):
				# 	self.goto_game_vote("icons/mario.png", 10)

				if(self.voting):
					if(cmd == "voteyea"):
						self.yeaVotes += 1
					if(cmd == "votenay"):
						self.nayVotes += 1


				if(cmd == "restart video" or cmd == "restart" or cmd == "restart1" or cmd == "restart video1"):
					# self.socketio.emit("restart")
					twitchBot.chat("Restarting lagless1!")
					os.system("taskkill /f /im streamr")

				if(cmd == "restart video2" or cmd == "restart2"):
					twitchBot.chat("Restarting lagless2!")
					os.system("taskkill /f /im jsmpeg-vnc.exe")

				if(cmd == "restart video3" or cmd == "restart3"):
					twitchBot.chat("Restarting lagless3!")
					os.system("taskkill /f /im ffmpeg.exe")
					os.system("taskkill /f /im node.exe")

				if(cmd == "restart server"):
					twitchBot.chat("Restarting the Server! maybe @fosse if you're using this!")
					self.socketio.emit("restart server")

				if(cmd == "restart script"):
					twitchBot.chat("Restarting the Python Script!")
					sys.exit()


				if("+" in cmd):
					btns = [x.strip() for x in cmd.split("+")]

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



	def loop(self):

		# control switch here:

		self.botend = time.clock()
		diffInSeconds = self.botend - self.botstart
		diffInMilliSeconds = diffInSeconds*1000
		if(diffInMilliSeconds > 1000*60*5):
			self.socketio.emit("IamController")
			self.botstart = time.clock()
			msg = "Join the discord server! https://discord.gg/ARTbddH\
			hate the stream delay? go here! https://twitchplaysnintendoswitch.com"
			twitchBot.chat(msg)

		self.controllerEnd = time.clock()
		diffInSeconds2 = self.controllerEnd - self.controllerStart
		diffInMilliSeconds2 = diffInSeconds2*1000
		if(diffInMilliSeconds2 > 3000):
			self.socketio.emit("IamController")
			self.controllerStart = time.clock()


		# get modlist:
		# with urllib.request.urlopen("https://tmi.twitch.tv/group/user/twitchplaysconsoles/chatters") as url:
		# 	data = json.loads(url.read().decode())
		# 	print(data)


		response = twitchBot.stayConnected()
		#response = "none"
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

	# rnd = random.uniform(0, 1)
	# if(rnd > 0.99):
	#client.on_controller_state(client.oldArgs2, 0)

	#print(client.oldArgs2)

	client.loop()

	sleep(0.0001)

	
	# if win32api.GetAsyncKeyState(ord("P")):
	# 	laglessEnabled = not laglessEnabled



	# so I don't get stuck:
	if(win32api.GetAsyncKeyState(win32con.VK_ESCAPE)):
		controller.send("RELEASE")
		controller.ser.close()
		exit()