
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
# to exit:
import sys

pwa_app = pywinauto.application.Application()

try:
	w_handle = pywinauto.findwindows.find_windows(title="scriptxbox")[1]
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

# try:
# 	hwnd = pywinauto.findwindows.find_windows(title="obs64")[0]
# 	# hwnd = win.FindWindow(None, win.String("obs64"))
# 	win.SetWindowText(hwnd, win.String("ps4window"))
# 	print("changing obs64 to \"ps4window\"")
# except IndexError:
# 	print("couldn't find obs64 window")

# switchTitle = "switch"

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
from SwitchController.SwitchController3 import SwitchController3

# xbox controller:
# from XboxController.XboxController import XboxController

# controller manager:
from ControllerManager import ControllerManager

# twitch:
from TwitchBot.TwitchBot import *
# # get sub list:
# from TwitchBot.TwitchSubs import *

# discord:
# from DiscordBot.DiscordBot import *

# youtube:
# from YoutubeBot.YoutubeBot import *

# socketio
import socketio

from threading import Thread

# OpenCV / image utils:
import imutils
import cv2
from PIL import Image

# set window title:
ctypes.windll.kernel32.SetConsoleTitleW("scriptxbox")

# to get json info
import urllib.request, json

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
	sio.connect("http://remotegames.io:8051")
except:
	print("sio connection failed")
	killscript()

connectCounter = 30
connectMax = connectCounter
controllers = []

# controllers.append(SwitchController2())

# xbox:
# try:
# controllers[0].connect(1)
# except:
	# print("controllers[0] error")


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

	try:
		controller = controllers[cNum]
		controller.setBtns()
		controller.send()
		if (duration > 0):
			sleep(duration)
		if (reset):
			controller.reset()
			controller.setBtns()
			controller.send()
	except:
		print("controller send error")

# def thread_destroyer(thread, time):
# 	sleep(time)
# 	thread.exit()
# 	print("exited thread")

def round_down(num, divisor):
	return num - (num % divisor)


pluslist = []
modlist = []
banlist = []
sublist = []

class Client(object):

	def __init__(self):

		self.controllerManager = ControllerManager(1)
		self.controllerManager.init()

		sio.emit("joinSecure", {"room": "controller", "password": ROOM_SECRET})
		sio.emit("banlist", banlist)
		sio.emit("modlist", modlist)
		sio.emit("pluslist", pluslist)
		sio.emit("sublist", sublist)

		self.locked = False

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

		if (cNum > 0):
			return

		cNum = data["cNum"]
		btns = data["btns"]
		LX = data["axes"][0]
		LY = data["axes"][1]
		RX = data["axes"][2]
		RY = data["axes"][3]
		LT = data["axes"][4]
		RT = data["axes"][5]
		
		print(str(cNum), btns, data["axes"][0], data["axes"][1], data["axes"][2], data["axes"][3])

		client.controllerManager.send(cNum, btns, LX, LY, RX, RY, LT, RT)

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

		message = data["text"].lower()
		username = data["username"].lower()

		if (data["isReplay"]):
			return

		# self.handleChat(username, message, "site", None)
		# handleChatTimer = Timer(0, client.handleChat, (username, message, "site", None))
		# handleChatTimer.start()

		return

	def loop(self):

		return

client = Client()

# def start():
while True:
	client.loop()
	sleep(0.0001)