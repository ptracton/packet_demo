#! /usr/bin/env python3

'''
This is our Serial Port class.  It inherits from PySerial.  We extend it for
our needs as a packet communication system.
'''

import serial
import serial.tools.list_ports
import array


class SerialPort(serial.Serial):

    """
    This is the SerialPort class.  It inherits from pyserial,
    http://pyserial.sourceforge.net/.  It defaults to 115200 baud rate
    8 data bits, no parity and 1 stop bit.
    """

    def __init__(self, port="/dev/ttyUSB0"):
        """
        SerialPort constructor.  This will open the serial port specified
        or terminate the program if it can not open it.
        """
        super(SerialPort, self).__init__(timeout=0.25)
        print("SerialPort constructor called")

        com_port_list = list(serial.tools.list_ports.comports())
        self.ports = [x[0] for x in com_port_list]

        self.setPort(port)
        self.setByteSize(serial.EIGHTBITS)
        self.setParity(serial.PARITY_NONE)
        self.setStopbits(serial.STOPBITS_ONE)
        print(str(self._isOpen))
        try:
            self.open()
        except OSError:
            print("Failed to open %s" % port)
#            sys.exit(-1)

        print(str(self._isOpen))
        return

    def get_list_of_ports(self):
        """
        Returns a list of serial ports on this computer
        """
        return self.ports

    def transmit_binary(self, data):
        """
        Send binary data and NOT ASCII data.  We expect a list of numbers to be
        transmitted.
        """
        #
        # http://stackoverflow.com/questions/472977/binary-data-with-pyserialpython-serial-port
        #
        print("Trans Binary: ", data)
        transmit = array.array('B', data).tostring()
        print("Transmit", transmit)
        self.write(transmit)

        return
