#! /usr/bin/env python3
"""
This is the class for handling the LEDs on the board. Each is a radio button.  When clicked they
toggle state.  "clicked" means LED ON, "unclicked" means LED OFF
"""

import logging

##
# The GUI libraries since we build some GUI components here
##
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class LedsUI:

    def __init__(self, leds_count=1):
        """
        create the GUI elements for the list of LEDS
        """

        #
        # create an array of radio button elements since we find out
        # at run time how many LEDS we have
        #
        self.leds_count = leds_count
        self.leds_list = []
        for x in range(leds_count):
            y = QCheckBox()
            y.setCheckState(Qt.Unchecked)
            y.setCheckable(False)
            y.setText("Led %d" % (x))
            QObject.connect(y, SIGNAL("clicked()"), self.clicked)
            self.leds_list.append(y)
            del(y)

        #
        # Add each checkbox to the GUI layout
        #
        self.layOut = QHBoxLayout()
        for x in range(leds_count):
            self.layOut.addWidget(self.leds_list[x])

        pass

    def getLayout(self):
        """
        Return our layout for easy GUI integration
        """
        return self.layOut

    def setCheckable(self, state):
        """
        changes the state of all of the checkboxes to either checkable (True) or
        un-checkable (False)
        """
        for x in range(self.leds_count):
            self.leds_list[x].setCheckable(state)
        return

    def clicked(self):
        """
        Handler for when ANY of the buttons is clicked.  Sends a packet to the board 
        to change LED state
        """
        logging.info("%s clicked" % (__name__))
        # for x in range(self.leds_count):
        #    print("%d %s " % (x, self.leds_list[x].isChecked()))
        return
