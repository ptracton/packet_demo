#! /usr/bin/python3

import logging
import PyQt5
import PyQt5.QtWidgets
import UI_CentralWindow


class PacketDemoUI(PyQt5.QtWidgets.QMainWindow):
    """
    """

    def __init__(self, configuration=None, parent=None):
        # call super to init GUI
        super(PacketDemoUI, self).__init__(parent)

        # store off the passed in configuration
        self.configuration = configuration

        # Create Main Window Elements
        self.statusBar().showMessage('Status Bar')
        self.setWindowTitle('STM32 Packet Demo GUI')

        # Create our central widget
        self.centralWindow = UI_CentralWindow.UI_CentralWindow()
        self.setCentralWidget(self.centralWindow)

        self.show()

        return
