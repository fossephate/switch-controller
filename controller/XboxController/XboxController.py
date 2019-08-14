
try:
	from .XboxControllerManager import XboxControllerManager
except:
	from XboxControllerManager import XboxControllerManager

# config
# try:
# 	from .config import *
# except:
# 	from config import *


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

# def gamepad_input(self, buttons, l_trigger=0, r_trigger=0, l_thumb_x=0,
#                   l_thumb_y=0, r_thumb_x=0, r_thumb_y=0):
#     """
#     Send gamepad input
#
#     Args:
#         buttons (:class:`GamePadButton`): Gamepad buttons bits
#         l_trigger (int): Left trigger value
#         r_trigger (int): Right trigger value
#         l_thumb_x (int): Left thumbstick X-axis value
#         l_thumb_y (int): Left thumbstick Y-axis value
#         r_thumb_x (int): Right thumbstick X-axis value
#         r_thumb_y (int): Right thumbstick Y-axis value

class XboxController():

	def __init__(self):

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

		self.LX = STICK_CENTER
		self.LY = STICK_CENTER
		self.RX = STICK_CENTER
		self.RY = STICK_CENTER

		self.output = ""

		self.controller = XboxControllerManager()

	def reset(self):

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

		self.LX = STICK_CENTER
		self.LY = STICK_CENTER
		self.RX = STICK_CENTER
		self.RY = STICK_CENTER

	def send(self):
		self.controller.send_input(self)
		return

	def connect(self, deviceNumber):
		return
