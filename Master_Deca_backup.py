#Instruction
#First Execute the Client Scripts on the Raspis and then Execute this Master Raspi Script

#This is the python Script for Main Master Raspi which schedules the 
#Ranging operation and calculates the Final Co-ordinates.


import serial
from time import sleep
import time
import numpy as np
import socket
import statistics as sp
import matplotlib.pyplot as plt


s=bytearray([0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0])

TCP_IP1 = '192.168.43.168' # Address of Beacon 1(Specified by the folder in Home Directory)
#TCP_IP1 = '127.0.0.1' # Test with Local Host First
TCP_PORT1 = 5060
TCP_IP2 = '192.168.43.47' # Address of Beacon 2(Specified by the folder in the Home Directory)
# TCP_IP2 = '127.0.0.1' #Test with Local Host First
TCP_PORT2 = 5097
BUFFER_SIZE = 200
MESSAGE = "Start"
  
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s1.connect((TCP_IP1, TCP_PORT1))# Socket Connection for Beacon 1
s2.connect((TCP_IP2, TCP_PORT2))# Socket connection for Beacon 2




ser1 = serial.Serial('/dev/ttyUSB0', 115200) # Establish the connection on a specific port

i=0


MAX_RANGE=40 # In meters

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


waitTime=0.5      #Time Required by the Beacons to collect all the mobile ranges.




def EuDistSq(A,B):   # A and B are arrays of length 2
    return (A[0]-B[0])**2 + (A[1]-B[1])**2

def trilat(BMdist):
    B=np.matrix([[0,0],[2.5,2],[5.0,0]]) ##You need to append this to the GUI too Master, Beacon 2 ,Beacon1 
    n=len(B)
    print n
    
    BDS=np.zeros([n])
    for i in range(n):
        BDS[i]=EuDistSq(np.squeeze(np.asarray(B[0,:])),np.squeeze(np.asarray(B[i,:])))
        
    M=B[1:n,:]
    print M
    N=len(BMdist)
    Cord=np.zeros([2,N])
    
    for i in range(N):
        radii=np.squeeze(np.asarray(BMdist[i,:]))
        b=np.zeros([n-1,1])
        
        for ix in range(n-1):
            b[ix,0]=(radii[0]-radii[ix+1]+BDS[ix+1])/2.0
        
        M_=np.matmul(np.linalg.inv(np.matmul(np.transpose(M),M)),np.transpose(M))
        Cord[:,[i]]=np.matmul(M_,b)
        
    return Cord

plt.ion() ## The real time GUI using Python Matplotlib

while 1:
# sleep(0.5)
 #Accepting Data from Master Beacon 
 print "Now from Master Beacon"
 loop_flag=1
 init_time=time.time()
 for i in range(10):
     ser1.write(bytes('R'))
     sleep(0.05)
 counter=0
 dis1_m_id1=0
 dis1_m_id2=0
 dis1_m_id3=0
 dis1_m_id1_count=0.0
 dis1_m_id2_count=0.0
 dis1_m_id3_count=0.0
 dis1_list=[]
 id1_list=[]
 dis1_m_id1_median=[]
 dis1_m_id2_median=[]
 dis1_m_id3_median=[]
 x=[]
 y=[]

 x.append(2.5)
 y.append(2)
 x.append(0)
 y.append(0)
 x.append(5)
 y.append(0)


 while loop_flag:
    
    mul_flag=1
    mul_time=5
    distance1=0
    unique_id1=0

    

    s=bytearray(ser1.readline());
    #print "Got Something"
    for i in range(5,10):
	    mul_flag=1;
	    for j in range (0,mul_time):
		    mul_flag=mul_flag*10;

	    mul_time=mul_time-1

	    distance1=distanq  ce1+ (s[i]*mul_flag)

    # print distance1/10000.0,
    #print counter,
    if((distance1/10000.0)>MAX_RANGE):
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

    # if(unique_id1==125920):
	   #  print "Id = 1",
    # if(unique_id1==128480):
	   #  print "Id = 2",
    # if(unique_id1==133600):
	  	# print "Id = 3",
	
		
    # print unique_id1,
    id1_list.append(unique_id1) #Stores the Id out of the availables
    sleep(.001)
    ser1.flush()
    counter=counter+1
    if(time.time()-init_time>=waitTime):
      #  print time.time()-init_time
        ser1.write(bytes('S'))#Stop the Ranging Process
        #print "Out of Loop"
        loop_flag=0
 

