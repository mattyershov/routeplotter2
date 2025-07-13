import rangefinder
from gpsdclient import GPSDClient
from geopy.distance import geodesic
from geopy.distance import VincentyDistance
from geopy import Point
from time import sleep
import math
import numpy as np

posdiffsm  = 0

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

lightbar = ['o', 'o', 'o', 'o', 'o', 'o']


def is_angle_between(target, start, end):
    target = target % 360
    start = start % 360
    end = end % 360

    if start <= end:
        return start <= target <= end
    else:
        # Wrap-around case
        return target >= start or target <= end

def get_bearing(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1)*math.sin(lat2) - \
        math.sin((lat1))*math.cos(lat2)*math.cos(dLon)
    brng = math.degrees(math.atan2(y, x))
    return (brng + 360) % 360

def compass(brng, track, spd):
    diff = (float(brng) - float(track) + 360) % 360  # angular difference
    if diff > 180:
        diff -= 360  # make it range from -180 to +180
    normalized = (diff + 180) / 360  # scale to 0.0–1.0
    index = int(round(normalized * (len(lightbar) - 1)))

    # Clamp index just in case 
    index = max(0, min(index, len(lightbar) - 1))

    new_lightbar = ['o'] * len(lightbar)
    new_lightbar[index] = '|'

    return new_lightbar, diff

def findmode(targetbrng): #NOTE: This is in absolute degrees, not pos/neg degrees based on port/stbd
    if is_angle_between(target=targetbrng, start=320, end=40):
        mode = "U"
    elif 140 <= targetbrng <= 220:
        mode = "D"
    else:
        mode = "R"
    return mode

def layline(dist, brng, wangle):
    tack = "P"
    updown = "U"
    mleg1 = dist * math.sin((2*math.pi)/9)
    mleg2 = dist * math.tan((2*math.pi)/9)
    if tack == "P" and updown == "U":
        bleg1 = wangle + 40
        bleg2 = bleg1 - 90
    elif tack == "S" and updown == "U":
        bleg1 = wangle - 40
        bleg2 = bleg1 + 90
    elif tack == "P" and updown == "D":
        bleg1 = wangle - 10
        bleg2 = bleg1 - 90
    elif tack == "S" and updown == "D":
        bleg1 = wangle + 10
        bleg2 = bleg1 + 90
    return bleg1 % 360, mleg1, bleg2 % 360, mleg2

def checkwaypt(curlat, curlon):
    pos = geopy.Point(curlat, curlon)
    bleg1, mleg1, bleg2, mleg2 = layline(dist=rangefinder.dist_nm, brng=rangefinder.targetbrng, wangle=0)
    tackdest = VincentyDistance(kilometers=1.852 * mleg1).destination(pos, bleg1)
    finaldest = VincentyDistance(kilometers=1.852 * mleg2).destination(tackdest, bleg2)
    if pos == tackdest:
        return 1
    elif pos == finaldest:
        return 2
    else:
        return 0


def main():
    while True:
        rangefinder.clear()
        with GPSDClient() as client:
            while True:
                result = next(client.dict_stream(convert_datetime=True, filter=["TPV"]))
                print(result)
                lat = result.get("lat", "n/a")
                lon = result.get("lon", "n/a")
                trk = result.get("track", 0)
                spd = result.get("speed", 0)
                if lat != "n/a" and lon != "n/a":
                    break

        origin = Point(lat, lon)
        destination = geodesic(nautical = rangefinder.dist_nm).destination(point = origin, bearing = rangefinder.targetbrng)

        if trk:
            # brng = get_bearing(lat, lon, destination.latitude, destination.longitude)
            bleg1, mleg1, bleg2, mleg2 = layline(dist=rangefinder.dist_nm, brng=rangefinder.targetbrng, wangle=0)
            lightbar, posdiffsm = compass(bleg1, trk, spd)
            # print(f"Bearing: {brng}")
            print(f"Lightbar: {lightbar}")
            print(f"Small Bearing (offset): {posdiffsm}")
            sleep(1.5)


if __name__ == "__main__":
    main()