import configparser
import PyQt5
import PyQt5.QtWidgets

import UI_SerialPort


class UI_CentralWindow(PyQt5.QtWidgets.QDialog):
    """
    This class holds the GUI elements 
    """

    def __init__(self, configuration=None, parent=None):
        super(UI_CentralWindow, self).__init__(parent)

        # keep the configuration file and pass it along to other modules that need it
        self.configuration = configuration

        self.topVBox = PyQt5.QtWidgets.QVBoxLayout()
        self.hbox = PyQt5.QtWidgets.QHBoxLayout()
        self.serialPortLayout = PyQt5.QtWidgets.QVBoxLayout()

        # Add in the serial port UI
        self.serialPortUI = UI_SerialPort.UI_SerialPort(configuration=configuration)
        self.serialPortLayout.addLayout(self.serialPortUI.getLayout())

        # Direct data transmission, lets us send any data we want
        transmitLabel = PyQt5.QtWidgets.QLabel("Transmit Data")
        self.transmitData = PyQt5.QtWidgets.QLineEdit()
        self.transmitPushButton = PyQt5.QtWidgets.QPushButton("Transmit Data")
        self.hbox.addWidget(transmitLabel)
        self.hbox.addWidget(self.transmitData)
        self.hbox.addWidget(self.transmitPushButton)

        # Put elements together
        self.topVBox.addLayout(self.serialPortLayout)
        self.topVBox.addLayout(self.hbox)
        self.setLayout(self.topVBox)

        return
