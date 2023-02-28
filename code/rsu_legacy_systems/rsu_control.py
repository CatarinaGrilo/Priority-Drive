#!/usr/bin/env python
# #################################################
## RSU legacy system control - example traffic light systems/external sensors and actuators
#################################################
from socket import MsgFlag
import time
from application.message_handler import *
from application.self_driving_test import *

def traffic_light(node, start_flag, light, mode, engine_flag):

	red_time = 12
	green_time = 8
	yellow_time = 4
	t=0
	
	while not start_flag.isSet():
		time.sleep (1)
	while not engine_flag.isSet():
		time.sleep (1)

	init_gpio()
	if(int(node)%2==1):
		green_on(1)
	else:
		red_on(2)
	print('STATUS: Ready to start - THREAD: traffic_light - NODE: {}'.format(node),'\n')
	print(mode)
	#temos de criar outros perfis para semáforos no mesmo cruzamento~
	if RASPBERRY==True:
		init_gpio()
	while(True):
		while (mode['id']==1):
			blue_off(1)
			if(light.get("color") == "red" and t >= red_time):
				light.update({'color': 'green'})
				if(int(node)%2==1):
					red_off(1)
					green_on(1)
				else:
					red_off(2)
					green_on(2)
				t=0
			elif(light.get("color") == "green" and t >= green_time):
				light.update({'color': 'yellow'})
				if(int(node)%2==1):
					green_off(1)
					amber_on(1)
				else:
					green_off(2)
					amber_on(2)
				t=0
			elif(light.get("color") == "yellow" and t >= yellow_time):
				light.update({'color': 'red'})
				if(int(node)%2==1):
					amber_off(1)
					red_on(1)
				else:
					amber_off(2)
					red_on(2)
				t=0
			else:
				time.sleep(1)
				t=t+1
				print('Cor do semaforo ' + light['color'])
		
		while(mode['id'] == 2):
				print('URGENCIA - Verde')
				time.sleep(1)
				light.update({'color': 'green'})
				if(int(node)%2==1):
					red_off(1)
					green_off(1)
					amber_off(1)
					blue_on(1)
					green_on(1)
				else:
					red_off(2)
					green_off(2)
					amber_off(2)
					blue_on(2)
					green_on(2)
				
		
		while(mode['id'] == 3):
				print('URGENCIA - Vermelho')
				time.sleep(1)
				light.update({'color': 'red'})
				if(int(node)%2==1):
					red_off(1)
					green_off(1)
					amber_off(1)
					blue_on(1)
					red_on(1)
				else:
					red_off(2)
					green_off(2)
					amber_off(2)
					blue_on(2)
					red_on(2)


		
		

		





		



