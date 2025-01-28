#!/usr/bin/python3
import socket
import sys
import select
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM , 0)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

hostname = socket.gethostname()
s.bind((socket.gethostbyname(hostname),2910))
s.listen(1)
while True :
        s2 , addr = s.accept()
        while True :
                data = s2.recv(1500)
                if data ==b'':
                        break
                s2.send(data)
        s2.close()


