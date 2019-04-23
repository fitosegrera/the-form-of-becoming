#main.py
import qlearning
import sys, os
import random
from adafruit_servokit import ServoKit
import datetime

from gevent import monkey
monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect

import json

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
thread = None

totalBoards = 1
agentsPerBoard = 8
kit = ServoKit(channels=agentsPerBoard)

agents = [None for x in range(agentsPerBoard)] 
previousState = [None for x in range(agentsPerBoard)] 
angles = [None for x in range(agentsPerBoard)]
rt = [None for x in range(agentsPerBoard)]
isDone = [None for x in range(agentsPerBoard)]

max_angle = 165 # maximum angle for the motor before the linear actuator passes the vertical limit

N_STATES = 33  # 165/5 = 33 (each state is 5 degrees of rotation)
ACTIONS = ['down', 'up']   
EPSILON = 0.9   
ALPHA = 0.1     
GAMMA = 0.9    
MAX_EPISODES = 0 #50, will take over 1 hour  
REFRESH_TIME_MIN = 0.2 #use minimum 0.2
REFRESH_TIME_MAX = 0.25 #use maximum 0.8
EPISODE_TIME = 0

stopThread = False
shutdown = False
rebootAction = False
restartSystem = False

#############################################
def setupQl():
	global rt
	print ("\nInitiating Agents...")
	print ("Callibrating Motors...")
	
	for agent in range(agentsPerBoard):
		r = random.uniform(REFRESH_TIME_MIN,REFRESH_TIME_MAX)
		ql = qlearning.Qlearning(N_STATES, ACTIONS, EPSILON, ALPHA, 
			GAMMA, MAX_EPISODES, r, 
			EPISODE_TIME, False)
				
		rt[agent] = r	
		agents[agent] = ql
		previousState[agent] = 0
		angles[agent] = 0
		isDone[agent] = agent

	for i in range(len(kit.servo)):
		kit.servo[i].angle = 0
	
	time.sleep(1)		
	return agents

#############################################	
def restartAll():
	global restartSystem, thread
	restartSystem = False
	if thread is not None:
		print("Thread Stopped")
		print("thread is alive:",thread.isAlive())
		thread.join() 
		thread = None
	print("in balance and silence...")
	sleep(5)
	print("Restarting...")
	initThread()
	
#############################################	
def agents_learning():
	global stopThread, systemRun, thread
	ql = setupQl()
	print("\nSystem Initiated!")
	currentDT = datetime.datetime.now()
	print ("\nStarting Time:",str(currentDT), "\n")
	while True:
		for agent in range(agentsPerBoard):
			ql[agent].run()
			if ql[agent].S != previousState[agent]:
				previousState[agent] = ql[agent].S 
				angle = 0
				if ql[agent].S == "terminal":
					if(agent==2):
						angle = 0
					else:
						angle = max_angle
					#print("Agent", agent, "terminal!")
				else:
					if(agent==2):
						angle = max_angle - ql[agent].S * 5
					else:
						angle = ql[agent].S * 5
						
				angles[agent] = angle
				kit.servo[agent].angle = angle
			#time.sleep(0.1)
			if ql[agent].done:
				if agent in isDone:
					try:
						isDone.remove(agent)
					except:
						pass
					print("REMOVING agent", agent)	
					print(isDone)					
				if len(isDone) == 0:
					print("ALL AGENTS DONE!")
					stopThread = True
					restartSystem = True
					
		time.sleep(0.05)
		socketio.emit('message', {'data': angles}, namespace='/main')
		if stopThread:
			print("STOPPED")
			#socketio.stop()
			stopThread = False
			if(shutdown):
				os.system("sudo shutdown -h now")
			if(rebootAction):
				os.system("sudo reboot")
			break
	print("Loop Break")
	if(restartSystem):
		restartAll()

#############################################
def parallelTest():
    for i in range(len(kit.servo)):
        kit.servo[i].angle = 0
    time.sleep(1)
    for i in range(len(kit.servo)):
        kit.servo[i].angle = 165
    time.sleep(3)
    for i in range(len(kit.servo)):
        kit.servo[i].angle = 0
    time.sleep(1)
    
#############################################
def serialTest():
    d=0.8
    for i in range(len(kit.servo)):
        kit.servo[i].angle = 0
    time.sleep(1)
    for i in range(len(kit.servo)):
        kit.servo[i].angle = 165
        time.sleep(d)
    time.sleep(1)
    for i in range(len(kit.servo)):
        kit.servo[i].angle = 0
        time.sleep(d)
    time.sleep(1)

#############################################
def initThread():
	global thread
	print("starting thread")
	print(thread)
	if thread is None:
		print("thread", thread)
		thread = Thread(target=agents_learning)
		thread.daemon = True
		thread.start()
		print("Started!")

#############################################
@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('start', namespace='/main')
def start(msg):
	global thread, rt
	print("START:", msg['data'])
	if(msg['data']):
		initThread()
		rtData = {
		"RT": rt
		}
		emit('refresh_times', json.dumps(rtData))
		#print("RT:", rtData)
		
@socketio.on('stop', namespace='/main')
def stop(msg):
	global stopThread, thread
	print("STOP:", msg['data'])
	if(msg['data']):
		stopThread = True
		if thread is not None:
			print("Thread Stopped")
			print("thread is alive:",thread.isAlive())
			thread.join() 
			thread = None

@socketio.on('test', namespace='/main')
def test(msg):
	global stopThread, thread
	time.sleep(1)
	if thread is not None:
		stopThread = True
		rebootAction = True
		thread.join() 
		print("Thread Stopped")
		print("thread is alive:",thread.isAlive())
		thread = None
	print("TEST:", msg)
	if msg['data'] == 'p':
		parallelTest()
	if msg['data'] == 's':
		serialTest()
	
@socketio.on('reboot', namespace='/main')
def reboot(msg):
	global stopThread, thread
	print(msg['data'])
	if(msg['data'] == 'REBOOT'):
		time.sleep(1)
		if thread is not None:
			stopThread = True
			rebootAction = True
			thread.join() 
			print("Thread Stopped")
			print("thread is alive:",thread.isAlive())
			thread = None
		else:
			os.system("sudo reboot")
		    
@socketio.on('power', namespace='/main')
def power(msg):
	global stopThread, thread
	print(msg['data'])
	if(msg['data'] == 'OFF'):
		time.sleep(1)
		if thread is not None:
			stopThread = True
			shutdown = True
			thread.join()
			print("Thread Stopped")
			print("thread is alive:",thread.isAlive())
			thread = None
		else: 
			os.system("sudo shutdown -h now")
			
@socketio.on('connect', namespace='/main')
def connect():
	emit('connect', {'data': 'connected'})
	initData = {
		'N_STATES': N_STATES,  
		'ACTIONS': ACTIONS,   
		'EPSILON': EPSILON,  
		'ALPHA': ALPHA,     
		'GAMMA': GAMMA,    
		'MAX_EPISODES': MAX_EPISODES,  
		'REFRESH_TIME_MIN': REFRESH_TIME_MIN,
		'REFRESH_TIME_MAX': REFRESH_TIME_MAX, 
		'EPISODE_TIME': EPISODE_TIME
	}
	#print (initData)
	emit('init_data', json.dumps(initData))
		
@socketio.on('disconnect', namespace='/main')
def disconnect():
    print('Client disconnected')
	
#############################################	
if __name__ == '__main__':
	try:
		socketio.run(app, host="0.0.0.0")
	except KeyboardInterrupt:
		sys.exit()
