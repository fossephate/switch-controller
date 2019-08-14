from subprocess import Popen, PIPE
from time import sleep

import sys, os
if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    # application_path = sys._MEIPASS
	application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.abspath(__file__))

class ControllerManager():

	def __init__(self, controllerCount):

		self.controllerCount = str(controllerCount)
		self.p = None


	def init(self):
		programPath = application_path + "\\controller\\controller.exe"
		# self.p = Popen([programPath, self.controllerCount], shell=True, stdout=PIPE, stdin=PIPE)
		self.p = Popen([programPath, self.controllerCount], shell=False, stdout=PIPE, stdin=PIPE)

	def send(self, cNum, btns, LX, LY, RX, RY, LT, RT):
		data = "{} {} {} {} {} {} {} {}\n".format(cNum, btns, LX, LY, RX, RY, LT, RT)
		# self.p.stdin.write(data.encode())

		try:
			self.p.stdin.write(data.encode())
		except IOError as e:
			if e.errno == errno.EPIPE or e.errno == errno.EINVAL:
				# Stop loop on "Invalid pipe" or "Invalid argument".
				# No sense in continuing with broken pipe.
				print("error!")
			else:
				# raise any other error
				raise
		self.p.stdin.flush()
		# result = p.stdout.readline().strip()
		# print(result.decode())
