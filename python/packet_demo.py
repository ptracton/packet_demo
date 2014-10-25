#! /usr/bin/env python3

'''
Application Name: packet_demo

Required Libraries:
serial, QT4
'''

from Hardware import SerialPort

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

    new = SerialPort.SerialPort()

 #   ListOfPorts = serial.tools.list_ports.comports()
 #   print (ListOfPorts)
