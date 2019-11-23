global Z_THRESH_val
global Z_DIFF_val
global Z_STDEV_val
global N
N=10.0
global avg_data 
global cumsum
global moving_avg
moving_avg = 0.0
cumsum = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Z_THRESH_val = 1.0
'''
def moving_avg():
	for i in range(N):
		x = input("Enter number :  ")
	    cumsum.pop(obj=0)
		moving_avg = sum(cumsum)/N
		print moving_avg


def Z_THRESH(acc):
	if acc > Z_THRESH_val:
		return True
	else:
		return False

while True:
    x = input("Enter number :  ")
    cumsum.pop(cumsum[0])
    cumsum.append(x)
    moving_avg = sum(cumsum)/N
    print cumsum
    print moving_avg
'''

import socket

UDP_IP = "10.1.85.29"
UDP_PORT = 5000

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

def Z_THRESH(acc):
	if acc > Z_THRESH_val:
		return True
	else:
		return False

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #print "received message:", data
    #if data[18:21] is 'ACC':
    data = data.split()
    if data[1] == 'ACC':
		data = data[2].split(',')
		x_acc = data[1]
		y_acc = data[2]
		z_acc = data[3]
		#print("X_ACC:%s\nY_ACC:%s\nZ_ACC:%s\n"%(x_acc,y_acc,z_acc))
		Z_THRESH_val = Z_THRESH(float(y_acc))
		if Z_THRESH_val:
			print "Pothole Detected"