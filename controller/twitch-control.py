
# time
from threading import Timer
import threading
import time
from time import sleep

# switch controller:
from switchcontroller.switchcontroller import *

# twitch:
from twitchbot.twitchbot import *

# get sub list:
from twitchbot.twitchsubs import *

# socketio
from socketIO_client_nexus import SocketIO, LoggingNamespace, BaseNamespace
import logging
# logging.getLogger("socketIO-client").setLevel(logging.DEBUG)
logging.basicConfig()

from threading import Thread

# OpenCV / image utils:
import imutils
import cv2
from PIL import Image

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

# random
import random


screenWidth, screenHeight = pyautogui.size()
x = screenWidth/2
y = screenHeight/2
prevX = 0
prevY = 0

controller1 = SwitchController()
controller2 = SwitchController()
controller3 = SwitchController()
controller4 = SwitchController()

try:
	controller1.connect("COM3")
except:
	print("controller1 error")

try:
	controller2.connect("COM6")
except:
	print("controller2 error")
	pass

try:
	controller3.connect("COM9")
except:
	print("controller3 error")
	pass

try:
	controller4.connect("COM10")
except:
	print("controller4 error")
	pass


twitchBot = TwitchBot()
twitchBot.connect(HOST, PASS2, PORT, CHAN, NICK2)

def delayed_reset(delay=0.1):
	Timer(delay, controller1.reset).start()


def accurateSleep(duration):
	s = time.time()
	e = time.time()
	diffInMilliSeconds = 0

	while (diffInMilliSeconds < duration):
		e = time.time()
		diffInMilliSeconds = (e - s)*1000

def send_and_reset(duration=0.1, reset=1, cNum=0):
	controller = None
	if (cNum == 0):
		controller = controller1
	elif (cNum == 1):
		controller = controller2
	elif (cNum == 2):
		controller = controller3
	elif (cNum == 3):
		controller = controller4

	controller.getOutput()
	controller.send(controller.output)
	# accurateSleep(duration)
	sleep(duration)
	if (reset):
		controller.reset()
		controller.getOutput()
		controller.send(controller.output)

def round_down(num, divisor):
	return num - (num % divisor)



gameList = ["mta", "hollow", "paladins", "snipperclips", "mk8", "human", "shovel", "octopath", "explosion", "jackbox4", "jackbox3", "fallout", "skyrim", "splatoon2", "celeste", "smo", "rocketleague", "pokemonquest", "wizard", "sonic", "arms", "kirby", "fortnite", "torquel", "botw"]
# plusCommands = []
# modCommands = []
# anyCommands = []
validCommands = ["!source", "!playing", "!randomgame", "!status", "!internetstatus", "!rainbow", "!setgame", "!forcegoto", "!sublist", "!4p", "!3p", "!2p", "!1p", "!modlist", "!lock", "!egg", "!rr", "!discord", "!games", "!setforfeitlength", "!setturnlength", "!banlist", "!disableinternet", "!enableinternet", "!forcerefresh", "nay", "yea", "!enablechat", "!disablechat", "!enablegoto", "!disablegoto", "!unmod", "!mod", "!fixcontrollers", "!goto snipperclips", "!pluslist", "!unban", "!ban", "!removeplus", "!giveplus", "!goto human", "!goto shovel", "!goto octopath", "!goto explosion", "!goto jackbox4", "!goto jackbox3", "!commands", "!goto fallout", "!goto fortnite", "!goto torquel", "!goto pokemonquest", "!restart", "!restart1", "!restart2", "!restart3", "!restartscript", "!restartserver", "!help", "votenay", "voteyea", "!goto wizard", "!goto cave", "!goto sonic", "!goto skyrim", "!goto rocketleague", "!goto arms", "!goto celeste", "!goto mk8", "!goto splatoon2", "!goto isaac", "!goto mario", "!goto botw", "!goto kirby", "!goto smo", "!goto", "hhsprint", "hsprint", "sprint", "!controls", "!goto", "home", "lstick", "rstick", "spin", "swim", "back flip", "ground pound", "groundpound", "gp", "bf", "cap bounce", "sdive", "sdive2", "hdive", "hdive2", "hdive3", "dive", "dive2", "dive3", "roll", "roll2", "backflip", "backflip2", "sssu", "sssd", "sssl", "sssr", "sb", "suu", "", "up", "down", "left", "right", "u", "d", "l", "r", "hup", "hdown", "hleft", "hright", "hhup", "hhdown", "hhleft", "hhright", "hu", "hd", "hl", "hr", "su", "sd", "sl", "sr", "sup", "sdown", "sleft", "sright", "ssu", "ssd", "ssl", "ssr", "ssup", "ssdown", "ssleft", "ssright", "look up", "look down", "look left", "look right", "lu", "ld", "ll", "lr", "hlu", "hld", "hll", "hlr", "slu", "sld", "sll", "slr", "dup", "ddown", "dleft", "dright", "du", "dd", "dl", "dr", "a", "b", "x", "y", "ha", "hb", "hx", "hy", "hhb", "hhhb", "l", "zl", "r", "zr", "plus", "minus", "long jump", "long jump2", "long jump3", "jump forward", "jump forward2", "jump back", "jump back2", "dive", "dive2"]
pluslist = []
modlist = ["beanjr_yt", "alua2020", "ogcristofer", "stravos96", "splatax", "silvermagpi", "twitchplaysconsoles", "fosseisanerd", "tpnsbot"]
banlist = []
sublist = []
voted = []
singlePlayerGames = ["The Legend of Zelda: Breath of the Wild"]

commandQueue = []
nextCommands = []
oldArgs = "800000000000000 128 128 128 128"


# load plus list:
if (os.path.exists("pluslist.pkl")):
	with open("pluslist.pkl", "rb") as f:
		pluslist = pickle.load(f)[0]
# load ban list:
if (os.path.exists("banlist.pkl")):
	with open("banlist.pkl", "rb") as f:
		banlist = pickle.load(f)[0]

# get sub list:
sublist = getSubList()
print(sublist)


