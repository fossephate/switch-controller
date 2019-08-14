from time import sleep

import pygame

# switch controller:
from SwitchController.SwitchController import *
from SwitchController.SwitchController2 import SwitchController2


controllers = [SwitchController(), SwitchController(), SwitchController(), SwitchController(), SwitchController2()]

for i in range(0, 4):
	com = "COM" + str(i + 1)
	try:
		controllers[i].connect(com)
		controllers[i].start()
	except:
		pass



# while True:
# 	sleep(1)

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

pygame.init()

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
# joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


# Get count of joysticks
joystick_count = pygame.joystick.get_count()

# while (True):
#
# 	sleep(0.1)
#
# 	# EVENT PROCESSING STEP
# 	for event in pygame.event.get(): # User did something
# 		if event.type == pygame.QUIT: # If user clicked close
# 			done=True # Flag that we are done so we exit this loop
#
# 			# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
# 		if event.type == pygame.JOYBUTTONDOWN:
# 			print("Joystick button pressed.")
# 		if event.type == pygame.JOYBUTTONUP:
# 			print("Joystick button released.")

	# # For each joystick:
	# for i in range(joystick_count):
	# 	joystick = pygame.joystick.Joystick(i)
	# 	joystick.init()
	#
	# 	num_axes = joystick.get_numaxes()
	# 	for i in range( num_axes ):
	# 		axis = joystick.get_axis(i)
	# 		# textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis)
	# 	# textPrint.unindent()
	#
	# 	num_buttons = joystick.get_numbuttons()
	# 	# textPrint.print(screen, "Number of buttons: {}".format(buttons) )
	# 	# textPrint.indent()
	# 	for i in range(num_buttons):
	# 		button = joystick.get_button(i)
	# 		# textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )
	# 		print(button)

# print(joysticks[0].get_button())
# print(joysticks[1])
# print(joysticks[2])

# -------- Main Program Loop -----------
while True:
	sleep(0.1)
	# EVENT PROCESSING STEP
	for event in pygame.event.get(): # User did something
		# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
		if event.type == pygame.JOYBUTTONDOWN:
			print("Joystick button pressed.")
		if event.type == pygame.JOYBUTTONUP:
			print("Joystick button released.")

	# Get count of joysticks
	joystick_count = pygame.joystick.get_count()

	# For each joystick:
	for i in range(joystick_count):
		joystick = pygame.joystick.Joystick(i)
		joystick.init()

		# Get the name from the OS for the controller/joystick
		name = joystick.get_name()

		# Usually axis run in pairs, up/down for one, and left/right for
		# the other.
		axes = joystick.get_numaxes()

		for i in range(axes):
			axis = joystick.get_axis( i )

		buttons = joystick.get_numbuttons()

		for i in range(buttons):
			button = joystick.get_button(i)

		# Hat switch. All or nothing for direction, not like joysticks.
		# Value comes back in an array.
		hats = joystick.get_numhats()

		for i in range(hats):
			hat = joystick.get_hat(i)

	# Limit to 20 frames per second
	# clock.tick(20)

# Close the window and quit.
pygame.quit()
