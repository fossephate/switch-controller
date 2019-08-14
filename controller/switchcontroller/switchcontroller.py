
import serial
from time import sleep

import binascii
import struct

from threading import Thread

STICK_MIN		= -1
STICK_MAX		= 1
STICK_CENTER	= 0

DPAD_UP          = 0x00
DPAD_UP_RIGHT    = 0x01
DPAD_RIGHT       = 0x02
DPAD_DOWN_RIGHT  = 0x03
DPAD_DOWN        = 0x04
DPAD_DOWN_LEFT   = 0x05
DPAD_LEFT        = 0x06
DPAD_UP_LEFT     = 0x07
DPAD_CENTER      = 0x08

SWITCH_Y       = 0x01
SWITCH_B       = 0x02
SWITCH_A       = 0x04
SWITCH_X       = 0x08
SWITCH_L       = 0x10
SWITCH_R       = 0x20
SWITCH_ZL      = 0x40
SWITCH_ZR      = 0x80
SWITCH_MINUS  = 0x100
SWITCH_PLUS   = 0x200
SWITCH_LSTICK  = 0x400
SWITCH_RSTICK  = 0x800
SWITCH_HOME    = 0x1000
SWITCH_CAPTURE = 0x2000

# import logging

# logger = logging.getLogger(__name__)

def is_pressed(btns, n):
	return ((btns & (1 << n)) != 0)

