#!/usr/bin/env python3
import time
import my_pyfirmata.pyfirmata as pyfirmata

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

"""
Reading onboard accelerometer sensor with demo

Included:
* I2C read/write

Requires PyOpenGL:
* Linux:
	sudo pip3 install PyOpenGL
* Windows:
	download PyOpenGL .whl file from http://www.lfd.uci.edu/~gohlke/pythonlibs/
		(official PyOpenGL windows release is broken at this moment)
	pip3 install <PyOpenGL-3.1.1-cp36-cp36m-win_amd64.whl>
		(downloaded wheel file)
"""

board = pyfirmata.util.autoload_board()
it = pyfirmata.util.Iterator(board)
it.start()

LIS3DE_I2C_ADDRESS = 0x28

# Accelerometer constants:
LIS3DE_AUTO_INCREMENT = 0x80

LIS3DE_CTRL_REG1 = 0x20
LIS3DE_X_L_REGISTER = 0x28
LIS3DE_Y_L_REGISTER = 0x2A
LIS3DE_Z_L_REGISTER = 0x2C

LIS3DE_DATARATE_400_HZ = 0b0111
LIS3DE_DATARATE_200_HZ = 0b0110
LIS3DE_DATARATE_100_HZ = 0b0101
LIS3DE_DATARATE_50_HZ = 0b0100
LIS3DE_DATARATE_25_HZ = 0b0011
LIS3DE_DATARATE_10_HZ = 0b0010
LIS3DE_DATARATE_1_HZ = 0b0001
LIS3DE_DATARATE_POWERDOWN = 0,
LIS3DE_DATARATE_LOWPOWER_1K6HZ = 0b1000
LIS3DE_DATARATE_LOWPOWER_5KHZ = 0b1001

# 3D setup:
ACC_FILTERING = 10
X_SIZE = 1.0
Y_SIZE = 5.0
Z_SIZE = 2.5

################################################################################

# Setup accelerometer
value = 0b0111  # Enables all three axis
value |= (LIS3DE_DATARATE_10_HZ << 4)  # Set sampling interval
board.i2c.send(LIS3DE_I2C_ADDRESS, [value], register=LIS3DE_CTRL_REG1)


def get_acceleration():
	data = board.i2c.read(LIS3DE_I2C_ADDRESS, 6, register=LIS3DE_X_L_REGISTER | LIS3DE_AUTO_INCREMENT)
	# Lower bits of precision aren't used on LIS3DE
	acc_x = data[1]
	if acc_x > 128:
		acc_x -= 256
	acc_y = data[3]
	if acc_y > 128:
		acc_y -= 256
	acc_z = data[5]
	if acc_z > 128:
		acc_z -= 256
	return (acc_x, acc_y, acc_z)


class ValueFilter:
	"""Trivial filter for sensor values."""

	def __init__(self, count):
		self.count = count
		self.values = []

	def add(self, value):
		self.values.append(value)
		while len(self.values) > self.count:
			self.values.pop(0)

	def avarage(self):
		if len(self.values) == 0:
			return 0
		return sum(self.values) / len(self.values)


def InitGL(Width, Height):
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glClearDepth(1.0)
	glDepthFunc(GL_LESS)
	glEnable(GL_DEPTH_TEST)
	glShadeModel(GL_SMOOTH)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)


acc_x_values = ValueFilter(ACC_FILTERING)
acc_y_values = ValueFilter(ACC_FILTERING)
acc_z_values = ValueFilter(ACC_FILTERING)


def DrawGLScene():
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	glLoadIdentity()
	glTranslatef(0.0, 0.0, -16.0)

	# Rotate according to (filtered) accelerometer values
	(acc_x, acc_y, acc_z) = get_acceleration()
	time.sleep(0.03)
	print(" " * 50, end="\r")  # Erase line
	print("X:", acc_x, "\tY:", acc_y, "\tZ:", acc_z, end="\r")

	acc_x_values.add(acc_x)
	acc_y_values.add(acc_y)
	acc_z_values.add(acc_z)
	X_AXIS = acc_x_values.avarage() / 256 * 360
	Y_AXIS = acc_y_values.avarage() / 256 * 360
	Z_AXIS = acc_z_values.avarage() / 256 * 360
	glRotatef(X_AXIS, 1.0, 0.0, 0.0)
	glRotatef(Y_AXIS, 0.0, 1.0, 0.0)
	glRotatef(Z_AXIS, 0.0, 0.0, 1.0)

	# Draw Cube (multiple quads)
	glBegin(GL_QUADS)

	glColor3f(0.0, 1.0, 0.0)
	glVertex3f(X_SIZE, Y_SIZE, -Z_SIZE)
	glVertex3f(-X_SIZE, Y_SIZE, -Z_SIZE)
	glVertex3f(-X_SIZE, Y_SIZE, Z_SIZE)
	glVertex3f(X_SIZE, Y_SIZE, Z_SIZE)

	glColor3f(1.0, 0.0, 0.0)
	glVertex3f(X_SIZE, -Y_SIZE, Z_SIZE)
	glVertex3f(-X_SIZE, -Y_SIZE, Z_SIZE)
	glVertex3f(-X_SIZE, -Y_SIZE, -Z_SIZE)
	glVertex3f(X_SIZE, -Y_SIZE, -Z_SIZE)

	glColor3f(0.0, 1.0, 1.0)
	glVertex3f(X_SIZE, Y_SIZE, Z_SIZE)
	glVertex3f(-X_SIZE, Y_SIZE, Z_SIZE)
	glVertex3f(-X_SIZE, -Y_SIZE, Z_SIZE)
	glVertex3f(X_SIZE, -Y_SIZE, Z_SIZE)

	glColor3f(1.0, 1.0, 0.0)
	glVertex3f(X_SIZE, -Y_SIZE, -Z_SIZE)
	glVertex3f(-X_SIZE, -Y_SIZE, -Z_SIZE)
	glVertex3f(-X_SIZE, Y_SIZE, -Z_SIZE)
	glVertex3f(X_SIZE, Y_SIZE, -Z_SIZE)

	glColor3f(0.0, 0.0, 1.0)
	glVertex3f(-X_SIZE, Y_SIZE, Z_SIZE)
	glVertex3f(-X_SIZE, Y_SIZE, -Z_SIZE)
	glVertex3f(-X_SIZE, -Y_SIZE, -Z_SIZE)
	glVertex3f(-X_SIZE, -Y_SIZE, Z_SIZE)

	glColor3f(1.0, 0.0, 1.0)
	glVertex3f(X_SIZE, Y_SIZE, -Z_SIZE)
	glVertex3f(X_SIZE, Y_SIZE, Z_SIZE)
	glVertex3f(X_SIZE, -Y_SIZE, Z_SIZE)
	glVertex3f(X_SIZE, -Y_SIZE, -Z_SIZE)

	glEnd()

	glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(640, 480)

window = glutCreateWindow(b'Y Soft Playboard onboard accelerometer demo')

glutDisplayFunc(DrawGLScene)
glutIdleFunc(DrawGLScene)
InitGL(640, 480)
glutMainLoop()

# while True:
# 	(acc_x, acc_y, acc_z) = get_acceleration()
# 	time.sleep(0.1)
# 	print(" " * 50, end="\r")  # Erase line
# 	print("X:", acc_x, "\tY:", acc_y, "\tZ:", acc_z, end="\r")
