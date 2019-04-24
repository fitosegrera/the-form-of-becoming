#main.py
import qlearning
import sys, os
import random
import datetime
import time
from threading import Thread

thread = None

agentsPerBoard = 8

agents = [None for x in range(agentsPerBoard)] 
previousState = [None for x in range(agentsPerBoard)] 
angles = [None for x in range(agentsPerBoard)]
rt = [None for x in range(agentsPerBoard)]
isDone = [None for x in range(agentsPerBoard)]

max_angle = 180 # maximum angle for the motor before the linear actuator passes the vertical limit

N_STATES = 18  # 165/5 = 33 (each state is 5 degrees of rotation)
ACTIONS = ['down', 'up']   
EPSILON = 0.9   
ALPHA = 0.1     
GAMMA = 0.9    
MAX_EPISODES = 0 #50, will take over 1 hour  
REFRESH_TIME_MIN = 0.01 #use minimum 0.2
REFRESH_TIME_MAX = 0.05 #use maximum 0.8
EPISODE_TIME = 0

stopThread = False
restartSystem = False

#############################################
def setupQl():
	global rt
	print ("\nInitiating Agents...")
	
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
	
	time.sleep(1)		
	return agents

#############################################	
def restartAll():
	global restartSystem, thread, isDone, agentsPerBoard
	restartSystem = False
	if thread is not None:
		print("Thread Stopped")
		print("thread is alive:",thread.isAlive())
		#thread.join() 
		thread = None
	print("in balance and silence...")
	time.sleep(5)
	print("Restarting...")
	isDone = [None for x in range(agentsPerBoard)]
	initThread()
	
#############################################	
def agents_learning():
	global stopThread, thread, restartSystem
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
					angle = max_angle
					#print("Agent", agent, "terminal!")
				else:
					angle = ql[agent].S * 10	
				angles[agent] = angle
				#print(agent, angle)
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
					
		#time.sleep(0.005)
		if stopThread:
			print("STOPPED")
			stopThread = False
			break
	print("Loop Break")
	if(restartSystem):
		restartAll()
	print("EXITING THREADING FUNCTION")

#############################################
def initThread():
	global thread
	print("starting thread")
	print(thread)
	if thread is None:
		print("thread", thread)
		thread = Thread(target=agents_learning)
		#thread.daemon = True
		thread.start()
		print("Started!")

#############################################	
if __name__ == '__main__':
	try:
		initThread()
	except KeyboardInterrupt:
		if thread is not None:
			print("Thread Stopped")
			print("thread is alive:",thread.isAlive())
			thread.join() 
			thread = None
		sys.exit()
