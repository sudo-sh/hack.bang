

import serial
from time import sleep
import time
import numpy as np
import statistics as sp
import matplotlib.pyplot as plt
import math as Math
from mpmath import mp





mp.dps=100# The resolution of cosine calculation

global PI
PI=3.14159265358979323846




ser1 = serial.Serial('/dev/ttyUSB0', 115200) # Establish the connection on a specific port

i=0

distance1=0
mul_flag=1
mul_time=5
unique_id1=0
loop_flag=1
distance2=0
unique_id2=0
distance3=0
unique_id3=0

dis1_list=[]


id1_list=[]

counter=0
cnt_dis1=1
cnt_dis2=1

plt.ion() ## The real time GUI using Python Matplotlib

#These two list is used to Plot the real time Data.

x=[]
y=[]



#fh=open("datalog.txt","w")
while 1:
 #Accepting Data from Beacon 1
 print "Now from Beacon 1"
 loop_flag=1
 init_time=time.time()
 #ser1 = serial.Serial('/dev/ttyUSB0', 115200) # Establish the connection on a specific port
 for i in range(10):s
    ser1.write(bytes('R'))
    print "Sent R"
    sleep(0.05)


 counter=0
 dis1_m_id1=0
 
 dis1_m_id1_count=0.0

 dis1_list=[]
 id1_list=[]
 dis1_m_id1_median=[]
 sprint "Going to loop"
 while loop_flag:
    
    mul_flag=1
    mul_time=5
    distance1=0
    unique_id1=0

    
    print "Waiting"
    s=bytearray(ser1.readline());
    #print "Got Something"
    for i in range(5,10):
	    mul_flag=1;
	    for j in range (0,mul_time):
		    mul_flag=mul_flag*10;

	    mul_time=mul_time-1

	    distance1=distance1+ (s[i]*mul_flag)

    print distance1/10000.0,
    #print counter,
    #fh.write(str(distance1/10000.0))
    #fh.write('\n')
    if((distance1/10000.0)>40):  #Upper Range is 40 The Maximum distance it can range.
        continue

    dis1_list.append(distance1/10000.0)# The elements in this list are in meters

    mul_flag=1
    mul_time=5
	
    for i in range(0,5):
	    mul_flag=1;
	    for j in range (0,mul_time):
	        mul_flag=mul_flag*10;

	    mul_time=mul_time-1

	    unique_id1=unique_id1+(s[i]*mul_flag)

    if(unique_id1==133600):
	  	print "Id = 3",
	

x.append(0)# This is the origin and the location of the Car. 
y.append(0)

plt.scatter(x,y,s=80,maker=">")

plt.grid()
plt.pause(0.05)




