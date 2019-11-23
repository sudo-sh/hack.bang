import math as Math
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

print calculate_initial_compass_bearing((12.977982,77.713086),(12.978062,77.713101))