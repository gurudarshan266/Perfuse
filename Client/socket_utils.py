#!/usr/bin/python

import socket
from constants import *

class ChunkServerConnection:
    'Used for creating connection to chunk server'
    sock = None

    def __init__(self):
        host = socket.gethostname()
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM) #Get socket
        self.sock.connect((host,CHUNK_SERVER_PORT))

    def close(self):
        self.sock.close()

    def read(self):
        print self.sock.recv(1024)


c = ChunkServerConnection()

c.read()