#Here we need to segregate the data and take the average of the Multiple ranges obtained from the Beacon
 # print "counter", 
 # print counter 

 # print dis1_m_id1, 
 # print dis1_m_id2,
 # print dis1_m_id3,

 for i in range(0,counter):
    if(id1_list[i]==125920):
        #print "Id = 1",
        dis1_m_id1=dis1_m_id1+dis1_list[i]
        dis1_m_id1_count=dis1_m_id1_count+1
        dis1_m_id1_median.append(dis1_list[i])
       # print dis1_m_id1/ dis1_m_id1_count

    if(id1_list[i]==128480):
        # print "Id = 2",
        dis1_m_id2=dis1_m_id2+dis1_list[i]
        dis1_m_id2_count=dis1_m_id2_count+1
        dis1_m_id2_median.append(dis1_list[i])
        

    if(id1_list[i]==133600):
        # print "Id = 3",
        dis1_m_id3=dis1_m_id3+dis1_list[i]
        dis1_m_id3_count=dis1_m_id3_count+1
        dis1_m_id3_median.append(dis1_list[i])


 # print "Distances after adding all available distances"
 # print dis1_m_id1, 
 # print dis1_m_id2,
 # print dis1_m_id3

 if(dis1_m_id1_count>0):
    dis1_m_id1=(dis1_m_id1/dis1_m_id1_count)
 else:
    dis1_m_id1=-1.0

 if(dis1_m_id2_count > 0):
    dis1_m_id2=(dis1_m_id2/dis1_m_id2_count)
 else:
    dis1_m_id2=-1.0

 if(dis1_m_id3_count> 0):
    dis1_m_id3=(dis1_m_id3/dis1_m_id3_count)
 else:
    dis1_m_id3=-1.0

 print "id 1  ",
 print dis1_m_id1
 if dis1_m_id1 is not -1.0:
    print sp.median(dis1_m_id1_median)

 
 print "id 2  ",
 print dis1_m_id2
 if dis1_m_id2 is not -1.0:
    print sp.median(dis1_m_id2_median)
 
 print "id 3  ",
 print dis1_m_id3
 if dis1_m_id3 is not -1.0:
    print sp.median(dis1_m_id3_median)
 
 

 print "Now from Beacon 1"

 #Now we need to send the Instruction to the Beacon 1 to start the ranging Operaion.

 s1.send(MESSAGE) # We send an start ranging message to the Beacon 1.
 print "Message sent to Beacon 1 waiting for reply"
 
 #We have to wait for the time Beacon 1 Ranges all the Mobiles.

 data = s1.recv(BUFFER_SIZE)

 #The Data contains the Co-ordinates of the Mobiles in String Form We need to Extract the Required Data. 
 # Format: send_data=str(dis1_m_id1_int_cm)+","+str(dis1_m_id2_int_cm)+","+str(dis1_m_id1_int_cm)
 # We need to Split the Data.



 #Getting Required Data from the Obtained String

 dis2_m_id1_str,dis2_m_id2_str,dis2_m_id3_str=data.split(",") # After the Split we will get the Strings

 dis2_m_id1=float(dis2_m_id1_str)
 dis2_m_id2=float(dis2_m_id2_str)
 dis2_m_id3=float(dis2_m_id3_str)

 # The sent was in the Form of CentiMeters.Converting to the meter form.

 dis2_m_id1=dis2_m_id1/100.0
 dis2_m_id2=dis2_m_id2/100.0
 dis2_m_id3=dis2_m_id3/100.0

 print "id 1  ",
 print dis2_m_id1
 print "id 2  ",
 print dis2_m_id2
 print "id 3  ",
 print dis2_m_id3



 print "Now with Beacon 2"

 #Now We need to Ping the Beacon 2 so that it can Start Ranging 
 s2.send(MESSAGE) # We send an start ranging message to the Beacon 2.
 
 #We have to wait for the time Beacon 2 Ranges all the Mobiles.

 data = s2.recv(BUFFER_SIZE)


 #The Data contains the Co-ordinates of the Mobiles in String Form We need to Extract the Required Data. 
 # Format: send_data=str(dis1_m_id1_int_cm)+","+str(dis1_m_id2_int_cm)+","+str(dis1_m_id1_int_cm)
 # We need to Split the Data.



 #Getting Required Data from the Obtained String

 dis3_m_id1_str,dis3_m_id2_str,dis3_m_id3_str=data.split(",") # After the Split we will get the Strings

 dis3_m_id1=float(dis3_m_id1_str)
 dis3_m_id2=float(dis3_m_id2_str)
 dis3_m_id3=float(dis3_m_id3_str)

 # The sent was in the Form of CentiMeters.Converting to the meter form.

 dis3_m_id1=dis3_m_id1/100.0
 dis3_m_id2=dis3_m_id2/100.0
 dis3_m_id3=dis3_m_id3/100.0

 print "id 1  ",
 print dis3_m_id1
 print "id 2  ",
 print dis3_m_id2
 print "id 3  ",
 print dis3_m_id3

 BMdist1=np.matrix([[dis3_m_id1**2,dis1_m_id1**2,dis2_m_id1**2]])#Square of the Distance as input
 BMdist2=np.matrix([[dis3_m_id2**2,dis1_m_id2**2,dis2_m_id2**2]])#Square of the Distance as input
 BMdist3=np.matrix([[dis3_m_id3**2,dis1_m_id3**2,dis2_m_id3**2]])#Square of the Distance as input
 
 print BMdist1
 print BMdist2
 print BMdist3

 print "id 1  ",
 print trilat(BMdist3)
 print "id 2  ",
 print trilat(BMdist2)
 print "id 3  ",
 print trilat(BMdist3)

 cod1=trilat(BMdist1)
 cod2=trilat(BMdist2)
 cod3=trilat(BMdist3)
 plt.clf()

 if((dis1_m_id1 is not -1.0)and (dis2_m_id1 is not -1.0) and(dis3_m_id1 is not -1.0)):
     x.append(cod1[0][0])
     y.append(cod1[1][0])

 if((dis1_m_id2 is not -1.0)and (dis2_m_id2 is not -1.0)and (dis3_m_id2 is not -1.0)):
     x.append(cod2[0][0])
     y.append(cod2[1][0])

 if((dis1_m_id3 is not -1.0)and (dis2_m_id3 is not -1.0)and (dis3_m_id3 is not -1.0)):
     x.append(cod3[0][0])
     y.append(cod3[1][0])

 print x
 print y
 plt.scatter(x, y)
 plt.grid()
 plt.pause(0.05)
