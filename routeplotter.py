import rangefinder
from gpsdclient import GPSDClient
from geopy.distance import geodesic
from geopy import Point

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

with GPSDClient() as client:
    for result in client.dict_stream(convert_datetime=True, filter=["TPV"]):
        lat =  result.get("lat", "n/a")
        lon = result.get("lon", "n/a")
        trk = int(result.get("track", "n/a"))
        spd = int((result.get("speed", "n/a")) * 0.51445)
        if lat and lon:
            break

    print(f"{lat}, {lon}, {trk}, {spd}")
    
    origin = Point(lat, lon)

    destination = geodesic(nautical = rangefinder.dist_nm).destination(point = origin, bearing = trk)

    print(f"{destination.latitude}, {destination.longitude}")

    
    def calcvmg(bspd, twa):
        twarad = twa * (math.pi / 180)
        vmg = bspd * math.cos(twarad)
        return vmg

    def optimizevmg(twa):
        if 0 <= twa <=90:
            twalimit = 90
        if 90 < twa <= 180:
            twalimit = 90
        if 270 <= twa < 0:
            twalimit = 0
        if 180 < twa < 270:
            twalimit = 270
        maxvmg = [0, 0] # [twa, vmg]
        for i in range(twalimit - 90, twalimit):
           vmgattempt = -0.131+0.0229(float(i))-.000168(float(i))^2+.000000499(float(i))^3-.000000000566(float(i))^4 # line of best fit, use Google Sheets to find one when you have the actual polar
           if vmgattempt > maxvmg[1]:
                maxvmg = [i, vmgattempt]
        return maxvmg