#!/usr/bin/env python3

import my_pyfirmata.pyfirmata as pyfirmata  # Use forked version from local directory
import time

"""
Basic example of pyfirmata usage - blinking LEDs according to potentiometer.

Included:
*  Use digital I/O pins for LEDs
* Use digital I/O pins in PWM mode for RGB led
* Use analog input for potentiometer
"""

board = pyfirmata.util.autoload_board()
it = pyfirmata.util.Iterator(board)
it.start()

leds = []
leds.append(board.get_pin('d:5:o'))  # red LED
leds.append(board.get_pin('d:6:o'))  # yellow LED
leds.append(board.get_pin('d:7:o'))  # green LED

rgb_pwm = []
rgb_pwm.append(board.get_pin('d:10:p'))  # R
rgb_pwm.append(board.get_pin('d:11:p'))  # G
rgb_pwm.append(board.get_pin('d:12:p'))  # B

analog = board.get_pin('a:5:i')  # Potentiometer

angle = 0
angle_step = 1
while True:
	time.sleep(0.1)

	value = analog.read()
	if value is None:
		print(value)
		continue

	# Leds
	leds[0].write(value > 1.0 / 4)
	leds[1].write(value > 1.0 / 2)
	leds[2].write(value > 3.0 / 4)

	# RGB:
	v = round(value, 2)
	rgb_pwm[0].write(max(0, 1 - 3 * abs(v - 1)))
	rgb_pwm[1].write(max(0, 1 - 3 * abs(v - 0.5)))
	rgb_pwm[2].write(max(0, 1 - 3 * abs(v - 0)))
