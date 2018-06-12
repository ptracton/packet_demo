
import serial
import serial.tools.list_ports


class Communication():
    """
    Handle communication hardware details between PC and target
    """

    def __init__(self):
        """
        """

        self.baudrate = 115200
        self.port = "/dev/ttyACM0"
        self.data = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stopBits = serial.STOPBITS_ONE
        self.portList = []
        self.serialPort = serial.Serial(port=self.port,
                                        baudrate=self.baudrate,
                                        bytesize=self.data,
                                        parity=self.parity,
                                        stopbits=self.stopBits)

    def listOfPorts(self):
        try:
            comPortList = list(serial.tools.list_ports.comports())
            self.portsList = [x[0] for x in comPortList]
        except (NameError, TypeError):
            self.portsList = [self.port]

        print(self.portsList)
        return self.portList

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
