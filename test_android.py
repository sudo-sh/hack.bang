'''
import socket

TCP_IP='10.1.85.29'
TCP_PORT=8088

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)#2 Maximum Number of Queued connection.

conn, addr = s.accept() #Accepts Connection from the Master/Server.
print 'Connection address:', addr
print "data"
data=conn.recv(1024)
print data
while 1:
	# conn, addr = s.accept() #Accepts Connection from the Master/Server.
	# print 'Connection address:', addr
	print "data"
	data=conn.recv(1024)
	print data

	
import socket, traceback
host = '10.1.85.28'
port = 8080	
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
while 1:
	try:
		message, address = s.recvfrom(8192)
		print message
	'''

import socket
import sys
 
HOST = '10.1.85.29'   # Symbolic name, meaning all available interfaces
PORT = 8088 # Arbitrary non-privileged port
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
#Start listening on socket
s.listen(10)
print 'Socket now listening'
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    #s.send("Hello from Raspberry Pi")
s.close()
