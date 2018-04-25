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

def send_and_reset(duration=0.1, reset=1):
	controller.getOutput()
	controller.send(controller.output)
	sleep(duration)
	if(reset):
		controller.reset()

validCommands = ["spin", "swim", "back flip", "ground pound", "groundpound", "gp", "bf", "cap bounce", "sdive", "sdive2", "hdive", "hdive2", "hdive3", "dive", "dive2", "dive3", "roll", "roll2", "backflip", "backflip2", "sssu", "sssd", "sssl", "sssr", "sb", "suu", "", "up", "down", "left", "right", "u", "d", "l", "r", "hup", "hdown", "hleft", "hright", "hhup", "hhdown", "hhleft", "hhright", "hu", "hd", "hl", "hr", "su", "sd", "sl", "sr", "sup", "sdown", "sleft", "sright", "ssu", "ssd", "ssl", "ssr", "ssup", "ssdown", "ssleft", "ssright", "look up", "look down", "look left", "look right", "lu", "ld", "ll", "lr", "hlu", "hld", "hll", "hlr", "slu", "sld", "sll", "slr", "dup", "ddown", "dleft", "dright", "du", "dd", "dl", "dr", "a", "b", "x", "y", "ha", "hb", "hx", "hy", "hhb", "hhhb", "l", "zl", "lock", "r", "zr", "plus", "minus", "long jump", "long jump2", "long jump3", "jump forward", "jump forward2", "jump back", "jump back2", "dive", "dive2"]


commandQueue = []
nextCommands = []

lockon = False

