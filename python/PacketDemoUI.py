#! /usr/bin/python3

import logging
import PyQt5
import PyQt5.QtWidgets
import UI_CentralWindow


class PacketDemoUI(PyQt5.QtWidgets.QMainWindow):
    """
    This is our top level GUI.  It handles the connections for actions
    since it can see all of the data structures and elements
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
        self.centralWindow = UI_CentralWindow.UI_CentralWindow(configuration)
        self.setCentralWidget(self.centralWindow)

        self.centralWindow.serialPortUI.serialPortPushButton.clicked.connect(
            self.serialPortPushButtonClicked)

        self.centralWindow.transmitPushButton.clicked.connect(self.transmitDataPushButtonClicked)

        self.show()

        return

    def transmitDataPushButtonClicked(self):
        """
        Connection for the transmitDataPushButton
        Read the data in the line edit and send it to the device
        """

        # Only send the data if it is all digits.  Target does NOT process strings
        data = self.centralWindow.transmitData.text()
        if data.isdigit():
            n = 2
            dataList = [data[i:i+n] for i in range(0, len(data), n)]
            dataList = [int(x) for x in dataList]
            print(dataList)
            self.centralWindow.serialPortUI.transmitData(dataList)

        return

    def serialPortPushButtonClicked(self):
        """
        Open or close the serial port based on its current state.  Switch it to the
        next one.
        """
        if self.centralWindow.serialPortUI.serialPort.is_open is True:
            self.centralWindow.serialPortUI.serialPortPushButton.setText("Open Port")
            self.centralWindow.serialPortUI.setEnabled(True)
            self.centralWindow.serialPortUI.serialPort.close()
            logging.info("Serial Port Closed")

        else:
            self.centralWindow.serialPortUI.serialPortPushButton.setText("Close Port")
            self.centralWindow.serialPortUI.setEnabled(False)
            self.centralWindow.serialPortUI.open()
            logging.info("Serial Port Opened")

        return
