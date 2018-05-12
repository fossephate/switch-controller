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

class SwitchController():

	def __init__(self):

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
		self.output += '1' if (self.lstick) else '0'
		self.output += '1' if (self.l) else '0'
		self.output += '1' if (self.zl) else '0'
		self.output += '1' if (self.minus) else '0'
		self.output += '1' if (self.capture) else '0'

		self.output += '1' if (self.a) else '0'
		self.output += '1' if (self.b) else '0'
		self.output += '1' if (self.x) else '0'
		self.output += '1' if (self.y) else '0'
		self.output += '1' if (self.rstick) else '0'
		self.output += '1' if (self.r) else '0'
		self.output += '1' if (self.zr) else '0'
		self.output += '1' if (self.plus) else '0'
		self.output += '1' if (self.home) else '0'

		self.output += " " + str(self.LX)
		self.output += " " + str(self.LY)
		self.output += " " + str(self.RX)
		self.output += " " + str(self.RY)

	def send(self, msg):
		try:
			self.ser.write(f'{msg}\r\n'.encode('utf-8'));
		except:
			print("some write error")
			pass


	def connect(self, port):
		self.ser = serial.Serial(port, 38400)