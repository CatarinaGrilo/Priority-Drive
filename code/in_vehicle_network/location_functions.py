#!/usr/bin/env python
# #################################################
## FUNCTIONS USED IN VEHICLE - (x,y) location
#################################################
import time
from in_vehicle_network.car_motor_functions import *

speed_atualization = 0.5

# the funtion made by us to locate the car in cm 
def calculate_location(speed, direction, stop):
    
    if(direction=='f'):
        if(speed<=0):
            delta = 0
            if(stop!=0):
                stop=0
                stop_vehicle()
        elif(speed==10):
            delta = (4.826/0.5)*speed_atualization
        elif(speed==20):
            delta = (14.986/0.5)*speed_atualization
        elif(speed==30):
            delta = (27.178/0.5)*speed_atualization
        elif(speed==40):
            delta = (40.132/0.5)*speed_atualization
        elif(speed==50):
            delta = (59.436/0.5)*speed_atualization
        elif(speed==60):
            delta = (78.486/0.5)*speed_atualization
        elif(speed==70):
            delta = (106.426/0.5)*speed_atualization
        elif(speed==80):
            delta = (129.54/0.5)*speed_atualization
        elif(speed==90):
            delta = (153.924/0.5)*speed_atualization
        else:
            delta = (169.672/0.5)*speed_atualization
    if(direction=='b'):
        if(speed<=0):
            delta = 0
            if(stop!=0):
                stop=0
                stop_vehicle()
        if(speed==10):
            delta = (3.556/0.5)*speed_atualization
        elif(speed==20):
            delta = (10.414/0.5)*speed_atualization
        elif(speed==30):
            delta = (18.796/0.5)*speed_atualization
        elif(speed==40):
            delta = (30.48/0.5)*speed_atualization
        elif(speed==50):
            delta =  (43.688/0.5)*speed_atualization
        elif(speed==60):
            delta =  (60.198/0.5)*speed_atualization
        elif(speed==70):
            delta =  (76.454/0.5)*speed_atualization
        elif(speed==80):
            delta =  (91.44/0.5)*speed_atualization
        elif(speed==90):
            delta =  (105.156/0.5)*speed_atualization
        else:
            delta = (115.062/0.5)*speed_atualization
    
    return (delta)

#------------------------------------------------------------------------------------------------
# position_update - updates x,y,t based on the current position, direction and heading. 
#       Note: No speed ot real behaviour of the vehicles is included
#       TIP: you can add here your position_update function. But, keep the parameters updated
#------------------------------------------------------------------------------------------------
def position_update(coordinates, obd_2_interface, stop):

    speed, direction, heading=get_vehicle_info(obd_2_interface)
    if direction=='-':
        return
    #include here assisted gps: estimate new position based on current coordinates, speed and directio
    #We consider a simple fowarding movement of delta positions per unit time.
    if(heading=='E' or heading=='O'):
        dummy_delta_x = calculate_location(speed, direction, stop)
        dummy_delta_y = 0
    if(heading=='N' or heading=='S'):
        dummy_delta_x = 0
        dummy_delta_y = calculate_location(speed, direction, stop)
    
    if (((heading=='E') and (direction=='f')) or ((heading=='O') and (direction=='b'))):
        x=coordinates['x'] + dummy_delta_x
        y=coordinates['y']
    elif (((heading=='E') and (direction=='b')) or ((heading=='O') and (direction=='f'))):
         x=coordinates['x'] - dummy_delta_x
         y=coordinates['y']
    elif (((heading=='N') and (direction=='f')) or ((heading=='S') and (direction=='b'))):
        x=coordinates['x']
        y=coordinates['y'] + dummy_delta_y
    elif (((heading=='N') and (direction=='b')) or ((heading=='S') and (direction=='f'))):
        x=coordinates['x']
        y=coordinates['y'] - dummy_delta_y
    
    t=time.time()
    coordinates.update({'x':x, 'y':y, 't':t})
    return


#------------------------------------------------------------------------------------------------
# position_read - last known position
#------------------------------------------------------------------------------------------------
def position_read(coordinates):

    x=coordinates['x']
    y=coordinates['y']
    t=coordinates['t']

    return x,y,t