class Client(object):

	def __init__(self):
		self.socketio = SocketIO("http://twitchplaysnintendoswitch.com:8110")

		self.socketio.on("controllerState1", self.on_controller_state1)
		self.socketio.on("controllerState2", self.on_controller_state2)
		self.socketio.on("controllerState3", self.on_controller_state3)
		self.socketio.on("controllerState4", self.on_controller_state4)
		self.socketio.on("turnTimesLeft", self.on_turn_times_left)
		self.socketio.on("internetStatus", self.on_internet_status)
		self.socketio.emit("joinSecure", {"room": "controller", "password": ROOM_SECRET})
		self.socketio.emit("banlist", banlist)
		self.socketio.emit("modlist", modlist)
		self.socketio.emit("pluslist", pluslist)
		self.socketio.emit("sublist", sublist)

		self.receive_events_thread = Thread(target=self._receive_events_thread)
		self.receive_events_thread.daemon = True
		self.receive_events_thread.start()

		self.start = time.time()
		self.end = time.time()
		
		self.botstart = time.time()
		self.botend = time.time()

		self.controllerStart = time.time()
		self.controllerEnd = time.time()

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

		if (not client.controllerEnabled):
			return

		# if (client.currentPla)

		state = args[1]
		cNum = args[2]

		if (cNum > 0 and client.currentGame in singlePlayerGames):
			return

		print("controller state " + str(cNum) + ":", state)

		client.oldArgs2 = state

		controller = None

		if (cNum == 0):
			controller = controller1
		elif (cNum == 1):
			controller = controller2
		elif (cNum == 2):
			controller = controller3
		elif (cNum == 3):
			controller = controller4

		controller.reset()

		inputs = state.split()
		cPlayer = ""
		try:
			cPlayer = client.currentPlayers[cNum]
		except:
			pass

		if (state == "800000000000000 128 128 128 128"):
			controller.reset()
			controller.getOutput()
			controller.send(controller.output)
			return

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

	# player 2:
	def on_controller_state2(*args):
		client.on_controller_state(args[1], 1)
	
	# player 3:
	def on_controller_state3(*args):
		client.on_controller_state(args[1], 2)

	# player 4:
	def on_controller_state4(*args):
		client.on_controller_state(args[1], 3)

	def on_internet_status(*args):
		msg = ""
		if (args[1]):
			msg = "The internet is on right now!"
		else:
			msg = "The internet is off right now!"
		twitchBot.chat(msg)

	def findImage(self, frame, imagefile, threshold=0.6):

		img_rgb = frame# where we're looking for the icon
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		template = cv2.imread(imagefile, 0)
		w, h = template.shape[::-1]

		iconLocationX = -1
		iconLocationY = -1

		res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
		# threshold = 0.6
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


	def findImage2(self, imagefile, x1, y1, width, height, windowName, threshold=0.6):


		SSx1 = x1;
		SSy1 = y1;
		SSWidth = width
		SSHeight = height

		#get window position and info
		hwnd = win32gui.FindWindow(None, windowName)


		wDC = win32gui.GetWindowDC(hwnd)
		myDC = win32ui.CreateDCFromHandle(wDC)
		newDC = myDC.CreateCompatibleDC()
		myBitMap = win32ui.CreateBitmap()
		myBitMap.CreateCompatibleBitmap(myDC, SSWidth, SSHeight)
		newDC.SelectObject(myBitMap)
		newDC.BitBlt((0, 0), (SSWidth, SSHeight) , myDC, (SSx1,SSy1), win32con.SRCCOPY)

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






		img_rgb = frame# where we're looking for the icon
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		template = cv2.imread(imagefile, 0)
		w, h = template.shape[::-1]

		iconLocationX = -1
		iconLocationY = -1

		res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
		# threshold = 0.6
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

		# disable controls while we do this:
		self.controllerEnabled = False
		self.chatEnabled = False

		# if (self.currentGame == "The Legend of Zelda: Breath of the Wild"):
		# 	controller1.reset()
		# 	controller1.plus = 1
		# 	send_and_reset(0.1, 1)
		# 	controller1.r = 1
		# 	send_and_reset(0.1, 1)
		# 	controller1.r = 1
		# 	send_and_reset(0.1, 1)

		# if (self.currentGame == "Super Mario Odyssey"):
		# 	controller1.reset()
		# 	controller1.plus = 1
		# 	send_and_reset(0.1, 1)
		# 	controller1.LY = STICK_MAX
		# 	send_and_reset(0.1, 1)
		# 	sleep(0.5)
		# 	controller1.LY = STICK_MAX
		# 	send_and_reset(0.1, 1)
		# 	sleep(0.5)
		# 	controller1.LY = STICK_MAX
		# 	send_and_reset(0.1, 1)
		# 	sleep(0.5)
		# 	controller1.LY = STICK_MAX
		# 	send_and_reset(0.1, 1)
		# 	sleep(0.5)
		# 	controller1.a = 1
		# 	send_and_reset(0.1, 1)
		# 	sleep(8)

		# update the current game
		self.currentGame = nameofgame

		# get to game selection screen:
		controller1.reset()
		controller1.home = 1
		send_and_reset(0.1, 1)
		sleep(2)
		controller1.LX = STICK_MAX
		send_and_reset(3, 1)
		controller1.a = 1
		send_and_reset(0.1)

		sleep(2)

		


		# SSx1 = 255 - 1920;# left monitor
		# SSy1 = 70;
		# SSWidth = 1280
		# SSHeight = 720
		SSx1 = 319 - 1920;# left monitor
		SSy1 = 61 + 360;
		SSWidth = 1280
		SSHeight = 720

		#get window position and info
		hwnd = win32gui.FindWindow(None, "OBS")
		# hwnd = win32gui.GetDesktopWindow()#for screenshot of entire screen

		iconLoc = None
		counter = 0
		while (iconLoc == None and counter < 5):

			if (counter > 0):
				# move down and try again:
				# move down 3 times and up once:
				controller1.LY = STICK_MAX
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller1.LY = STICK_MAX
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller1.LY = STICK_MAX
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller1.LY = STICK_MIN
				send_and_reset(0.1, 1)
				sleep(0.5)

			wDC = win32gui.GetWindowDC(hwnd)
			myDC = win32ui.CreateDCFromHandle(wDC)
			newDC = myDC.CreateCompatibleDC()
			myBitMap = win32ui.CreateBitmap()
			myBitMap.CreateCompatibleBitmap(myDC, SSWidth, SSHeight)
			newDC.SelectObject(myBitMap)
			newDC.BitBlt((0, 0), (SSWidth, SSHeight) , myDC, (SSx1,SSy1), win32con.SRCCOPY)

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

			if (iconLoc != None):
				break

			counter += 1


		# give up if we still can't find it:
		if iconLoc == None:
			controller1.LY = STICK_MIN
			send_and_reset(1.5, 1)
			controller1.a = 1
			send_and_reset(0.1)
			self.controllerEnabled = True
			return


		print(iconLoc)


		# iconLoc[0] = int(round(iconLoc[0]/100)-1)# the number of times to move right
		# iconLoc[1] = int(round(iconLoc[1]/100)-2)# the number of times to move down

		# so that when we round down its always above the nearest multiple of 185
		iconLoc[0] += 10
		iconLoc[1] += 10

		iconLoc[0] = int((round_down(iconLoc[0], 185)/185))# the number of times to move right
		iconLoc[1] = int((round_down(iconLoc[1], 185)/185)-1)# the number of times to move down

		# iconLoc[0] = int(iconLoc[0]/2)
		# iconLoc[1] = int(iconLoc[1]/2)

		print(iconLoc)


		for i in range(0, iconLoc[0]):
			controller1.LX = STICK_MAX
			send_and_reset(0.1, 1)
			sleep(0.5)
		for i in range(0, iconLoc[1]):
			controller1.LY = STICK_MAX
			send_and_reset(0.1, 1)
			sleep(0.5)

		controller1.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller1.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller1.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller1.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller1.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller1.a = 1
		send_and_reset(0.1)
		sleep(delay)
		controller1.a = 1
		send_and_reset(0.1)
		controller1.a = 1
		send_and_reset(0.1)
		controller1.a = 1
		send_and_reset(0.1)
		controller1.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller1.a = 1
		send_and_reset(0.1)
		controller1.a = 1
		send_and_reset(0.1)
		sleep(2)
		controller1.a = 1
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


		self.controllerEnabled = True
		self.chatEnabled = True

		return

	def end_goto_vote(self, imagefile, delay, nameofgame="Twitch Plays"):
		# twitchBot.chat("Voting has ended!")
		msg = "With " + str(self.yeaVotes) + " VoteYea and " + str(self.nayVotes) + " VoteNay"
		
		leaving = False
		timeGotoisDisabled = 0

		if (self.yeaVotes > self.nayVotes):
			self.gotoLeft = True
			msg = msg + " We will be LEAVING"
			leaving = True
			timeGotoisDisabled = 8*60
		else:
			self.gotoLeft = False
			msg = msg + " We will be STAYING"
			timeGotoisDisabled = 2*60

		self.gotoUsed = True
		gotoTimer = Timer(timeGotoisDisabled, self.reenable_goto)
		gotoTimer.start()

		twitchBot.chat(msg)

		self.voting = False

		del voted[:]

		if (leaving):
			self.goto_game(imagefile, delay, nameofgame)
		return

	def reenable_goto(self):
		self.gotoUsed = False


	def goto_game_vote(self, imagefile, delay=50, nameofgame="Twitch Plays"):

		if (self.voting == True):
			msg = "The !goto command is disabled right now"
			twitchBot.chat(msg)
			return

		if (self.gotoUsed == True):
			msg = ""
			if (self.gotoLeft == True):
				msg = "The !goto command was used in the last 8 minutes, please wait before trying to change the game again"
			else:
				msg = "The !goto command was used in the last 2 minutes, please wait before trying to change the game again"
			twitchBot.chat(msg)
			return

		self.yeaVotes = 0
		self.nayVotes = 0
		twitchBot.chat("A vote has been started to goto " + nameofgame + "! Vote now with VoteYea to LEAVE and VoteNay to STAY! Voting ends in 20 seconds!")
		self.voting = True

		voteTimer = Timer(20.0, self.end_goto_vote, (imagefile, delay, nameofgame))
		voteTimer.start()

		return



	def handleChat(self, username, message):
		print(username + ": " + message)

		commands = None
		if ("," in message):
			commands = [x.strip() for x in message.split(",")]
		else:
			commands = [x.strip() for x in message.split(" ")]

		cmd = "none"

		valid = True
		for cmd in commands:
			if (cmd not in validCommands and "+" not in cmd):
				valid = False
			if ("plus" in cmd and username not in pluslist):
				valid = False
			if ("home" in cmd and username not in modlist):
				valid = False

			if (self.voting):
				if ((cmd == "voteyea" or cmd == "yea") and username not in voted):
					voted.append(username)
					self.yeaVotes += 1
				if ((cmd == "votenay" or cmd == "nay") and username not in voted):
					voted.append(username)
					self.nayVotes += 1



		if len(commands) == 1:

			cmd = commands[0]


			if (cmd == "!controls" or cmd == "!help"):
				msg = "goto https://twitchplaysnintendoswitch.com or look at the description for the chat controls,\
				 you can also type \"!goto [game]\" (without brackets) to switch games. use !goto for a list of games! use !commands for a list of commands!"
				twitchBot.chat(msg)

			if (cmd == "!goto" or cmd == "!games"):
				msg = "use \"!goto [game]\" (without brackets) to switch games! list: "
				for game in gameList:
					msg += game + ", "
				msg = msg[:-2]
				twitchBot.chat(msg)

			if (cmd == "!status" or cmd == "!internetstatus"):
				# msg = "Checking internet status!"
				# twitchBot.chat(msg)
				self.socketio.emit("getInternetStatus")

			if (cmd == "!commands"):
				msg1 = "(mods only): \"!restartscript\", \"!restartserver\" \"!giveplus [user]\", \"!ban [user]\", \"!unban [user]\", \"!removeplus [user]\", \
				\"!disablechat\", \"!enablechat\", \"!disablegoto\", \"!enablegoto\", \"!setturnlength [lengthInMS]\", \"!setforfeitlength [lengthInMS]\""
				msg2 = "(plus only): \"!disableinternet\", \"!enableinternet\", \"!fixcontrollers\", \"!rr [user]\", \"!rainbow [user]\""
				msg3 = "(anyone): \"!restart1\", \"!restart2\", \"!restart3\", \"!banlist\", \"!pluslist\", \"!sublist\", \"!modlist\", \"!discord\", \"!site\", \"!source\", \"!internetstatus\", \"!randomgame\", \"!playing\", \"!goto [game]\""
				twitchBot.chat(msg1)
				twitchBot.chat(msg2)
				twitchBot.chat(msg3)

			if (cmd == "!discord"):
				msg = "Discord invite link: https://discord.gg/ARTbddH/"
				twitchBot.chat(msg)

			if (cmd == "!site"):
				msg = "https://twitchplaysnintendoswitch.com"
				twitchBot.chat(msg)

			if (cmd == "!source"):
				msg = "https://github.com/mfosse/twitchplays/ https://github.com/mfosse/switch-controller/ https://github.com/mfosse/streamr/"
				twitchBot.chat(msg)

			if (cmd == "!pluslist"):
				msg = "plus list: "
				for user in pluslist:
					msg += user + ", "
				msg = msg[:-2]
				twitchBot.chat(msg)

			if (cmd == "!modlist"):
				msg = "mod list: "
				for user in modlist:
					msg += user + ", "
				msg = msg[:-2]
				twitchBot.chat(msg)

			if (cmd == "!banlist"):
				msg = "ban list: "
				for user in banlist:
					msg += user + ", "
				msg = msg[:-2]
				twitchBot.chat(msg)

			if (cmd == "!sublist"):
				msg = "sub list: "
				for user in sublist:
					msg += user + ", "
				msg = msg[:-2]
				twitchBot.chat(msg)

			if (cmd == "!restart1" or cmd == "!restart"):
				# self.socketio.emit("restart")
				twitchBot.chat("Restarting lagless1!")
				os.system("taskkill /f /im streamr.exe")

			if (cmd == "!restart2"):
				twitchBot.chat("Restarting lagless2!")
				self.socketio.emit("restart2")

			if (cmd == "!restart3"):
				twitchBot.chat("Restarting lagless3!")
				self.socketio.emit("restart3")

			if (cmd == "!restartserver" and username in modlist):
				twitchBot.chat("Restarting the server! maybe @fosse if you're using this!")
				self.socketio.emit("restart server")

			if (cmd == "!restartscript" and username in modlist):
				twitchBot.chat("Restarting the python script!")
				with open("pluslist.pkl", "wb") as f:
					pickle.dump([pluslist], f)
				os.system("taskkill /f /im python.exe")

			if (cmd == "!disablegoto" and username in modlist):
				msg = "Disabling !goto"
				twitchBot.chat(msg)
				self.voting = True
			if (cmd == "!enablegoto" and username in modlist):
				msg = "Enabling !goto"
				twitchBot.chat(msg)
				self.voting = False

			if (cmd == "!disablechat" and username in modlist):
				msg = "Disabling chat commands!"
				twitchBot.chat(msg)
				self.chatEnabled = False
			if (cmd == "!enablechat" and username in modlist):
				msg = "Enabling chat commands!"
				twitchBot.chat(msg)
				self.chatEnabled = True

			if (cmd == "!lock" and username in pluslist):
				msg = "locking!"
				twitchBot.chat(msg)
				self.voting = True
				self.chatEnabled = False
				self.socketio.emit("lock")

			if (cmd == "!unlock" and username in modlist):
				msg = "Unlocking!"
				twitchBot.chat(msg)
				self.voting = False
				self.chatEnabled = True
				self.socketio.emit("unlock")

			if (cmd == "!1p" and username in modlist):
				msg = "Changing to 1 Player Mode!"
				twitchBot.chat(msg)
				self.socketio.emit("setMaxPlayers", 1)

			if (cmd == "!2p" and username in modlist):
				msg = "Changing to 2 Player Mode!"
				twitchBot.chat(msg)
				self.socketio.emit("setMaxPlayers", 2)

			if (cmd == "!3p" and username in modlist):
				msg = "Changing to 3 Player Mode!"
				twitchBot.chat(msg)
				self.socketio.emit("setMaxPlayers", 3)

			if (cmd == "!4p" and username in modlist):
				msg = "Changing to 4 Player Mode!"
				twitchBot.chat(msg)
				self.socketio.emit("setMaxPlayers", 4)

			if (cmd == "!5p" and username in modlist):
				msg = "Changing to 5 Player Mode!"
				twitchBot.chat(msg)
				self.socketio.emit("setMaxPlayers", 5)

			if (cmd == "!forcerefresh" and username in modlist):
				self.socketio.emit("forceRefresh")

			if (cmd == "!disableinternet" and username in pluslist):
				msg = "Disabling internet accesss!"
				twitchBot.chat(msg)
				self.socketio.emit("disableInternet")
			if (cmd == "!enableinternet" and username in pluslist):
				msg = "Enabling internet access!"
				twitchBot.chat(msg)
				self.socketio.emit("enableInternet")

			if (cmd == "!egg"):
				# msg = "Rickrolling!: " + commands[1]
				# twitchBot.chat(msg)
				self.socketio.emit("rickroll", username)

			if (cmd == "!rr"):
				self.socketio.emit("rickroll", username)


			if (cmd == "!rainbow"):
				self.socketio.emit("rainbow", username)

			# if (cmd == "!randomgame"):
			# 	auto_goto()

			if (cmd == "!playing"):
				msg = "The current player(s) are: "
				count = 0
				for player in self.currentPlayers:
					if (player != None):
						count += 1
						msg += player + ", "
				msg = msg[:-2]
				if (count == 0):
					msg = "No one is playing right now."

				twitchBot.chat(msg)


			if (cmd == "!fixcontrollers" and username in pluslist):
				twitchBot.chat("Fixing controller order!")
				# disable lagless while we do this:
				self.controllerEnabled = False
				self.chatEnabled = False

				# reset controller
				controller1.reset()
				# go home
				controller1.home = 1
				send_and_reset(0.1, 1)
				sleep(2)

				# navigate to re-pair section
				controller1.LY = STICK_MAX
				send_and_reset(0.1, 1)
				controller1.LX = STICK_MAX
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller1.LX = STICK_MAX
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller1.LX = STICK_MAX
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller1.a = 1
				send_and_reset(0.1, 1)
				sleep(0.5)

				sleep(3)

				# press a on all controllers, in the correct order
				controller1.a = 1
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller1.a = 1
				send_and_reset(0.1, 1, 0)
				sleep(2)
				controller2.a = 1
				send_and_reset(0.1, 1, 1)
				sleep(2)
				controller3.a = 1
				send_and_reset(0.1, 1, 2)
				sleep(2)
				controller4.a = 1
				send_and_reset(0.1, 1, 3)
				sleep(2)
				# controller3.a = 1
				# send_and_reset3(0.1, 1)
				# sleep(1)
				# controller4.a = 1
				# send_and_reset4(0.1, 1)

				# go back to the game
				controller1.a = 1
				send_and_reset(0.1, 1)
				controller1.a = 1
				send_and_reset(0.1, 1)
				sleep(2)
				controller1.b = 1
				send_and_reset(0.1, 1)
				sleep(1)
				controller1.LY = STICK_MIN
				send_and_reset(0.1, 1)
				sleep(2)
				controller1.LX = STICK_MIN
				send_and_reset(1, 1)
				controller1.a = 1
				send_and_reset(0.1, 1)


				# re-enable lagless
				self.controllerEnabled = True
				self.chatEnabled = True


		if len(commands) == 2:

			if (commands[0] == "!giveplus" and username in modlist):

				msg = "Giving plus permission to: " + commands[1]
				twitchBot.chat(msg)

				pluslist.append(commands[1])

				# write pluslist to file:
				with open("pluslist.pkl", "wb") as f:
					pickle.dump([pluslist], f)

			if (commands[0] == "!removeplus" and username in modlist):

				msg = "Removing plus permissions from: " + commands[1]
				twitchBot.chat(msg)

				# revoke plus permission:
				if commands[1] in pluslist:
					pluslist.remove(commands[1])

				# write pluslist to file:
				with open("pluslist.pkl", "wb") as f:
					pickle.dump([pluslist], f)


			if (commands[0] == "!ban" and username in modlist):
				msg = "Banning: " + commands[1]
				twitchBot.chat(msg)
				banlist.append(commands[1])
				self.socketio.emit("banlist", banlist)

				# write banlist to file:
				with open("banlist.pkl", "wb") as f:
					pickle.dump([banlist], f)
				

			if (commands[0] == "!unban" and username in modlist):
				msg = "Unbanning: " + commands[1]
				twitchBot.chat(msg)
				banlist.remove(commands[1])
				self.socketio.emit("banlist", banlist)

				# write banlist to file:
				with open("banlist.pkl", "wb") as f:
					pickle.dump([banlist], f)

			if (commands[0] == "!setturnlength" and username in modlist):
				msg = "Setting turn length to: " + commands[1]
				twitchBot.chat(msg)
				self.socketio.emit("setTurnLength", commands[1])

			if (commands[0] == "!setforfeitlength" and username in modlist):
				msg = "Setting forfeit length to: " + commands[1]
				twitchBot.chat(msg)
				self.socketio.emit("setForfeitLength", commands[1])

			if (commands[0] == "!rr" and username in pluslist):
				self.socketio.emit("rickroll", commands[1])

			if (commands[0] == "!rainbow" and username in pluslist):
				self.socketio.emit("rainbow", commands[1])

			# if (commands[0] == "!game" and username in modlist):
			# 	self.currentGame = commands[1]
			# 	msg = "Setting game to: " + commands[1]
			# 	twitchBot.chat(msg)


			# if (commands[0] == "!mod" and username in adminlist):
			# 	msg = "Modding: " + commands[1]
			# 	twitchBot.chat(msg)
			# 	banlist.append(commands[1])
			# 	self.socketio.emit("banlist", banlist)

			# if (commands[0] == "!unmod" and username in adminlist):
			# 	msg = "UnModding: " + commands[1]
			# 	twitchBot.chat(msg)
			# 	modlist.remove(commands[1])
			# 	self.socketio.emit("banlist", banlist)


			# goto commands:
			if (commands[0] == "!goto" or (commands[0] == "!forcegoto" and username in modlist) or (commands[0] == "!setgame" and username in modlist)):
				cmd = commands[1]

				goto = None
				waitTime = 0
				imageLoc = ""
				nameofgame = ""

				if (cmd not in gameList):
					return

				if (cmd == "smo"):
					imageLoc, waitTime, nameofgame = "icons/smo.png", 30, "Super Mario Odyssey"
				if (cmd == "botw"):
					imageLoc, waitTime, nameofgame = "icons/botw.png", 20, "The Legend of Zelda: Breath of the Wild"
				if (cmd == "celeste"):
					imageLoc, waitTime, nameofgame = "icons/celeste.png", 10, "Celeste"
				if (cmd == "kirby"):
					imageLoc, waitTime, nameofgame = "icons/kirby.png", 10, "Kirby: Star Allies"
				if (cmd == "splatoon2"):
					imageLoc, waitTime, nameofgame = "icons/splatoon2.png", 10, "Splatoon 2"
				if (cmd == "sonic"):
					imageLoc, waitTime, nameofgame = "icons/sonic.png", 10, "Sonic Mania"
				if (cmd == "mk8"):
					imageLoc, waitTime, nameofgame = "icons/mk8.png", 10, "Mario Kart 8"
				if (cmd == "arms"):
					imageLoc, waitTime, nameofgame = "icons/arms.png", 10, "Arms"
				if (cmd == "skyrim"):
					imageLoc, waitTime, nameofgame = "icons/skyrim.png", 40, "The Elder Scrolls V: Skyrim"
				if (cmd == "rocketleague"):
					imageLoc, waitTime, nameofgame = "icons/rocketleague.png", 10, "Rocket League"
				if (cmd == "wizard"):
					imageLoc, waitTime, nameofgame = "icons/wizard.png", 10, "Wizard of Legend"
				if (cmd == "pokemonquest"):
					imageLoc, waitTime, nameofgame = "icons/pokemonquest.png", 10, "Pokemon Quest"
				if (cmd == "torquel"):
					imageLoc, waitTime, nameofgame = "icons/torquel.png", 10, "TorqueL"
				if (cmd == "fallout"):
					imageLoc, waitTime, nameofgame = "icons/fallout.png", 10, "Fallout Shelter"
				if (cmd == "fortnite"):
					imageLoc, waitTime, nameofgame = "icons/fortnite2.png", 10, "Fortnite"
				if (cmd == "jackbox3"):
					imageLoc, waitTime, nameofgame = "icons/jackbox3.png", 10, "The Jackbox Party Pack 3"
				if (cmd == "jackbox4"):
					imageLoc, waitTime, nameofgame = "icons/jackbox4.png", 10, "The Jackbox Party Pack 4"
				if (cmd == "shovel"):
					imageLoc, waitTime, nameofgame = "icons/shovel.png", 10, "Shovel Knight"
				if (cmd == "octopath"):
					imageLoc, waitTime, nameofgame = "icons/octopathprologuedemo.png", 10, "Octopath Traveler"
				if (cmd == "explosion"):
					imageLoc, waitTime, nameofgame = "icons/explosion.png", 10, "Graceful Explosion Machine"
				if (cmd == "human"):
					imageLoc, waitTime, nameofgame = "icons/human.png", 10, "Human: Fall Flat"
				if (cmd == "snipperclips"):
					imageLoc, waitTime, nameofgame = "icons/snipperclips.png", 10, "Snipperclips: Cut It Out, Together!"
				if (cmd == "paladins"):
					imageLoc, waitTime, nameofgame = "icons/paladins.png", 10, "Paladins"
				if (cmd == "hollow"):
					imageLoc, waitTime, nameofgame = "icons/hollow.png", 10, "Hollow Knight"
				if (cmd == "mta"):
					imageLoc, waitTime, nameofgame = "icons/mta.png", 10, "Mario Tennis Aces"
				# if (cmd == "!goto cave"):
				# 	imageLoc, waitTime, nameofgame = "icons/cave.png", 10, "Cave Story"
				# if (cmd == "!goto isaac"):
				# 	imageLoc, waitTime, nameofgame = "icons/isaac.png", 10, "The Binding of Isaac: Afterbirth"
				# if (cmd == "!goto mario"):
				# 	imageLoc, waitTime, nameofgame = "icons/mario.png", 10, "Twitch Plays"


				if (self.currentGame == nameofgame):
					msg = "We're already playing this game!"
					twitchBot.chat(msg)
					return

				if (commands[0] == "!setgame"):
					self.currentGame = nameofgame
					msg = "!game " + nameofgame
					twitchBot.chat(msg)
					return



				if (commands[0] == "!forcegoto"):
					goto = self.goto_game
				else:
					goto = self.goto_game_vote

				goto(imageLoc, waitTime, nameofgame)

		if (not self.chatEnabled):
			return

		if (len(commands) > 20):
			valid = False

		if (not valid):
			commands = []

		for cmd in commands:
			commandQueue.append(cmd)



	def decreaseQueue(self):

		#sleep(0.0001)

		self.end = time.time()
		diffInMilliSeconds = (self.end - self.start)*1000
		if (diffInMilliSeconds > 8.33333):
			self.start = time.time()
			#controller1.send(controller1.output)

			if (len(commandQueue) > 0):
				nextCommands.append(commandQueue[0])
				del commandQueue[0]

			duration = 0
			reset = 1

			if (len(nextCommands) > 0):
				# print(nextCommands)
				cmd = nextCommands[-1]
				del nextCommands[-1]

				if (cmd == "sssleft" or cmd == "sssl"):
					controller1.LX = STICK_MIN
					duration = 0.01
					reset = 1
				if (cmd == "sssright" or cmd == "sssr"):
					controller1.LX = STICK_MAX
					duration = 0.01
					reset = 1
				if (cmd == "sssup" or cmd == "sssu"):
					controller1.LY = STICK_MIN
					duration = 0.01
					reset = 1
				if (cmd == "sssdown" or cmd == "sssd"):
					controller1.LY = STICK_MAX
					duration = 0.01
					reset = 1

				if (cmd == "ssleft" or cmd == "ssl"):
					controller1.LX = STICK_MIN
					duration = 0.1
					reset = 1
				if (cmd == "ssright" or cmd == "ssr"):
					controller1.LX = STICK_MAX
					duration = 0.1
					reset = 1
				if (cmd == "ssup" or cmd == "ssu"):
					controller1.LY = STICK_MIN
					duration = 0.1
					reset = 1
				if (cmd == "ssdown" or cmd == "ssd"):
					controller1.LY = STICK_MAX
					duration = 0.1
					reset = 1

				if (cmd == "sleft" or cmd == "sl"):
					controller1.LX = STICK_MIN
					duration = 0.3
					reset = 1
				if (cmd == "sright" or cmd == "sr"):
					controller1.LX = STICK_MAX
					duration = 0.3
					reset = 1
				if (cmd == "sup" or cmd == "su"):
					controller1.LY = STICK_MIN
					duration = 0.3
					reset = 1
				if (cmd == "sdown" or cmd == "sd"):
					controller1.LY = STICK_MAX
					duration = 0.3
					reset = 1

				if (cmd == "left" or cmd == "l"):
				# if (cmd == "left"):
					controller1.LX = STICK_MIN
					duration = 0.6
					reset = 1
				if (cmd == "right" or cmd == "r"):
				# if (cmd == "right"):
					controller1.LX = STICK_MAX
					duration = 0.6
					reset = 1
				if (cmd == "up" or cmd == "u"):
					controller1.LY = STICK_MIN
					duration = 0.6
					reset = 1
				if (cmd == "down" or cmd == "d"):
					controller1.LY = STICK_MAX
					duration = 0.6
					reset = 1

				if (cmd == "hleft" or cmd == "hl"):
					controller1.LX = STICK_MIN
					duration = 1.5
					reset = 1
				if (cmd == "hright" or cmd == "hr"):
					controller1.LX = STICK_MAX
					duration = 1.5
					reset = 1
				if (cmd == "hup" or cmd == "hu"):
					controller1.LY = STICK_MIN
					duration = 1.5
					reset = 1
				if (cmd == "hdown" or cmd == "hd"):
					controller1.LY = STICK_MAX
					duration = 1.5
					reset = 1

				if (cmd == "hhleft"):
					controller1.LX = STICK_MIN
					duration = 4.0
					reset = 1
				if (cmd == "hhright"):
					controller1.LX = STICK_MAX
					duration = 4.0
					reset = 1
				if (cmd == "hhup"):
					controller1.LY = STICK_MIN
					duration = 4.0
					reset = 1
				if (cmd == "hhdown"):
					controller1.LY = STICK_MAX
					duration = 4.0
					reset = 1

				
				if (cmd == "dleft" or cmd == "dl"):
					controller1.dpad = DPAD_LEFT
					duration = 0.3
					reset = 1
				if (cmd == "dright" or cmd == "dr"):
					controller1.dpad = DPAD_RIGHT
					duration = 0.3
					reset = 1
				if (cmd == "dup" or cmd == "du"):
					controller1.dpad = DPAD_UP
					duration = 0.3
					reset = 1
				if (cmd == "ddown" or cmd == "dd"):
					controller1.dpad = DPAD_DOWN
					duration = 0.3
					reset = 1



				if (cmd == "slook left" or cmd == "sll"):
					controller1.RX = STICK_MIN
					duration = 0.1
					reset = 1
				if (cmd == "slook right" or cmd == "slr"):
					controller1.RX = STICK_MAX
					duration = 0.1
					reset = 1
				if (cmd == "slook up" or cmd == "slu"):
					controller1.RY = STICK_MIN
					duration = 0.1
					reset = 1
				if (cmd == "slook down" or cmd == "sld"):
					controller1.RY = STICK_MAX
					duration = 0.1
					reset = 1

				if (cmd == "look left" or cmd == "ll"):
					controller1.RX = STICK_MIN
					duration = 0.3
					reset = 1
				if (cmd == "look right" or cmd == "lr"):
					controller1.RX = STICK_MAX
					duration = 0.3
					reset = 1
				if (cmd == "look up" or cmd == "lu"):
					controller1.RY = STICK_MIN
					duration = 0.3
					reset = 1
				if (cmd == "look down" or cmd == "ld"):
					controller1.RY = STICK_MAX
					duration = 0.3
					reset = 1

				if (cmd == "hlook left" or cmd == "hll"):
					controller1.RX = STICK_MIN
					duration = 0.6
					reset = 1
				if (cmd == "hlook right" or cmd == "hlr"):
					controller1.RX = STICK_MAX
					duration = 0.6
					reset = 1
				if (cmd == "hlook up" or cmd == "hlu"):
					controller1.RY = STICK_MIN
					duration = 0.6
					reset = 1
				if (cmd == "hlook down" or cmd == "hld"):
					controller1.RY = STICK_MAX
					duration = 0.6
					reset = 1
				
				if (cmd == "a"):
					controller1.a = 1
					duration = 0.3
					reset = 1
				if (cmd == "ha"):
					controller1.a = 1
					duration = 0.5
					reset = 1
				if (cmd == "sb"):
					controller1.b = 1
					duration = 0.1
					reset = 1
				if (cmd == "b"):
					controller1.b = 1
					duration = 0.4
					reset = 1
				if (cmd == "hb"):
					controller1.b = 1
					duration = 0.5
					reset = 1
				if (cmd == "hhb"):
					controller1.b = 1
					duration = 0.8
					reset = 1
				if (cmd == "hhhb"):
					controller1.b = 1
					duration = 1.8
					reset = 1
				if (cmd == "x"):
					controller1.x = 1
					duration = 0.3
					reset = 1
				if (cmd == "hx"):
					controller1.x = 1
					duration = 0.5
					reset = 1
				if (cmd == "y"):
					controller1.y = 1
					duration = 0.3
					reset = 1
				if (cmd == "hy"):
					controller1.y = 1
					duration = 0.7
					reset = 1
				if (cmd == "lstick"):
					controller1.lstick = 1
					duration = 0.1
					reset = 1
				if (cmd == "rstick"):
					controller1.rstick = 1
					duration = 0.1
					reset = 1
				if (cmd == "l"):
					controller1.l = 1
					duration = 0.1
					reset = 1
				if (cmd == "r"):
					controller1.r = 1
					duration = 0.1
					reset = 1
				if (cmd == "hr"):
					controller1.r = 1
					duration = 1
					reset = 1
				if (cmd == "zl"):
					controller1.zl = 1
					duration = 0.1
					reset = 1
				if (cmd == "zr"):
					controller1.zr = 1
					duration = 0.1
					reset = 1
				if (cmd == "minus"):
					controller1.minus = 1
					duration = 0.1
					reset = 1
				if (cmd == "plus"):
					controller1.plus = 1
					duration = 0.1
					reset = 1
				if (cmd == "home"):
					controller1.home = 1
					duration = 0.1
					reset = 1

				if (cmd == "long jump"):
					controller1.LY = STICK_MIN
					duration = 0.6
					nextCommands.insert(0, "long jump2")
					reset = 0
				if (cmd == "long jump2"):
					controller1.LY = STICK_MIN
					controller1.zl = 1
					duration = 0.01
					nextCommands.insert(0, "long jump3")
					reset = 0
				if (cmd == "long jump3"):
					controller1.LY = STICK_MIN
					controller1.b = 1
					duration = 0.1
					nextCommands.insert(0, "long jump4")
					reset = 0
				if (cmd == "long jump4"):
					controller1.LY = STICK_MIN
					controller1.b = 1
					controller1.zl = 0
					duration = 1
					reset = 1

				if (cmd == "jump forward"):
					controller1.LY = STICK_MIN
					duration = 0.3
					nextCommands.insert(0, "jump forward2")
					reset = 0
				if (cmd == "jump forward2"):
					controller1.LY = STICK_MIN
					controller1.b = 1
					duration = 0.4
					reset = 1

				if (cmd == "jump back"):
					controller1.LY = STICK_MAX
					duration = 0.3
					nextCommands.insert(0, "jump forward2")
					reset = 0
				if (cmd == "jump back2"):
					controller1.LY = STICK_MAX
					controller1.b = 1
					duration = 0.4
					reset = 1

				if (cmd == "cap bounce"):
					# b, y, sdive, hy, y, sdive
					nextCommands.insert(0, "b")
					nextCommands.insert(0, "y")
					nextCommands.insert(0, "sdive")
					nextCommands.insert(0, "hy")
					nextCommands.insert(0, "y")
					nextCommands.insert(0, "sdive")

				if (cmd == "swim"):
					# b, b, b, b
					nextCommands.insert(0, "b")
					nextCommands.insert(0, "b")
					nextCommands.insert(0, "b")
					nextCommands.insert(0, "b")


				if (cmd == "sdive"):
					controller1.zl = 1
					duration = 0.1
					nextCommands.insert(0, "sdive2")
					reset = 0
				if (cmd == "sdive2"):
					controller1.y = 1
					duration = 0.1
					reset = 1

				if (cmd == "dive"):
					controller1.b = 1
					duration = 0.1
					nextCommands.insert(0, "dive2")
					reset = 0
				if (cmd == "dive2"):
					controller1.zl = 1
					duration = 0.01
					nextCommands.insert(0, "dive3")
					reset = 0
				if (cmd == "dive3"):
					controller1.y = 1
					duration = 0.1
					reset = 1

				if (cmd == "hdive"):
					controller1.b = 1
					duration = 0.2
					nextCommands.insert(0, "hdive2")
					reset = 0
				if (cmd == "hdive2"):
					controller1.zl = 1
					duration = 0.01
					nextCommands.insert(0, "hdive3")
					reset = 0
				if (cmd == "hdive3"):
					controller1.y = 1
					duration = 0.1
					reset = 1

				if (cmd == "roll"):
					controller1.zl = 1
					duration = 0.01
					nextCommands.insert(0, "roll2")
					reset = 0
				if (cmd == "roll2"):
					controller1.y = 1
					duration = 0.1
					reset = 1

				if (cmd == "backflip" or cmd == "bf" or cmd == "back flip"):
					controller1.zl = 1
					duration = 0.01
					nextCommands.insert(0, "backflip2")
					reset = 0
				if (cmd == "backflip2"):
					controller1.b = 1
					duration = 0.1
					reset = 1

				if (cmd == "ground pound" or cmd == "gp" or cmd == "groundpound"):
					controller1.b = 1
					duration = 0.01
					nextCommands.insert(0, "ground pound2")
					reset = 0
				if (cmd == "ground pound2"):
					controller1.zl = 1
					duration = 0.1
					reset = 1



				if (cmd == "sprint"):
					controller1.LY = STICK_MIN
					controller1.b = 1
					duration = 0.6
					reset = 1
				if (cmd == "hsprint"):
					controller1.LY = STICK_MIN
					controller1.b = 1
					duration = 1.5
					reset = 1
				if (cmd == "hhsprint"):
					controller1.LY = STICK_MIN
					controller1.b = 1
					duration = 3
					reset = 1




				d = 0.001

				if (cmd == "spin"):
					controller1.LX = STICK_CENTER
					controller1.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin2")
					reset = 0
				if (cmd == "spin2"):
					controller1.LX = STICK_MAX
					controller1.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin3")
					reset = 0
				if (cmd == "spin3"):
					controller1.LX = STICK_MAX
					controller1.LY = STICK_CENTER
					duration = d
					nextCommands.insert(0, "spin4")
					reset = 0
				if (cmd == "spin4"):
					controller1.LX = STICK_CENTER
					controller1.LY = STICK_MAX
					duration = d
					nextCommands.insert(0, "spin5")
					reset = 0
				if (cmd == "spin5"):
					controller1.LX = STICK_MIN
					controller1.LY = STICK_MAX
					duration = d
					nextCommands.insert(0, "spin6")
					reset = 0
				if (cmd == "spin6"):
					controller1.LX = STICK_MIN
					controller1.LY = STICK_CENTER
					duration = d
					nextCommands.insert(0, "spin7")
					reset = 0
				if (cmd == "spin7"):
					controller1.LX = STICK_MIN
					controller1.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin8")
					reset = 0
				if (cmd == "spin8"):
					controller1.LX = STICK_CENTER
					controller1.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin9")
					reset = 0
				if (cmd == "spin9"):
					controller1.LX = STICK_CENTER
					controller1.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin10")
					reset = 0
				if (cmd == "spin10"):
					controller1.LX = STICK_MAX
					controller1.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin11")
					reset = 0
				if (cmd == "spin11"):
					controller1.LX = STICK_MAX
					controller1.LY = STICK_CENTER
					duration = d
					nextCommands.insert(0, "spin12")
					reset = 0
				if (cmd == "spin12"):
					controller1.LX = STICK_CENTER
					controller1.LY = STICK_MAX
					duration = d
					nextCommands.insert(0, "spin13")
					reset = 0
				if (cmd == "spin13"):
					controller1.LX = STICK_MIN
					controller1.LY = STICK_MAX
					duration = d
					nextCommands.insert(0, "spin14")
					reset = 0
				if (cmd == "spin14"):
					controller1.LX = STICK_MIN
					controller1.LY = STICK_CENTER
					duration = d
					nextCommands.insert(0, "spin15")
					reset = 0
				if (cmd == "spin15"):
					controller1.LX = STICK_MIN
					controller1.LY = STICK_MIN
					duration = d
					nextCommands.insert(0, "spin16")
					reset = 0
				if (cmd == "spin16"):
					controller1.LX = STICK_CENTER
					controller1.LY = STICK_MIN
					duration = d
					#nextCommands.insert(0, "spin6")
					reset = 1


				if ("+" in cmd):
					btns = [x.strip() for x in cmd.split("+")]

					for btn in btns:
						duration = 0.3
						reset = 1

						if ("s" in btn):
							duration = 0.01
						if ("h" in btn):
							duration = 0.6
						if ("hh" in btn):
							duration = 1.5
						if ("hhh" in btn):
							duration = 5

						btn = btn.replace("s","")
						btn = btn.replace("h","")

						if (btn == "left"):
							controller1.LX = STICK_MIN
						if (btn == "rigt"):
							controller1.LX = STICK_MAX
						if (btn == "up"):
							controller1.LY = STICK_MIN
						if (btn == "down"):
							controller1.LY = STICK_MAX
						if (btn == "dleft"):
							controller1.dpad = DPAD_LEFT
						if (btn == "drigt"):
							controller1.dpad = DPAD_RIGHT
						if (btn == "dup"):
							controller1.dpad = DPAD_UP
						if (btn == "ddown"):
							controller1.dpad = DPAD_DOWN
						
						if (btn == "look left"):
							controller1.RX = STICK_MIN
						if (btn == "look rigt"):
							controller1.RX = STICK_MAX
						if (btn == "look up"):
							controller1.RY = STICK_MIN
						if (btn == "look down"):
							controller1.RY = STICK_MAX
						if (btn == "a"):
							controller1.a = 1
						if (btn == "b"):
							controller1.b = 1
						if (btn == "x"):
							controller1.x = 1
						if (btn == "y"):
							controller1.y = 1
						if (btn == "l"):
							controller1.l = 1
						if (btn == "r"):
							controller1.r = 1
						if (btn == "zl"):
							controller1.zl = 1
						if (btn == "zr"):
							controller1.zr = 1
						if (btn == "minus"):
							controller1.minus = 1
				send_and_reset(duration, reset)



	def loop(self):

		# control switch here:

		self.botend = time.time()
		diffInMilliSeconds = (self.botend - self.botstart)*1000
		if (diffInMilliSeconds > 1000*60*5):
			self.botstart = time.time()

			self.socketio.emit("joinSecure", {"room": "controller", "password": ROOM_SECRET})
			self.socketio.emit("banlist", banlist)
			self.socketio.emit("modlist", modlist)
			self.socketio.emit("pluslist", pluslist)
			self.socketio.emit("sublist", sublist)
			
			msg = "Type \"!help\" for help! Join the discord server! https://discord.gg/ARTbddH/\
			hate the stream delay? go here! https://twitchplaysnintendoswitch.com"
			twitchBot.chat(msg)

		self.controllerEnd = time.time()
		diffInMilliSeconds2 = (self.controllerEnd - self.controllerStart)*1000
		if (diffInMilliSeconds2 > 6000):
			self.controllerStart = time.time()

			self.socketio.emit("joinSecure", {"room": "controller", "password": ROOM_SECRET})
			self.socketio.emit("banlist", banlist)
			self.socketio.emit("modlist", modlist)
			self.socketio.emit("pluslist", pluslist)
			self.socketio.emit("sublist", sublist)


		# get modlist:
		# with urllib.request.urlopen("https://tmi.twitch.tv/group/user/twitchplaysconsoles/chatters") as url:
		# 	data = json.loads(url.read().decode())
		# 	print(data)


		response = twitchBot.stayConnected()
		if (response != "none"):
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

