
import array
import logging
import PyQt5
import PyQt5.QtWidgets
import Communication


class UI_SerialPort(PyQt5.QtWidgets.QDialog):
    """
    This class handles all of the UI details for using the serial port
    """

    def __init__(self, configuration=None, parent=None):
        super(UI_SerialPort, self).__init__(parent)

        self.configuration = configuration

        # This is our physical serial port.  This must come AFTER self.processConfiguration
        # so we have the values from the config file if there are any
        try:
            self.communication = Communication.Communication()

        except FileNotFoundError:
            import sys
            import traceback
            print(traceback.format_exc())
            logging.error(traceback.format_exc())
            sys.exit(-1)

        # Find our list of serial ports on this PC
        self.portList = self.communication.listOfPorts()

        self.processConfiguration()

        self.serialPortLayout = PyQt5.QtWidgets.QHBoxLayout()

        serialPortLabel = PyQt5.QtWidgets.QLabel("Serial Port")
        self.serialPortComboBox = PyQt5.QtWidgets.QComboBox()
        self.serialPortComboBox.addItems(self.communication.portsList)

        serialPortBaudRateLabel = PyQt5.QtWidgets.QLabel("Baud Rate")
        baudRateList = ["9600", "115200"]
        self.serialPortBaudRateComboBox = PyQt5.QtWidgets.QComboBox()
        self.serialPortBaudRateComboBox.addItems(baudRateList)

        serialPortByteSizeLabel = PyQt5.QtWidgets.QLabel("Byte Size")
        byteSizeList = ["5", "6", "7", "8"]
        self.serialPortByteSizeComboBox = PyQt5.QtWidgets.QComboBox()
        self.serialPortByteSizeComboBox.addItems(byteSizeList)

        serialPortParityLabel = PyQt5.QtWidgets.QLabel("Parity Bits")
        parityList = ["None", "Odd", "Even"]
        self.serialPortParityComboBox = PyQt5.QtWidgets.QComboBox()
        self.serialPortParityComboBox.addItems(parityList)

        serialPortStopBitsLabel = PyQt5.QtWidgets.QLabel("Stop Bits")
        stopBitsList = ["1", "1.5", "2"]
        self.serialPortStopBitsComboBox = PyQt5.QtWidgets.QComboBox()
        self.serialPortStopBitsComboBox.addItems(stopBitsList)

        self.serialPortPushButton = PyQt5.QtWidgets.QPushButton("Close Port")

        self.serialPortLayout.addWidget(serialPortLabel)
        self.serialPortLayout.addWidget(self.serialPortComboBox)
        self.serialPortLayout.addWidget(serialPortBaudRateLabel)
        self.serialPortLayout.addWidget(self.serialPortBaudRateComboBox)
        self.serialPortLayout.addWidget(serialPortByteSizeLabel)
        self.serialPortLayout.addWidget(self.serialPortByteSizeComboBox)
        self.serialPortLayout.addWidget(serialPortParityLabel)
        self.serialPortLayout.addWidget(self.serialPortParityComboBox)
        self.serialPortLayout.addWidget(serialPortStopBitsLabel)
        self.serialPortLayout.addWidget(self.serialPortStopBitsComboBox)
        self.serialPortLayout.addWidget(self.serialPortPushButton)

        self.serialPortComboBox.setCurrentIndex(0)
        self.serialPortBaudRateComboBox.setCurrentIndex(1)
        self.serialPortByteSizeComboBox.setCurrentIndex(3)
        self.serialPortParityComboBox.setCurrentIndex(0)
        self.serialPortStopBitsComboBox.setCurrentIndex(0)

        self.setEnabled(False)

        return

    def setEnabled(self, state=None):
        """
        Turn the  comboboxes on or off
        """
        self.serialPortComboBox.setEnabled(state)
        self.serialPortBaudRateComboBox.setEnabled(state)
        self.serialPortByteSizeComboBox.setEnabled(state)
        self.serialPortParityComboBox.setEnabled(state)
        self.serialPortStopBitsComboBox.setEnabled(state)

        return

    def processConfiguration(self):
        """
        Read the values from the configuration file.  If there is a section,
         use it otherwise go with the defaults
        """

        if self.configuration.has_option('UART', "baudrate"):
            self.communication.baudrate = int(self.configuration["UART"]["baudrate"])

        if self.configuration.has_option('UART', "port"):
            self.communication.port = self.configuration["UART"]["port"]

        if self.configuration.has_option('UART', "data"):
            self.communication.data = self.communication.configToByteSize(
                int(self.configuration["UART"]["data"]))

        if self.configuration.has_option('UART', "parity"):
            self.parity = self.communication.configToParity(
                int(self.configuration["UART"]["parity"]))

        if self.configuration.has_option('UART', "stopbits"):
            self.communication.stopBits = self.communication.configToStopBits(
                float(self.configuration["UART"]["stopbits"]))
        return

    def open(self):
        """
        Configure the serial port based on UI inputs and then open it
        """
        self.communication.port = self.serialPortComboBox.currentText()
        self.communication.baudrate = int(self.serialPortBaudRateComboBox.currentText())
        self.communication.data = self.configToByteSize(
            self.serialPortByteSizeComboBox.currentText())
        self.communication.parity = self.configToParity(self.serialPortParityComboBox.currentText())
        self.communication.stopBits = self.configToStopBits(
            self.serialPortStopBitsComboBox.currentText())

        # Only modify if closed!
        if self.communication.serialPort.is_open:
            self.communication.serialPort.close()

        # Reconfigure serial port based on UI values
        self.communication.serialPort.baudrate = self.communication.baudrate
        self.communication.serialPort.port = self.communication.port
        self.communication.serialPort.bytesize = self.communication.data
        self.communication.serialPort.parity = self.communication.parity
        self.communication.serialPort.stopbits = self.communication.stopBits

        # Try to open port with new configuration
        try:
            self.communication.serialPort.open()
            self.setEnabled(False)

        except:
            logging.error("Failed to open Serial Port!")
            self.communication.serialPort.close()
            self.setEnabled(True)
            self.serialPortPushButton.setText("Open Port")

        # Clear anything waiting to be sent or received and unprocessed
        self.communication.serialPort.reset_input_buffer()
        self.communication.serialPort.reset_output_buffer()

        return

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.serialPortLayout
