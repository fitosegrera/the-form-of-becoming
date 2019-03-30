import time
from adafruit_servokit import ServoKit
 
# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)
 
for i in range(len(kit.servo)):
    kit.servo[i].angle = 180
time.sleep(1)

"""
for i in range(len(kit.servo)):
    kit.servo[i].angle = 0
time.sleep(1)
"""
