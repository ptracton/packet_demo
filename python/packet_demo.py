#! /usr/bin/env python3

import configparser
import logging
import sys
import os
import PyQt5
import PacketDemoUI


if __name__ == "__main__":

    # Append path to get our local libraries
    sys.path.append(os.getcwd())

    config_file = "packet_demo.cfg"
    try:
        configuration = configparser.ConfigParser()
        configuration.read(config_file)
    except OSError:
        print("%s exists but we can not open or read it!" %
              (config_file))
        sys.exit(-1)

    # Parse log file for log file name and set up logging
    if configuration.has_section('LOGING'):
        log_file_name = configuration['LOGING']['LOGING_FILE']
    else:
        log_file_name = "default.log"

    if configuration.has_section('LOGING'):
        log_level = configuration['LOGING']['LOGING_LEVEL']
    else:
        log_level = logging.INFO

    try:
        logging.basicConfig(filename=log_file_name,
                            level=log_level,
                            format='%(asctime)s,%(levelname)s,%(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
    except:
        print("Failed to open log file %s" % (log_file_name))
        sys.exit(-1)

    logging.info("Program Starting")

    app = PyQt5.QtWidgets.QApplication(sys.argv)
    GUI = PacketDemoUI.PacketDemoUI()
    GUI.show()
    app.exec_()
