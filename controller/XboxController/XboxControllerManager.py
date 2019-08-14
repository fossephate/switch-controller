
# config
try:
	from .config import *
except:
	from config import *

import sys
import logging
import argparse

import gevent.socket
from gevent import signal

from xbox.webapi.authentication.manager import AuthenticationManager

from xbox.sg.console import Console
from xbox.sg.enum import ConnectionState, GamePadButton
from xbox.sg.manager import InputManager
from xbox.sg.scripts import TOKENS_FILE

input_map = {
	"i": GamePadButton.DPadUp,
	"k": GamePadButton.DPadDown,
	"j": GamePadButton.DPadLeft,
	"l": GamePadButton.DPadRight,

	"a": GamePadButton.PadA,
	"b": GamePadButton.PadB,
	"x": GamePadButton.PadX,
	"y": GamePadButton.PadY,

	"t": GamePadButton.View,
	"z": GamePadButton.Nexu,
	"u": GamePadButton.Menu
}


def on_timeout():
	print('Connection Timeout')
	sys.exit(1)


class XboxControllerManager():

	def __init__(self):
		parser = argparse.ArgumentParser(description="Basic smartglass client")
		parser.add_argument('--tokens', '-t', default=TOKENS_FILE,
							help="Token file, created by xbox-authenticate script")
		parser.add_argument('--address', '-a',
							help="IP address of console")
		parser.add_argument('--refresh', '-r', action='store_true',
							help="Refresh xbox live tokens in provided token file")

		args = parser.parse_args()

		args.address = CONSOLE_IP

		logging.basicConfig(level=logging.DEBUG)

		try:
			auth_mgr = AuthenticationManager.from_file(args.tokens)
			auth_mgr.authenticate(do_refresh=args.refresh)
			auth_mgr.dump(args.tokens)
		except Exception as e:
			print("Failed to authenticate with provided tokens, Error: %s" % e)
			print("Please re-run xbox-authenticate to get a fresh set")
			sys.exit(1)

		userhash = auth_mgr.userinfo.userhash
		token = auth_mgr.xsts_token.jwt
		discovered = Console.discover(timeout=1, addr=args.address)
		if len(discovered):
			self.console = discovered[0]
			self.console.on_timeout += on_timeout
			self.console.add_manager(InputManager)
			state = self.console.connect(userhash, token)
			if state != ConnectionState.Connected:
				print("Connection failed")
				sys.exit(1)
			self.console.wait(1)

			# getch = get_getch_func()
			# while True:
				# ch = getch().decode("ASCII")
				# ch = getch()
				# print(ch)
				# if ord(ch) == 3:  # CTRL-C
				# 	sys.exit(1)
				#
				# elif ch not in input_map:
				# 	print("NOT_IN_MAP")
				# 	continue

				# button = input_map[ch]
				# console.gamepad_input(button)
				# console.wait(0.1)
				# console.gamepad_input(GamePadButton.Clear)

			# signal.signal(signal.SIGINT, lambda *args: console.protocol.stop())
			# console.protocol.serve_forever()

		else:
			print("No consoles discovered")
			sys.exit(1)

	def send_input(self, state):

		if (not self.console):
			return

		btns = 0

		if (state.up):
			btns |= GamePadButton.DPadUp.value
		if (state.down):
			btns |= GamePadButton.DPadDown.value
		if (state.left):
			btns |= GamePadButton.DPadLeft.value
		if (state.right):
			btns |= GamePadButton.DPadRight.value

		if (state.a):
			btns |= GamePadButton.PadA.value
		if (state.b):
			btns |= GamePadButton.PadB.value
		if (state.x):
			btns |= GamePadButton.PadX.value
		if (state.y):
			btns |= GamePadButton.PadY.value

		if (state.minus):
			btns |= GamePadButton.View.value
		if (state.plus):
			btns |= GamePadButton.Menu.value

		if (state.home):
			btns |= GamePadButton.Nexu.value




		self.console.gamepad_input(btns, 0, 0, (state.LX * 127), (state.LY * 127))

		return
