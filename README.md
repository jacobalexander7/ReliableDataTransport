# ReliableDataTransport
Provides RDT over UDP

This project implements reliable data concepts (SYN/ACK flags, checksum, and retransmission) for sending messages over UDP. 

# Instructions
Dependencies: Python3.10, socket, argparse, random

To run, use 'python3 server.py <flags>'. Flags are used to set the port of the server, port and ip to connect to from the client, and message.
Use 'python3 client.py -h' for a detailed explanation of each flag. 

# Notes
I could not get 2 features working:
1. The random number generator - I am generating a positive integer and converting it into bytes, but the client crashes when working on the bytes within the bytearray. 

2. Packet Corruption/Infinite Looping - When using the corrupt packet function, the data will be transmitted/retransmitted to the server as expected. However, the server begins sending an infinite stream of NACKS. I will fix this in a later version, but any debugging help is appreciated. 

