
import array
import configparser
import logging
import PyQt5
import PyQt5.QtWidgets

import serial
import serial.tools.list_ports


class UI_SerialPort(PyQt5.QtWidgets.QDialog):
    """
    This class handles all of the UI details for using the serial port
    """

    def __init__(self, configuration=None, parent=None):
        super(UI_SerialPort, self).__init__(parent)

        self.configuration = configuration
        self.baudrate = 115200
        self.port = "/dev/ttyACM0"
        self.data = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stopBits = serial.STOPBITS_ONE

        self.processConfiguration()

        # This is our physical serial port.  This must come AFTER self.processConfiguration
        # so we have the values from the config file if there are any
        try:
            self.serialPort = serial.Serial(port=self.port,
                                            baudrate=self.baudrate,
                                            bytesize=self.data,
                                            parity=self.parity,
                                            stopbits=self.stopBits)
        except FileNotFoundError:
            import sys
            import traceback
            print(traceback.format_exc())
            logging.error(traceback.format_exc())
            sys.exit(-1)

        # Find our list of serial ports on this PC
        try:
            comPortList = list(serial.tools.list_ports.comports())
            self.portsList = [x[0] for x in comPortList]
        except (NameError, TypeError):
            self.portsList = [self.port]
        print(self.portsList)

        self.serialPortLayout = PyQt5.QtWidgets.QHBoxLayout()

        serialPortLabel = PyQt5.QtWidgets.QLabel("Serial Port")
        self.serialPortComboBox = PyQt5.QtWidgets.QComboBox()
        self.serialPortComboBox.addItems(self.portsList)

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

    def configToByteSize(self, byteSize=None):
        """
        Turn the string from the config file into a serial port parameter value
        """
        retValue = serial.EIGHTBITS

        if 5 == byteSize:
            retValue = serial.FIVEBITS
        if 6 == byteSize:
            retValue = serial.SIXBITS
        if 7 == byteSize:
            retValue = serial.SEVENBITS
        if 8 == byteSize:
            retValue = serial.EIGHTBITS

        return retValue

    def configToParity(self, parity=None):
        """
        Convert a number in config file into serial port partiy parameter
        """
        retValue = serial.PARITY_NONE
        if 0 == parity:
            retValue = serial.PARITY_NONE
        if 1 == parity:
            retValue = serial.PARITY_ODD
        if 2 == parity:
            retValue = serial.PARITY_EVEN
        return retValue

    def configToStopBits(self, stopBits=None):
        """
        Convert a config file stop bits value to serial parameter
        """
        retValue = serial.STOPBITS_ONE
        if 1 == stopBits:
            retValue = serial.STOPBITS_ONE
        if 1.5 == stopBits:
            retValue = serial.STOPBITS_ONE_POINT_FIVE
        if 2 == stopBits:
            retValue = serial.STOPBITS_TWO
        return retValue

    def processConfiguration(self):
        """
        Read the values from the configuration file.  If there is a section,
         use it otherwise go with the defaults
        """

        if self.configuration.has_option('UART', "baudrate"):
            self.baudrate = int(self.configuration["UART"]["baudrate"])

        if self.configuration.has_option('UART', "port"):
            self.port = self.configuration["UART"]["port"]

        if self.configuration.has_option('UART', "data"):
            self.data = self.configToByteSize(int(self.configuration["UART"]["data"]))

        if self.configuration.has_option('UART', "parity"):
            self.parity = self.configToParity(int(self.configuration["UART"]["parity"]))

        if self.configuration.has_option('UART', "stopbits"):
            self.stopBits = self.configToStopBits(float(self.configuration["UART"]["stopbits"]))

        return

    def open(self):
        """
        Configure the serial port based on UI inputs and then open it
        """
        self.port = self.serialPortComboBox.currentText()
        self.baudrate = int(self.serialPortBaudRateComboBox.currentText())
        self.data = self.configToByteSize(self.serialPortByteSizeComboBox.currentText())
        self.parity = self.configToParity(self.serialPortParityComboBox.currentText())
        self.stopBits = self.configToStopBits(self.serialPortStopBitsComboBox.currentText())

        # Only modify if closed!
        if self.serialPort.is_open:
            self.serialPort.close()

        # Reconfigure serial port based on UI values
        self.serialPort.baudrate = self.baudrate
        self.serialPort.port = self.port
        self.serialPort.bytesize = self.data
        self.serialPort.parity = self.parity
        self.serialPort.stopbits = self.stopBits

        # Try to open port with new configuration
        try:
            self.serialPort.open()
            self.setEnabled(False)

        except:
            logging.error("Failed to open Serial Port!")
            self.serialPort.close()
            self.setEnabled(True)
            self.serialPortPushButton.setText("Open Port")

        # Clear anything waiting to be sent or received and unprocessed
        self.serialPort.reset_input_buffer()
        self.serialPort.reset_output_buffer()

        return

    def transmitData(self, data=None):
        """
        Send the data out the door of the serial port
        """

        #
        # http://stackoverflow.com/questions/472977/binary-data-with-pyserialpython-serial-port
        #

        transmit = array.array('B', data).tostring()
        print("transmitData {} as {}".format(data, transmit))
        logging.info("transmitData {} as {}".format(data, transmit))

        self.serialPort.write(transmit)
        return

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.serialPortLayout
