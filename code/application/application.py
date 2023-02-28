#!/usr/bin/env python
# #####################################################################################################
# SENDING/RECEIVING APPLICATION THREADS - add your business logic here!
## Note: you can use a single thread, if you prefer, but be carefully when dealing with concurrency.
#######################################################################################################
from distutils import core
from socket import MsgFlag
import time
from application.message_handler import *
from application.self_driving_test import *
from in_vehicle_network.location_functions import position_read
import math




# #####################################################################################################
# constants
warm_up_time = 10

#-----------------------------------------------------------------------------------------
# Thread: application transmission. In this example user triggers CA and DEN messages. 
#		CA message generation requires the sender identification and the inter-generation time.
#		DEN message generarion requires the sender identification, and all the parameters of the event.
#		Note: the sender is needed if you run multiple instances in the same system to allow the 
#             application to identify the intended recipiient of the user message.
#		TIPS: i) You may want to add more data to the messages, by adding more fields to the dictionary
# 			  ii)  user interface is useful to allow the user to control your system execution.
#-----------------------------------------------------------------------------------------
def application_txd(node, start_flag, my_system_rxd_queue, ca_service_txd_queue, den_service_txd_queue, urgent, tipo):

	if(tipo=='S'):
		while not start_flag.isSet():
			time.sleep (1)
			print('STATUS: Ready to start - THREAD: application_txd - NODE: {}'.format(node),'\n')

			time.sleep(warm_up_time)
			ca_user_data  = trigger_ca(node)
		#	print('STATUS: Message from user - THREAD: application_txd - NODE: {}'.format(node),' - MSG: {}'.format(ca_user_data ),'\n')
			ca_service_txd_queue.put(int(ca_user_data))
			i=0
			while True:
				i=i+1
		#		den_user_data = trigger_event(node)
		#		print('STATUS: Message from user - THREAD: application_txd - NODE: {}'.format(node),' - MSG: {}'.format(den_user_data ),'\n')
		#		den_service_txd_queue.put(den_user_data)
		return
	else:
		while not start_flag.isSet():
			time.sleep (1)
		print('STATUS: Ready to start - THREAD: application_txd - NODE: {}'.format(node),'\n')

		time.sleep(warm_up_time)
		if(urgent['urgency'] == 'no') :
			ca_user_data  = trigger_ca(node)
			#print('STATUS: Message from user - THREAD: application_txd - NODE: {}'.format(node),' - MSG: {}'.format(ca_user_data ),'\n')
			ca_service_txd_queue.put(int(ca_user_data))
		else:
			i=0
			while True:
				i=i+1
				den_user_data = trigger_event(node)
				#print('STATUS: Message from user - THREAD: application_txd - NODE: {}'.format(node),' - MSG: {}'.format(den_user_data ),'\n')
				den_service_txd_queue.put(den_user_data)
		return


#-----------------------------------------------------------------------------------------
# Thread: application reception. In this example it receives CA and DEN messages. 
# 		Incoming messages are send to the user and my_system thread, where the logic of your system must be executed
# 		CA messages have 1-hop transmission and DEN messages may have multiple hops and validity time
#		Note: current version does not support multihop and time validity. 
#		TIPS: i) if you want to add multihop, you need to change the thread structure and add 
#       		the den_service_txd_queue so that the node can relay the DEN message. 
# 				Do not forget to this also at IST_core.py
#-----------------------------------------------------------------------------------------
def application_rxd(node, start_flag, services_rxd_queue, my_system_rxd_queue):

	while not start_flag.isSet():
		time.sleep (1)
	print('STATUS: Ready to start - THREAD: application_rxd - NODE: {}'.format(node),'\n')

	while True :
		msg_rxd=services_rxd_queue.get()
		#print('STATUS: Message received/send - THREAD: application_rxd - NODE: {}'.format(node),' - MSG: {}'.format(msg_rxd),'\n')
		if msg_rxd['node']!=node:
			my_system_rxd_queue.put(msg_rxd)

	return


