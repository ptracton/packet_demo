#! /usr/bin/env python3

'''
This is our Serial Port class.  It inherits from PySerial.  We extend it for
our needs as a packet communication system.
'''

import logging
import serial
import serial.tools.list_ports
import array


class SerialPort(serial.Serial):

    """
    This is the SerialPort class.  It inherits from pyserial,
    http://pyserial.sourceforge.net/.  It defaults to 115200 baud rate
    8 data bits, no parity and 1 stop bit.
    """

    def __init__(self, port="/dev/ttyUSB0", baud_rate="115200", bits=8,
                 parity="None", stop_bits=1):
        """
        SerialPort constructor.  This will open the serial port specified
        or terminate the program if it can not open it.
        """
        super(SerialPort, self).__init__(timeout=0.25)

        try:
            com_port_list = list(serial.tools.list_ports.comports())
            self.ports = [x[0] for x in com_port_list]
        except (NameError, TypeError):
            self.ports = ["/dev/ttyUSB0"]

        self.setPort(port)

        # self.setBaudrate(baud_rate)

        if bits == 8:
            self.setByteSize(serial.EIGHTBITS)
        elif bits == 7:
            self.setByteSize(serial.SEVENBITS)
        elif bits == 6:
            self.setByteSize(serial.SIXBITS)
        elif bits == 5:
            self.setByteSize(serial.FIVEBITS)

        if parity == "None":
            self.setParity(serial.PARITY_NONE)
        elif parity == "Even":
            self.setParity(serial.PARITY_EVEN)
        elif parity == "Odd":
            self.setParity(serial.PARITY_ODD)
        elif parity == "Mark":
            self.setParity(serial.PARITY_MARK)
        elif parity == "Space":
            self.setParity(serial.PARITY_SPACE)

        if stop_bits == 1:
            self.setStopbits(serial.STOPBITS_ONE)
        elif stop_bits == 2:
            self.setStopbits(serial.STOPBITS_TWO)

        return

    def connect(self):
        """
        attempt to open the serial port
        """
        try:
            self.open()
            logging.info("%s: Open Serial Port successful %s" %
                        (__name__, self.getPort()))
        except OSError:
            logging.error("%s: Failed to open Serial Port %s" %
                          (__name__, self.getPort()))
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
