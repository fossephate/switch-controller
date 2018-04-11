#!/usr/bin/env python3
import argparse
import serial
from time import sleep
import pynput
import pyautogui
import win32api
import win32con

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



screenWidth, screenHeight = pyautogui.size()
x = screenWidth/2
y = screenHeight/2
prevX = 0
prevY = 0

controller = SwitchController()
controller.connect("COM6")

twitchBot = TwitchBot()
twitchBot.connect(HOST, PASS, PORT, CHAN)

start = time.clock()

def delayed_reset(delay=0.1):
	Timer(delay, controller.reset).start()

def send_and_reset(duration=0.1):
	controller.getOutput()
	controller.send(controller.output)
	sleep(duration)
	controller.reset()



commandQueue = []
nextCommands = []


while True:

	# control switch here:

	duration = 0.2



	# if win32api.GetAsyncKeyState(ord("W")):
	# 	controller.LY = STICK_MIN
	# 	delayed_reset()
	# if win32api.GetAsyncKeyState(ord("S")):
	# 	controller.LY = STICK_MAX
	# 	delayed_reset()
	# if win32api.GetAsyncKeyState(ord("A")):
	# 	controller.LX = STICK_MIN
	# 	delayed_reset()
	# if win32api.GetAsyncKeyState(ord("D")):
	# 	controller.LX = STICK_MAX
	# 	delayed_reset()

	# if(win32api.GetAsyncKeyState(win32con.VK_RIGHT)):
	# 	controller.a = 1
	# 	delayed_reset()
	# if(win32api.GetAsyncKeyState(win32con.VK_DOWN)):
	# 	controller.b = 1
	# 	delayed_reset()
	# if(win32api.GetAsyncKeyState(win32con.VK_UP)):
	# 	controller.x = 1
	# 	delayed_reset()
	# if(win32api.GetAsyncKeyState(win32con.VK_LEFT)):
	# 	controller.y = 1
	# 	delayed_reset()



	response = twitchBot.stayConnected()
	#response = "none"
	if(response != "none"):
		username = re.search(r"\w+", response).group(0) # return the entire match
		message = CHAT_MSG.sub("", response)
		message = message.strip()
		message = message.lower()
		# print(username + ": " + message)
		# print("0" + message + "0")

		commands = [x.strip() for x in message.split(',')]
		cmd = "none"

		if(commands[0] != "hold"):
			if(len(commands) > 8):
				commands = []
				continue
			for cmd in commands:
				commandQueue.append(cmd)
				# print(commandQueue)
				# print(nextCommands)

		if (commands[0] == "hold"):
			for cmd in commands:
				duration = 0.9
				if(cmd == "left"):
					controller.LX = STICK_MIN
					delayed_reset(duration)
				if(cmd == "right"):
					controller.LX = STICK_MAX
					delayed_reset(duration)
				if(cmd == "up"):
					controller.LY = STICK_MIN
					delayed_reset(duration)
				if(cmd == "down"):
					controller.LY = STICK_MAX
					delayed_reset(duration)

				if(cmd == "dleft"):
					controller.dpad = DPAD_LEFT
					delayed_reset(duration)
				if(cmd == "dright"):
					controller.dpad = DPAD_RIGHT
					delayed_reset(duration)
				if(cmd == "dup"):
					controller.dpad = DPAD_UP
					delayed_reset(duration)
				if(cmd == "ddown"):
					controller.dpad = DPAD_DOWN
					delayed_reset(duration)

				if(cmd == "look left"):
					controller.RX = STICK_MIN
					delayed_reset(duration)
				if(cmd == "look right"):
					controller.RX = STICK_MAX
					delayed_reset(duration)
				if(cmd == "look up"):
					controller.RY = STICK_MIN
					delayed_reset(duration)
				if(cmd == "look down"):
					controller.RY = STICK_MAX
					delayed_reset(duration)
				
				if(cmd == "a"):
					controller.a = 1
					delayed_reset(duration)
				if(cmd == "b"):
					controller.b = 1
					delayed_reset(duration)
				if(cmd == "x"):
					controller.x = 1
					delayed_reset(duration)
				if(cmd == "y"):
					controller.y = 1
					delayed_reset(duration)

				if(cmd == "l"):
					controller.l = 1
					delayed_reset(duration)
				if(cmd == "r"):
					controller.r = 1
					delayed_reset(duration)
				if(cmd == "zl"):
					controller.zl = 1
					delayed_reset(duration)
				if(cmd == "zr"):
					controller.zr = 1
					delayed_reset(duration)

				if(cmd == "minus"):
					controller.plus = 1
					delayed_reset(duration)
				if(cmd == "plus"):
					controller.plus = 1
					delayed_reset(duration)
	

	# so I don't get stuck:
	# if(win32api.GetAsyncKeyState(win32con.VK_ESCAPE)):
	# 	controller.send('RELEASE')
	# 	controller.ser.close()
	# 	exit()

	controller.getOutput()

	end = time.clock()
	diffInSeconds = end - start
	diffInMilliSeconds = diffInSeconds*1000

	if(diffInMilliSeconds > 160):
		start = time.clock()
		controller.send(controller.output)
		if(len(commandQueue) > 0):
			nextCommands.append(commandQueue[0])
			del commandQueue[0]

		if(len(nextCommands) > 0):
			# print(nextCommands)
			cmd = nextCommands[-1]
			del nextCommands[-1]

			duration = 0

			if(cmd == "left"):
				controller.LX = STICK_MIN
				duration = 0.3
			if(cmd == "right"):
				controller.LX = STICK_MAX
				duration = 0.3
			if(cmd == "up"):
				controller.LY = STICK_MIN
				duration = 0.3
			if(cmd == "down"):
				controller.LY = STICK_MAX
				duration = 0.3

			if(cmd == "hleft"):
				controller.LX = STICK_MIN
				duration = 2.0
			if(cmd == "hright"):
				controller.LX = STICK_MAX
				duration = 2.0
			if(cmd == "hup"):
				controller.LY = STICK_MIN
				duration = 2.0
			if(cmd == "hdown"):
				controller.LY = STICK_MAX
				duration = 2.0

			if(cmd == "hhleft"):
				controller.LX = STICK_MIN
				duration = 10.0
			if(cmd == "hhright"):
				controller.LX = STICK_MAX
				duration = 10.0
			if(cmd == "hhup"):
				controller.LY = STICK_MIN
				duration = 10.0
			if(cmd == "hhdown"):
				controller.LY = STICK_MAX
				duration = 10.0

			
			if(cmd == "dleft"):
				controller.dpad = DPAD_LEFT
				duration = 0.3
			if(cmd == "dright"):
				controller.dpad = DPAD_RIGHT
				duration = 0.3
			if(cmd == "dup"):
				controller.dpad = DPAD_UP
				duration = 0.3
			if(cmd == "ddown"):
				controller.dpad = DPAD_DOWN
				duration = 0.3
			
			if(cmd == "look left"):
				controller.RX = STICK_MIN
				duration = 0.4
			if(cmd == "look right"):
				controller.RX = STICK_MAX
				duration = 0.4
			
			if(cmd == "look up"):
				controller.RY = STICK_MIN
				duration = 0.3
			if(cmd == "look down"):
				controller.RY = STICK_MAX
				duration = 0.3
			
			if(cmd == "a"):
				controller.a = 1
				duration = 0.01
			if(cmd == "b"):
				controller.b = 1
				duration = 0.01
			if(cmd == "x"):
				controller.x = 1
				duration = 0.9
			if(cmd == "y"):
				controller.y = 1
				duration = 0.8
			if(cmd == "l"):
				controller.l = 1
				duration = 0.01
			if(cmd == "r"):
				controller.r = 1
				duration = 0.01
			if(cmd == "zl"):
				controller.zl = 1
				duration = 0.01
			if(cmd == "zr"):
				controller.zr = 1
				duration = 0.01
			if(cmd == "minus"):
				controller.plus = 1
				duration = 0.01
			if(cmd == "plus"):
				controller.plus = 1
				duration = 0.01
			send_and_reset(duration)

			controller.getOutput()
			controller.send(controller.output)

