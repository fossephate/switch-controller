
# random:
from random import randint

# vjoy:
import pyvjoy


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

def is_pressed(btns, n):
	return ((btns & (1 << n)) != 0)

class SwitchController2():

	def __init__(self):

		self.vjoy = None
		self.deviceNumber = 0
		self.gyroEnabled = 0

		self.btns = 0
		self.axes = [STICK_CENTER, STICK_CENTER, STICK_CENTER, STICK_CENTER, 0, 0]

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

	def reset(self):

		self.btns = 0
		self.axes = [STICK_CENTER, STICK_CENTER, STICK_CENTER, STICK_CENTER, 0, 0]

		self.dpad 		= DPAD_CENTER
		self.up			= 0
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

	def setButtons(self, btns):
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
		if (is_pressed(btns, 5)):
			self.zl = 1
		if (is_pressed(btns, 6)):
			self.lstick = 1
		if (is_pressed(btns, 7)):
			self.minus = 1
		if (is_pressed(btns, 8)):
			self.capture = 1
		if (is_pressed(btns, 9)):
			self.a = 1
		if (is_pressed(btns, 10)):
			self.b = 1
		if (is_pressed(btns, 11)):
			self.x = 1
		if (is_pressed(btns, 12)):
			self.y = 1
		if (is_pressed(btns, 13)):
			self.r = 1
		if (is_pressed(btns, 14)):
			self.zr = 1
		if (is_pressed(btns, 15)):
			self.rstick = 1
		if (is_pressed(btns, 16)):
			self.plus = 1
		if (is_pressed(btns, 17)):
			self.home = 1
		self.setDpad()

	def setBtns(self):
		return

	def queue_send(self):
		self.send()

	def send(self):

		buttons = []

		if (self.y):
			buttons.append(1)
		if (self.b):
			buttons.append(2)
		if (self.a):
			buttons.append(3)
		if (self.x):
			buttons.append(4)

		if (self.l):
			buttons.append(5)
		if (self.r):
			buttons.append(6)

		if (self.minus):
			buttons.append(9)
		if (self.plus):
			buttons.append(10)

		if (self.lstick):
			buttons.append(11)
		if (self.rstick):
			buttons.append(12)

		if (self.home):
			buttons.append(13)
		if (self.capture):
			buttons.append(14)


		# dpad:

		if (self.dpad == 0):# up
			buttons.append(21)

		if (self.dpad == 1):# up right
			buttons.append(22)

		if (self.dpad == 2):# right
			buttons.append(21)
			buttons.append(22)

		if (self.dpad == 3):# down right
			buttons.append(23)

		if (self.dpad == 4):# down
			buttons.append(21)
			buttons.append(23)

		if (self.dpad == 5):# down left
			buttons.append(22)
			buttons.append(23)

		if (self.dpad == 6):# left
			buttons.append(21)
			buttons.append(22)
			buttons.append(23)

		if (self.dpad == 7):# up left
			buttons.append(24)

		# if (self.dpad == 8):# nothing
		# 	self.vjoy.set_button(21, 0)
		# 	self.vjoy.set_button(22, 0)
		# 	self.vjoy.set_button(23, 0)
		# 	self.vjoy.set_button(24, 0)

		# self.vjoy.set_button(25, 1)

		# min = 250
		# max = 300
		min = 0
		max = 0

		# buttons
		btns = 0
		for num in buttons:
			btns += 2 ** (num-1)

		if (self.vjoy == None):
			self.connect(1)
			print("vJoy wasn't connected!")
			return

		self.vjoy.data.lButtons = btns

		# scale = 128
		# scale2 = 32768
		scale = 32768

		# self.vjoy.data.wAxisX = ((self.axes[0] * scale) + randint(min, max))
		# self.vjoy.data.wAxisY = ((self.axes[1] * scale) + randint(min, max))
		# self.vjoy.data.wAxisZ = ((self.axes[2] * scale) + randint(min, max))
		# self.vjoy.data.wAxisZRot = ((self.axes[3] * scale) + randint(min, max))
		# self.vjoy.data.wAxisXRot = int((self.axes[4] * scale2) + randint(min, max))
		# self.vjoy.data.wAxisYRot = int((self.axes[5] * scale2) + randint(min, max))
		self.vjoy.data.wAxisX 		= int(((self.axes[0] + 1) / 2) * scale)
		self.vjoy.data.wAxisY 		= int(((-self.axes[1] + 1) / 2) * scale)
		self.vjoy.data.wAxisZ 		= int(((self.axes[2] + 1) / 2) * scale)
		self.vjoy.data.wAxisZRot 	= int(((-self.axes[3] + 1) / 2) * scale)
		self.vjoy.data.wAxisXRot 	= int(self.axes[4] * scale)
		self.vjoy.data.wAxisYRot 	= int(self.axes[5] * scale)

		try:
			self.vjoy.update()
		except:
			print("some write error (xbox)")


	def connect(self, deviceNumber):
		self.deviceNumber = deviceNumber
		self.vjoy = pyvjoy.VJoyDevice(deviceNumber)
