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

from switchcontroller.switchcontroller import *

screenWidth, screenHeight = pyautogui.size()
x = screenWidth/2
y = screenHeight/2
prevX = 0
prevY = 0


controller = SwitchController()
controller.connect("COM6")

start = time.clock()


while True:

	prevX = x
	prevY = y
	x, y = pyautogui.position()

	# deltaX = x - prevX
	# deltaY = y - prevY
	deltaX = x - screenWidth/2
	deltaY = y - screenHeight/2
	# pyautogui.moveTo(screenWidth/2, screenHeight/2)
	length = sqrt(deltaX**2 + deltaY**2)
	# if(length > 200):
	# 	pyautogui.moveTo(prevX, prevY)

	multiplier = 16
	# controller.RX = int((deltaX*multiplier)+128)
	# controller.RY = int((deltaY*multiplier)+128)

	# clamp:
	controller.RX = max(STICK_MIN, min(controller.RX, STICK_MAX))
	controller.RY = max(STICK_MIN, min(controller.RY, STICK_MAX))

	

	#sleep(0.01)

	controller.reset()

	if win32api.GetAsyncKeyState(ord("W")):
		controller.LY = STICK_MIN
	if win32api.GetAsyncKeyState(ord("S")):
		controller.LY = STICK_MAX
	if win32api.GetAsyncKeyState(ord("A")):
		controller.LX = STICK_MIN
	if win32api.GetAsyncKeyState(ord("D")):
		controller.LX = STICK_MAX

	if win32api.GetAsyncKeyState(ord("I")):
		controller.RY = STICK_MIN
	if win32api.GetAsyncKeyState(ord("K")):
		controller.RY = STICK_MAX
	if win32api.GetAsyncKeyState(ord("J")):
		controller.RX = STICK_MIN
	if win32api.GetAsyncKeyState(ord("L")):
		controller.RX = STICK_MAX

	if(win32api.GetAsyncKeyState(win32con.VK_RIGHT)):
		controller.a = 1
	if(win32api.GetAsyncKeyState(win32con.VK_DOWN)):
		controller.b = 1
	if(win32api.GetAsyncKeyState(win32con.VK_UP)):
		controller.x = 1
	if(win32api.GetAsyncKeyState(win32con.VK_LEFT)):
		controller.y = 1


	if win32api.GetAsyncKeyState(ord("T")):
		controller.dpad = DPAD_UP
	if win32api.GetAsyncKeyState(ord("G")):
		controller.dpad = DPAD_DOWN
	if win32api.GetAsyncKeyState(ord("F")):
		controller.dpad = DPAD_LEFT
	if win32api.GetAsyncKeyState(ord("H")):
		controller.dpad = DPAD_RIGHT


	# l/r and zl/zr:
	if win32api.GetAsyncKeyState(ord("O")):
		controller.l = 1
	if win32api.GetAsyncKeyState(ord("P")):
		controller.r = 1
	if win32api.GetAsyncKeyState(ord("9")):
		controller.zl = 1
	if win32api.GetAsyncKeyState(ord("0")):
		controller.zr = 1

	# minus/plus
	if win32api.GetAsyncKeyState(ord("5")):
		controller.minus = 1
	if win32api.GetAsyncKeyState(ord("6")):
		controller.plus = 1


	# so I don't get stuck:
	if(win32api.GetAsyncKeyState(win32con.VK_ESCAPE)):
		controller.send("RELEASE")
		controller.ser.close()
		exit()

	controller.getOutput()

	end = time.clock()
	diffInSeconds = end - start
	diffInMilliSeconds = diffInSeconds*1000

	if(diffInMilliSeconds > 80):
		start = time.clock()
		controller.send(controller.output)