class SwitchController():

	def __init__(self):

		self.queue = []

		self.port = None

		self.btns = 0
		self.axs = [128, 128, 128, 128]


		self.ser = None

		# axes:
		self.axes = [0, 0, 0, 0]

		# buttons:
		self.dpad 		= DPAD_CENTER
		self.up 		= 0
		self.down 		= 0
		self.left 		= 0
		self.right 		= 0
		self.l 			= 0
		self.zl 		= 0
		self.lstick 	= 0
		self.minus		= 0
		self.capture	= 0

		self.a 		= 0
		self.b 		= 0
		self.x 		= 0
		self.y 		= 0
		self.r 		= 0
		self.zr		= 0
		self.rstick = 0
		self.plus	= 0
		self.home 	= 0

		self.output = ""

	def reset(self):

		self.btns = 0
		self.axs = [128, 128, 128, 128]
		self.axes = [0, 0, 0, 0]

		# buttons:
		self.dpad = DPAD_CENTER

		self.up 		= 0
		self.down 		= 0
		self.left 		= 0
		self.right 		= 0
		self.l 			= 0
		self.zl 		= 0
		self.lstick 	= 0
		self.minus		= 0
		self.capture	= 0

		self.a 		= 0
		self.b 		= 0
		self.x 		= 0
		self.y 		= 0
		self.r 		= 0
		self.zr		= 0
		self.rstick = 0
		self.plus	= 0
		self.home 	= 0

	def setButtons(self, btns):

		self.btns = 0

		if (is_pressed(btns, 0)):
			self.up = 1
		if (is_pressed(btns, 1)):
			self.down = 1
		if (is_pressed(btns, 2)):
			self.left = 1
		if (is_pressed(btns, 3)):
			self.right = 1

		if (is_pressed(btns, 4)):
			self.l = 1
			self.btns |= SWITCH_L
		if (is_pressed(btns, 5)):
			self.zl = 1
			self.btns |= SWITCH_ZL
		if (is_pressed(btns, 6)):
			self.lstick = 1
			self.btns |= SWITCH_LSTICK
		if (is_pressed(btns, 7)):
			self.minus = 1
			self.btns |= SWITCH_MINUS
		if (is_pressed(btns, 8)):
			self.capture = 1
			self.btns |= SWITCH_CAPTURE
		if (is_pressed(btns, 9)):
			self.a = 1
			self.btns |= SWITCH_A
		if (is_pressed(btns, 10)):
			self.b = 1
			self.btns |= SWITCH_B
		if (is_pressed(btns, 11)):
			self.x = 1
			self.btns |= SWITCH_X
		if (is_pressed(btns, 12)):
			self.y = 1
			self.btns |= SWITCH_Y
		if (is_pressed(btns, 13)):
			self.r = 1
			self.btns |= SWITCH_R
		if (is_pressed(btns, 14)):
			self.zr = 1
			self.btns |= SWITCH_ZR
		if (is_pressed(btns, 15)):
			self.rstick = 1
			self.btns |= SWITCH_RSTICK
		if (is_pressed(btns, 16)):
			self.plus = 1
			self.btns |= SWITCH_PLUS
		if (is_pressed(btns, 17)):
			self.home = 1
			self.btns |= SWITCH_HOME

		self.setDpad()

	def setDpad(self):
		if (self.up and self.left):
			self.dpad = 7
		elif (self.up and self.right):
			self.dpad = 1
		elif (self.down and self.left):
			self.dpad = 5
		elif (self.down and self.right):
			self.dpad = 3
		elif (self.up):
			self.dpad = 0
		elif (self.down):
			self.dpad = 4
		elif (self.left):
			self.dpad = 6
		elif (self.right):
			self.dpad = 2
		else:
			self.dpad = 8

	def setBtns(self):

		self.btns = 0

		if (self.l):
			self.btns |= SWITCH_L
		if (self.zl):
			self.btns |= SWITCH_ZL
		if (self.lstick):
			self.btns |= SWITCH_LSTICK
		if (self.minus):
			self.btns |= SWITCH_MINUS
		if (self.capture):
			self.btns |= SWITCH_CAPTURE
		if (self.a):
			self.btns |= SWITCH_A
		if (self.b):
			self.btns |= SWITCH_B
		if (self.x):
			self.btns |= SWITCH_X
		if (self.y):
			self.btns |= SWITCH_Y
		if (self.r):
			self.btns |= SWITCH_R
		if (self.zr):
			self.btns |= SWITCH_ZR
		if (self.rstick):
			self.btns |= SWITCH_RSTICK
		if (self.plus):
			self.btns |= SWITCH_PLUS
		if (self.home):
			self.btns |= SWITCH_HOME

		# set axs:
		for i in range(4):
			if (i == 1 or i == 3):
				self.axs[i] = int(((-self.axes[i] + 1) / 2) * 255)
			else:
				self.axs[i] = int(((self.axes[i] + 1) / 2) * 255)

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

		self.output += " " + str(self.axes[0])
		self.output += " " + str(self.axes[1])
		self.output += " " + str(self.axes[2])
		self.output += " " + str(self.axes[3])

		return self.output

	@property
	def bytes(self):
		"""Returns the state as a raw byte string."""
		return struct.pack("<HBBBBB", self.btns, self.dpad, *self.axs)

	@property
	def hex(self):
		"""Returns the state encoded as a hexadecimal byte string suitable for writing to a file or serial port."""
		return binascii.hexlify(self.bytes)

	def queue_send(self):
		# self.queue.append(self.hex)
		self.send(self.hex)

	def send(self, input):
		# https://stackoverflow.com/questions/39032581/python-serial-write-timeout
		# https://stackoverflow.com/questions/18313022/pyserial-write-instant-timeout/18314684#18314684
		try:
			# self.ser.write(f'{self.getOutput()}\r\n'.encode("utf-8"));
			self.ser.write(input + b"\n")
		except:
			print("some write error, probably write_timeout")
			# print("some write error, attempting reconnect:")
			# try:
			# 	# close old connection
			# 	self.ser.close()
			# 	# re-connect:
			# 	self.connect(self.port)
			# 	print("reconnected")
			# except:
			# 	print("reconnect failed")
			# pass


	def connect(self, port):
		self.port = port
		# self.ser = serial.Serial(self.port, 115200)# 38400
		self.ser = serial.Serial(
            self.port, 115200,
            bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE, timeout=9, write_timeout=9,
        )
		# self.ser = serial.Serial(
        #     self.port, 115200,
        #     bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
        #     stopbits=serial.STOPBITS_ONE, timeout=0, write_timeout=0,
        # )
		# self.ser.open()
		# print(self.ser.is_open)

	def loop(self):
		while True:
			# print(len(self.queue))
			if (len(self.queue) > 0):
				self.send(self.queue.pop(0))
			# sleep(0.000001)

	def start(self):
		# return
		thread = Thread(target=self.loop, args=())
		thread.start()
