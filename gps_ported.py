
import math as Math
global PI
from mpmath import mp
import requests


mp.dps=100
PI=3.14159265358979323846


URL = "http://10.1.85.31:12345/TexaGPS/result.json" 

PARAMS = {}

def http_data():
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
     
    # extracting data in json format
    data = r.json()
     
    #print data 
    heading = data['Heading']['trueHeading']
    latitude = data['Locations'][0]['latitude']
    longitude = data['Locations'][0]['longitude']
    print latitude, longitude
    print "heading",
    print heading
    return (latitude,longitude)





#This Function calculates the distance using the GPS Co-ordinates.
def calcraddistance(lat1,lon1,lat2,lon2):
    t1 = Math.sin(Math.radians(lat1)) * Math.sin(Math.radians(lat2))
    t2 = Math.cos(Math.radians(lat1))* Math.cos(Math.radians(lat2))
    t3 = Math.cos(Math.radians(lon1 - lon2))
    #print t3
    t4 = t2 * t3
    t5 = t1 + t4
    rad_dist = Math.atan(-t5/Math.sqrt(-t5 * t5 +1)) + 2 * Math.atan(1);
    mi=rad_dist * 3437.74677 * 1.1508
    ft=mi*5.2800102998e+3
    km=mi*1.6093470878864446
    meter=km*1000


    return meter  



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

print calcraddistance(12.977982,77.713086,12.978061,77.713077)
while True:
    latitude, longitude = http_data()
    theta = calculate_initial_compass_bearing((latitude,longitude), (12.977982,77.713086))
    print theta
