

import serial
from time import sleep
import time
import numpy as np
import statistics as sp
import matplotlib.pyplot as plt
import requests
import math as Math

global threshold_angle
threshold_angle = 24

global PI 
PI=3.14159265358979323846

##The Moving Average Variables
global N
N=10.0
global cumsum
global moving_avg
moving_avg = 0.0
cumsum = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]



URL = "http://10.1.85.31:12345/TexaGPS/result.json" 

PARAMS = {}

##The following code gives the latitude and longitude of the remote CAR.
def http_data():
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
     
    # extracting data in json format
    data = r.json()
     
    #print data 
    heading = data['Heading']['trueHeading']
    latitude = data['Locations'][0]['latitude']
    longitude = data['Locations'][0]['longitude']
    return latitude,longitude,heading
    #print("Latitude:%s\nLongitude:%s\nHeading:%s\n"%(latitude, longitude, heading))





'''
The sample points are the 
Measured Data and Will be 
obtained using the Mobile and 
Decawave combination


lat_car=
lon_car=
head_car=
'''

# lat1=
# lon1=
# head1=


# lat2=
# lon2=
# head2=


def calcraddistance(lat1,lon1,lat2,lon2):
    t1 = Math.sin(Math.radians(lat1)) * Math.sin(Math.radians(lat2))
    t2 = Math.cos(Math.radians(lat1))* Math.cos(Math.radians(lat2))
    t3 = Math.cos(Math.radians(lon1 - lon2))
    t4 = t2 * t3
    t5 = t1 + t4
    rad_dist = Math.atan(-t5/Math.sqrt(-t5 * t5 +1)) + 2 * Math.atan(1);
    mi=rad_dist * 3437.74677 * 1.1508
    ft=mi*5.2800102998e+3
    km=mi*1.6093470878864446
    meter=km*1000.0

    return meter  

#This function calculates the Bearing the angle measured from the North direction line North from the Compass. 

def calculate_initial_compass_bearing(pointA, pointB):

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = Math.radians(pointA[0])
    lat2 = Math.radians(pointB[0])

    diffLong = Math.radians(pointB[1] - pointA[1])

    x = Math.sin(diffLong) * Math.cos(lat2)
    y = Math.cos(lat1) * Math.sin(lat2) - (Math.sin(lat1)
            * Math.cos(lat2) * Math.cos(diffLong))

    initial_bearing = Math.atan2(x, y)

    initial_bearing = Math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

#This function calculates Determines the Quadrant the other is in

def check_quadrant(bearing):
    #We have assumed that the Car is at the center and the remote or the other car lies
    #in some other quadrant which is calculated by the Bearing angle.

    if bearing>0:
        return 1
    elif bearing>90 and bearing<180:
        return 2
    elif bearing>180 and bearing<270:
        return 3
    elif bearing>270 and bearing<360:
        return 4
    elif bearing >= 360:
        check_quadrant(bearing-360)

#This function calculates the heading angle difference with respect to the North of the Compass

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
 for i in range(10):
    ser1.write(bytes('R'))
    print "Sent R"
    sleep(0.05)


 counter=0
 dis1_m_id1=0
 
 dis1_m_id1_count=0.0

 dis1_list=[]
 id1_list=[]
 dis1_m_id1_median=[]
 print "Going to loop"
 while loop_flag:
    x=[]
    y=[]
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


    # cumsum.remove(cumsum[0])
    del cumsum[0]
    cumsum.append(distance1/10000.0)
    moving_avg = sum(cumsum)/len(cumsum)
    print cumsum
    print moving_avg
	
    latitude,longitude,heading = http_data()
    plt.clf()
    gps_heading = calculate_initial_compass_bearing((latitude,longitude), (12.977982,77.713086))
    quadrant = check_quadrant(gps_heading)
    #print "gps " + str(gps_heading)
    #gps_heading = gps_heading + threshold_angle # add or sub accordingly 
    #print (distance1/10000.0)*Math.sin(Math.radians(heading))
    x.append(0)# This is the origin and the location of the Car. 
    y.append(0)
    x.append((moving_avg)*Math.cos(Math.radians(heading)))
    y.append((moving_avg)*Math.sin(Math.radians(heading)))
    plt.xlim(-20,20)
    plt.ylim(-20,20)
    plt.scatter(x,y,s=80)

    plt.grid()
    plt.pause(0.05)
