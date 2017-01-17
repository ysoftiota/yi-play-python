#!/usr/bin/env python3
import my_pyfirmata.pyfirmata as pyfirmata
from my_pyfirmata.pyfirmata.util import from_two_bytes, to_two_bytes, two_byte_iter_to_bytes, str_to_two_byte_iter

USR_CMD_RF_CONFIG = 0x02
USR_CMD_RF_DATA = 0x03

board = pyfirmata.util.autoload_board(ports_filter=None)
it = pyfirmata.util.Iterator(board)
it.start()


def radio_data_received(nodeID_lsb, nodeID_msb, RSSI_lsb, RSSI_msb, *data):
	nodeID = from_two_bytes([nodeID_lsb, nodeID_msb])
	RSSI = from_two_bytes([RSSI_lsb, RSSI_msb])
	decoded_data = two_byte_iter_to_bytes(data)
	print(nodeID, RSSI, bytes(decoded_data).decode())

board.add_cmd_handler(USR_CMD_RF_DATA, radio_data_received)


def radio_config(networkID, nodeID, password=None):
	data = []
	data.extend(to_two_bytes(networkID))
	data.extend(to_two_bytes(nodeID))
	if password is not None:
		data.extend(str_to_two_byte_iter(password))
	board.send_sysex(USR_CMD_RF_CONFIG, data)


def radio_send(targetID, data):
	data_to_send = []
	data_to_send.extend(to_two_bytes(targetID))
	for c in data:
		data_to_send.extend(to_two_bytes(c))
	board.send_sysex(USR_CMD_RF_DATA, data_to_send)

radio_config(100, 1, "sampleEncryptKey")
# radio_send(2, bytearray("TEST", 'utf8'))
