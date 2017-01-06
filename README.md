#Python pyfirmata examples

##List of examples:

### Semafor
**Included:**
* Use digital I/O pins for LEDs
* Use digital I/O pins in PWM mode for RGB led
* Use analog input for potentiometer

**Source code:** [semafor.py](semafor.py)

**Schema:**

![Semafor](https://rawgithub.com/setnicka/pyfirmata_examples/master/semafor.svg)

### Onboard temperature and humidity sensors
**Included:**
* I2C communication

Onboard temperature and humidity sensor is connected to the I2C address 0x40.
After command to measure some value there must be some wait before reading out
output value.

**Source code:** [i2c_onboard_temperature.py](i2c_onboard_temperature.py)
