'''
This program simulates a UAV with a simple state engine, lets you control the heading using the arrow keys and outputs
the location of the simulated aircraft graphically at a refresh rate of 10Hz and prints the aircraft's parameters at a rate of 1Hz.

Initial state parameters can be edited through the config.json file

Controls:
Right arrow: +5 degrees to the right
Left arrow: +5 degrees to the left
'x' key: terminates the simulation


Ahmed Elsaharti
September, 2019
'''


import time
import math
import matplotlib
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import keyboard
import json
import os

plt.ion() # Enabling interactive plot mode
map = Basemap(projection='mill',llcrnrlat=20,urcrnrlat=50,\
              llcrnrlon=-130,urcrnrlon=-60,resolution='l') # Initiallizing map
map.drawcoastlines()
map.drawcountries()
plt.title('Flight Trajectory')
map.fillcontinents()
map.drawmapboundary()





# ---------- Fetching initial configuration:

CWD = os.getcwd()
FILE_PATH = '%s/%s' % (CWD, 'config.json')
UAV_DATA = {}

try:
    with open(FILE_PATH) as data_file:
        UAV_DATA = json.load(data_file)
except IOError as e:
    print (e)
    print ('IOError: Unable to open config file')
    exit(1)


lat,lon = UAV_DATA["latitude"],UAV_DATA["longitude"]
x,y = map(lon,lat)




# ---------- Utility functions:

def calc_replot(): # recalculate and replot
    easting = ((UAV_DATA["airspeed"] / 60.0) / 3600.0) * math.sin(math.radians(UAV_DATA["heading"]))  # only correct at equator
    northing = ((UAV_DATA["airspeed"] / 60.0) / 3600.0) * math.cos(math.radians(UAV_DATA["heading"]))
    UAV_DATA["latitude"] += northing
    UAV_DATA["longitude"] += easting
    lat,lon = UAV_DATA["latitude"],UAV_DATA["longitude"]
    x,y = map(lon,lat)
    map.plot(x,y,'r.')
    plt.pause(0.1)
    UAV_DATA["longitude"]=lon
    UAV_DATA["latitude"]=lat





x
# ---------- Main function:

while (True): # Outer loop (1Hz)
    for i in range(10): # Inner Loop (10 Hz)
        try:
            if keyboard.is_pressed('right'):  # if key right key is pressed 
                #print('You Pressed Right!')
                UAV_DATA["heading"]+=5
                calc_replot()
                
            elif keyboard.is_pressed('left'):  # if key left is pressed 
                UAV_DATA["heading"]-=5
                calc_replot()

            elif keyboard.is_pressed('x'):
                plt.close('all')
                break
            
            else:
                
                calc_replot()
                pass
        except:
            break  # if user pressed a key other than the given key the loop will break
    print("LAT: ",UAV_DATA["latitude"]," LONG: ", UAV_DATA["longitude"] ," ALT: ", UAV_DATA["altitude"]," HEAD: ", UAV_DATA["heading"]," ASPD: ", UAV_DATA["airspeed"])
    if keyboard.is_pressed('x'):
        plt.close('all')
        break
