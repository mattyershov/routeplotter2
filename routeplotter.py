import rangefinder
from gpsdclient import GPSDClient
from geopy.distance import geodesic
from geopy import Point
from time import sleep
import math
import numpy as np

sunfishpolar = { #twa : percentage of wind speed
    0 : 0,
   45 : 0.5,
   50 : 0.75,
   60 : 0.8,
   90 : 0.85,
   120 : 0.9,
   150 : 1,
   180 : 0.9,
   210 : 0.8,
   240 : 0.7,
   270 : 0.65,
   300 : 0.6,
   310 : 0.5,
   315 : 0.45
}

# def get_bearing(lat1,lon1,lat2,lon2):
#     dLon = lon2 - lon1
#     y = math.sin(dLon) * math.cos(lat2)
#     x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon)
#     brng = np.rad2deg(math.atan2(y, x))
#     if brng < 0: brng+= 360
#     return brng

# def compass(brng, track):
#     diff = brng - track
#     if math.abs(diff) > 120:
#         diff = 120
#     diffsmall = diff / 5
#     return diffsmall

while True:
    with GPSDClient() as client:
        for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
            lat =  result.get("lat", "n/a")
            lon = result.get("lon", "n/a")
            trk = int(result.get("track", "n/a"))
            spd = int((result.get("speed", "n/a")) * 0.51445)
            print(f"lat: {lat}, lon: {lon}, trk: {trk}, spd: {spd}")
            # if lat and lon and trk and spd:
            #     break

    print(f"lat: {lat}, lon: {lon}, trk: {trk}, spd: {spd}")
    
    origin = Point(lat, lon)

    destination = geodesic(nautical = rangefinder.dist_nm).destination(point = origin, bearing = trk)

    print(f"Destination: ({destination.latitude}, {destination.longitude})")
    if trk:
        print(f"Bearing: {compass(get_bearing(lat, lon, destination.latitude, destination.longitude), trk)}")
    sleep(1)

