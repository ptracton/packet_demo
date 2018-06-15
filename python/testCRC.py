#! /usr/bin/env python3


import zlib
import binascii

print(hex(binascii.crc32(b'hello-world') & 0xFFFFFFFF))
print(hex(zlib.crc32(b'hello-world') & 0xffffffff))


packet = [0xC7, 0x01, 0x2, 0xde, 0xad]
dataToSend = bytearray(packet)  # (bytearray(packet))
crcToSend1 = binascii.crc32(dataToSend)
crcToSend2 = zlib.crc32(dataToSend)
print(hex(crcToSend1))
print(hex(crcToSend2))
print(bytearray(crcToSend1))
