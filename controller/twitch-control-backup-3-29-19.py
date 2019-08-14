
# windows stuff
import ctypes
from ctypes import *
import win32api
import win32con
import win32com
import win32com.client
import win32gui
import win32ui

# check for duplicate programs:
import pywinauto
import sys

pwa_app = pywinauto.application.Application()

try:
	w_handle = pywinauto.findwindows.find_windows(title="script")[1]
	print("found")
	sys.exit()
except IndexError:
	print("not found")

# change obs64 window title to "switch"
# https://gist.github.com/mouseroot/3431554
# from ctypes import *
class Win32api():
	def __init__(self):
		#msdn for what dll to use
		self.SetWindowText = windll.user32.SetWindowTextA
		self.FindWindow = windll.user32.FindWindowA
	def String(self, s):
		# https://stackoverflow.com/questions/37888565/python-3-5-ctypes-typeerror-bytes-or-integer-address-expected-instead-of-str
		return c_char_p(s.encode("utf-8"))
		# return c_wchar_p(s)
win = Win32api()
try:
	hwnd = pywinauto.findwindows.find_windows(title="obs64")[0]
	# hwnd = win.FindWindow(None, win.String("obs64"))
	win.SetWindowText(hwnd, win.String("switch"))
	print("changing obs64 to \"switch\"")
except IndexError:
	print("couldn't find obs64 window")

# set high priority:
# https://stackoverflow.com/questions/1023038/change-process-priority-in-python-cross-platform
import psutil, os
p = psutil.Process(os.getpid())
p.nice(psutil.HIGH_PRIORITY_CLASS)

# time
from threading import Timer
import threading
import time
from time import sleep
import asyncio

# switch controller:
from SwitchController.SwitchController import *
from SwitchController.SwitchController2 import SwitchController2

# xbox controller:
# from XboxController.XboxController import XboxController

# twitch:
from TwitchBot.TwitchBot import *
# get sub list:
from TwitchBot.TwitchSubs import *

# discord:
# from DiscordBot.DiscordBot import *

# youtube:
from YoutubeBot.YoutubeBot import *

# socketio
import socketio

from threading import Thread

# OpenCV / image utils:
import imutils
import cv2
from PIL import Image

# set window title:
ctypes.windll.kernel32.SetConsoleTitleW("script")

# to get json info
import urllib.request, json

# to exit:
import sys

# numpy
import numpy as np

# save info
import pickle

# random
import random
from random import randint

def killscript():
	# sys.exit()
	os.system("taskkill /f /im python.exe")
	os.system("taskkill /f /im python.exe")

sio = socketio.Client()
try:
	sio.connect("http://remotegames.io:8100")
except:
	print("sio connection failed")
	killscript()

connectCounter = 30
connectMax = connectCounter
controllers = [SwitchController(), SwitchController(), SwitchController(), SwitchController(), SwitchController2()]

# xboxController1 = XboxController()

for i in range(0, 4):
	com = "COM" + str(i + 1)
	try:
		controllers[i].connect(com)
		# controllers[i].start()
	except:
		print("controllers[" + str(i) + "] error")

# xbox:
try:
	# controllers[4].connect("COM10")
	controllers[4].connect(1)
except:
	print("controller4 error")

# twitch bot:
twitchBot = TwitchBot()
try:
	twitchBot.connect(HOST, PASS2, PORT, CHAN, NICK2)
except:
	print("twitchbot connection failed")
	killscript()

# discord bot:
# discordBot = DiscordBot()
# discordBotThread = threading.Thread(target=discordBot.run, args=(DISCORDBOT_TOKEN,))
# discordBotThread.start()

# youtube bot:
# youtubeBot = YoutubeBot()
# youtubeBotThread = threading.Thread(target=youtubeBot.main)
# youtubeBotThread.start()


def accurateSleep(duration):
	s = time.time()
	e = time.time()
	diffInMilliSeconds = 0

	while (diffInMilliSeconds < duration):
		e = time.time()
		diffInMilliSeconds = (e - s) * 1000

sendThread1 = Thread(target=sleep, args=())
sendThread2 = Thread(target=sleep, args=())
# sendThread1.start()
# sendThread1.join()

def send_and_reset(duration=0.1, reset=1, cNum=0):
	# if (cNum == 1):
	# 	return
	try:
		controller = controllers[cNum]
		controller.setBtns()
		controller.queue_send()

		if (duration > 0):
			sleep(duration)

		if (reset):
			controller.reset()
			controller.queue_send()
	except:
		print("controller send error")

# def thread_destroyer(thread, time):
# 	sleep(time)
# 	thread.exit()
# 	print("exited thread")

def round_down(num, divisor):
	return num - (num % divisor)

