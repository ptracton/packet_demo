#! /usr/bin/env python3

'''
Application Name: packet_demo

Required Libraries:
serial, QT4
'''

__author__ = "Philip Tracton"
__copyright__ = "Copyright 2014, Philip Tracton"
__credits__ = ["Philip Tracton"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Philip Tracton"
__email__ = "ptracton@gmail.com"
__status__ = "Experimental"

import sys
import os
from PyQt4.QtGui import *
import PacketDemo.PacketDemoUI


if __name__ == "__main__":
    '''
    Program Entry Point
    '''
    sys.path.append(os.getcwd())
    print("Packet Demo")
    app = QApplication(sys.argv)
    GUI = PacketDemo.PacketDemoUI.PacketDemoUI()
    GUI.show()
    app.exec_()
