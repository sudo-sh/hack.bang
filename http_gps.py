# importing the requests library
import requests
 

URL = "http://10.1.85.31:12345/TexaGPS/result.json" 

PARAMS = {}
# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)
 
# extracting data in json format
data = r.json()
 
#print data 
heading = data['Heading']['trueHeading']
latitude = data['Locations'][0]['latitude']
longitude = data['Locations'][0]['longitude']
print("Latitude:%s\nLongitude:%s\nHeading:%s"%(latitude, longitude, heading))
