import enum


class PacketCommand(enum.Enum):
    """
    This is the enum that defines all the packet types and should match up
    with PacketHandelerCommands_TypeDef
    """
    PACKET_PING = (0, "Ping")
    PACKET_ID = (1, "ID")


class Packet():
    """
    This is the python version of PacketHandler_TypeDef
    with the functions to operate on it
    """

    def __init__(self, command=None, payLoad=None):
        """
        """
        self.preAmble = 0xC7
        self.command = command
        self.byteCount = len(payLoad)
        self.payLoad = payLoad
        self.crc = 0
        self._crcCalculated = False
        return

    def calculateCRC(self):
        """
        Calculate the CRC of the packet including the preamble,
        byteCount and payLoad
        """
        self._crcCalculated = True
        return

    def toBytes(self):
        """
        Turn the entire packet into a byte array to
        transmit via serial port
        """

        if self._crcCalculated is False:
            self.calculateCRC()

        return

    def __str__(self):
        """
        String representation of the packet        
        """
        packetString = "Pre: {} Command: {} Bytes: {} Payload: {} CRC: {}".format(
            self.preAmble, self.command, self.byteCount, self.payLoad, self.crc)

        return packetString
