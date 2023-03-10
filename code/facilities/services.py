#!/usr/bin/env python
# #################################################
## FUNCTIONS USED BY FACILITITES LAYER  - COMMMON SERVICES
#################################################
import time
from in_vehicle_network.car_motor_functions import *
from in_vehicle_network.location_functions import *
from in_vehicle_network.traffic_functions import *


#------------------------------------------------------------------------------------------------
# create_CA_message - create a cooperative awareness message based on the vehicle's informatiom
#                    - node: node that generates the event
#                    - msg_id: identification of the event used to discard duplicated DEN messages received
#                    - coordinates: real-time position (x,y) at the instant (t) when the message is created
#                    - obd_2_interface: vehicle's dynamic information (speed, direction and heading).
#-------------------------------------------------------------------------------------------------

def create_ca_message(node, msg_id,coordinates, obd_2_interface, light , tipo):
	
	if( tipo != 'S'):
		x,y,t = position_read(coordinates)
		s,d,h = get_vehicle_info(obd_2_interface)
		ca_msg= {'msg_type':'CA', 'node':node, 'msg_id':msg_id,'pos_x': x,'pos_y': y,'time':t,'speed': s, 'dir':d, 'heading':h, 'type' : 'C' }
		return ca_msg
	else : 
		x,y,t = position_read(coordinates)
		s,d,h = get_vehicle_info(obd_2_interface)
		color = get_color(light)
		ca_msg= {'msg_type':'CA', 'node':node, 'msg_id':msg_id,'pos_x': x,'pos_y': y,'time':t,'speed': s, 'dir':d, 'heading':h, 'light': color , 'type' : 'S'}
		return ca_msg
			

#------------------------------------------------------------------------------------------------
# create_DEN_message - create an event message (DEN) based on information received from application layer
#                    - node: node that generates the event
#                    - msg_id: identification of the event used to discard duplicated DEN messages received
#                    - coordinates: real-time position (x,y) at the instant (t) when the message is created
#                    - event: event information received from application layer.
#-------------------------------------------------------------------------------------------------
def create_den_message(node, msg_id, coordinates, event, obd_2_interface, light , tipo):
	if( tipo != 'S') : 
		x,y,t = position_read(coordinates)
		s,d,h = get_vehicle_info(obd_2_interface)
		den_msg= {'msg_type':'DEN', 'node':node, 'msg_id':msg_id,'pos_x': x,'pos_y':y, 'time':t, 'event': event, 'speed': s, 'dir':d, 'heading':h, 'type' : 'U' }
		return den_msg
	else : 
		x,y,t = position_read(coordinates)
		s,d,h = get_vehicle_info(obd_2_interface)
		color = get_color(light)
		den_msg= {'msg_type':'DEN', 'node':node, 'msg_id':msg_id,'pos_x': x,'pos_y':y, 'time':t, 'event': event, 'speed': s, 'dir':d, 'heading':h, 'type' : 'U' , 'light' : color}
		return den_msg


#
#
#

def create_start_message(node):
    start_msg= {'msg_type':'start', 'node':node }
    return start_msg