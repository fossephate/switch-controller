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

# random:
from random import randint

# vjoy:
import pyvjoy


STICK_MIN		= 0
STICK_MAX		= 255
STICK_CENTER	= 128

DPAD_UP          = 0x00
DPAD_UP_RIGHT    = 0x01
DPAD_RIGHT       = 0x02
DPAD_DOWN_RIGHT  = 0x03
DPAD_DOWN        = 0x04
DPAD_DOWN_LEFT   = 0x05
DPAD_LEFT        = 0x06
DPAD_UP_LEFT     = 0x07
DPAD_CENTER      = 0x08

class SwitchController2():

	def __init__(self):

		self.vjoy = None

		self.gyroEnabled = 0

		self.dpad 		= DPAD_CENTER
		self.up 		= 0
		self.down 		= 0
		self.left 		= 0
		self.right 		= 0

		self.lstick 	= 0
		self.l 			= 0
		self.zl 		= 0
		self.minus		= 0
		self.capture	= 0

		self.a 		= 0
		self.b 		= 0
		self.x 		= 0
		self.y 		= 0
		self.rstick = 0
		self.r 		= 0
		self.zr		= 0
		self.plus	= 0
		self.home 	= 0

		self.LX = STICK_CENTER
		self.LY = STICK_CENTER
		self.RX = STICK_CENTER
		self.RY = STICK_CENTER

		self.output = ""

	def reset(self):

		self.dpad 		= DPAD_CENTER
		self.up			= 0
		self.down 		= 0
		self.left 		= 0
		self.right 		= 0

		self.lstick 	= 0
		self.l 			= 0
		self.zl 		= 0
		self.minus		= 0
		self.capture	= 0

		self.a 		= 0
		self.b 		= 0
		self.x 		= 0
		self.y 		= 0
		self.rstick = 0
		self.r 		= 0
		self.zr		= 0
		self.plus	= 0
		self.home 	= 0

		self.LX = STICK_CENTER
		self.LY = STICK_CENTER
		self.RX = STICK_CENTER
		self.RY = STICK_CENTER

	def getOutput(self):

		self.output = ""

		self.output += str(self.dpad)
		# self.output += "1" if (self.up) else "0"
		# self.output += "1" if (self.down) else "0"
		# self.output += "1" if (self.left) else "0"
		# self.output += "1" if (self.right) else "0"
		self.output += "1" if (self.lstick) else "0"
		self.output += "1" if (self.l) else "0"
		self.output += "1" if (self.zl) else "0"
		self.output += "1" if (self.minus) else "0"
		self.output += "1" if (self.capture) else "0"

		self.output += "1" if (self.a) else "0"
		self.output += "1" if (self.b) else "0"
		self.output += "1" if (self.x) else "0"
		self.output += "1" if (self.y) else "0"
		self.output += "1" if (self.rstick) else "0"
		self.output += "1" if (self.r) else "0"
		self.output += "1" if (self.zr) else "0"
		self.output += "1" if (self.plus) else "0"
		self.output += "1" if (self.home) else "0"

		self.output += " " + str(self.LX)
		self.output += " " + str(self.LY)
		self.output += " " + str(self.RX)
		self.output += " " + str(self.RY)

	def send(self, msg):

		# try:

		# 1 -> y
		# 2 -> b?
		# 3 -> a?
		# 4 -> x
		# 12 -> rstick
		# 13 -> home
		# 14 -> capture

		# self.vjoy.reset()
		# self.vjoy.reset_buttons()
		# self.vjoy.reset_povs()

		buttons = []

		scale = 124


		# if (self.a):
		# 	buttons.append(3)
		# if (self.b):
		# 	buttons.append(2)
		# if (self.x):
		# 	buttons.append(4)
		# if (self.y):
		# 	buttons.append(1)
		#
		# if (self.rstick):
		# 	buttons.append(12)
		#
		# if (self.home):
		# 	buttons.append(13)
		# if (self.capture):
		# 	buttons.append(14)

		self.vjoy.set_button(1, self.y)
		self.vjoy.set_button(2, self.b)
		self.vjoy.set_button(3, self.a)
		self.vjoy.set_button(4, self.x)

		self.vjoy.set_button(5, self.l)
		self.vjoy.set_button(6, self.r)

		self.vjoy.set_button(9, self.minus)
		self.vjoy.set_button(10, self.plus)

		self.vjoy.set_button(13, self.home)
		self.vjoy.set_button(14, self.capture)
		# self.vjoy.set_button(3, self.a)


		# dpad:

		if (self.dpad == 0):# up
			self.vjoy.set_button(21, 1)

		if (self.dpad == 1):# up right
			self.vjoy.set_button(22, 1)

		if (self.dpad == 2):# right
			self.vjoy.set_button(21, 1)
			self.vjoy.set_button(22, 1)

		if (self.dpad == 3):# down right
			self.vjoy.set_button(23, 1)

		if (self.dpad == 4):# down
			self.vjoy.set_button(21, 1)
			self.vjoy.set_button(23, 1)

		if (self.dpad == 5):# down left
			self.vjoy.set_button(22, 1)
			self.vjoy.set_button(23, 1)

		if (self.dpad == 6):# left
			self.vjoy.set_button(21, 1)
			self.vjoy.set_button(22, 1)
			self.vjoy.set_button(23, 1)

		if (self.dpad == 7):# up left
			self.vjoy.set_button(24, 1)

		if (self.dpad == 8):# nothing
			self.vjoy.set_button(21, 0)
			self.vjoy.set_button(22, 0)
			self.vjoy.set_button(23, 0)
			self.vjoy.set_button(24, 0)

		self.vjoy.set_button(11, self.lstick)
		self.vjoy.set_button(12, self.rstick)

		# self.vjoy.set_button(25, 1)

		min = 100
		max = 300

		self.vjoy.set_axis(pyvjoy.HID_USAGE_X, (self.LX * scale) + randint(min, max))
		self.vjoy.set_axis(pyvjoy.HID_USAGE_Y, (self.LY * scale) + randint(min, max))

		self.vjoy.set_axis(pyvjoy.HID_USAGE_Z, (self.RX * scale) + randint(min, max))
		self.vjoy.set_axis(pyvjoy.HID_USAGE_RZ, (self.RY * scale) + randint(min, max))

		# print(self.LY)

		self.vjoy.set_button(15, self.zl)
		self.vjoy.set_button(16, self.zr)



		self.vjoy.set_axis(pyvjoy.HID_USAGE_RX, 0x1)
		self.vjoy.set_axis(pyvjoy.HID_USAGE_RY, 0x1)

		# enable gyro mode:
		self.vjoy.set_button(17, self.gyroEnabled)

		# if (self.zl):
		# 	self.vjoy.set_axis(pyvjoy.HID_USAGE_RX, 0x8000)
		# else:
		# 	self.vjoy.set_axis(pyvjoy.HID_USAGE_RX, 0x1)
		#
		# if (self.zr):
		# 	self.vjoy.set_axis(pyvjoy.HID_USAGE_RY, 0x8000)
		# else:
		# 	self.vjoy.set_axis(pyvjoy.HID_USAGE_RY, 0x1)

		# self.vjoy.set_axis(0x30, self.LX * scale)
		# self.vjoy.set_axis(0x31, self.LY * scale)
		# self.vjoy.set_axis(0x32, 0x4000)
		# self.vjoy.set_axis(0x33, self.RX * scale)
		# self.vjoy.set_axis(0x34, self.RY * scale)
		# self.vjoy.set_axis(0x35, 0x4000)

		# # buttons
		# btns = 0
		# for num in buttons:
		# 	btns += 2 ** num
		#
		# self.vjoy.data.lButtons = btns


		# self.vjoy.data.wAxisX = 0x4000
		# self.vjoy.data.wAxisY = 0x4000
		# self.vjoy.data.wAxisZ = 0x4000
		# self.vjoy.data.wAxisXRot = 0x4000
		# self.vjoy.data.wAxisYRot = 0x4000
		# self.vjoy.data.wAxisZRot = 0x4000

		# self.vjoy.update()
		# except:
		# 	print("some write error")


	def connect(self, deviceNumber):
		# self.ser = serial.Serial(port, 38400)
		self.vjoy = pyvjoy.VJoyDevice(deviceNumber)