#-----------------------------------------------------------------------------------------
# Thread: my_system - implements the business logic of your system. This is a very straightforward use case 
# 			to illustrate how to use cooperation to control the vehicle speed. 
# 			The assumption is that the vehicles are moving in the opposite direction, in the same lane.
#			In this case, the system receives CA messages from neigbour nodes and, 
# 			if the distance is smaller than a warning distance, it moves slower, 
# 			and the distance is smaller that the emergency distance, it stops.
#		TIPS: i) we can add DEN messages or process CAM messages in other ways. 
#			  ii) we can interact with other sensors and actuators to decid the actions to execute.
#			  iii) based on your business logic, your system may also generate events. In this case, 
# 				you need to create an event with the same structure that is used for the user and 
#               change the thread structure by adding the den_service_txd_queue so that this thread can send th DEN message. 
# 				Do not forget to this also at IST_core.py
#-----------------------------------------------------------------------------------------
def my_system(node, start_flag, coordinates, obd_2_interface, my_system_rxd_queue, movement_control_txd_queue, 
				lastmsg, light, mode, tipo, engine_flag, count_slower, count_faster, urgent):

	urgent_me=urgent['urgency']
	flag_da_emergencia = False
	if(tipo=='S'):
		obd_3_interface= dict()
		safety_emergency_distance = 20
		safety_warning_distance = 50
		walking_distance = safety_warning_distance + 50
		urgency_distance = 160
		while not start_flag.isSet():
			time.sleep (1)
		print('STATUS: Ready to start - THREAD: my_system - NODE: {}'.format(node),'\n')
		while not engine_flag.isSet():
			time.sleep (1)
			
		while True:
			msg_rxd=my_system_rxd_queue.get()
			if ( msg_rxd['msg_type']=='CA'):
				car_intersetionS(coordinates, obd_2_interface, msg_rxd, safety_emergency_distance, safety_warning_distance,
				walking_distance,movement_control_txd_queue)
			if (msg_rxd['msg_type']=='DEN'):
				print('SE MSG DEN = DEN ')
				my_s, my_dir, my_h = get_vehicle_info(obd_2_interface)
				my_x,my_y,my_t=position_read(coordinates)
				if(my_h != msg_rxd['heading']):
					obd_3_interface = {'speed': my_s, 'direction': my_dir, 'heading': msg_rxd['heading'], 'status': "0"}
					nodes_distance=distance (coordinates, obd_3_interface, msg_rxd)
				else:
					nodes_distance=distance (coordinates, obd_2_interface, msg_rxd)
				print(nodes_distance)
				if(nodes_distance < urgency_distance):
					print('devia entrar')
					while True:
						msg_rxd=my_system_rxd_queue.get()
						if (msg_rxd['msg_type']=='DEN' ):
							if((my_h=='E' and my_h==msg_rxd['heading'] and my_x>msg_rxd['pos_x']) or (my_h=='O' and my_h==msg_rxd['heading'] and my_x<msg_rxd['pos_x']) ):
								print('AQUIIIIIIIIIIII')
								car_intersetionS(coordinates, obd_2_interface, msg_rxd, safety_emergency_distance, safety_warning_distance,
								walking_distance,movement_control_txd_queue)
								mode['id']=2
								print('MODE22')
							elif((my_h=='N' and my_h==msg_rxd['heading'] and my_y>msg_rxd['pos_y']) or (my_h=='S' and my_h==msg_rxd['heading'] and my_y<msg_rxd['pos_y']) ):
								car_intersetionS(coordinates, obd_2_interface, msg_rxd, safety_emergency_distance, safety_warning_distance,
								walking_distance,movement_control_txd_queue)
								mode['id']=2
								print('MODE22')
							elif(((my_h=='N' or my_h=='S') and msg_rxd['heading']=='E' and my_h!=msg_rxd['heading'] and my_x>msg_rxd['pos_x']) or ((my_h=='N' or my_h=='S') and msg_rxd['heading']=='O' and my_h!=msg_rxd['heading'] and my_x<msg_rxd['pos_x'])):
								car_intersetionS(coordinates, obd_2_interface, msg_rxd, safety_emergency_distance, safety_warning_distance,
								walking_distance,movement_control_txd_queue)
								mode['id']=3
								print('MODE33')
							elif(((my_h=='E' or my_h=='O') and msg_rxd['heading']=='N' and my_h!=msg_rxd['heading'] and my_y>msg_rxd['pos_y']) or ((my_h=='E' or my_h=='O') and msg_rxd['heading']=='S' and my_h!=msg_rxd['heading'] and my_y<msg_rxd['pos_y'])):
								car_intersetionS(coordinates, obd_2_interface, msg_rxd, safety_emergency_distance, safety_warning_distance,
								walking_distance,movement_control_txd_queue)
								mode['id']=3
								print('MODE33')
							else:
								mode['id'] = 1
								print('MODE11')
								break

	else : 

		safety_emergency_distance = 20
		safety_warning_distance = 50
		walking_distance = safety_warning_distance + 50
		traffic_distance = 80

		while not start_flag.isSet():
			time.sleep (1)
		print('STATUS: Ready to start - THREAD: my_system - NODE: {}'.format(node),'\n')
		while not engine_flag.isSet():
			time.sleep (1)

		enter_car(movement_control_txd_queue)
		turn_on_car(movement_control_txd_queue)

		car_move_forward(movement_control_txd_queue)
		
		while True :
			msg_rxd=my_system_rxd_queue.get()
			my_s, my_dir, my_h = get_vehicle_info(obd_2_interface)
			#print('--- LAST MSG ---- ' + lastmsg['color'])
			print(my_s)
			
			if (msg_rxd['msg_type']=='CA' ):
				teste = 1
				if(msg_rxd['type'] == 'C' or  msg_rxd['type'] == 'U'):
					if(((my_h == 'E' or 'O') and (msg_rxd['heading'] =='E' or 'O')) or ((my_h == 'N' or 'S') and (msg_rxd['heading'] =='N' or 'S'))):
						if(urgent_me=='no'):
							count_slower['num'], count_slower['stop'], count_faster['num'] =car_intersetionC(coordinates, obd_2_interface, msg_rxd, safety_emergency_distance, safety_warning_distance,
							walking_distance,movement_control_txd_queue, flag_da_emergencia, count_slower['num'], count_faster['num'], count_slower['stop'])
							print('FASTER: '+ str(count_faster['num']))

				if(msg_rxd['type'] == 'S' and msg_rxd['heading'] == my_h):

					if(msg_rxd['light'] == 'green'):
						count_slower['num'], count_slower['stop'], count_faster['num']= sem_intersetion(coordinates, obd_2_interface, msg_rxd, msg_rxd['light'], node, msg_rxd['node'], movement_control_txd_queue,
						traffic_distance , lastmsg, teste, count_slower['num'], count_faster['num'], count_slower['stop'])
					elif (msg_rxd['light'] == 'yellow') :
						count_slower['num'], count_slower['stop'], count_faster['num']= sem_intersetion(coordinates, obd_2_interface, msg_rxd, msg_rxd['light'], node, msg_rxd['node'], movement_control_txd_queue,
						traffic_distance, lastmsg , teste, count_slower['num'], count_faster['num'], count_slower['stop'])
					elif (msg_rxd['light'] == 'red') :
						count_slower['num'], count_slower['stop'], count_faster['num']= sem_intersetion(coordinates, obd_2_interface, msg_rxd, msg_rxd['light'], node, msg_rxd['node'], movement_control_txd_queue,
						traffic_distance, lastmsg ,teste, count_slower['num'], count_faster['num'], count_slower['stop'])
			if(msg_rxd['msg_type'] == 'DEN') :
				print('Recebi uma msg DEN da ambulancia')
				flag_da_emergencia= True
				if(((my_h == 'E' or 'O') and (msg_rxd['heading'] =='E' or 'O')) or ((my_h == 'N' or 'S') and (msg_rxd['heading'] =='N' or 'S'))):
					count_slower['num'], count_slower['stop'], count_faster['num'] =car_intersetionC(coordinates, obd_2_interface, msg_rxd, safety_emergency_distance, safety_warning_distance,
					walking_distance,movement_control_txd_queue, flag_da_emergencia, count_slower['num'], count_faster['num'], count_slower['stop'])

		


