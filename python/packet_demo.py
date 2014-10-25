#! /usr/bin/env python3

'''
Application Name: packet_demo

Required Libraries:
serial, QT4
'''

import serial
import array

__author__ = "Philip Tracton"
__copyright__ = "Copyright 2014, Philip Tracton"
__credits__ = ["Philip Tracton"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Philip Tracton"
__email__ = "ptracton@gmail.com"
__status__ = "Experimental"


if __name__ == "__main__":
    '''
    Program Entry Point
    '''
    print("Packet Demo")
    port = serial.Serial(timeout=0.25)
    port.setByteSize(serial.EIGHTBITS)
    port.setParity(serial.PARITY_NONE)
    port.setStopbits(serial.STOPBITS_ONE)
    settings = port.getSettingsDict()
    port.applySettingsDict(settings)
    port.baudrate = 115200
    port.setBaudrate(port.baudrate)
    port.setPort("/dev/ttyUSB0")
    port.open()
    transmit = array.array('B', [0]).tostring()
    port.write(transmit)

 #   ListOfPorts = serial.tools.list_ports.comports()
 #   print (ListOfPorts)
