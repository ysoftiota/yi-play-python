#!/usr/bin/env python3
import time
import my_pyfirmata.pyfirmata as pyfirmata

"""
Reading onboard temperature and humidity sensors using I2C.

Included:
* I2C read/write
"""


board = pyfirmata.util.autoload_board(ports_filter=None)
it = pyfirmata.util.Iterator(board)
it.start()

SENSOR_ADDRESS = 0x40


def get_temperature():
	board.i2c.send(SENSOR_ADDRESS, [0xF3])
	time.sleep(0.5)
	data = board.i2c.read(SENSOR_ADDRESS, 2)
	temp = data[0] * 256 + data[1]
	return ((175.72 * temp) / 65536.0) - 46.85


def get_humidity():
	board.i2c.send(SENSOR_ADDRESS, [0xF5])
	time.sleep(0.5)
	data = board.i2c.read(SENSOR_ADDRESS, 2)
	humidity = data[0] * 256 + data[1]
	return ((125 * humidity) / 65536.0) - 6


while True:
	print("Temperature (°C):", get_temperature(), "\tHumidity (%):", get_humidity(), end="\r")