def car_intersetionS(coordinates, obd_2_interface, msg_rxd, safety_emergency_distance, safety_warning_distance,
					walking_distance,movement_control_txd_queue):
	nodes_distance=distance (coordinates, obd_2_interface, msg_rxd)
	my_x,my_y,my_t=position_read(coordinates)
	my_s, my_dir, my_h = get_vehicle_info(obd_2_interface)
	node_x,node_y,node_t = position_node(msg_rxd)
	node_s, node_dir, node_h = movement_node(msg_rxd)
	noderx=msg_rxd['node']
	if (nodes_distance == -1):
		return 
		#print('Mensagem proveniente de um carro cuja zona não controlo')
	return 
	


def sem_intersetion(coordinates, obd_2_interface, msg_rxd , color , nodein , noderx , movement_control_txd_queue , distancemax, lastmsg, teste,
					count_slower, count_faster, count_stop) :

	nodes_distance=distance (coordinates, obd_2_interface, msg_rxd)
	if(teste == 1 ):
		print ('CA semaforo ->   nodes_ distance ', nodes_distance)
	else :
		print ('DEN semaforo ->   nodes_ distance ', nodes_distance)
	my_s, my_dir, my_h = get_vehicle_info(obd_2_interface)
	my_x,my_y,my_t=position_read(coordinates)
	
	if(nodes_distance < distancemax ) :
		if((msg_rxd['heading'] == 'E' and ( my_x < msg_rxd['pos_x'])) or (msg_rxd['heading'] == 'N' and ( my_y < msg_rxd['pos_y'])) 
		or (msg_rxd['heading'] == 'O' and ( my_x > msg_rxd['pos_x'])) or (msg_rxd['heading'] == 'S' and ( my_x < msg_rxd['pos_y']))):
			if( color == 'red' ) :
				print(' Sinal vermelho => Carro parou por ordem do semaforo')
				if( lastmsg['color'] != 'red'):
					print('aqui!!!!')
					count_slower=math.ceil(my_s/20)
					count_stop=1
					car_move_slower(movement_control_txd_queue)
					lastmsg['color'] = 'red'
			elif ( color == 'yellow' ) : 
				print(' Sinal amarelo => Carro abrandou por ordem do semaforo')
				if( lastmsg['color'] != 'yellow'):
					count_slower=math.ceil(my_s/20)
					count_stop=1
					car_move_slower(movement_control_txd_queue)
					lastmsg['color']='yellow'
			elif ( color == 'green' ) :
				print(' Sinal verde => Carro avança')
				if(lastmsg['color'] == 'yellow') :
					new_movement(my_dir)
					count_faster = 1
					car_move_faster(movement_control_txd_queue)
					lastmsg['color']='green'
				elif(lastmsg['color'] == 'red'):
					new_movement(my_dir)
					count_faster = 1
					car_move_faster(movement_control_txd_queue)
					lastmsg['color'] = 'green'
					
	return(count_slower, count_stop,count_faster)


