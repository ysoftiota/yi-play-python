#!/usr/bin/env python3
import time
import my_pyfirmata.pyfirmata as pyfirmata

# 1. Board autoinit
board = pyfirmata.util.autoload_board(ports_filter="YSoft IOTA Play")
it = pyfirmata.util.Iterator(board)
it.start()


# 2. Two examplex of accesing digital pins
# a) direct access:
led1 = board.digital[25]
button1 = board.digital[30]
button1.mode = pyfirmata.INPUT  # Mode must be set by hand

# b) smart get_pin method:
led2 = board.get_pin('d:26:o')  # read as "digital pin 26 in output mode"
button2 = board.get_pin('d:31:i')  # read as "digital pin 31 in unput mode"

led1_state = 0
led2_state = 0


# 3. In endless loop read button values and switch on/off leds
while True:
	time.sleep(0.1)
	if button1.read() == 0:  # Because this built-in button is in reverse logic
		led1_state = not led1_state
	if button2.read() == 0:  # Because this built-in button is in reverse logic
		led2_state = not led2_state

	led1.write(led1_state)
	led2.write(led2_state)
