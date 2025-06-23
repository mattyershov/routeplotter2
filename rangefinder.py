import os
import keyboard
from time import sleep
import math

def clear():
    os.system('clear')

alt = 0
ele = -1

clear()

print(f"Altitude: {alt} ft.\nElevation: {ele}°")
while True:
    if keyboard.is_pressed('up arrow'):
        alt += 1
    if keyboard.is_pressed('down arrow'):
        alt -= 1
    if keyboard.is_pressed('right arrow'):
        ele += 1
    if keyboard.is_pressed('left arrow'):
        ele -= 1
    
    if keyboard.is_pressed('up arrow') or keyboard.is_pressed('down arrow') or keyboard.is_pressed('right arrow') or keyboard.is_pressed('left arrow'):
        clear()
        if ele == 0:
            ele = -1
        if alt < 0:
            alt = 0
        print(f"Altitude: {alt} ft.\nElevation: {ele}°")
        sleep(0.05)
    if keyboard.is_pressed('enter'):
        break

def calculate(alt, ele):
    dist = '%.2f'%(-alt * math.tan(ele))
    return dist

dist_nm = float(calculate(alt, ele)) * 0.00016457883