def send_message(msg, destination="twitch"):
	# sleep(0.2)
	if (destination == "twitch" or destination == "all"):
		try:
			if (len(msg) > 300):
				# split into 2 parts:
				firstpart, secondpart = msg[:len(msg)//2], msg[len(msg)//2:]
				send_message(firstpart, "twitch")
				send_message(secondpart, "twitch")
			else:
				twitchBot.send_message(msg)
		except:
			print("Twitch send_message error")
	if (destination == "youtube" or destination == "all"):
		try:
			if (len(msg) > 199):
				# split into 2 parts:
				firstpart, secondpart = msg[:len(msg)//2], msg[len(msg)//2:]
				send_message(firstpart, "youtube")
				send_message(secondpart, "youtube")
			# else:
			# 	youtubeBot.send_message(msg)
		except:
			print("Youtube send_message error")
	if (destination == "site" or destination == "all"):
		try:
			if (len(msg) > 400):
				# split into 2 parts:
				firstpart, secondpart = msg[:len(msg)//2], msg[len(msg)//2:]
				send_message(firstpart, "site")
				send_message(secondpart, "site")
			else:
				sio.emit("botMessage", msg)
		except:
			print("site send_message error")


switchGameList1 = []
switchGameList2 = []
gameList = ["baba", "tetris", "deltarune", "nsmbud", "smash", "botw", "celeste", "smo", "katamari", "undertale", "brawlhalla", "nes", "mta", "hollow", "paladins", "snipperclips", "mk8", "human", "shovelknight", "explosion", "jackbox4", "jackbox3", "skyrim", "splatoon2", "rocketleague", "wizard", "sonic", "arms", "kirby", "fortnite", "torquel"]
xboxGameList1 = ["Apex Legends", "Battleblock Theater", "Borderlands", "Braid", "Call of Duty(R): Black Ops 4", "Call of Duty(R): WaW", "Castle Crashers", "Celeste", "Crackdown",
"Crackdown 3: Campaign", "Crackdown 3: Wrecking Zone", "DOOM", "Fallout 3", "Forza Horizon 4", "Grand Theft Auto V", "GTA IV",
"Halo 5: Guardians", "Halo: Reach", "Halo: The Master Chief Collection", "Hue", "LEGO Star Wars: TCS", "LEGO(C) Indiana Jones(TM)",
"Minecraft", "Modern Warfare(R) 3", "Overwatch: Origins Edition", "PUBG", "Q.U.B.E. 2", "Red Dead Redemption 2", "Rocket League(R)",
"Sea of Thieves", "Super Lucky's Tale", "Terraria"]
xboxGameList2 = ["apex", "battleblock", "borderlands", "braid", "bo4", "waw", "castle", "celeste", "crackdown", "crackdown3",
"crackdown3w", "doom", "fallout3", "forzah4", "gta5", "gta4", "halo5", "halor", "halot", "hue", "legostar", "legojones",
"minecraft", "mw3", "overwatch", "pubg", "qube2", "rdr2", "rocketleague", "thieves", "lucky", "terraria"]
# plusCommands = []
# modCommands = []
# anyCommands = []
validCommands = ["!xboxsetgame", "!xboxforcegoto", "!xboxgames", "!xboxgamelist", "!gotoxbox", "!disablegyro", "!enablegyro", "!unlockqueues", "!lockqueues", "!friendcode", "!fc", "!expired", "!gamelist", "!source", "!playing", "!randomgame", "!status", "!rainbow", "!setgame", "!forcegoto", "!sublist", "!4p", "!3p", "!2p", "!1p", "!modlist", "!lock", "!egg", "!rr", "!discord", "!games", "!setforfeitlength", "!setturnlength", "!banlist", "!disableinternet", "!enableinternet", "!forcerefresh", "nay", "yea", "!enablechat", "!disablechat", "!enablegoto", "!disablegoto", "!unmod", "!mod", "!fixcontrollers", "!pluslist", "!unban", "!ban", "!removeplus", "!giveplus", "!commands", "!restart", "!restart1", "!restart2", "!restart3", "!restartscript", "!restartserver", "!help", "votenay", "voteyea", "!goto", "hhsprint", "hsprint", "sprint", "!controls", "!goto", "home", "lstick", "rstick", "spin", "swim", "back flip", "ground pound", "groundpound", "gp", "bf", "cap bounce", "sdive", "sdive2", "hdive", "hdive2", "hdive3", "dive", "dive2", "dive3", "roll", "roll2", "backflip", "backflip2", "sssu", "sssd", "sssl", "sssr", "sb", "suu", "", "up", "down", "left", "right", "u", "d", "l", "r", "hup", "hdown", "hleft", "hright", "hhup", "hhdown", "hhleft", "hhright", "hu", "hd", "hl", "hr", "su", "sd", "sl", "sr", "sup", "sdown", "sleft", "sright", "ssu", "ssd", "ssl", "ssr", "ssup", "ssdown", "ssleft", "ssright", "look up", "look down", "look left", "look right", "lu", "ld", "ll", "lr", "hlu", "hld", "hll", "hlr", "slu", "sld", "sll", "slr", "dup", "ddown", "dleft", "dright", "du", "dd", "dl", "dr", "a", "b", "x", "y", "ha", "hb", "hx", "hy", "hhb", "hhhb", "l", "zl", "r", "zr", "plus", "minus", "dive", "dive2"]
pluslist = []
modlist = ["melodiousmarci", "harmjan387", "beanjr_yt", "alua2020", "ogcristofer", "stravos96", "splatax", "silvermagpi", "remotegames", "fossephate", "tpnsbot"]
banlist = []
sublist = []
voted = []
singlePlayerGames = ["The Legend of Zelda: Breath of the Wild", "Celeste"]
twoPlayerGames = ["Super Mario Odyssey"]

commandQueue = []
nextCommands = []


# load plus list:
if (os.path.exists("pluslist.pkl")):
	with open("pluslist.pkl", "rb") as f:
		pluslist = pickle.load(f)[0]
# load ban list:
if (os.path.exists("banlist.pkl")):
	with open("banlist.pkl", "rb") as f:
		banlist = pickle.load(f)[0]

# get sub list:
sublist = None
try:
	sublist = getSubList()
except:
	sublist = []

# def stick_y(n):
# 	if (int(n) == 128):
# 		return 128
# 	else:
# 		return 255 - int(n)

class Client(object):

	def __init__(self):

		sio.emit("joinSecure", {"room": "controller", "password": ROOM_SECRET})
		sio.emit("banlist", banlist)
		sio.emit("modlist", modlist)
		sio.emit("pluslist", pluslist)
		sio.emit("sublist", sublist)

		self.start = time.time()
		self.end = time.time()

		self.botstart = time.time()
		self.botend = time.time()

		self.controllerStart = time.time()
		self.controllerEnd = time.time()

		self.lastInputs = [0, 0, 0, 0, 0, 0, 0, 0, 0]

		self.yeaVotes = 0
		self.nayVotes = 0
		self.voting = False
		self.locked = False
		self.gotoUsed = False
		self.gotoLeft = False
		self.chatEnabled = True
		self.switchControllerEnabled = True
		self.xboxControllerEnabled = True
		self.emergencySystemEnabled = True
		self.chatRelayEnabled = False
		self.controlQueues = [[], [], [], [], []]
		self.currentPlayers = []
		self.currentGame = "none"
		self.currentXboxGame = "none"

	@sio.on("turnTimesLeft")
	def on_turn_times_left(*args):
		try:
			client.currentPlayers = args[1]["currentPlayers"]
		except:
			pass

		return

	@sio.on("connect")
	def on_connect():
		print("connected")
		sio.emit("joinSecure", {"room": "controller", "password": ROOM_SECRET})
		sio.emit("banlist", banlist)
		sio.emit("modlist", modlist)
		sio.emit("pluslist", pluslist)
		sio.emit("sublist", sublist)

	@sio.on("disconnect")
	def on_disconnect():
		print("disconnected")
		killscript()

	@sio.on("stayConnected")
	def on_stay_connected():
		global connectCounter
		global connectMax
		connectCounter += 10
		if (connectCounter > connectMax):
			connectCounter = connectMax

	@sio.on("controllerState")
	def on_controller_state(data):

		# if (not client.controllerEnabled):
		# 	return

		cNum = data["cNum"]
		btns = data["btns"]

		if (not client.xboxControllerEnabled and cNum > 3):
			return
		if (not client.switchControllerEnabled and cNum < 4):
			return

		if (cNum > 0 and client.currentGame in singlePlayerGames and cNum < 4):
			return
		if (cNum > 1 and client.currentGame in twoPlayerGames and cNum < 4):
			return

		# print("controller state " + str(cNum) + ":", btns)
		print(str(cNum), btns, data["axes"][0], data["axes"][1], data["axes"][2], data["axes"][3])

		if (cNum > 4):
			return

		controller = controllers[cNum]

		cPlayer = ""
		try:
			cPlayer = client.currentPlayers[cNum]
		except:
			pass

		controller.reset()

		controller.btns = btns
		controller.axes[0] = data["axes"][0]
		controller.axes[1] = data["axes"][1]
		controller.axes[2] = data["axes"][2]
		controller.axes[3] = data["axes"][3]
		if (cNum > 3 and len(data["axes"]) > 4):
			controller.axes[4] = data["axes"][4]
			controller.axes[5] = data["axes"][5]

		controller.setButtons(btns)

		# duration = 0.001
		# duration = 0.0001
		duration = 0
		reset = 0
		# send_and_reset(duration, reset, cNum)

		sendThread = Thread(target=send_and_reset, args=(duration, reset, cNum))
		sendThread.start()

		return

	@sio.on("afk")
	def on_afk():
		game = random.choice(gameList)
		msg = "!goto " + game
		send_message(msg, "all")
		client.handleChat("tpnsbot", msg)
		sleep(1)
		msg = "yea"
		send_message(msg, "all")
		client.handleChat("tpnsbot", msg)
		return

	@sio.on("lock")
	def on_lock():
		client.locked = True
		client.voting = True
		client.chatEnabled = False
		return

	@sio.on("unlock")
	def on_unlock():
		client.locked = False
		client.voting = False
		client.chatEnabled = True
		return

	@sio.on("chatMessage")
	def on_chat_message(data):

		message = data["message"].lower()
		username = data["username"].lower()

		if (data["isReplay"]):
			return

		# ignore TPNSbot on site:
		if (username == "TPNSbot" or username == "tpnsbot"):
			return

		if (client.chatRelayEnabled):

			if (message[0] != "[" and username != "tpnsbot" and username != "TPNSbot"):
				msg = "[site:" + username + "] " + message
				chatRelayTimer = Timer(0, send_message, (msg, "twitch"))
				chatRelayTimer.start()
				chatRelayTimer = Timer(0, send_message, (msg, "youtube"))
				chatRelayTimer.start()

		# self.handleChat(username, message, "site", None)
		handleChatTimer = Timer(0, client.handleChat, (username, message, "site", None))
		handleChatTimer.start()

		return

	def enableChatRelay(self):
		self.chatRelayEnabled = True
		return

	def findImage(self, frame, imagefile, threshold=0.6):

		img_rgb = frame# where we're looking for the icon
		img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
		template = cv2.imread(imagefile, 0)
		w, h = template.shape[::-1]

		iconLocationX = -1
		iconLocationY = -1

		res = cv2.matchTemplate(img_gray, template,cv2.TM_CCOEFF_NORMED)
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

	# https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
	def findImage2(self, imagefile, x1, y1, width, height, windowName, threshold=0.6, showImage=False):


		SSx1 = x1;
		SSy1 = y1;
		SSWidth = width
		SSHeight = height

		location = None

		try:
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

			# for pt in zip(*loc[::-1]):
			for pt in zip(*[loc[-1], loc[-2]]):
				# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
				# pt = max_loc
				cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
				iconLocationX = pt[0] + (w/2)
				iconLocationX = pt[1] + (h/2)
				cv2.circle(img_rgb, (int(iconLocationX), int(iconLocationY)), int(2), (0, 255, 255), 2)
				# print(pt)
				location = [pt[0], pt[1]]

			if (showImage):
				img.show()
				# cv2.imshow("icon match", img_rgb)
				# cv2.waitKey(10)
				sleep(10)
		except:
			send_message("couldn't find window title! (probably)", "all")
			return None

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
		self.switchControllerEnabled = False
		self.chatEnabled = False
		self.emergencySystemEnabled = False

		# reset controllers
		for i in range(0, 4):
			controllers[i].reset()
			# send in thread to prevent main thread from crashing when the hardware fails:
			sendThread = Thread(target=send_and_reset, args=(0.1, 1, i))
			sendThread.start()
			# destroyThread = Thread(target=thread_destroyer, args=(sendThread, 0.1))
			# destroyThread.start()

		controller = controllers[0]

		# get to game selection screen:
		controller.reset()
		controller.home = 1
		send_and_reset(0.1, 1, 0)
		sleep(2)
		controller.axes[0] = STICK_MAX
		send_and_reset(3, 1, 0)
		controller.a = 1
		send_and_reset(0.1, 1, 0)

		sleep(2)

		x1 = 0
		y1 = 0
		width = 1920
		height = 1080
		windowName = "switch"
		iconLoc = None

		counter = 0
		waitTime = 0.5# 2

		while (iconLoc == None and counter < 5):

			if (counter > 0):
				# move down and try again:
				# move down 3 times and up once:
				controller.axes[1] = STICK_MAX
				send_and_reset(0.1, 1, 0)
				sleep(waitTime)
				controller.axes[1] = STICK_MAX
				send_and_reset(0.1, 1, 0)
				sleep(waitTime)
				controller.axes[1] = STICK_MAX
				send_and_reset(0.1, 1, 0)
				sleep(waitTime)
				controller.axes[1] = STICK_MIN
				send_and_reset(0.1, 1, 0)
				sleep(waitTime)

			iconLoc = self.findImage2(imagefile, x1, y1, width, height, windowName, 0.8, False)

			if (iconLoc != None):
				break

			counter += 1


		# give up if we still can't find it:
		if iconLoc == None:
			controller.axes[1] = STICK_MIN
			send_and_reset(1.5, 1)
			controller.a = 1
			send_and_reset(0.1)
			self.switchControllerEnabled = True
			self.chatEnabled = True
			self.emergencySystemEnabled = True
			msg = "Failed to find game, going back to previous game!"
			send_message(msg, "all")
			return

		# only update the game if we succesfully changed the game
		self.currentGame = nameofgame

		print(iconLoc)


		# iconLoc[0] = int(round(iconLoc[0]/100)-1)# the number of times to move right
		# iconLoc[1] = int(round(iconLoc[1]/100)-2)# the number of times to move down

		# so that when we round down its always above the nearest multiple of 185
		iconLoc[0] += 10
		iconLoc[1] += 10

		size = 275# 185

		iconLoc[0] = int((round_down(iconLoc[0], size)/size))# the number of times to move right
		iconLoc[1] = int((round_down(iconLoc[1], size)/size)-1)# the number of times to move down

		# iconLoc[0] = int(iconLoc[0]/2)
		# iconLoc[1] = int(iconLoc[1]/2)

		print(iconLoc)


		for i in range(0, iconLoc[0]):
			controller.axes[0] = STICK_MAX
			send_and_reset(0.1, 1)
			sleep(waitTime)
		for i in range(0, iconLoc[1]):
			controller.axes[1] = STICK_MAX
			send_and_reset(0.1, 1)
			sleep(waitTime)


		# select left most profile:
		controller.a = 1
		send_and_reset(0.1)
		sleep(1)
		controller.a = 1
		send_and_reset(0.1)
		sleep(3)
		controller.axes[0] = STICK_MIN
		send_and_reset(1)
		sleep(0.1)

		for i in range(0, 15):
			controller.a = 1
			send_and_reset(0.1)
			sleep(1)
		sleep(15)
		for i in range(0, 15):
			controller.a = 1
			send_and_reset(0.1)
			sleep(1)

		msg = "!game " + nameofgame
		send_message(msg, "all")


		# draw a circle on the image:
		# x = 200
		# y = 200
		# r = 5
		# cv2.circle(frame, (int(x), int(y)), int(r), (0, 255, 255), 2)

		# show screen capture and mask
		#cv2.imshow("screen capture", frame)

		# mask = cv2.inRange(hsv, colorLower1, colorUpper1)
		# cv2.imshow("mask", mask)
		# cv2.waitKey(1)


		self.switchControllerEnabled = True
		self.chatEnabled = True
		self.emergencySystemEnabled = True

		return

	def end_goto_vote(self, imagefile, delay, nameofgame="Twitch Plays"):

		msg = "With " + str(self.yeaVotes) + " VoteYea and " + str(self.nayVotes) + " VoteNay"

		leaving = False
		timeGotoisDisabled = 0

		if (self.yeaVotes > self.nayVotes):
			self.gotoLeft = True
			msg = msg + " We will be LEAVING"
			leaving = True
			timeGotoisDisabled = 10 * 60# 10 minutes
		else:
			self.gotoLeft = False
			msg = msg + " We will be STAYING"
			timeGotoisDisabled = 4 * 60# 4 minutes

		self.gotoUsed = True
		gotoTimer = Timer(timeGotoisDisabled, self.reenable_goto)
		gotoTimer.start()

		send_message(msg, "all")

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
			send_message(msg, "all")
			return

		if (self.gotoUsed == True):
			msg = ""
			if (self.gotoLeft == True):
				msg = "The !goto command was used in the last 10 minutes, please wait before trying to change the game again"
			else:
				msg = "The !goto command was used in the last 4 minutes, please wait before trying to change the game again"
			send_message(msg, "all")
			return

		self.yeaVotes = 0
		self.nayVotes = 0
		msg = "A vote has been started to goto " + nameofgame + "! Vote now with \"yea\" to LEAVE and \"nay\" to STAY! Voting ends in 20 seconds!"
		send_message(msg, "all")
		sio.emit("voteStarted")
		self.voting = True

		voteTimer = Timer(20.0, self.end_goto_vote, (imagefile, delay, nameofgame))
		voteTimer.start()

		return

	def end_goto_xbox_vote(self, delay, nameofgame="Twitch Plays"):

		msg = "With " + str(self.yeaVotes) + " VoteYea and " + str(self.nayVotes) + " VoteNay"

		leaving = False
		timeGotoisDisabled = 0

		if (self.yeaVotes > self.nayVotes):
			self.gotoLeft = True
			msg = msg + " We will be LEAVING"
			leaving = True
			timeGotoisDisabled = 10*60# 10 minutes
		else:
			self.gotoLeft = False
			msg = msg + " We will be STAYING"
			timeGotoisDisabled = 4*60# 4 minutes

		self.gotoUsed = True
		gotoTimer = Timer(timeGotoisDisabled, self.reenable_goto)
		gotoTimer.start()

		send_message(msg, "all")

		self.voting = False

		del voted[:]

		if (leaving):
			self.goto_xbox_game(delay, nameofgame)
		else:
			self.xboxControllerEnabled = True
			self.chatEnabled = True
			self.emergencySystemEnabled = True
		return

	def goto_xbox_game(self, delay=50, nameofgame="Twitch Plays"):

		# disable controls while we do this:
		self.xboxControllerEnabled = False
		self.chatEnabled = False
		self.emergencySystemEnabled = False
		# update the game
		self.currentXboxGame = nameofgame

		cNum = 4# xbox controller

		# reset controller(s):
		controllers[cNum].reset()
		send_and_reset(0.1, 1, cNum)

		controller = controllers[cNum]

		# get to game selection screen:
		# home a down a right
		controller.reset()
		controller.home = 1
		send_and_reset(0.1, 1, cNum)
		sleep(2)
		controller.b = 1
		send_and_reset(0.1, 1, cNum)
		sleep(15)
		controller.axes[1] = STICK_MAX
		send_and_reset(0.1, 1, cNum)
		sleep(1)
		controller.b = 1
		send_and_reset(0.1, 1, cNum)
		sleep(6)
		controller.axes[0] = STICK_MAX
		send_and_reset(0.1, 1, cNum)
		sleep(0.5)

		index = xboxGameList1.index(nameofgame)

		timesToMoveDown = int(index / 4)
		timesToMoveRight = (index % 4)

		print(index, timesToMoveDown, timesToMoveRight)

		waitTime = 0.5

		# navigate to game
		for i in range(0, timesToMoveRight):
			controller.axes[0] = STICK_MAX
			send_and_reset(0.1, 1, cNum)
			sleep(waitTime)
		for i in range(0, timesToMoveDown):
			controller.axes[1] = STICK_MAX
			send_and_reset(0.1, 1, cNum)
			sleep(waitTime)

		sleep(0.5)

		# mash a:
		for i in range(0, 10):
			controller.b = 1
			send_and_reset(0.1, 1, cNum)
			sleep(1)
		sleep(10)
		for i in range(0, 10):
			controller.b = 1
			send_and_reset(0.1, 1, cNum)
			sleep(1)

		# msg = "!game " + nameofgame
		# send_message(msg, "all")


		self.xboxControllerEnabled = True
		self.chatEnabled = True
		self.emergencySystemEnabled = True

		return

	def goto_xbox_game_vote(self, delay=50, nameofgame="Twitch Plays"):

		if (self.voting == True):
			msg = "The !goto command is disabled right now"
			send_message(msg, "all")
			return

		if (self.gotoUsed == True):
			msg = ""
			if (self.gotoLeft == True):
				msg = "The !goto command was used in the last 10 minutes, please wait before trying to change the game again"
			else:
				msg = "The !goto command was used in the last 4 minutes, please wait before trying to change the game again"
			send_message(msg, "all")
			return

		self.yeaVotes = 0
		self.nayVotes = 0
		msg = "A vote has been started to goto " + nameofgame + "! Vote now with \"yea\" to LEAVE and \"nay\" to STAY! Voting ends in 20 seconds!"
		send_message(msg, "all")
		sio.emit("voteStarted")
		self.voting = True

		voteTimer = Timer(20.0, self.end_goto_xbox_vote, (delay, nameofgame))
		voteTimer.start()

		return

	def handleChat(self, username, message, source="twitch", uniqueID=None):
		print("<" + username + "> " + message)

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
					print(username)
					voted.append(username)
					self.yeaVotes += 1
				if ((cmd == "votenay" or cmd == "nay") and username not in voted):
					voted.append(username)
					self.nayVotes += 1

		if len(commands) == 1:

			cmd = commands[0]


			if (cmd == "!controls" or cmd == "!help"):
				msg = "goto https://remotegames.io or look at the description for the chat controls,\
				 you can also type \"!goto [game]\" (without brackets) to switch games. use !goto for a list of games! use !commands for a list of commands!"
				send_message(msg, "all")

			if (cmd == "!goto" or cmd == "!games" or cmd == "!gamelist"):
				msg = "use \"!goto [game]\" (without brackets) to switch games! list: "
				for game in gameList:
					msg += game + ", "
				msg = msg[:-2]
				send_message(msg, "all")

			if (cmd == "!xboxgoto" or cmd == "!xboxgames" or cmd == "!xboxgamelist"):
				msg = "use \"!xboxgoto [game]\" (without brackets) to switch games! list: "
				for game in xboxGameList2:
					msg += game + ", "
				msg = msg[:-2]
				send_message(msg, "all")

			# if (cmd == "!status" or cmd == "!internetstatus"):
				# msg = "Checking internet status!"
				# send_message(msg, source)
				# sio.emit("getInternetStatus")

			if (cmd == "!commands"):
				msg1 = "(mods only): \"!restartscript\", \"!restartserver\" \"!giveplus [user]\", \"!ban [user]\", \"!unban [user]\", \"!removeplus [user]\", \
				\"!disablechat\", \"!enablechat\", \"!disablegoto\", \"!enablegoto\", \"!setturnlength [lengthInMS]\", \"!setforfeitlength [lengthInMS]\""
				msg2 = "(plus only): \"!disableinternet\", \"!enableinternet\", \"!fixcontrollers\", \"!rr [user]\", \"!rainbow [user]\""
				msg3 = "(anyone): \"!restart1\", \"!restart2\", \"!restart3\", \"!banlist\", \"!pluslist\", \"!sublist\", \"!modlist\", \"!discord\", \"!site\", \"!source\", \"!fc\", \"!playing\", \"!goto [game]\""
				send_message(msg1, "all")
				send_message(msg2, "all")
				send_message(msg3, "all")

			if (cmd == "!discord"):
				msg = "Discord invite link: https://discord.io/remotegames/"

				send_message(msg, "all")

			if (cmd == "!site"):
				msg = "https://remotegames.io"
				send_message(msg, "all")

			if (cmd == "!source"):
				msg = "https://github.com/mfosse/remotegames/ https://github.com/mfosse/switch-controller/ https://github.com/mfosse/streamr/"
				send_message(msg, "all")

			if (cmd == "!fc" or cmd == "!friendcode"):
				msg = "SW-4621-9617-9306"
				send_message(msg, "all")

			if (cmd == "!pluslist"):
				msg = "plus list: "
				for user in pluslist:
					msg += user + ", "
				msg = msg[:-2]
				# split into 2 parts:
				firstpart, secondpart = msg[:len(msg)//2], msg[len(msg)//2:]
				send_message(firstpart, "all")
				send_message(secondpart, "all")

				# send_message(msg, source)

			if (cmd == "!modlist"):
				msg = "mod list: "
				for user in modlist:
					msg += user + ", "
				msg = msg[:-2]
				send_message(msg, "all")

			if (cmd == "!banlist"):
				msg = "ban list: "
				for user in banlist:
					msg += user + ", "
				msg = msg[:-2]
				send_message(msg, "all")

			if (cmd == "!sublist"):
				msg = "sub list: "
				for user in sublist:
					msg += user + ", "
				msg = msg[:-2]
				send_message(msg, "all")

			# if (cmd == "!restart1" or cmd == "!restart"):
			# 	msg = "restarting lagless1!"
			# 	send_message(msg, "all")
			# 	os.system("taskkill /f /im streamr.exe")
			# 	# sio.emit("restart")
			#
			# if (cmd == "!restart2"):
			# 	msg = "restarting lagless2!"
			# 	send_message(msg, "all")
			# 	sio.emit("restart2")
			#
			# if (cmd == "!restart3"):
			# 	msg = "restarting lagless3!"
			# 	send_message(msg, "all")
			# 	sio.emit("restart3")

			if (cmd == "!restartserver" and username in modlist):
				msg = "restarting the server!"
				send_message(msg, "all")
				sio.emit("restartServer")

			if (cmd == "!restartscript" and username in modlist):
				msg = "restarting the python script! This can take up to 30 seconds."
				send_message(msg, "all")
				with open("pluslist.pkl", "wb") as f:
					pickle.dump([pluslist], f)
				killscript()

			if (cmd == "!disablegoto" and username in modlist):
				msg = "disabling !goto"
				send_message(msg, "all")
				self.voting = True
			if (cmd == "!enablegoto" and username in modlist):
				msg = "enabling !goto"
				send_message(msg, "all")
				self.voting = False

			if (cmd == "!disablechat" and username in modlist):
				msg = "disabling chat commands!"
				send_message(msg, "all")
				self.chatEnabled = False
			if (cmd == "!enablechat" and username in modlist):
				msg = "Enabling chat commands!"
				send_message(msg, "all")
				self.chatEnabled = True

			if (cmd == "!lock" and username in pluslist):
				msg = "locking!"
				send_message(msg, "all")
				self.locked = True
				self.voting = True
				self.chatEnabled = False
				sio.emit("lock")

			if (cmd == "!unlockqueues" and username in modlist):
				msg = "unlocking queues!"
				send_message(msg, "all")
				sio.emit("unlockqueues")

			if (cmd == "!lockqueues" and username in modlist):
				msg = "locking queues!"
				send_message(msg, "all")
				sio.emit("lockqueues")

			if (cmd == "!disablegyro"):
				msg = "disabling gyro controls!"
				send_message(msg, "all")
				controller0.gyroEnabled = 0

			if (cmd == "!enablegyro"):
				msg = "enabling gyro controls!"
				send_message(msg, "all")
				controllers[0].gyroEnabled = 1

			if (cmd == "!unlock" and username in modlist):
				msg = "unlocking!"
				send_message(msg, "all")
				self.locked = False
				self.voting = False
				self.chatEnabled = True
				sio.emit("unlock")

			if (cmd == "!1p" and username in pluslist):
				msg = "changing to 1 Player Mode!"
				send_message(msg, "all")
				sio.emit("setMaxPlayers", 1)

			if (cmd == "!2p" and username in pluslist):
				msg = "changing to 2 Player Mode!"
				send_message(msg, "all")
				sio.emit("setMaxPlayers", 2)

			if (cmd == "!3p" and username in pluslist):
				msg = "changing to 3 Player Mode!"
				send_message(msg, "all")
				sio.emit("setMaxPlayers", 3)

			if (cmd == "!4p" and username in pluslist):
				msg = "changing to 4 Player Mode!"
				send_message(msg, "all")
				sio.emit("setMaxPlayers", 4)

			if (cmd == "!5p" and username in pluslist):
				msg = "changing to 5 Player Mode!"
				send_message(msg, "all")
				sio.emit("setMaxPlayers", 5)

			if (cmd == "!forcerefresh" and username in modlist):
				sio.emit("forceRefresh")

			if (cmd == "!disableinternet" and username in pluslist):
				msg = "disabling internet accesss!"
				send_message(msg, "all")
				sio.emit("disableInternet")

			if (cmd == "!enableinternet" and username in pluslist):
				msg = "enabling internet access!"
				send_message(msg, "all")
				sio.emit("enableInternet")


			# if (cmd == "!expired"):
			# 	msg = "expired status: " + youtubeBot.credentials.expired()
			# 	send_message(msg, "all")

			if (cmd == "!egg"):
				sio.emit("rickroll", username)

			if (cmd == "!rr"):
				sio.emit("rickroll", username)


			if (cmd == "!rainbow"):
				sio.emit("rainbow", username)

			if (cmd == "!playing"):
				msg = "the current player(s) are: "
				count = 0
				for player in self.currentPlayers:
					if (player != None):
						count += 1
						msg += player + ", "
				msg = msg[:-2]
				if (count == 0):
					msg = "no one is playing right now."

				send_message(msg, source)


			if (cmd == "!fixcontrollers" and username in pluslist):
				msg = "fixing controller order!"
				send_message(msg, "all")

				# disable lagless while we do this:
				self.switchControllerEnabled = False
				self.chatEnabled = False

				# reset controllers
				for i in range(0, 4):
					controllers[i].reset()
					# send in thread to prevent main thread from crashing when the hardware fails:
					sendThread = Thread(target=send_and_reset, args=(0.1, 1, i))
					sendThread.start()

				controller = controllers[0]

				# go home
				controller.home = 1
				send_and_reset(0.1, 1)
				sleep(2)

				# navigate to re-pair section
				controller.axes[1] = STICK_MAX
				send_and_reset(0.1, 1)
				controller.axes[0] = STICK_MAX
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller.axes[0] = STICK_MAX
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller.axes[0] = STICK_MAX
				send_and_reset(0.1, 1)
				sleep(0.5)
				controller.a = 1
				send_and_reset(0.1, 1)
				sleep(0.5)

				sleep(3)

				# press a on all controllers, in the correct order
				controllers[0].a = 1
				send_and_reset(0.1, 1)
				sleep(0.5)
				controllers[0].a = 1
				send_and_reset(0.1, 1, 0)
				sleep(2)
				controllers[1].a = 1
				send_and_reset(0.1, 1, 1)
				sleep(2)
				controllers[2].a = 1
				send_and_reset(0.1, 1, 2)
				sleep(2)
				controllers[3].a = 1
				send_and_reset(0.1, 1, 3)
				sleep(2)
				# controllers[4].a = 1
				# send_and_reset(0.1, 1, 3)
				# sleep(2)
				# controllers[5].a = 1
				# send_and_reset(0.1, 1, 3)
				# sleep(2)
				# controllers[6].a = 1
				# send_and_reset(0.1, 1, 3)
				# sleep(2)
				# controllers[7].a = 1
				# send_and_reset(0.1, 1, 3)
				# sleep(2)

				# go back to the game
				controller.a = 1
				send_and_reset(0.1, 1)
				controller.a = 1
				send_and_reset(0.1, 1)
				sleep(2)
				controller.b = 1
				send_and_reset(0.1, 1)
				sleep(1)
				controller.axes[1] = STICK_MIN
				send_and_reset(0.1, 1)
				sleep(2)
				controller.axes[0] = STICK_MIN
				send_and_reset(1, 1)
				controller.a = 1
				send_and_reset(0.1, 1)


				# re-enable lagless
				self.switchControllerEnabled = True
				self.chatEnabled = True


		if len(commands) == 2:

			if (commands[0] == "!giveplus" and username in modlist):

				msg = "giving plus permission to: " + commands[1]
				send_message(msg, "all")

				pluslist.append(commands[1])

				# write pluslist to file:
				with open("pluslist.pkl", "wb") as f:
					pickle.dump([pluslist], f)

			if (commands[0] == "!removeplus" and username in modlist):

				msg = "removing plus permissions from: " + commands[1]
				send_message(msg, "all")

				# revoke plus permission:
				if commands[1] in pluslist:
					pluslist.remove(commands[1])

				# write pluslist to file:
				with open("pluslist.pkl", "wb") as f:
					pickle.dump([pluslist], f)


			if (commands[0] == "!unban" and username in modlist):
				msg = "unbanning: " + commands[1]
				send_message(msg, "all")
				sio.emit("unban", commands[1])

			if (commands[0] == "!tempban" and username in modlist):
				msg = "tempbanning: " + commands[1]
				send_message(msg, "all")
				sio.emit("tempBan", commands[1])

			if (commands[0] == "!permaban" and username in modlist):
				msg = "permabanning: " + commands[1]
				send_message(msg, "all")
				sio.emit("permaBan", commands[1])

			if (commands[0] == "!setturnlength" and username in modlist):
				msg = "setting turn length to: " + commands[1]
				send_message(msg, "all")
				sio.emit("setTurnLength", int(commands[1]) * 1000)

			if (commands[0] == "!setforfeitlength" and username in modlist):
				msg = "setting forfeit length to: " + commands[1]
				send_message(msg, "all")
				sio.emit("setForfeitLength", int(commands[1]) * 1000)

			if (commands[0] == "!rr" and username in pluslist):
				sio.emit("rickroll", commands[1])

			if (commands[0] == "!rainbow" and username in pluslist):
				sio.emit("rainbow", commands[1])

			# if (commands[0] == "!game" and username in modlist):
			# 	self.currentGame = commands[1]
			# 	msg = "Setting game to: " + commands[1]
			# 	send_message(msg, "all")


			# if (commands[0] == "!mod" and username in adminlist):
			# 	msg = "Modding: " + commands[1]
			# 	send_message(msg, "all")
			# 	banlist.append(commands[1])
			# 	sio.emit("banlist", banlist)

			# if (commands[0] == "!unmod" and username in adminlist):
			# 	msg = "UnModding: " + commands[1]
			#	send_message(msg, "all")
			# 	modlist.remove(commands[1])
			# 	sio.emit("banlist", banlist)


			# goto commands:
			if (commands[0] == "!goto" or (commands[0] == "!forcegoto" and username in modlist) or (commands[0] == "!setgame" and username in modlist)):
				game = commands[1]

				goto = None
				waitTime = 0
				imageLoc = ""
				nameofgame = ""

				if (game not in gameList):
					return

				if (game == "smo"):
					imageLoc, waitTime, nameofgame = "images/icons/smo.png", 30, "Super Mario Odyssey"
				if (game == "botw"):
					imageLoc, waitTime, nameofgame = "images/icons/botw.png", 20, "The Legend of Zelda: Breath of the Wild"
				if (game == "celeste"):
					imageLoc, waitTime, nameofgame = "images/icons/celeste.png", 10, "Celeste"
				if (game == "kirby"):
					imageLoc, waitTime, nameofgame = "images/icons/kirby.png", 10, "Kirby: Star Allies"
				if (game == "splatoon2"):
					imageLoc, waitTime, nameofgame = "images/icons/splatoon2.png", 10, "Splatoon 2"
				if (game == "sonic"):
					imageLoc, waitTime, nameofgame = "images/icons/sonic.png", 10, "Sonic Mania"
				if (game == "mk8"):
					imageLoc, waitTime, nameofgame = "images/icons/mk8.png", 10, "Mario Kart 8"
				if (game == "arms"):
					imageLoc, waitTime, nameofgame = "images/icons/arms.png", 10, "Arms"
				if (game == "skyrim"):
					imageLoc, waitTime, nameofgame = "images/icons/skyrim.png", 40, "The Elder Scrolls V: Skyrim"
				if (game == "rocketleague"):
					imageLoc, waitTime, nameofgame = "images/icons/rocketleague.png", 10, "Rocket League"
				if (game == "wizard"):
					imageLoc, waitTime, nameofgame = "images/icons/wizard.png", 10, "Wizard of Legend"
				if (game == "torquel"):
					imageLoc, waitTime, nameofgame = "images/icons/torquel.png", 10, "TorqueL"
				if (game == "fortnite"):
					imageLoc, waitTime, nameofgame = "images/icons/fortnite4.png", 10, "Fortnite"
				if (game == "jackbox3"):
					imageLoc, waitTime, nameofgame = "images/icons/jackbox3.png", 10, "The Jackbox Party Pack 3"
				if (game == "jackbox4"):
					imageLoc, waitTime, nameofgame = "images/icons/jackbox4.png", 10, "The Jackbox Party Pack 4"
				if (game == "shovelknight"):
					imageLoc, waitTime, nameofgame = "images/icons/shovelknight.png", 10, "Shovel Knight"
				if (game == "explosion"):
					imageLoc, waitTime, nameofgame = "images/icons/explosion.png", 10, "Graceful Explosion Machine"
				if (game == "human"):
					imageLoc, waitTime, nameofgame = "images/icons/human.png", 10, "Human: Fall Flat"
				if (game == "snipperclips"):
					imageLoc, waitTime, nameofgame = "images/icons/snipperclips.png", 10, "Snipperclips: Cut It Out, Together!"
				if (game == "paladins"):
					imageLoc, waitTime, nameofgame = "images/icons/paladins.png", 10, "Paladins"
				if (game == "hollow"):
					imageLoc, waitTime, nameofgame = "images/icons/hollow.png", 10, "Hollow Knight"
				if (game == "mta"):
					imageLoc, waitTime, nameofgame = "images/icons/mta.png", 10, "Mario Tennis Aces"
				if (game == "nes"):
					imageLoc, waitTime, nameofgame = "images/icons/nes.png", 1, "Nintendo Entertainment System"
				if (game == "brawlhalla"):
					imageLoc, waitTime, nameofgame = "images/icons/brawlhalla.png", 10, "Brawlhalla"
				if (game == "undertale"):
					imageLoc, waitTime, nameofgame = "images/icons/undertale.png", 10, "Undertale"
				if (game == "smash"):
					imageLoc, waitTime, nameofgame = "images/icons/smash.png", 1, "Super Smash Bros. Ultimate"
				if (game == "katamari"):
					imageLoc, waitTime, nameofgame = "images/icons/katamari.png", 1, "Katamari Damacy: Reroll"
				if (game == "nsmbud"):
					imageLoc, waitTime, nameofgame = "images/icons/nsmbud.png", 1, "New Super Mario Bros. U Deluxe"
				if (game == "deltarune"):
					imageLoc, waitTime, nameofgame = "images/icons/deltarune.png", 1, "Deltarune"
				if (game == "tetris"):
					imageLoc, waitTime, nameofgame = "images/icons/tetris.png", 1, "Tetris"
				if (game == "baba"):
					imageLoc, waitTime, nameofgame = "images/icons/baba.png", 1, "Baba is You"
				# if (game == "youtube"):
				# 	imageLoc, waitTime, nameofgame = "images/icons/youtube.png", 10, "YouTube"
				# if (cmd == "!goto cave"):
				# 	imageLoc, waitTime, nameofgame = "images/icons/cave.png", 10, "Cave Story"
				# if (cmd == "!goto isaac"):
				# 	imageLoc, waitTime, nameofgame = "images/icons/isaac.png", 10, "The Binding of Isaac: Afterbirth"
				# if (cmd == "!goto mario"):
				# 	imageLoc, waitTime, nameofgame = "images/icons/mario.png", 10, "Twitch Plays"
				# if (game == "pokemonquest"):
					# imageLoc, waitTime, nameofgame = "icons/pokemonquest.png", 10, "Pokemon Quest"
				# if (game == "fallout"):
					# imageLoc, waitTime, nameofgame = "images/icons/fallout.png", 10, "Fallout Shelter"



				if (self.currentGame == nameofgame):
					msg = "We're already playing this game!"
					send_message(msg, source)
					return

				if (commands[0] == "!setgame"):
					self.currentGame = nameofgame
					msg = "!game " + nameofgame
					send_message(msg, "all")
					return

				if (commands[0] == "!forcegoto"):
					goto = self.goto_game
				else:
					goto = self.goto_game_vote

				goto(imageLoc, waitTime, nameofgame)
				# gotoThread = Thread(target=goto, args=(imageLoc, waitTime, nameofgame))
				# gotoThread.start()


			if ((commands[0] == "!xboxgoto" and username in pluslist) or (commands[0] == "!xboxforcegoto" and username in modlist) or (commands[0] == "!xboxsetgame" and username in modlist)):

				game = commands[1]

				goto = None
				waitTime = 50
				imageLoc = ""
				nameofgame = ""

				if (game not in xboxGameList2):
					return

				# if (game == "smo"):
				# 	imageLoc, waitTime, nameofgame = "icons/smo.png", 30, "Super Mario Odyssey


				index = xboxGameList2.index(game)
				nameofgame = xboxGameList1[index]

				if (index in [8, 9]):
					msg = "This game is disabled right now."
					send_message(msg, source)
					return

				if (self.currentXboxGame == nameofgame):
					msg = "We're already playing this game!"
					send_message(msg, source)
					return

				if (commands[0] == "!xboxsetgame"):
					self.currentXboxGame = nameofgame
					msg = "!game " + nameofgame
					send_message(msg, "all")
					return

				if (commands[0] == "!xboxforcegoto"):
					goto = self.goto_xbox_game
				else:
					goto = self.goto_xbox_game_vote

				goto(waitTime, nameofgame)
				# gotoThread = Thread(target=goto, args=(waitTime, nameofgame))
				# gotoThread.start()

		if (not self.chatEnabled):
			return

		if (len(commands) > 20):
			valid = False

		if (not valid):
			commands = []

		for cmd in commands:
			commandQueue.append(cmd)



	def decreaseQueue(self):

		diffInMilliSeconds = (time.time() - self.start) * 1000

		if (diffInMilliSeconds > 8.33333):
			self.start = time.time()

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
					controllers[0].axes[0] = STICK_MIN
					duration = 0.01
					reset = 1
				if (cmd == "sssright" or cmd == "sssr"):
					controllers[0].axes[0] = STICK_MAX
					duration = 0.01
					reset = 1
				if (cmd == "sssup" or cmd == "sssu"):
					controllers[0].axes[1] = STICK_MIN
					duration = 0.01
					reset = 1
				if (cmd == "sssdown" or cmd == "sssd"):
					controllers[0].axes[1] = STICK_MAX
					duration = 0.01
					reset = 1

				if (cmd == "ssleft" or cmd == "ssl"):
					controllers[0].axes[0] = STICK_MIN
					duration = 0.1
					reset = 1
				if (cmd == "ssright" or cmd == "ssr"):
					controllers[0].axes[0] = STICK_MAX
					duration = 0.1
					reset = 1
				if (cmd == "ssup" or cmd == "ssu"):
					controllers[0].axes[1] = STICK_MIN
					duration = 0.1
					reset = 1
				if (cmd == "ssdown" or cmd == "ssd"):
					controllers[0].axes[1] = STICK_MAX
					duration = 0.1
					reset = 1

				if (cmd == "sleft" or cmd == "sl"):
					controllers[0].axes[0] = STICK_MIN
					duration = 0.3
					reset = 1
				if (cmd == "sright" or cmd == "sr"):
					controllers[0].axes[0] = STICK_MAX
					duration = 0.3
					reset = 1
				if (cmd == "sup" or cmd == "su"):
					controllers[0].axes[1] = STICK_MIN
					duration = 0.3
					reset = 1
				if (cmd == "sdown" or cmd == "sd"):
					controllers[0].axes[1] = STICK_MAX
					duration = 0.3
					reset = 1

				if (cmd == "left" or cmd == "l"):
				# if (cmd == "left"):
					controllers[0].axes[0] = STICK_MIN
					duration = 0.6
					reset = 1
				if (cmd == "right" or cmd == "r"):
				# if (cmd == "right"):
					controllers[0].axes[0] = STICK_MAX
					duration = 0.6
					reset = 1
				if (cmd == "up" or cmd == "u"):
					controllers[0].axes[1] = STICK_MIN
					duration = 0.6
					reset = 1
				if (cmd == "down" or cmd == "d"):
					controllers[0].axes[1] = STICK_MAX
					duration = 0.6
					reset = 1

				if (cmd == "hleft" or cmd == "hl"):
					controllers[0].axes[0] = STICK_MIN
					duration = 1.5
					reset = 1
				if (cmd == "hright" or cmd == "hr"):
					controllers[0].axes[0] = STICK_MAX
					duration = 1.5
					reset = 1
				if (cmd == "hup" or cmd == "hu"):
					controllers[0].axes[1] = STICK_MIN
					duration = 1.5
					reset = 1
				if (cmd == "hdown" or cmd == "hd"):
					controllers[0].axes[1] = STICK_MAX
					duration = 1.5
					reset = 1

				if (cmd == "hhleft"):
					controllers[0].axes[0] = STICK_MIN
					duration = 4.0
					reset = 1
				if (cmd == "hhright"):
					controllers[0].axes[0] = STICK_MAX
					duration = 4.0
					reset = 1
				if (cmd == "hhup"):
					controllers[0].axes[1] = STICK_MIN
					duration = 4.0
					reset = 1
				if (cmd == "hhdown"):
					controllers[0].axes[1] = STICK_MAX
					duration = 4.0
					reset = 1


				if (cmd == "dleft" or cmd == "dl"):
					controllers[0].dpad = DPAD_LEFT
					duration = 0.3
					reset = 1
				if (cmd == "dright" or cmd == "dr"):
					controllers[0].dpad = DPAD_RIGHT
					duration = 0.3
					reset = 1
				if (cmd == "dup" or cmd == "du"):
					controllers[0].dpad = DPAD_UP
					duration = 0.3
					reset = 1
				if (cmd == "ddown" or cmd == "dd"):
					controllers[0].dpad = DPAD_DOWN
					duration = 0.3
					reset = 1



				if (cmd == "slook left" or cmd == "sll"):
					controllers[0].axes[2] = STICK_MIN
					duration = 0.1
					reset = 1
				if (cmd == "slook right" or cmd == "slr"):
					controllers[0].axes[2] = STICK_MAX
					duration = 0.1
					reset = 1
				if (cmd == "slook up" or cmd == "slu"):
					controllers[0].axes[3] = STICK_MIN
					duration = 0.1
					reset = 1
				if (cmd == "slook down" or cmd == "sld"):
					controllers[0].axes[3] = STICK_MAX
					duration = 0.1
					reset = 1

				if (cmd == "look left" or cmd == "ll"):
					controllers[0].axes[2] = STICK_MIN
					duration = 0.3
					reset = 1
				if (cmd == "look right" or cmd == "lr"):
					controllers[0].axes[2] = STICK_MAX
					duration = 0.3
					reset = 1
				if (cmd == "look up" or cmd == "lu"):
					controllers[0].axes[3] = STICK_MIN
					duration = 0.3
					reset = 1
				if (cmd == "look down" or cmd == "ld"):
					controllers[0].axes[3] = STICK_MAX
					duration = 0.3
					reset = 1

				if (cmd == "hlook left" or cmd == "hll"):
					controllers[0].axes[2] = STICK_MIN
					duration = 0.6
					reset = 1
				if (cmd == "hlook right" or cmd == "hlr"):
					controllers[0].axes[2] = STICK_MAX
					duration = 0.6
					reset = 1
				if (cmd == "hlook up" or cmd == "hlu"):
					controllers[0].axes[3] = STICK_MIN
					duration = 0.6
					reset = 1
				if (cmd == "hlook down" or cmd == "hld"):
					controllers[0].axes[3] = STICK_MAX
					duration = 0.6
					reset = 1

				if (cmd == "a"):
					controllers[0].a = 1
					duration = 0.3
					reset = 1
				if (cmd == "b"):
					controllers[0].b = 1
					duration = 0.4
					reset = 1
				if (cmd == "x"):
					controllers[0].x = 1
					duration = 0.3
					reset = 1
				if (cmd == "y"):
					controllers[0].y = 1
					duration = 0.3
					reset = 1
				if (cmd == "lstick"):
					controllers[0].lstick = 1
					duration = 0.1
					reset = 1
				if (cmd == "rstick"):
					controllers[0].rstick = 1
					duration = 0.1
					reset = 1
				if (cmd == "l"):
					controllers[0].l = 1
					duration = 0.1
					reset = 1
				if (cmd == "r"):
					controllers[0].r = 1
					duration = 0.1
					reset = 1
				if (cmd == "zl"):
					controllers[0].zl = 1
					duration = 0.1
					reset = 1
				if (cmd == "zr"):
					controllers[0].zr = 1
					duration = 0.1
					reset = 1
				if (cmd == "minus"):
					controllers[0].minus = 1
					duration = 0.1
					reset = 1
				if (cmd == "plus"):
					controllers[0].plus = 1
					duration = 0.1
					reset = 1
				if (cmd == "home"):
					controllers[0].home = 1
					duration = 0.1
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
							controllers[0].axes[0] = STICK_MIN
						if (btn == "rigt"):
							controllers[0].axes[0] = STICK_MAX
						if (btn == "up"):
							controllers[0].axes[1] = STICK_MIN
						if (btn == "down"):
							controllers[0].axes[1] = STICK_MAX
						if (btn == "dleft"):
							controllers[0].dpad = DPAD_LEFT
						if (btn == "drigt"):
							controllers[0].dpad = DPAD_RIGHT
						if (btn == "dup"):
							controllers[0].dpad = DPAD_UP
						if (btn == "ddown"):
							controllers[0].dpad = DPAD_DOWN

						if (btn == "look left"):
							controllers[0].axes[2] = STICK_MIN
						if (btn == "look rigt"):
							controllers[0].axes[2] = STICK_MAX
						if (btn == "look up"):
							controllers[0].axes[3] = STICK_MIN
						if (btn == "look down"):
							controllers[0].axes[3] = STICK_MAX
						if (btn == "a"):
							controllers[0].a = 1
						if (btn == "b"):
							controllers[0].b = 1
						if (btn == "x"):
							controllers[0].x = 1
						if (btn == "y"):
							controllers[0].y = 1
						if (btn == "l"):
							controllers[0].l = 1
						if (btn == "r"):
							controllers[0].r = 1
						if (btn == "zl"):
							controllers[0].zl = 1
						if (btn == "zr"):
							controllers[0].zr = 1
						if (btn == "minus"):
							controllers[0].minus = 1
				send_and_reset(duration, reset)

	def loop(self):

		# control switch here:

		diffInMilliSeconds = (time.time() - self.botstart) * 1000
		if (diffInMilliSeconds > 1000 * 60 * 5):
			self.botstart = time.time()

			sio.emit("joinSecure", {"room": "controller", "password": ROOM_SECRET})
			sio.emit("banlist", banlist)
			sio.emit("modlist", modlist)
			sio.emit("pluslist", pluslist)
			sio.emit("sublist", sublist)

			msg = "Type \"!help\" for help! Join the discord server! https://discord.io/remotegames/\
			use the website for low latency and better controls: https://remotegames.io"
			send_message(msg, "twitch")
			send_message(msg, "youtube")

		diffInMilliSeconds2 = (time.time() - self.controllerStart) * 1000
		if (diffInMilliSeconds2 > 5000):
			self.controllerStart = time.time()

			sio.emit("joinSecure", {"room": "controller", "password": ROOM_SECRET})
			sio.emit("banlist", banlist)
			sio.emit("modlist", modlist)
			sio.emit("pluslist", pluslist)
			sio.emit("sublist", sublist)

		# todo: get modlist:
		# only grabs mods that are in the chat:
		# with urllib.request.urlopen("https://tmi.twitch.tv/group/user/remotegames/chatters") as url:
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

				if (self.chatRelayEnabled):
					if (message[0] != "[" and username != "tpnsbot" and username != "TPNSbot"):
						msg = "[twitch:" + username + "] " + str(message)
						chatRelayTimer = Timer(0, send_message, (msg, "youtube"))
						chatRelayTimer.start()
						chatRelayTimer = Timer(0, send_message, (msg, "site"))
						chatRelayTimer.start()
				# self.handleChat(username, message, "twitch", None)
				handleChatTimer = Timer(0, self.handleChat, (username, message, "twitch", None))
				handleChatTimer.start()

			except:
				print("twitch chat error")

		# while (len(youtubeBot.messages) > 0):
		# 	channelID = youtubeBot.messages[0]["channelID"]
		# 	username = youtubeBot.messages[0]["username"]
		# 	message = youtubeBot.messages[0]["message"]
		# 	message = message.lower()
		# 	youtubeBot.messages.pop(0)
		#
		# 	# ignore TPNSbot on youtube:
		# 	if (username == "TPNSbot"):
		# 		continue
		#
		# 	if (self.chatRelayEnabled):
		# 		if (message[0] != "[" and username != "tpnsbot" and username != "TPNSbot"):
		# 			msg = "[youtube:" + username + "] " + message
		# 			# send_message(msg, "twitch")
		# 			# send_message(msg, "site")
		# 			chatRelayTimer = Timer(0, send_message, (msg, "twitch"))
		# 			chatRelayTimer.start()
		# 			chatRelayTimer = Timer(0, send_message, (msg, "site"))
		# 			chatRelayTimer.start()
		#
		# 	# youtube re-sends old messages on startup, don't process them:
		# 	if (self.chatRelayEnabled):
		# 		# self.handleChat(username, message, "youtube", None)
		# 		handleChatTimer = Timer(0, self.handleChat, (username, message, "youtube", None))
		# 		handleChatTimer.start()

		self.decreaseQueue()


lockInterval = 1

def emergency_lock():
	global client
	# if (client == None):
	# 	lockTimer = Timer(lockInterval, emergency_lock)
	# 	lockTimer.start()
	# 	return

	x1 = 0
	y1 = 0
	width = 1920
	height = 1080

	windowName = "switch"
	iconLoc = None

	# botw game over:
	# if (client.currentGame == "The Legend of Zelda: Breath of the Wild"):
	# 	iconLoc = client.findImage2("icons/screenshots/botw-game-over.png", x1, y1, width, height, windowName, 0.8)
	# 	if (iconLoc != None):
	# 		controllers[0].a = 1
	# 		send_and_reset(0.1)
	# 		iconLoc = None

	if (iconLoc == None):
		iconLoc = client.findImage2("images/screenshots/smash-language.png", x1, y1, width, height, windowName, 0.8)
	if (iconLoc == None):
		iconLoc = client.findImage2("images/screenshots/smash-options.png", x1, y1, width, height, windowName, 0.8)

	if (iconLoc != None):
		for i in range(5):
			controllers[0].reset()
			controllers[0].b = 1
			send_and_reset(0.1)
			iconLoc = None

	if (iconLoc == None):
		iconLoc = client.findImage2("images/screenshots/settingspage.png", x1, y1, width, height, windowName, 0.8)

	# if (iconLoc == None):
	# 	iconLoc = client.findImage2("icons/screenshots/deletegame.png", x1, y1, width, height, windowName, 0.8)


	# print(iconLoc)
	# print(client.locked)

	if (iconLoc != None and client.emergencySystemEnabled):

		if (client.locked == False):
			msg = "Emergency locking!"
			send_message(msg, "all")

			sio.emit("lock")
			# discordBot.send_message(487328538173767692, "Emergency locking! <@&443263913359048705>")

			print("LOCKING")

		# if (client.currentPlayers[0] not in modlist):
		# 	controllers[0].b = 1
		# 	send_and_reset(0.1)
		# 	controllers[0].b = 1
		# 	send_and_reset(0.1)
		# 	controllers[0].b = 1
		# 	send_and_reset(0.1)
		# 	controllers[0].b = 1
		# 	send_and_reset(0.1)


	lockTimer = Timer(lockInterval, emergency_lock)
	lockTimer.start()
lockTimer = Timer(lockInterval, emergency_lock)
lockTimer.start()

subInterval = 30
def getSubListForever():
	try:
		sublist = getSubList()
	except:
		sublist = []
	subTimer = Timer(subInterval, getSubListForever)
	subTimer.start()
subTimer = Timer(subInterval, getSubListForever)
subTimer.start()

def checkConnectedForever():
	global connectCounter
	# if (client.emergencySystemEnabled == True):
	connectCounter -= 5

	if (connectCounter < 20):
		print(connectCounter)
	# if (connectCounter < 0 and not client.voting):
	if (connectCounter < 0):
		killscript()

	# maybe keep controllers alive:
	# try:
	# 	for i in range(0, len(controllers)):
	# 		controllers[i].queue_send()
	# except:
	# 	pass

	connectTimer = Timer(5, checkConnectedForever)
	connectTimer.start()
connectTimer = Timer(50, checkConnectedForever)
connectTimer.start()

client = Client()

enableChatRelayTimer = Timer(20.0, client.enableChatRelay)
enableChatRelayTimer.start()

send_message("The python script has restarted.", "all")

# def start():
while True:
	client.loop()
	sleep(0.0001)

# mainThread = threading.Thread(target=start, args=(0, 0))
# mainThread.start()
