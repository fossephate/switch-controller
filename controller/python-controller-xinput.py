import pyvjoy

#Pythonic API, item-at-a-time

vjoy = pyvjoy.VJoyDevice(1)

#turn button number 15 on
vjoy.set_button(15,1)

#Notice the args are (buttonID,state) whereas vJoy's native API is the other way around.


#turn button 15 off again
vjoy.set_button(15,0)

#Set X axis to fully left
vjoy.set_axis(pyvjoy.HID_USAGE_X, 0x1)

#Set X axis to fully right
j.set_axis(pyvjoy.HID_USAGE_X, 0x8000)

#Also implemented:

vjoy.reset()
vjoy.reset_buttons()
vjoy.reset_povs()


# #The 'efficient' method as described in vJoy's docs - set multiple values at once

# j.data
# >>> <pyvjoy._sdk._JOYSTICK_POSITION_V2 at 0x....>


vjoy.data.lButtons = 19 # buttons number 1,2 and 5 (1+2+16)
vjoy.data.wAxisX = 0x2000 
vjoy.data.wAxisY = 0x7500

#send data to vJoy device
vjoy.update()
