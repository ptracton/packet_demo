#! /usr/bin/env python3

'''
This is the top level UI element of the packet_demo project
'''

#
# Built in imports
#
import sys
import configparser
import logging
#
# 3rd party imports
#
from PyQt4.QtCore import *
from PyQt4.QtGui import *

#
# Our local custom imports
#
sys.path.append("..")
sys.path.append(".")
import Hardware.SerialPort
import Hardware.SerialPortUI
import PacketDemo.LedsUI


class PacketDemoUI(QDialog):

    def __init__(self, parent=None, config_file="packet_demo.cfg"):
        super(PacketDemoUI, self).__init__(parent)

        #
        # Read in project configuration file
        #
        self.configparser = configparser.SafeConfigParser()
        self.configparser.read(config_file)
        # print(self.configparser.sections())

        #
        # Set up logging.  Attempt to get FILE and LEVEL from the LOGGING
        # section of the config file.  If any of this is missing, use defaults
        #
        if 'LOGGING' in self.configparser.sections():
            if 'FILE' in self.configparser['LOGGING']:
                log_file = self.configparser['LOGGING']['FILE']
            else:
                log_file = "packet_demo.log"

            if 'LEVEL' in self.configparser['LOGGING']:
                log_level_str = self.configparser['LOGGING']['LEVEL']
                if log_level_str == "DEBUG":
                    log_level = logging.DEBUG
                elif log_level_str == "INFO":
                    log_level = logging.INFO
                elif log_level_str == "ERROR":
                    log_level = logging.ERROR
                elif log_level_str == "WARNING":
                    log_level = logging.WARNING
                elif log_level_str == "CRITCAL":
                    log_level = logging.CRITICAL
        else:
            log_file = "packet_demo.log"
            log_level = logging.INFO

        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', filename=log_file,
                            level=log_level)
        logging.info("Packet Demo Starting!")

        #
        # If UART is in the config file, use the values specified in it
        # else use these hard coded defaults
        #
        if 'UART' in self.configparser.sections():
            port = self.configparser['UART']['port']
            baudrate = self.configparser['UART']['baudrate']
            data = self.configparser['UART']['data']
            parity = self.configparser['UART']['parity']
            stop_bits = self.configparser['UART']['stopbits']
        else:
            port = "/dev/ttyUSB0"
            baudrate = "115200"
            data = 8
            parity = None
            stop_bits = 1

        #
        # layOut is out top level GUI item
        #
        layOut = QVBoxLayout()

        #
        # Add in Serial Port GUI, this instantiates a serial port instance
        #
        self.serial_port_ui = Hardware.SerialPortUI.SerialPortUI(
            port, baudrate, data, parity, stop_bits)

        layOut.addLayout(self.serial_port_ui.getLayout())

        #
        # LEDS
        #
        self.LEDS = PacketDemo.LedsUI.LedsUI(leds_count=8)
        layOut.addLayout(self.LEDS.getLayout())

        #
        # connect signals and slots
        #
        QObject.connect(self.serial_port_ui.SerialConnectButton, SIGNAL(
            "clicked()"), self.SerialConnectButtonClicked)
        QObject.connect(self.serial_port_ui.SerialDisConnectButton, SIGNAL(
            "clicked()"), self.SerialDisConnectButtonClicked)

        #
        # Get the GUI ip and running
        #
        self.setLayout(layOut)
        self.setWindowTitle("Learning Python and Embedded Software 1  Packet Demo")
        pass

    def SerialConnectButtonClicked(self):
        print("serial connect clicked")
        self.serial_port_ui.serial_port.connect()
        if self.serial_port_ui.serial_port._isOpen:
            self.LEDS.setCheckable(True)
        else:
            self.LEDS.setCheckable(False)
        return

    def SerialDisConnectButtonClicked(self):
        print("serial dis connect clicked")
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    GUI = PacketDemoUI(config_file="../packet_demo.cfg")
    GUI.show()
    app.exec_()
