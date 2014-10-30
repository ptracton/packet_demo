#! /usr/bin/env python3

'''
This is the top level UI element of the packet_demo project
'''

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

sys.path.append("..")
import Hardware.SerialPort
import Hardware.SerialPortUI


class PacketDemoUI(QDialog):

    def __init__(self, parent=None):
        super(PacketDemoUI, self).__init__(parent)

        layOut = QHBoxLayout()
        self.serial_port_ui = Hardware.SerialPortUI.SerialPortUI()
        layOut.addLayout(self.serial_port_ui.getLayout())

        self.setLayout(layOut)
        self.setWindowTitle("Learning Python and Embedded Software 1  Packet Demo")
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = PacketDemoUI()
    GUI.show()
    app.exec_()
