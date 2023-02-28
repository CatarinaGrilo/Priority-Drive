#!/usr/bin/env python
# #################################################
## ACCESS TO IN-VEIHICLE SENSORS/ATUATORS AND GPS
#################################################
import time
from in_vehicle_network.car_motor_functions import *
from in_vehicle_network.location_functions import *

#-----------------------------------------------------------------------------------------
# Thread - update location based on last known position, movement direction and heading. 
#         Note: No speed information and vehicles measurements are included.
#         TIP: In case, you want to include them, use obd_2_interface for this purpose
#-----------------------------------------------------------------------------------------
def update_location(node, start_flag, coordinates, obd_2_interface, engine_flag, count_slower):
	gps_time = speed_atualization

	while not start_flag.isSet():
		time.sleep (1)
	print('STATUS: Ready to start - THREAD: update_location - NODE: {}\n'.format(node),'\n')
	while not engine_flag.isSet():
		time.sleep (1)

	while True:
		time.sleep(gps_time)
		stop = count_slower['stop']
		position_update(coordinates, obd_2_interface, stop)
#		print('STATUS: New position update - THREAD: update_location - NODE: {}\n'.format(coordinates),'\n')
	return


#-----------------------------------------------------------------------------------------
# Car Finite State Machine
# 		initial state: 	car_closed  - Car is closed and GPIO/PWN are not initialise
#				input: 	car_command = 'e' (enter car): next_state: car_open
#		next_state:		car_opened 	- Car is open and GPIO/PWN are initialised
#				input: 	car_command = '1' (turn on):	next_state: car_ready
#						car_command = 'x' (disconnect): next_state: car_closed
# 		next_state:		car_ready	- Car is ready to move and enable is turned on
#				input: 	car_command in ['f','b',r','l','s'] - next_state: car_moving
#						car_command = '0' (turn off):	next_state: car_ready
# 						car_command = 'x' (disconnect): next_state: car_closed					
#-----------------------------------------------------------------------------------------

car_closed = 0			# Car is closed and GPIO/PWN are not initialised
car_opened = 1			# Car is open and GPIO/PWN are initialised
car_ready  = 2			# Car is ready to move forward, backward, turn left or right or stop and enable is turned on

car_parked = '-'		# Unknown moving direction
speed_inc = 10			# TIP: you can configure these limits you you want to change the step of speed variance
speed_dec = -20

#-----------------------------------------------------------------------------------------
# Thread - control the car movement - uses the FSM described before
#-----------------------------------------------------------------------------------------
def movement_control(node, start_flag, coordinates, obd_2_interface, movement_control_txd_queue, engine_flag, count_slower, count_faster):
	TIME_INTERVAL = 5
	
	while not start_flag.isSet():
		time.sleep (1)
	print('STATUS: Ready to start - THREAD: movement_control - NODE: {}\n'.format(node),'\n')
	while not engine_flag.isSet():
		time.sleep (1)
	
	direction = car_parked
	status=car_closed
	speed = obd_2_interface['speed']
	slower = count_slower['num']
	faster = count_faster['num']

	while True:
		move_command=movement_control_txd_queue.get()
		if (status == car_closed):
			if (move_command == 'e'):
				pwm_tm_control, pwm_dm_control=open_vehicle(speed)
				status=car_opened
		elif (status == car_opened):
			if (move_command == '1'):
				turn_vehicle_on()
				status=car_ready
			elif (move_command == 'x'):
				close_vehicle()
				status = car_closed
		elif (status == car_ready):
			if (move_command in ['f','b','l','r','s','d','i']):
				new_movement(move_command)
				if (move_command in ['f', 'b']):
					direction=move_command				
				elif(move_command == 'i'):
					faster = count_faster['num']
					print('STATUS MOVEMENT CONTROL INCREASE!!!')
					if(faster!=0):		
						speed= vehicle_var_speed(speed, speed_inc, pwm_tm_control)
						faster= faster -1
						count_faster['num']=0
				elif(move_command == 'd'):
					slower = count_slower['num']
					print('STATUS MOVEMENT CONTROL DECREASE!!!')
					print('slower'+str(slower))
					if(slower!=0):
						print('Car_control' + str(count_slower))
						speed= vehicle_var_speed(speed, speed_dec, pwm_tm_control)
						slower = slower-1
						count_slower['num']=0	
				elif (move_command == 's'):
					stop_vehicle()
					direction = car_parked
				elif (move_command == 'v'):
					speed= vehicle_var_speed(speed, -30, pwm_tm_control)
			elif (move_command == '0'):
				turn_vehicle_off()
				direction = car_parked
				status=car_opened
			elif (move_command == 'x'):
				close_vehicle()
				direction = car_parked
				status = car_closed
		else:
			print ('ERROR: movement control -> invalid status')

		set_vehicle_info (obd_2_interface, speed, direction, status)
		position_update(coordinates, obd_2_interface, 1)
		time.sleep(TIME_INTERVAL)
	return
