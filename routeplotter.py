import rangefinder
from gpsdclient import GPSDClient
from geopy.distance import geodesic
from geopy import Point

with GPSDClient() as client:
    for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
        lat =  result.get("lat", "n/a")
        lon = result.get("lon", "n/a")
        trk = result.get("track", "n/a")
        spd = (result.get("speed", "n/a")) * 0.51445
        if lat and lon:
            break

    print(f"{lat}, {lon}, {trk}, {spd}")
    
    origin = Point(lat, lon)

    destination = geodesic(nautical = rangefinder.dist_nm).destination(point = origin, bearing = trk)

    print(f"{destination.latitude}, {destination.longitude}")

    twa = 15
    def calcvmg(bspd, twa):
        twa_r = twa * (math.pi / 180)
        vmg = bspd * math.cos(twa_r)
        return vmg