#! /usr/bin/env python3

"""
UI class for Serial Port hardware.  This will have an instantiation of a
Serial port.
"""

#
# The GUI libraries since we build some GUI components here
#
from PyQt4.QtGui import *
from PyQt4.QtCore import *

import sys
sys.path.append("..")
import Hardware.SerialPort


class SerialPortUI:

    def __init__(self, parent=None, name="Serial Port", port="/dev/ttyUSB0",
                 baud_rate="115200", bits=8, parity=None, stop_bits=1):

        #
        # Serial Port
        #
        self.serial_port = Hardware.SerialPort.SerialPort(port, baud_rate,
                                                          bits, parity,
                                                          stop_bits)

        #
        # GUI components
        #
        self.SerialPortName = QLabel(name)
        self.SerialPortComboBox = QComboBox()
        self.SerialPortComboBox.addItems(self.serial_port.get_list_of_ports())

        baud_rate_list = ["115200", "57600", "38400", "9600"]
        self.BaudRateSelected = baud_rate_list[0]
        self.BaudRateComboBox = QComboBox()
        self.BaudRateComboBox.addItems(baud_rate_list)

        self.SerialPortLayout = QHBoxLayout()

        self.SerialConnectButton = QPushButton("Connect")
        self.SerialDisConnectButton = QPushButton("Disconnect")

        self.SerialPortLayout.addWidget(self.SerialPortName)
        self.SerialPortLayout.addWidget(QLabel("Select Port"))
        self.SerialPortLayout.addWidget(self.SerialPortComboBox)

        self.SerialPortLayout.addWidget(QLabel("Select Baud Rate"))
        self.SerialPortLayout.addWidget(self.BaudRateComboBox)

        self.SerialPortLayout.addWidget(self.SerialConnectButton)
        self.SerialPortLayout.addWidget(self.SerialDisConnectButton)

        #
        # Serial port configs based on GUI selection (defaults)
        #
        self.serial_port.setBaudrate(self.BaudRateSelected)
        self.serial_port.setPort("/dev/ttyUSB0")

        pass

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.SerialPortLayout


if __name__ == "__main__":
    import sys

    class TestUI(QDialog):

        def __init__(self, parent=None):
            super(TestUI, self).__init__(parent)
            layOut = QHBoxLayout()
            self.serial_port_ui = SerialPortUI()
            layOut.addLayout(self.serial_port_ui.getLayout())

            self.setLayout(layOut)
            pass

    app = QApplication(sys.argv)
    GUI = TestUI()
    GUI.show()
    app.exec_()
