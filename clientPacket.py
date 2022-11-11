# Jacob Coomer
# This file contains a class for a client to simulate reliable data transfer over UDP.
# Python3.10.1 Dependencies: socket, random


from socket import * 
import random 

class clientPacket():
    def __init__(self, ip, port, message):
        self.ip = ip
        self.port = port
        self.message = self.processMessage(message)

        self.identifier = 'J'
        self.length = 0
        self.packetPort = port.to_bytes(2, 'big')
        self.randomNum = random.randint(257, 65535).to_bytes(2, 'big')
        self.field = 'S'
        self.seqNum = False
        self.checkSum = '256'

        self.connection = socket(AF_INET, SOCK_DGRAM)
        self.connection.bind(('',10001))
        print(self.randomNum)
        print(self.message)
        
    def processMessage(self, m):
        zeros = 8 - (len(m) % 8)
        if zeros > 0: 
            m += '0' * zeros
        split = [m[i:i+8] for i in range(0, len(m), 8)]
        split[-1] = split[-1][0:(8-zeros)]
        return(split)
    #Splitting into 8 byte segments and then sending each packet
    def sendMessage(self):
        for byteMsg in self.message:
            self.updateHeader(byteMsg)
            packet = self.condensePacket(byteMsg)
            self.updateChecksum(packet)
            finPacket = bytearray([self.checkSum[0], self.checkSum[1]]) + packet
            while True:
                #tempPacket = self.corruptPacket(finPacket)
               #Need to check for correct seq num here as well
                self.connection.sendto(finPacket, (self.ip,self.port))
                print(finPacket)
                serverResponse = self.connection.recv(2048)
                print(serverResponse)
                print(serverResponse[6])
                if chr(serverResponse[6]) == 'A':
                    break
                #Send
                #Receive
                #Check for ACK. If NACK, continue, else break

    #Currently, the corrupt function causes an infinite loop
    # def corruptPacket(self, packet):
    #     rand = random.randint(1,10)
    #     print(rand)
    #     if rand == 10:
    #         packet[3] = 0
    #     return packet

    def updateHeader(self, msg):
        self.seqNum =  not self.seqNum
        self.length = 10 + len(msg)

    def condensePacket(self, msg):
        packet = bytearray()
        packet.append(ord(self.identifier))
        packet.append(self.length)
        packet.extend(self.packetPort)
        #packet.extend(self.randomNum)
        packet.append(ord(self.field))
        if self.seqNum:
            packet.append(1)
        else:
            packet.append(0)
        for letter in msg:
            packet.append(ord(letter))
        return packet
    
    def updateChecksum(self, pkt):
        checksum = None
        temp = pkt.copy()
        if len(pkt) % 2 == 1:
            temp.extend(int(0).to_bytes(1, 'big'))
    
        checkSum = (temp[0] + temp[1]) ^ (65535)
        i = 2
        j = 3
        while i < len(temp):
            while j < len(temp):
                temporaryChecksum = checkSum ^ (temp[i]+temp[j])
                j += 2
                checkSum = temporaryChecksum
            i += 2 
        self.checkSum = checkSum.to_bytes(2, 'big')