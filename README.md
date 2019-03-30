# the-form-of-becoming
In this abstract system, each intelligent agent is embodied as a motor, the states in its environment is represented as an angular range of rotation and the actions as one of two directions in which each agent can move a linear actuator. Each linear system holds a segment of a long black string, this translates as a point in the represented line. Once the system runs, each agent learns, from informational equivalents of pain and pleasure, to move towards the highest values within its environment, this means ultimately to displace its position from point A to B. In order for an agent to learn, it needs time, generations of exploration, each agent will get punished for bad decisions and rewarded for appropriate ones. Every time a learning generation is finished, a light will blink for that particular agent, indicating the end of a cycle and the achievement of new knowledge; the agent becomes more intelligent. Once all agents learned to be and stay in point B, the system, as a collective, has successfully mutated into a stable, balanced, symmetric and silent form; a straight line. Finally, after a few seconds, the sculpture forgets, all agents are rebooted and the cycle of creation, chaos and order restarts, this time with a totally different and unique behavior. 

##Requirenments

This software has been tested on a Raspberry pi 3 Model B+ (2017) running 2018-11-13-raspbian-stretch-full with Python 3.5.3 with the following dependencies:

- adafruit_servokit
- Flask
- Flask-SocketIO
- gevent
- gevent-socketio
- gevent-websocket
- greenlet
- itsdangerous
- Jinja2
- MarkupSafe
- Werkzeug

There is a requirenment.txt file which you can try installing using pip3:

	sudo pip3 install -r requirenments.txt
	
If this does not work please install them manually. These are all common python libraries easy to find. 
The adafruit_servokit library can be found here: [servokit](https://github.com/adafruit/Adafruit_CircuitPython_ServoKit)
