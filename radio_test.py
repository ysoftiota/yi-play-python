#!/usr/bin/env python3
import my_pyfirmata.pyfirmata as pyfirmata
from my_pyfirmata.pyfirmata.util import from_two_bytes, to_two_bytes, two_byte_iter_to_bytes, str_to_two_byte_iter

USR_CMD_RF_CONFIG = 0x02
USR_CMD_RF_DATA = 0x03

board = pyfirmata.util.autoload_board(ports_filter="YSoft IOTA Play")
it = pyfirmata.util.Iterator(board)
it.start()

########################################################################
# Own sysexes:
#
# Configuration of networkID, nodeID and encrypt passphrase
# Password is optional, but when used, it must be 16 bytes long
# 0  START_SYSEX        (0xF0)
# 1  USR_CMD_RF_CONFIG  (0x02)
# 2  networkID LSB
# 3  networkID MSB
# 4  nodeID LSB
# 5  nodeID MSB
# 6  (optional) first password char LSB
# 7  (optional) first password char MSB
# ... additional password chars at positions 8-37
# 6/37 END_SYSEX (0xF7)
#
# Data to send or received data
# (when sending data nodeID is target, when receiving data nodeID is source)
# 0  START_SYSEX        (0xF0)
# 1  USR_CMD_RF_DATA    (0x03)
# 2  nodeID LSB
# 3  nodeID MSB
# 4  RSSI LSB (only used for received message)
# 5  RSSI MSB (only used for received message)
# 4/6 first byte LSB
# 5/7 first byte MSB
# ... additional bytes
# N  END_SYSEX (0xF7)
########################################################################


def radio_data_received(nodeID_lsb, nodeID_msb, RSSI_lsb, RSSI_msb, *data):
	nodeID = from_two_bytes([nodeID_lsb, nodeID_msb])
	RSSI = from_two_bytes([RSSI_lsb, RSSI_msb])
	RSSI -= 256
	decoded_data = two_byte_iter_to_bytes(data)
	print("Message from {0} [RSSI {1}dBm]: {2}".format(nodeID, RSSI, bytes(decoded_data).decode()))

board.add_cmd_handler(USR_CMD_RF_DATA, radio_data_received)


def radio_config(networkID, nodeID, password=None):
	data = []
	data.extend(to_two_bytes(networkID))
	data.extend(to_two_bytes(nodeID))
	if password is not None:
		data.extend(str_to_two_byte_iter(password))
	board.send_sysex(USR_CMD_RF_CONFIG, data)


def radio_send(targetID, data):
	if isinstance(data, str):
		data = bytearray(data, 'utf-8')

	data_to_send = []
	data_to_send.extend(to_two_bytes(targetID))
	for c in data:
		data_to_send.extend(to_two_bytes(c))
	board.send_sysex(USR_CMD_RF_DATA, data_to_send)

radio_config(100, 1, "sampleEncryptKey")
# radio_send(2, bytearray("TEST", 'utf8'))
