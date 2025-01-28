#!/usr/bin/python3
import socket
import sys
import select
s = socket.socket(socket.AF_INET6 , socket.SOCK_STREAM , 0)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((socket.gethostbyname(),0))
s.listen(1)
l=[]
while True :
        s2 , addr = s.accept()
        while True :
                data = s2.recv(1500)
                if data ==b'':
                        break
                s2.send(data)
        s2.close()

while True :
	l1, l2, l3 = select.select(l+[s],[],[])
	for i in l1:
		if i == s:
			sc,a = s . accept ()
			print ( " new client : " , a )
			l.append(sc)
		else:
			msg=i.recv(1500)
			if len(msg) == 0:
				print ( " client disconnected " )
				notifcd="Client disconnected : " + nick[i].decode('utf-8') +'\n'
				for m in l:
					m.sendall(notifcd.encode('utf-8'))
				i.close ()
				l.remove(i)
				break
			t = msg.split(maxsplit=2)
			if t[0]==b"MSG":
				for j in l:
					if i != j:
						j.sendall(nick[i] + b" : " + t[1] + b"\n")
			elif t[0]==b"NICK":
				print (" Nick changed : " + nick[i].decode('utf-8') + " to " + t[1].decode('utf-8') + "\n")
				nick[i]=t[1]
			elif t[0]==b"WHO" :
				for n in l:
					i.sendall(nick[n] + b'\n')
			elif t[0]==b"QUIT" :
				for o in l:
					if i != o:
						o.sendall(nick[i] + b" : " + t[1] + b"\n")
						notifcd="Client disconnected : " + nick[i].decode('utf-8') +'\n'
						o.sendall(notifcd.encode('utf-8'))
				print ( " client disconnected " )
				i.close()
				l.remove(i)
			elif t[0]==b"KILL":
				for p in l:
					if t[1]==nick[p]:
						p.sendall(t[2] + b"\n")
						p.close ()
						l.remove(p)
						print ( " client disconnected " )
						notifcd="Client disconnected : " + nick[i].decode('utf-8') +'\n'
			else:
				msg=b"Invalid command\n"
				i.sendall(msg)
s.close()
