# vmcattempt = -0.131+0.0229(x)-.000168(x)^2+.000000499(x)^3-.000000000566(x)^4 # line of best fit, use Google Sheets to find one when you have the actual polar
import rangefinder
from gpsdclient import GPSDClient
import math
import keyboard

bestupvmg = ['''wind angle 1, wind angle 2''']
bestdownvmg = ['''wind angle 1, wind angle 2''']
vmgs = {}

# mode = upwind, downwind, reach
def getvmg(bspd, twa):
    vmg = bspd * math.cos(twa)
    return vmg

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
        if keyboard.is_pressed('enter'):
            twaentry = input('TWA: ')
            vmgs.update({twaentry : spd})