while True:

	# control switch here:

	duration = 0.2

	response = twitchBot.stayConnected()
	#response = "none"
	if(response != "none"):
		username = re.search(r"\w+", response).group(0) # return the entire matcsh
		message = CHAT_MSG.sub("", response)
		message = message.strip()
		message = message.lower()
		# print(username + ": " + message)
		# print("0" + message + "0")

		commands = [x.strip() for x in message.split(',')]
		cmd = "none"

		if(commands[0] == "!controls"):
			msg = "@" + username + " look at the description Kappa (this is a bot)"
			msg = "------------------------------------------\
(Case does NOT matter)---------------------------------------\
(sleft/sright/sup/sdown holds for 0.1 seconds)--------------\
(left/right/up/down holds for 0.3 seconds)-----------------\
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
		if (not valid):
			commands = ["none"]


		if(len(commands) > 20):
			commands = []
			continue
		for cmd in commands:
			commandQueue.append(cmd)


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
			reset = 1

			if(cmd == "sssleft" or cmd == "sssl"):
				controller.LX = STICK_MIN
				duration = 0.01
			if(cmd == "sssright" or cmd == "sssr"):
				controller.LX = STICK_MAX
				duration = 0.01
			if(cmd == "sssup" or cmd == "sssu"):
				controller.LY = STICK_MIN
				duration = 0.01
			if(cmd == "sssdown" or cmd == "sssd"):
				controller.LY = STICK_MAX
				duration = 0.01

			if(cmd == "ssleft" or cmd == "ssl"):
				controller.LX = STICK_MIN
				duration = 0.1
			if(cmd == "ssright" or cmd == "ssr"):
				controller.LX = STICK_MAX
				duration = 0.1
			if(cmd == "ssup" or cmd == "ssu"):
				controller.LY = STICK_MIN
				duration = 0.1
			if(cmd == "ssdown" or cmd == "ssd"):
				controller.LY = STICK_MAX
				duration = 0.1

			if(cmd == "sleft" or cmd == "sl"):
				controller.LX = STICK_MIN
				duration = 0.3
			if(cmd == "sright" or cmd == "sr"):
				controller.LX = STICK_MAX
				duration = 0.3
			if(cmd == "sup" or cmd == "su"):
				controller.LY = STICK_MIN
				duration = 0.3
			if(cmd == "sdown" or cmd == "sd"):
				controller.LY = STICK_MAX
				duration = 0.3

			if(cmd == "suup" or cmd == "suu"):
				controller.LY = STICK_MIN
				duration = 0.5

			if(cmd == "left" or cmd == "l"):
				controller.LX = STICK_MIN
				duration = 0.6
			if(cmd == "right" or cmd == "r"):
				controller.LX = STICK_MAX
				duration = 0.6
			if(cmd == "up" or cmd == "u"):
				controller.LY = STICK_MIN
				duration = 0.6
			if(cmd == "down" or cmd == "d"):
				controller.LY = STICK_MAX
				duration = 0.6

			if(cmd == "hleft" or cmd == "hl"):
				controller.LX = STICK_MIN
				duration = 1.5
			if(cmd == "hright" or cmd == "hr"):
				controller.LX = STICK_MAX
				duration = 1.5
			if(cmd == "hup" or cmd == "hu"):
				controller.LY = STICK_MIN
				duration = 1.5
			if(cmd == "hdown" or cmd == "hd"):
				controller.LY = STICK_MAX
				duration = 1.5

			if(cmd == "hhleft"):
				controller.LX = STICK_MIN
				duration = 4.0
			if(cmd == "hhright"):
				controller.LX = STICK_MAX
				duration = 4.0
			if(cmd == "hhup"):
				controller.LY = STICK_MIN
				duration = 4.0
			if(cmd == "hhdown"):
				controller.LY = STICK_MAX
				duration = 4.0

			
			if(cmd == "dleft" or cmd == "dl"):
				controller.dpad = DPAD_LEFT
				duration = 0.3
			if(cmd == "dright" or cmd == "dr"):
				controller.dpad = DPAD_RIGHT
				duration = 0.3
			if(cmd == "dup" or cmd == "du"):
				controller.dpad = DPAD_UP
				duration = 0.3
			if(cmd == "ddown" or cmd == "dd"):
				controller.dpad = DPAD_DOWN
				duration = 0.3



			if(cmd == "slook left" or cmd == "sll"):
				controller.RX = STICK_MIN
				duration = 0.1
			if(cmd == "slook right" or cmd == "slr"):
				controller.RX = STICK_MAX
				duration = 0.1
			if(cmd == "slook up" or cmd == "slu"):
				controller.RY = STICK_MIN
				duration = 0.1
			if(cmd == "slook down" or cmd == "sld"):
				controller.RY = STICK_MAX
				duration = 0.1

			if(cmd == "look left" or cmd == "ll"):
				controller.RX = STICK_MIN
				duration = 0.3
			if(cmd == "look right" or cmd == "lr"):
				controller.RX = STICK_MAX
				duration = 0.3
			if(cmd == "look up" or cmd == "lu"):
				controller.RY = STICK_MIN
				duration = 0.3
			if(cmd == "look down" or cmd == "ld"):
				controller.RY = STICK_MAX
				duration = 0.3

			if(cmd == "hlook left" or cmd == "hll"):
				controller.RX = STICK_MIN
				duration = 0.6
			if(cmd == "hlook right" or cmd == "hlr"):
				controller.RX = STICK_MAX
				duration = 0.6
			if(cmd == "hlook up" or cmd == "hlu"):
				controller.RY = STICK_MIN
				duration = 0.6
			if(cmd == "hlook down" or cmd == "hld"):
				controller.RY = STICK_MAX
				duration = 0.6
			
			if(cmd == "a"):
				controller.a = 1
				duration = 0.3
			if(cmd == "ha"):
				controller.a = 1
				duration = 0.5
			if(cmd == "sb"):
				controller.b = 1
				duration = 0.1
			if(cmd == "b"):
				controller.b = 1
				duration = 0.4
			if(cmd == "hb"):
				controller.b = 1
				duration = 0.5
			if(cmd == "hhb"):
				controller.b = 1
				duration = 0.8
			if(cmd == "hhhb"):
				controller.b = 1
				duration = 1.8
			if(cmd == "x"):
				controller.x = 1
				duration = 0.3
			if(cmd == "hx"):
				controller.y = 1
				duration = 0.5
			if(cmd == "y"):
				controller.y = 1
				duration = 0.3
			if(cmd == "hy"):
				controller.y = 1
				duration = 0.7
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
				controller.minus = 1
				duration = 0.01
			if(cmd == "lock"):
				lockon == not(lockon)
			if(lockon):
				controller.zl = 1
				duration = 1
			# if(cmd == "plus"):
			# 	controller.plus = 1
			# 	duration = 0.01

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
				duration = 1.0

			if(cmd == "jump forward"):
				controller.LY = STICK_MIN
				duration = 0.3
				nextCommands.insert(0, "jump forward2")
				reset = 0
			if(cmd == "jump forward2"):
				controller.LY = STICK_MIN
				controller.b = 1
				duration = 0.4

			if(cmd == "jump back"):
				controller.LY = STICK_MAX
				duration = 0.3
				nextCommands.insert(0, "jump forward2")
				reset = 0
			if(cmd == "jump back2"):
				controller.LY = STICK_MAX
				controller.b = 1
				duration = 0.4

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

			if(cmd == "roll"):
				controller.zl = 1
				duration = 0.01
				nextCommands.insert(0, "roll2")
				reset = 0
			if(cmd == "roll2"):
				controller.y = 1
				duration = 0.1

			if(cmd == "backflip" or cmd == "bf" or cmd == "back flip"):
				controller.zl = 1
				duration = 0.01
				nextCommands.insert(0, "backflip2")
				reset = 0
			if(cmd == "backflip2"):
				controller.b = 1
				duration = 0.1

			if(cmd == "ground pound" or cmd == "gp" or cmd == "groundpound"):
				controller.b = 1
				duration = 0.01
				nextCommands.insert(0, "ground pound2")
				reset = 0
			if(cmd == "ground pound2"):
				controller.zl = 1
				duration = 0.1

			d = 0.01

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
				#nextCommands.insert(0, "spin6")
				reset = 1

			if("+" in cmd):
				btns = [x.strip() for x in cmd.split('+')]
				for btn in btns:
					if(btn == "left"):
						controller.LX = STICK_MIN
						duration = 0.6
					if(btn == "right"):
						controller.LX = STICK_MAX
						duration = 0.6
					if(btn == "up"):
						controller.LY = STICK_MIN
						duration = 0.6
					if(btn == "down"):
						controller.LY = STICK_MAX
						duration = 0.6
					if(btn == "dleft"):
						controller.dpad = DPAD_LEFT
						duration = 0.3
					if(btn == "dright"):
						controller.dpad = DPAD_RIGHT
						duration = 0.3
					if(btn == "dup"):
						controller.dpad = DPAD_UP
						duration = 0.3
					if(btn == "ddown"):
						controller.dpad = DPAD_DOWN
						duration = 0.3
					
					if(btn == "look left"):
						controller.RX = STICK_MIN
						duration = 0.4
					if(btn == "look right"):
						controller.RX = STICK_MAX
						duration = 0.4
					if(btn == "look up"):
						controller.RY = STICK_MIN
						duration = 0.3
					if(btn == "look down"):
						controller.RY = STICK_MAX
						duration = 0.3
					if(btn == "a"):
						controller.a = 1
						duration = 0.3
					if(btn == "b"):
						controller.b = 1
						duration = 0.4
					if(btn == "x"):
						controller.x = 1
						duration = 0.9
					if(btn == "y"):
						controller.y = 1
						duration = 0.8
					if(btn == "l"):
						controller.l = 1
						duration = 0.01
					if(btn == "r"):
						controller.r = 1
						duration = 0.01
					if(btn == "zl"):
						controller.zl = 1
						duration = 0.01
					if(btn == "zr"):
						controller.zr = 1
						duration = 0.01
					if(btn == "minus"):
						controller.minus = 1
						duration = 0.01


			send_and_reset(duration, reset)

			controller.getOutput()
			controller.send(controller.output)

