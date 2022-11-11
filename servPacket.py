# Jacob Coomer
# This file contains a class for a server to simulate reliable data transfer over UDP.
# Python3.10.1 Dependencies: socket, random

from socket import * 
from random import randint

class servPacket():
    def __init__(self, port):
        self.port = port

        self.identifier = 'J'
        self.length = 0
        self.packetPort = port.to_bytes(2, 'big')
        self.randomNum = randint(257, 65535).to_bytes(2, 'big')
        self.field = 'S'
        self.seqNum = False
        self.checkSum = '256'

        self.connection = socket(AF_INET, SOCK_DGRAM)
        self.connection.bind(('',self.port))
        self.main()


    def main(self):
        while True: #Check for 'J'
            message, clientInfo = self.connection.recvfrom(2048)
            self.updateChecksum(message[2::])
            if bytearray([self.checkSum[0],self.checkSum[1]]) == message[0:2]:
                self.field = 'A'
                self.seqNum = message[7]
                print(self.seqNum)
                print(message[8::].decode())
            else:
                self.field = 'N'
            self.packetPort = message[4:6]
            finPacket = bytearray([self.checkSum[0],self.checkSum[1]]) + self.condensePacket()
            self.connection.sendto(finPacket, clientInfo)
            

    # def printMsg(self, msg):
    #     print(''.join(chr(x) for x in msg))

    # def transformChecksum(self, msg):
    #     msg = msg.encode()
    #     transform = bytearray()
    #     for i in msg:
    #         transform.append(ord(i))
    #     return transform
    
    def condensePacket(self):
        packet = bytearray()
        packet.append(ord(self.identifier))
        packet.append(self.length)
        packet.extend(self.packetPort)
        #packet.extend(self.randomNum)
        packet.append(ord(self.field))
        packet.append(self.seqNum)
        return packet

    def updateChecksum(self, oldPacket):
        pkt = bytearray()
        for x in oldPacket:
            pkt.append(x)
        temp = pkt.copy()
        if len(pkt) % 2 == 1:
            temp.extend(int(0).to_bytes(1, 'big'))
        # Need to make this bytearray and then xor the 2 bytearrays
        checkSum = (temp[0] + temp[1]) ^ (65535)
        i = 2
        j = 3
        while i < len(temp):
            while j < len(temp):
                temporaryChecksum = checkSum ^ (temp[i]+temp[j]) # make this bytearray
                j += 2
                checkSum = temporaryChecksum
            i += 2 
        self.checkSum = checkSum.to_bytes(2, 'big')