# https://stackoverflow.com/questions/2697039/python-equivalent-of-setinterval
# class ThreadJob(threading.Thread):
# 	def __init__(self,callback,event,interval):
# 		'''runs the callback function after interval seconds

# 		:param callback:  callback function to invoke
# 		:param event: external event for controlling the update operation
# 		:param interval: time in seconds after which are required to fire the callback
# 		:type callback: function
# 		:type interval: int
# 		'''
# 		self.callback = callback
# 		self.event = event
# 		self.interval = interval
# 		super(ThreadJob,self).__init__()

# 	def run(self):
# 		while not self.event.wait(self.interval):
# 			self.callback()

# event = threading.Event()

# k = ThreadJob(auto_goto, event, 10)
# k.start()

# def set_interval(func, sec):
# 	def func_wrapper():
# 		set_interval(func, sec)
# 		func()
# 	t = threading.Timer(sec, func_wrapper)
# 	t.start()
# 	return t

# set_interval(auto_goto, 50)

interval = 60*60

def auto_goto():
	if (len(client.currentPlayers) == 0):
		game = random.choice(gameList)
		msg = "!goto " + game
		twitchBot.chat(msg)
		sleep(1)
		msg = "yea"
		twitchBot.chat(msg)
		try:
			autoGotoTimer.cancel()
		except:
			pass

		msg = "!disableinternet"
		twitchBot.chat(msg)

	autoGotoTimer = Timer(interval, auto_goto)
	autoGotoTimer.start()

autoGotoTimer = Timer(interval, auto_goto)
autoGotoTimer.start()




lockInterval = 1

def emergency_lock():

	x1 = 319 - 1920;# left monitor
	y1 = 61 + 360;
	width = 1280
	height = 720
	windowName = "OBS"
	iconLoc = client.findImage2("icons/screenshots/settingspage.png", x1, y1, width, height, windowName, 0.6)

	if (iconLoc != None):
		if (client.voting == False or client.chatEnabled == True):
			msg = "Emergency Locking!"
			twitchBot.chat(msg)
			client.voting = True
			client.chatEnabled = False
			client.socketio.emit("lock")

		if (client.currentPlayers[0] not in modlist):
			controller1.b = 1
			send_and_reset(0.1)
			controller1.b = 1
			send_and_reset(0.1)
			controller1.b = 1
			send_and_reset(0.1)
			controller1.b = 1
			send_and_reset(0.1)

	lockTimer = Timer(lockInterval, emergency_lock)
	lockTimer.start()

lockTimer = Timer(lockInterval, emergency_lock)
lockTimer.start()

client = Client()
while True:
	client.loop()
	sleep(0.0001)