def car_intersetionC(coordinates, obd_2_interface, msg_rxd, safety_emergency_distance, safety_warning_distance,
					walking_distance,movement_control_txd_queue,flag_da_emergencia, count_slower, count_faster, count_stop):
	nodes_distance=distance (coordinates, obd_2_interface, msg_rxd)

	my_x,my_y,my_t=position_read(coordinates)
	my_s, my_dir, my_h = get_vehicle_info(obd_2_interface)
	node_x,node_y,node_t = position_node(msg_rxd)
	node_s, node_dir, node_h = movement_node(msg_rxd)
	noderx=msg_rxd['node']
	print ('MSG FROM : ' + noderx + 'CA ->   nodes_ distance ', nodes_distance)

	if( (my_y == node_y and my_dir == node_dir and ((my_h == 'O' or my_h == 'E') and (node_h == 'O' or node_h == 'E')))):
		if( my_h == node_h ):
			if (nodes_distance < safety_warning_distance):
				if(my_h == 'E'):
					if(my_x > node_x and not(flag_da_emergencia)):
						print('-------- gajo atras ---------' +'eu x:' + str(my_x) + 'eu v:' + str(my_s))
					elif(my_x > node_x and flag_da_emergencia):
						print('ambulancia atras')
						if( my_s < node_s ):
							count_faster = (node_s-my_s)/10
							car_move_faster(movement_control_txd_queue)

					elif(my_x < node_x):
						print('----------estou atras----------' + 'eu x:' + str(my_x) + 'eu v:' + str(my_s))
						print ('----------------slow down-------------------')
						if(count_slower==0):
							count_slower=math.ceil(my_s/20)
							count_stop=1
							print('Count_slower:' + str(count_slower))
							car_move_slower(movement_control_txd_queue)

				elif(my_h == 'O'):
					if(my_x < node_x and not(flag_da_emergencia)):
						print('-------- gajo atras ---------' )
					elif(my_x < node_x and flag_da_emergencia):
						print('ambulancia atras')
						if( my_s < node_s ):
							count_faster = 1
							car_move_faster(movement_control_txd_queue)

					elif (my_x > node_x):
						print('----------estou atras----------')
						print ('----------------slow down-------------------')
						count_slower=math.ceil(my_s/20)
						count_stop=1
						car_move_slower(movement_control_txd_queue)

			elif(nodes_distance >= walking_distance):
				print ('----------------MOVE FASTER------------------------------ and my_s = ' + str(my_s))
				if(not(flag_da_emergencia)):
					if(my_s < node_s and my_s == 0 and count_faster==0):
						count_faster = 1
						print('AQUIIIIIIIIIIIIIIIII')
						print('count faster = ' + str(count_faster))
						car_move_faster(movement_control_txd_queue)
				elif(flag_da_emergencia):
					if(my_s == 0):
						count_faster = 1
						car_move_faster(movement_control_txd_queue)

			elif (nodes_distance < safety_emergency_distance):
				print ('---------------- STOP  ------------------------------')
				stop_car(movement_control_txd_queue)

		else:
			if (nodes_distance < safety_warning_distance):
				print (' ------------ direcao oposta ----------- ')
				print ('---------------- STOP  ------------------------------')
				print('teste')
				stop_car(movement_control_txd_queue)

	if( (my_x == node_x and my_dir == node_dir and ((my_h == 'N' or my_h == 'S') and (node_h == 'N' or node_h == 'S')))):
		if( my_h == node_h ):
			if (nodes_distance < safety_warning_distance):
				if(my_h == 'N'):
					if(my_y > node_y and not(flag_da_emergencia)):
						print('-------- gajo atras ---------' +'eu x:' + str(my_y) + 'eu v:' + str(my_s))
					elif(my_x > node_x and flag_da_emergencia):
						print('ambulancia atras')
						if( my_s < node_s ):
							count_faster = (node_s-my_s)/10
							car_move_faster(movement_control_txd_queue)

					elif(my_y < node_y):
						print('----------estou atras----------' + 'eu x:' + str(my_y) + 'eu v:' + str(my_s))
						print ('----------------slow down-------------------')
						count_slower=math.ceil(my_s/20)
						count_stop=1
						print('Count_slower:' + str(count_slower))
						car_move_slower(movement_control_txd_queue)
				else:
					if(my_y < node_y and not(flag_da_emergencia)):
						print('-------- gajo atras ---------' )
					elif(my_y < node_y and flag_da_emergencia):
						print('ambulancia atras')
						if( my_s < node_s ):
							count_faster = 1
							car_move_faster(movement_control_txd_queue)

					elif (my_y > node_y):
						print('----------estou atras----------')
						print ('----------------slow down-------------------')
						count_slower=math.ceil(my_s/20)
						count_stop=1
						car_move_slower(movement_control_txd_queue)

			elif(nodes_distance >= safety_warning_distance):
				print ('----------------MOVE FASTER------------------------------ and my_s = ' + str(my_s))
				if(not(flag_da_emergencia)):
					if(my_s < node_s and my_s == 0 and count_faster==0):
						count_faster = 1
						car_move_faster(movement_control_txd_queue)
				elif(flag_da_emergencia):
					if(my_s == 0):
						car_move_faster(movement_control_txd_queue)
			elif (nodes_distance < safety_emergency_distance):
				print ('---------------- STOP  ------------------------------')
				stop_car(movement_control_txd_queue)

		else:
			if (nodes_distance < safety_warning_distance):
				print (' ------------ direcao oposta ----------- ')
				print ('---------------- STOP  ------------------------------')
				stop_car(movement_control_txd_queue)
	return(count_slower, count_stop,count_faster)