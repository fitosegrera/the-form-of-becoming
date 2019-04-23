import time
from adafruit_servokit import ServoKit
 
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=8)

for i in range(len(kit.servo)):
    #kit.servo[i].set_pulse_width_range(500, 2500)
    #kit.servo[i].angle = 0
    #time.sleep(0.5)
    #print("servo", i, "reset")
    pass
    
def fullTest():
    d=1

    for i in range(len(kit.servo)):
        kit.servo[i].angle = 165
        time.sleep(d)
    time.sleep(3)

    for i in range(len(kit.servo)):
        kit.servo[i].angle = 0
        time.sleep(d)
    time.sleep(3)

def stepsTest():
    d = 1
    a = 0
    for state in range(18):
        for i in range(len(kit.servo)):
            kit.servo[i].angle = a
            time.sleep(d)
        a+=10
        print(a)
        time.sleep(1)

    for i in range(len(kit.servo)):
        kit.servo[i].angle = 0
        time.sleep(d)
    time.sleep(1)

def inverseTest():
    d=1
    for i in range(len(kit.servo)):
        if(i==2):
            kit.servo[i].angle = 0
    time.sleep(3)

    for i in range(len(kit.servo)):
        if(i==2):
            kit.servo[i].angle = 165
    time.sleep(3)

#fullTest()
#stepsTest()
inverseTest()
